#!/usr/bin/env python3
"""Evaluate one fixed decoder interpolation; resumable, no training and no runtime guard."""
from datetime import datetime,timezone
import argparse
import fcntl
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import time

from prepare_champion8 import CELLS, ROOT, REFERENCE, PARENT, digest
from run_champion7_experiment import record,verify_roundtrip
from supervise_champion7 import gpu_state

PYTHON=ROOT/".venv-codec/bin/python"


def execute(*args):
    print("RUN",*map(str,args),flush=True)
    subprocess.run([str(PYTHON),*map(str,args)],cwd=ROOT,check=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cell",choices=CELLS);parser.add_argument("gpu",type=int)
    args=parser.parse_args()
    if args.gpu not in range(4):raise ValueError("GPU must be0..3")
    run=ROOT/f"runs/champion8_{args.cell}"
    assert (ROOT/"runs/champion8_setup/SETUP_COMPLETE").exists()
    assert run.is_dir()
    lock=(run/".pipeline.lock").open("a");fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if (run/"PIPELINE_COMPLETE").exists():return
    gpu_lock=(ROOT/"runs"/f".champion4_gpu{args.gpu}.lock").open("a")
    fcntl.flock(gpu_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    logfile=(run/"pipeline.log").open("a",buffering=1)
    os.dup2(logfile.fileno(),1);os.dup2(logfile.fileno(),2)
    setup=json.loads((ROOT/"CHAMPION8_SETUP.audit").read_text())
    evidence=setup["cells"][args.cell]
    checkpoint=run/"checkpoints/interpolated.pt"
    assert digest(checkpoint)==evidence["checkpoint_sha256"]
    assert all(digest(ROOT/p)==sha for p,sha in setup["source_sha256_unchanged"].items())

    def state(status,**extra):
        data={"status":status,"gpu":args.gpu,"updated_utc":datetime.now(timezone.utc).isoformat(),
              "new_gradient_updates":0,"runtime_resource_poll":False,**extra}
        tmp=run/"state.tmp";tmp.write_text(json.dumps(data,indent=2)+"\n");tmp.replace(run/"supervisor_state.json")
        print(json.dumps(data),flush=True)

    prior_status=None
    while True:
        if shutil.disk_usage(ROOT).free<10*2**30:raise RuntimeError("Prelaunch disk below10GiB")
        total,free,pids=gpu_state(args.gpu)
        if free>=8192:break
        if prior_status!="waiting":state("waiting_for_gpu_capacity",free_MiB=free,sharing_authorized=True)
        prior_status="waiting";time.sleep(30)
    os.environ.update(CUDA_VISIBLE_DEVICES=str(args.gpu),PYTHONNOUSERSITE="1",
        TORCH_HOME=str(ROOT/"data/torch-cache"),PYTHONUNBUFFERED="1",OMP_NUM_THREADS="4")
    lineage=evidence["lineage"]
    note=(f"Posthoc decoder-parameter interpolation, ZERO new training, NOT untrained initialization. "
          f"alpha={lineage['alpha']}; parent500k51.624336 and donor C7local100k/cumulative600k. "
          "All encoder/latent/RVQ input+output projections/codebooks/EMA/buffers bitwise parent; "
          "no optimizer or discriminator in inference-only export. Four registered dev-search candidates only. "
          "CHAMPION8_PLAN.md/SETUP.audit; source SHAs in lineage.json. No runtime resource guard per user.")
    out=run/"evaluation";out.mkdir(exist_ok=True)
    (run/"run_metadata.json").write_text(json.dumps({"created_utc":datetime.now(timezone.utc).isoformat(),
        "kind":"posthoc interpolation evaluation only","gpu":args.gpu,"new_gradient_updates":0,
        "checkpoint_sha256":evidence["checkpoint_sha256"],"alpha":lineage["alpha"],
        "source_sha256":setup["source_sha256_unchanged"],"launch_free_MiB":free,"runtime_resource_poll":False},indent=2)+"\n")
    state("running",phase="evaluation",launch_free_MiB=free,sharing_authorized=True)
    try:
        record(run,f"champion8_{args.cell}","running",checkpoint=checkpoint,note=note)
        shafile=out/"checkpoint.sha256"
        if shafile.exists():assert shafile.read_text().split()[0]==digest(checkpoint)
        else:shafile.write_text(f"{digest(checkpoint)}  {checkpoint}\n")
        if not (out/"ROUNDTRIP_COMPLETE").exists():
            execute("scripts/encode.py","--checkpoint",checkpoint,"--input-dir",REFERENCE,"--output-dir",out/"bitstreams","--device","cuda")
            for bit in (out/"bitstreams").glob("*.bin"):
                assert bit.read_bytes()==(PARENT.parent.parent/"evaluation/bitstreams"/bit.name).read_bytes()
            assert len(list((out/"bitstreams").glob("*.bin")))==200
            execute("scripts/decode.py","--checkpoint",checkpoint,"--bitstream-dir",out/"bitstreams","--output-dir",out/"reconstructed","--device","cuda")
            execute("scripts/validate_submission.py","--input-dir",REFERENCE,"--bitstream-dir",out/"bitstreams","--output-dir",out/"reconstructed")
            actual=verify_roundtrip(REFERENCE,out)
            actual["all200_bitstreams_identical_to_parent"]=True
            (out/"roundtrip_audit.json").write_text(json.dumps(actual,indent=2)+"\n")
            (out/"ROUNDTRIP_COMPLETE").touch()
        if not (out/"metrics/summary.json").exists():
            execute("scripts/evaluate.py","--reference-dir",REFERENCE,"--reconstructed-dir",out/"reconstructed","--output-dir",out/"metrics","--device","cuda")
        execute("scripts/complexity.py","--checkpoint",checkpoint,"--output",out/"complexity.json")
        summary=json.loads((out/"metrics/summary.json").read_text())
        cost=json.loads((out/"complexity.json").read_text())
        assert summary["files"]==200 and not summary["utmos_skipped"]
        assert all(math.isfinite(x) for x in summary["means"].values()) and math.isfinite(summary["objective_quality_score"])
        assert cost==evidence["complexity"]
        assert all(digest(ROOT/p)==sha for p,sha in setup["source_sha256_unchanged"].items())
        record(run,f"champion8_{args.cell}","complete",checkpoint=checkpoint,evaluation=out,
            note=note+f" Gain_vs_parent={summary['objective_quality_score']-setup['parent_score']:+.10f}.")
        (run/"PIPELINE_COMPLETE").touch();state("complete",score=summary["objective_quality_score"])
    except Exception as error:
        state("failed",error=repr(error))
        record(run,f"champion8_{args.cell}","failed",checkpoint=checkpoint,note=note+" Error:"+repr(error))
        raise


if __name__=="__main__":main()
