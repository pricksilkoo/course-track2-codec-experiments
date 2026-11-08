#!/usr/bin/env python3
"""Prepare exactly four posthoc decoder-only candidates on CPU; no optimization."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import torch
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from ssp_codec.model import CourseCodec
from ssp_codec.config import load_config
from ssp_codec.checkpoint_io import save_checkpoint_atomic
from ssp_codec.decoder_interpolation import interpolate_decoder

PARENT=ROOT/"runs/champion6_b_s3407_fourier_gru/checkpoints/last.pt"
PARENT_SHA="c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23"
CELLS=("a_from_a10","b_from_a25","c_from_b10","d_from_b25")
EXPECTED=dict(zip(CELLS,(("a",.10),("a",.25),("b",.10),("b",.25))))
DONORS={"a":("champion7_a_continue","8dcebc6cdf298ef29c420c3d09be66e9f2b995e27eb76176b62caf8ba924313a"),
        "b":("champion7_b_si","8741b75536892152d09adb176ec1a0db6c345496b499443c092051ca24d9b3f4")}
REFERENCE=ROOT/"runs/fast_b64_2s_v1/validation_200"


def digest(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()


def tensors_digest(state,keys):
    h=hashlib.sha256()
    for k in sorted(keys):
        t=state[k].detach().cpu().contiguous()
        h.update(f"{k}:{t.dtype}:{tuple(t.shape)}\n".encode());h.update(t.numpy().tobytes())
    return h.hexdigest()


def main():
    torch.set_num_threads(4)
    output=ROOT/"CHAMPION8_SETUP.audit"
    if output.exists():raise RuntimeError("Setup already exists: never regenerate")
    assert digest(PARENT)==PARENT_SHA
    parent=torch.load(PARENT,map_location="cpu",weights_only=False)
    assert parent["global_step"]==500000
    model=CourseCodec(**parent["model_config"])
    parameter_names=set(dict(model.named_parameters()))
    source_hashes={str(PARENT.relative_to(ROOT)):PARENT_SHA}
    frozen200=json.loads((ROOT/"CHAMPION7_SETUP.audit").read_text())
    for path,sha in frozen200["data_hashes"].items():assert digest(ROOT/path)==sha
    for name,sha in frozen200["fixed200_sha256"].items():assert digest(REFERENCE/name)==sha
    report={"created_utc":datetime.now(timezone.utc).isoformat(),"kind":"posthoc decoder-parameter interpolation, zero new gradient updates",
        "parent":str(PARENT),"parent_sha256":PARENT_SHA,"parent_global_step":500000,
        "parent_score":51.62433613863932,"frozen200_sha256":frozen200["fixed200_sha256"],
        "data_counts":frozen200["data_counts"],"data_hashes":frozen200["data_hashes"],"cells":{}}
    for cell in CELLS:
        run=ROOT/f"runs/champion8_{cell}";config=load_config(ROOT/f"configs/champion8/{cell}.yaml")
        spec=config["posthoc_interpolation"];donor_name,donor_sha=DONORS[spec["donor_label"]]
        assert (spec["donor_label"],spec["alpha"])==EXPECTED[cell]
        donor_path=ROOT/f"runs/{donor_name}/checkpoints/step_00100000.pt"
        assert digest(donor_path)==donor_sha
        source_hashes[str(donor_path.relative_to(ROOT))]=donor_sha
        donor=torch.load(donor_path,map_location="cpu",weights_only=False)
        assert donor["global_step"]==100000 and donor["model_config"]==parent["model_config"]==config["model"]
        checkpoint=run/"checkpoints/interpolated.pt"
        if checkpoint.exists():raise RuntimeError(f"Preserve existing candidate:{checkpoint}")
        mixed,keys=interpolate_decoder(parent["model"],donor["model"],parameter_names,spec["alpha"])
        fixed=sorted(mixed.keys()-set(keys))
        assert all(torch.equal(mixed[k],parent["model"][k]) for k in fixed)
        assert all(torch.isfinite(v).all() for v in mixed.values() if v.is_floating_point())
        assert all(k in fixed for k in mixed if k.startswith(("encoder.","analysis_","latent_norm.","quantizer.")))
        model.load_state_dict(mixed,strict=True)
        lineage={"kind":"posthoc_decoder_parameter_interpolation","inference_only":True,
            "formula":"(1-alpha)*parent + alpha*donor, only listed decoder parameters",
            "alpha":spec["alpha"],"parent_checkpoint":str(PARENT),"parent_sha256":PARENT_SHA,"parent_global_step":500000,
            "donor_checkpoint":str(donor_path),"donor_sha256":donor_sha,"donor_stage_step":100000,"donor_cumulative_step":600000,
            "new_gradient_updates":0,"global_step_semantics":"0 posthoc local optimizer updates; sources are trained",
            "interpolated_parameter_keys":keys,"frozen_tensor_keys":fixed,
            "all_encoder_and_rvq_tensors_and_all_buffers_bitwise_parent":True,
            "frozen_tensors_sha256":tensors_digest(mixed,fixed),"decoder_parameters_sha256":tensors_digest(mixed,keys)}
        checkpoint.parent.mkdir(parents=True,exist_ok=True)
        save_checkpoint_atomic({"global_step":0,"model":mixed,"model_config":parent["model_config"],
            "checkpoint_kind":"posthoc_decoder_interpolation","inference_only":True,"lineage":lineage},checkpoint)
        (run/"lineage.json").write_text(json.dumps(lineage,indent=2)+"\n")
        config["training"]["output_dir"]=str(run)
        (run/"effective_config.yaml").write_text(yaml.safe_dump(config,sort_keys=False))
        subprocess.run([str(ROOT/".venv-codec/bin/python"),"scripts/complexity.py","--checkpoint",str(checkpoint),
                        "--output",str(run/"preflight_complexity.json")],cwd=ROOT,check=True,env={**os.environ,"OMP_NUM_THREADS":"4"})
        cost=json.loads((run/"preflight_complexity.json").read_text())
        assert cost["parameters"]==1868064 and cost["total_mflop_per_s"]<=700 and cost["decoder_mflop_per_s"]<=300
        assert cost["algorithmic_lookahead_ms"]==30 and cost["unclassified_mmac_per_s"]==0 and cost["bitrate_bps"]==2400
        report["cells"][cell]={"checkpoint":str(checkpoint),"checkpoint_sha256":digest(checkpoint),
            "lineage":lineage,"config_sha256":digest(run/"effective_config.yaml"),"complexity":cost,
            "interpolated_tensors":len(keys),"frozen_tensors":len(fixed)}
        print(f"PREPARED {cell},alpha={spec['alpha']},mixed={len(keys)},frozen={len(fixed)}",flush=True)
        del donor,mixed
    assert all(digest(ROOT/path)==sha for path,sha in source_hashes.items())
    report["source_sha256_unchanged"]=source_hashes
    output.write_text(json.dumps(report,indent=2)+"\n")
    setup=ROOT/"runs/champion8_setup";setup.mkdir(exist_ok=True)
    (setup/"preflight_report.json").write_text(output.read_text())
    (setup/"SETUP_COMPLETE").touch()


if __name__=="__main__":main()
