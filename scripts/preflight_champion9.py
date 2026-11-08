#!/usr/bin/env python3
"""Create four genuinely untrained initializations; never regenerate after launch."""
from datetime import datetime,timezone
import copy
import json
import os
from pathlib import Path
import subprocess
import sys

import torch
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from ssp_codec.model import CourseCodec,CausalTemporalStack
from ssp_codec.config import load_config
from ssp_codec.adversarial import MultiResolutionSTFTDiscriminator
from ssp_codec.checkpoint_io import save_checkpoint_atomic
from prepare_champion8 import digest
from run_champion7_experiment import record

CELLS=("a_g4_d0","b_g8_d0","c_g4_d2","d_g8_d2")
FACTORS=((4,0),(8,0),(4,2),(8,2))
SEED=20261108
STEPS=500000
ENDPOINTS=(250000,500000)
REFERENCE=ROOT/"runs/fast_b64_2s_v1/validation_200"


def read(p):return json.loads(Path(p).read_text())


def main():
    torch.set_num_threads(4)
    out=ROOT/"runs/champion9_setup";out.mkdir(exist_ok=True)
    if (ROOT/"CHAMPION9_SETUP.audit").exists() or (out/"PREFLIGHT_COMPLETE").exists():
        raise RuntimeError("Setup exists: do not regenerate")
    if any((ROOT/f"runs/champion9_{c}/run_metadata.json").exists() for c in CELLS):
        raise RuntimeError("Formal launch metadata exists: preserve setup")
    tests=(out/"cpu_tests.log").read_text();assert "64 passed" in tests and "FAILED" not in tests
    prior=read(ROOT/"CHAMPION8_SETUP.audit")
    protected={ROOT/p:h for p,h in prior["source_sha256_unchanged"].items()}
    selection=read(ROOT/"CHAMPION8_RESULTS.audit")["selection"]
    protected[Path(selection["checkpoint"])]=selection["checkpoint_sha256"]
    for p in (ROOT/"model_registry").glob("strong_baseline_v2.*"):
        if p.suffix in (".json",".yaml"):protected[p]=digest(p)
    assert all(digest(p)==h for p,h in protected.items())
    for p,h in prior["data_hashes"].items():assert digest(ROOT/p)==h
    for name,h in prior["frozen200_sha256"].items():assert digest(REFERENCE/name)==h
    report={"created_utc":datetime.now(timezone.utc).isoformat(),"trained":False,"global_step":0,
        "initialization":"fresh constructor codec/RVQ/discriminator; no learned/smoke checkpoint",
        "seed":SEED,"data_order_seed":SEED,"training_steps":STEPS,"endpoints":list(ENDPOINTS),
        "data_counts":prior["data_counts"],"data_hashes":prior["data_hashes"],
        "fixed200_sha256":prior["frozen200_sha256"],"unchanged_historical_sha256":{str(p.relative_to(ROOT)):h for p,h in protected.items()},
        "cpu_test_log_sha256":digest(out/"cpu_tests.log"),"cpu_tests":"64 passed in13.75s",
        "no_gpu_smoke_or_profile_per_user":True,"new_architecture_fullGAN_memory_peak_not_measured":True,
        "cells":{},"matched_decoder_tcn_pairs":{}}
    sources={};models={}
    torch.manual_seed(SEED+300000)
    decoder_tcn=CausalTemporalStack(160,2,3,1,0)
    for cell,(groups,layers) in zip(CELLS,FACTORS):
        cfg=load_config(ROOT/f"configs/champion9/{cell}.yaml")
        assert cfg["seed"]==cfg["training"]["data_order_seed"]==SEED
        assert (cfg["model"]["encoder_groups"],cfg["model"]["decoder_temporal_layers"])==(groups,layers)
        assert cfg["model"]["encoder_temporal_layers"]==0 and cfg["model"]["encoder_lookahead_frames"]==2
        assert cfg["model"]["synthesis_initialization_seed"]==SEED+200000
        torch.manual_seed(SEED);model=CourseCodec(**cfg["model"]).eval()
        shared=[];new=[]
        if sources:
            src=sources[groups] if groups in sources else sources[4]
            target=model.state_dict()
            common={k:v for k,v in src["model"].items() if k in target and target[k].shape==v.shape}
            missing=model.load_state_dict(common,strict=False).missing_keys
            shared=sorted(common);new=missing
            assert all(k.startswith(("encoder.blocks.","synthesis_temporal.")) for k in new)
            assert all(torch.equal(model.state_dict()[k],v) for k,v in common.items())
        if layers:model.synthesis_temporal.load_state_dict(decoder_tcn.state_dict(),strict=True)
        torch.manual_seed(SEED+100000)
        discriminator=MultiResolutionSTFTDiscriminator(cfg["adversarial"]["resolutions"],cfg["adversarial"].get("periods",()))
        assert model.quantizer.update_count.item()==0
        assert all(not bool(v) for k,v in model.quantizer.named_buffers() if k.endswith("initialized"))
        state={"global_step":0,"trained":False,"seed":SEED,"model_config":cfg["model"],
            "model":model.state_dict(),"discriminator":discriminator.state_dict(),
            "initialization_kind":"fresh constructor, matched untrained tensors; never learned parent"}
        if layers==0:sources[groups]=state
        snapshot=out/f"step0_{cell}.pt"
        if snapshot.exists():raise RuntimeError(f"Preserve existing initialization:{snapshot}")
        save_checkpoint_atomic(state,snapshot)
        if cell==CELLS[0]:save_checkpoint_atomic(state,out/"source_step0.pt")
        run=ROOT/f"runs/champion9_{cell}";run.mkdir(exist_ok=True)
        cfg["training"]["output_dir"]=str(run)
        (run/"effective_config.yaml").write_text(yaml.safe_dump(cfg,sort_keys=False))
        subprocess.run([str(ROOT/".venv-codec/bin/python"),"scripts/complexity.py","--checkpoint",str(snapshot),
            "--output",str(run/"preflight_complexity.json")],cwd=ROOT,check=True,env={**os.environ,"OMP_NUM_THREADS":"4"},stdout=subprocess.DEVNULL)
        cost=read(run/"preflight_complexity.json")
        assert cost["total_mflop_per_s"]<=700 and cost["decoder_mflop_per_s"]<=300
        assert cost["total_algorithmic_delay_ms"]==30 and cost["algorithmic_lookahead_ms"]==20
        assert cost["unclassified_mmac_per_s"]==0 and cost["bitrate_bps"]==2400
        lineage={"trained_initialization":False,"global_step":0,"seed":SEED,"discriminator_seed":SEED+100000,
            "GRU_Fourier_seed":SEED+200000,"decoder_TCN_seed":SEED+300000 if layers else None,
            "snapshot":str(snapshot),"snapshot_sha256":digest(snapshot),
            "matched_source":str(out/"source_step0.pt"),"source_trained":False,"shared_keys":shared,"new_shape_keys":new}
        (run/"lineage.json").write_text(json.dumps(lineage,indent=2)+"\n")
        report["cells"][cell]={"groups":groups,"decoder_tcn_layers":layers,"snapshot":str(snapshot.relative_to(ROOT)),
            "snapshot_sha256":digest(snapshot),"effective_config":cfg,"config_sha256":digest(run/"effective_config.yaml"),
            "complexity":cost,"lineage":lineage}
        models[cell]=model
        record(run,run.name,"planned",checkpoint=snapshot,note=("CHAMPION9 new grouped/SnakeBeta encoder, no encoder TCN; "
            f"groups{groups}/decoderTCN{layers}; genuinely UNTRAINED step0 SHA{digest(snapshot)}. "
            "500k scratch; score only250k/500k;20 validations;10ms collection+20ms lookahead=30ms total. CHAMPION9_PLAN.md."))
        print(f"PREPARED {cell}, total={cost['total_mflop_per_s']:.4f},decoder={cost['decoder_mflop_per_s']:.4f}",flush=True)
    for lo,hi in ((CELLS[0],CELLS[2]),(CELLS[1],CELLS[3])):
        a=models[lo].state_dict();c=models[hi].state_dict()
        assert all(torch.equal(v,c[k]) for k,v in a.items())
        x=torch.randn(1,1,1607)
        with torch.inference_mode():
            aa,ai,_=models[lo](x);cc,ci,_=models[hi](x)
        torch.testing.assert_close(aa,cc,rtol=0,atol=0);assert torch.equal(ai,ci)
        report["matched_decoder_tcn_pairs"][f"{hi}-{lo}"]={"all_shared_model_tensors_identical":True,
            "zero_output_TCN_step0_audio_and_codes_identical":True,"shared_tensor_count":len(a)}
    source_discriminator=torch.load(out/f"step0_{CELLS[0]}.pt",map_location="cpu",weights_only=False)["discriminator"]
    for e in report["cells"].values():
        saved=torch.load(ROOT/e["snapshot"],map_location="cpu",weights_only=False)
        assert saved["global_step"]==0 and saved["trained"] is False and "optimizer" not in saved
        assert saved["model"]["quantizer.update_count"].item()==0
        assert all(not bool(v) for k,v in saved["model"].items() if k.startswith("quantizer.") and k.endswith("initialized"))
        assert all(torch.equal(v,source_discriminator[k]) for k,v in saved["discriminator"].items())
    assert all(digest(p)==h for p,h in protected.items())
    report["source_step0_sha256"]=digest(out/"source_step0.pt")
    report["code_sha256"]={p:digest(ROOT/p) for p in ("src/ssp_codec/model.py","src/ssp_codec/champion_analysis.py",
        "src/ssp_codec/champion_synthesis.py","scripts/complexity.py","scripts/train.py","src/ssp_codec/checkpoint_io.py",
        "scripts/preflight_champion9.py","scripts/run_champion9_experiment.py","scripts/supervise_champion9.py","scripts/launch_champion9.py")}
    (ROOT/"CHAMPION9_SETUP.audit").write_text(json.dumps(report,indent=2)+"\n")
    (out/"preflight_report.json").write_text(json.dumps(report,indent=2)+"\n")
    (out/"PREFLIGHT_COMPLETE").touch()
    print("PREFLIGHT_COMPLETE: four untrained snapshots, pairs/data/source hashes verified",flush=True)


if __name__=="__main__":main()
