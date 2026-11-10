#!/usr/bin/env python3
"""Exactly one fresh500k cell and two registered dev-search weights; resumable."""
from datetime import datetime,timezone
import argparse
import fcntl
import json
import math
import os
from pathlib import Path
import subprocess

import torch
from preflight_champion10 import ROOT,CELLS,STEPS,ENDPOINTS,REFERENCE,read,digest
from run_champion7_experiment import record,verify_roundtrip

PYTHON=ROOT/".venv-codec/bin/python"


def execute(*args):
    print("RUN",*map(str,args),flush=True)
    subprocess.run([str(PYTHON),*map(str,args)],cwd=ROOT,check=True)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("cell",choices=CELLS);p.add_argument("gpu",type=int)
    args=p.parse_args();assert args.gpu in range(4)
    run=ROOT/f"runs/champion10_{args.cell}"
    lock=(run/".pipeline.lock").open("a");fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if (run/"PIPELINE_COMPLETE").exists():return
    logfile=(run/"pipeline.log").open("a",buffering=1);os.dup2(logfile.fileno(),1);os.dup2(logfile.fileno(),2)
    os.environ.update(CUDA_VISIBLE_DEVICES=str(args.gpu),OMP_NUM_THREADS="4",PYTHONUNBUFFERED="1",
        TORCH_HOME=str(ROOT/"data/torch-cache"),PYTHONNOUSERSITE="1")
    torch.set_num_threads(4)
    setup=read(ROOT/"CHAMPION10_SETUP.audit");cell=setup["cells"][args.cell]
    snapshot=ROOT/cell["snapshot"]
    assert digest(snapshot)==cell["snapshot_sha256"]
    assert all(digest(ROOT/p)==h for p,h in setup["code_sha256"].items())
    assert all(digest(ROOT/p)==h for p,h in setup["data_hashes"].items())
    assert digest(run/"effective_config.yaml")==cell["config_sha256"]
    note=(f"CHAMPION10 scratch capacity2x2, no learned parent. groups8/decoderTCN2; encoder{cell['encoder_channels']}/decoderhidden{cell['fourier_hidden']}; "
        "encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; "
        f"initSHA{cell['snapshot_sha256']}; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. "
        "Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION10_PLAN.md/SETUP.audit.")
    def phase(value,**extra):
        data={"phase":value,"updated_utc":datetime.now(timezone.utc).isoformat(),**extra}
        tmp=run/"pipeline_phase.tmp";tmp.write_text(json.dumps(data,indent=2)+"\n");tmp.replace(run/"pipeline_phase.json")
        print(json.dumps(data),flush=True)
    last=run/"checkpoints/last.pt"
    try:
        record(run,run.name,"running",checkpoint=last if last.exists() else snapshot,note=note)
        if not (run/"TRAINING_COMPLETE").exists():
            completed=0
            if last.exists():
                state=torch.load(last,map_location="cpu",weights_only=False)
                completed=state["global_step"];assert state["model_config"]==cell["effective_config"]["model"]
                assert state["optimizer"]["state"] and state["discriminator_optimizer"] is not None
                assert 0<completed<=STEPS
                event={"utc":datetime.now(timezone.utc).isoformat(),"resume_step":completed,"sha256":digest(last),
                    "optimizer_reset":False,"non_bitwise_worker_crop_RNG_replay":True}
                with (run/"resume_events.jsonl").open("a") as f:f.write(json.dumps(event)+"\n")
                del state
            if completed<STEPS:
                phase("training",resume_step=completed,initialization="latest last" if completed else "new untrained step0")
                command=["scripts/train.py","--config",run/"effective_config.yaml","--train-manifest",ROOT/"data/manifests/vctk_libritts/train.scp",
                    "--valid-manifest",ROOT/"data/manifests/vctk_libritts/valid.scp","--output-dir",run,
                    "--device","cuda","--max-total-steps",STEPS]
                command += ["--resume",last] if completed else ["--init-checkpoint",snapshot]
                execute(*command)
            final=torch.load(last,map_location="cpu",weights_only=False);assert final["global_step"]==STEPS
            del final;(run/"TRAINING_COMPLETE").touch()
        validations=[json.loads(line) for line in (run/"metrics.jsonl").read_text().splitlines()]
        assert [v["global_step"] for v in validations]==list(range(25000,STEPS+1,25000))
        nodes=[]
        for step in ENDPOINTS:
            phase("evaluation",step=step)
            ck=run/"checkpoints"/f"step_{step:08d}.pt"
            state=torch.load(ck,map_location="cpu",weights_only=False);assert state["global_step"]==step;del state
            sha=digest(ck);out=run/"evaluation"/f"step_{step:08d}";out.mkdir(parents=True,exist_ok=True)
            shafile=out/"checkpoint.sha256"
            if shafile.exists():assert shafile.read_text().split()[0]==sha
            else:shafile.write_text(f"{sha}  {ck}\n")
            if not (out/"ROUNDTRIP_COMPLETE").exists():
                execute("scripts/encode.py","--checkpoint",ck,"--input-dir",REFERENCE,"--output-dir",out/"bitstreams","--device","cuda")
                execute("scripts/decode.py","--checkpoint",ck,"--bitstream-dir",out/"bitstreams","--output-dir",out/"reconstructed","--device","cuda")
                execute("scripts/validate_submission.py","--input-dir",REFERENCE,"--bitstream-dir",out/"bitstreams","--output-dir",out/"reconstructed")
                actual=verify_roundtrip(REFERENCE,out)
                (out/"roundtrip_audit.json").write_text(json.dumps(actual,indent=2)+"\n");(out/"ROUNDTRIP_COMPLETE").touch()
            if not (out/"metrics/summary.json").exists():
                execute("scripts/evaluate.py","--reference-dir",REFERENCE,"--reconstructed-dir",out/"reconstructed","--output-dir",out/"metrics","--device","cuda")
            execute("scripts/complexity.py","--checkpoint",ck,"--output",out/"complexity.json")
            s=read(out/"metrics/summary.json");cost=read(out/"complexity.json")
            assert s["files"]==200 and not s["utmos_skipped"] and all(math.isfinite(v) for v in s["means"].values())
            assert math.isfinite(s["objective_quality_score"]) and cost==cell["complexity"]
            record(run,f"{run.name}_step{step:06d}","complete",checkpoint=ck,evaluation=out,note=note+f" Declared searched scratch endpoint{step}.")
            nodes.append({"step":step,"checkpoint":str(ck),"checkpoint_sha256":sha,"evaluation":str(out),"summary":s})
        selected=max(nodes,key=lambda n:(n["summary"]["objective_quality_score"],-n["step"]))
        selected["delta_vs_historical_best"]=selected["summary"]["objective_quality_score"]-51.66706654001837
        (run/"selection.json").write_text(json.dumps({"candidates":nodes,"selected":selected,"selection_kind":"two-node fixed development search, not confirmation"},indent=2)+"\n")
        out=Path(selected["evaluation"]);phase("selected_rvq_diagnostics",step=selected["step"])
        if not (out/"rvq_diagnostics.json").exists():
            execute("scripts/diagnose_rvq.py","--checkpoint",selected["checkpoint"],"--input-dir",REFERENCE,"--output",out/"rvq_diagnostics.json","--device","cuda")
        assert all(digest(ROOT/p)==h for p,h in setup["unchanged_historical_sha256"].items())
        record(run,run.name,"complete",checkpoint=Path(selected["checkpoint"]),evaluation=out,note=note+f" Selectedstep{selected['step']};delta_vs51.667066={selected['delta_vs_historical_best']:+.10f}.")
        (run/"PIPELINE_COMPLETE").touch();phase("complete",selected_step=selected["step"],score=selected["summary"]["objective_quality_score"])
    except Exception as error:
        phase("failed",error=repr(error))
        try:record(run,run.name,"failed",checkpoint=last if last.exists() else snapshot,note=note+" Error:"+repr(error))
        except Exception:pass
        raise


if __name__=="__main__":main()
