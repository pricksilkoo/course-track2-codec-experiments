#!/usr/bin/env python3
"""Two new matched scratch-initialization pairs; never inherit trained weights."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ssp_codec.model import CourseCodec
from ssp_codec.config import load_config
from ssp_codec.adversarial import MultiResolutionSTFTDiscriminator

CELLS = (("a_s3407_control",3407,False),("b_s3407_fourier_gru",3407,True),
         ("c_s8128_control",8128,False),("d_s8128_fourier_gru",8128,True))

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def main():
    torch.set_num_threads(2)
    out=ROOT/"runs/champion6_setup"
    out.mkdir(exist_ok=True)
    if any((ROOT/"runs"/f"champion6_{cell}"/"run_metadata.json").exists() for cell,_,_ in CELLS):
        raise RuntimeError("formal training already started; never regenerate initialization")
    if (out/"PREFLIGHT_COMPLETE").exists():
        raise RuntimeError("preflight exists; inspect evidence instead of regenerating it")
    report={"trained":False,"global_step":0,"pairs":{},"cells":{},"initialization":"fresh constructor weights, no learned checkpoint"}
    sources={}
    for cell,seed,candidate in CELLS:
        config=load_config(ROOT/f"configs/champion6/{cell}.yaml")
        assert config["seed"]==config["training"]["data_order_seed"]==seed
        assert config["model"]["synthesis_initialization_seed"]==seed+200000
        torch.manual_seed(seed)
        model=CourseCodec(**config["model"]).eval()
        torch.manual_seed(seed+100000)
        discriminator=MultiResolutionSTFTDiscriminator(config["adversarial"]["resolutions"],config["adversarial"].get("periods",()))
        if not candidate:
            source={"global_step":0,"trained":False,"seed":seed,"model_config":config["model"],
                    "model":model.state_dict(),"discriminator":discriminator.state_dict()}
            source_path=out/f"source_step0_seed{seed}.pt"
            assert not source_path.exists(), source_path
            torch.save(source,source_path)
            sources[seed]=source
            report["pairs"][str(seed)]={"source_sha256":digest(source_path),"source":str(source_path.relative_to(ROOT)),
                "discriminator_initialization_seed":seed+100000,"new_module_initialization_seed":seed+200000}
            loaded=list(model.state_dict())
            missing=[]
        else:
            source=sources[seed]
            shared={key:value for key,value in source["model"].items() if not key.startswith(("decoder.","analysis_gru."))}
            missing=model.load_state_dict(shared,strict=False).missing_keys
            assert all(key.startswith(("decoder.","analysis_gru.")) for key in missing)
            assert all(torch.equal(value,model.state_dict()[key]) for key,value in shared.items())
            assert all(torch.equal(value,discriminator.state_dict()[key]) for key,value in source["discriminator"].items())
            loaded=list(shared)
        snapshot=out/f"step0_{cell}.pt"
        assert not snapshot.exists(), snapshot
        state={"global_step":0,"trained":False,"seed":seed,"model_config":config["model"],
            "model":model.state_dict(),"discriminator":discriminator.state_dict(),
            "source_untrained_initialization":str(out/f"source_step0_seed{seed}.pt")}
        torch.save(state,snapshot)
        run=ROOT/"runs"/f"champion6_{cell}"
        run.mkdir(exist_ok=True)
        (run/"effective_config.yaml").write_text(yaml.safe_dump(config,sort_keys=False))
        complexity_path=run/"preflight_complexity.json"
        subprocess.run([sys.executable,"scripts/complexity.py","--config",f"configs/champion6/{cell}.yaml","--output",str(complexity_path)],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
        complexity=json.loads(complexity_path.read_text())
        assert complexity["bitrate_bps"]==2400 and complexity["frame_samples"]==160
        assert complexity["algorithmic_lookahead_ms"]==30 and complexity["total_mflop_per_s"]<=700
        assert complexity["decoder_mflop_per_s"]<=300 and complexity["unclassified_mmac_per_s"]==0
        with torch.inference_mode():
            output=model(torch.randn(1,1,3200))[0]
        assert output.shape[-1]==3200 and torch.isfinite(output).all()
        report["cells"][cell]={"seed":seed,"candidate":candidate,"snapshot_sha256":digest(snapshot),
            "shared_or_source_tensors":loaded,"new_tensors":missing,"effective_config":config,"complexity":complexity}
        subprocess.run([sys.executable,"scripts/record_experiment.py","--name",run.name,"--status","planned",
            "--config",str(run/"effective_config.yaml"),"--run-dir",str(run),"--dataset-summary","data/manifests/vctk_libritts/summary.json",
            "--complexity-summary",str(complexity_path),"--output","EXPERIMENT_LOG.md","--note",
            f"Matched new-seed scratch confirmation; untrained snapshot SHA256={digest(snapshot)}; fixed500000-step endpoint"],cwd=ROOT,check=True)
    old=json.loads((ROOT/"CHAMPION5_RESULTS.audit").read_text())
    report["data_hashes"]={name:digest(ROOT/name) for name in old["data_hashes"]}
    assert report["data_hashes"]==old["data_hashes"]
    reference=ROOT/"runs/fast_b64_2s_v1/validation_200"
    report["fixed200_sha256"]={path.name:digest(path) for path in sorted(reference.glob("*.wav"))}
    assert report["fixed200_sha256"]==old["fixed200_sha256"]
    (out/"preflight_report.json").write_text(json.dumps(report,indent=2)+"\n")
    (out/"PREFLIGHT_COMPLETE").touch()
    print("Four fresh never-trained snapshots and matched pairs verified")

if __name__=="__main__":
    main()
