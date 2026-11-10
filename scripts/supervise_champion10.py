#!/usr/bin/env python3
"""Startup capacity only; no runtime resource polling or automatic failure retry."""
from datetime import datetime,timezone
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time

from preflight_champion10 import ROOT,CELLS,STEPS
from supervise_champion7 import gpu_state,stop_own_pipeline


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("cell",choices=CELLS);p.add_argument("gpu",type=int)
    args=p.parse_args();assert args.gpu in range(4)
    run=ROOT/f"runs/champion10_{args.cell}"
    lock=(run/".supervisor.lock").open("a");fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    gpu_lock=(ROOT/f"runs/.champion4_gpu{args.gpu}.lock").open("a");fcntl.flock(gpu_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    child=None
    def state(status,**extra):
        data={"status":status,"updated_utc":datetime.now(timezone.utc).isoformat(),"gpu":args.gpu,
            "launch_free_MiB":8192,"runtime_resource_poll":False,"sharing_authorized":True,
            "training_total_steps":STEPS,**extra}
        tmp=run/"supervisor_state.tmp";tmp.write_text(json.dumps(data,indent=2)+"\n");tmp.replace(run/"supervisor_state.json")
        print(json.dumps(data),flush=True)
    def interrupted(signum,frame):
        if child is not None:stop_own_pipeline(child)
        state("interrupted",signal=signum)
        raise SystemExit(128+signum)
    signal.signal(signal.SIGINT,interrupted);signal.signal(signal.SIGTERM,interrupted)
    if (run/"PIPELINE_COMPLETE").exists():state("complete");return
    prior=None
    while True:
        disk=shutil.disk_usage(ROOT).free
        total,free,pids=gpu_state(args.gpu)
        if disk>=10*2**30 and free>=8192:break
        if prior!="waiting":state("waiting_for_gpu_capacity",observed_free_MiB=free,disk_free_GiB=disk/2**30)
        prior="waiting";time.sleep(30)
    command=[str(ROOT/".venv-codec/bin/python"),"-u","scripts/run_champion10_experiment.py",args.cell,str(args.gpu)]
    state("running",command=command,observed_launch_free_MiB=free,existing_gpu_pids=pids)
    child=subprocess.Popen(command,cwd=ROOT,start_new_session=True,
        env={**os.environ,"OMP_NUM_THREADS":"4","PYTHONUNBUFFERED":"1"})
    # Explicit user policy: no GPU/disk checks after pipeline begins. Locks and
    # signal scoping persist, but outside processes and memory drops never stop it.
    child.wait()
    if child.returncode:
        state("failed",exit_code=child.returncode,reason="diagnose actual exit before resuming affected run; no blind retries")
        raise SystemExit(child.returncode if child.returncode>0 else 1)
    if not (run/"PIPELINE_COMPLETE").exists():
        state("needs_attention",reason="runner exited zero without completion marker");return
    state("complete")


if __name__=="__main__":main()
