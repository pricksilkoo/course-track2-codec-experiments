#!/usr/bin/env python3
"""User-approved C6 capacity sharing; own lock, startup gate, no runtime polling."""
from datetime import datetime, timezone
import fcntl
import json
import os
import shutil
import signal
import subprocess
import time
from supervise_champion7 import ROOT, gpu_state, stop_own_pipeline

STEPS = 500000


def choose_gpu():
    candidates = []
    for gpu in range(4):
        total, free, pids = gpu_state(gpu)
        if free >= 8192:
            candidates.append((gpu, free, pids))
    return max(candidates, key=lambda item: (item[1], -item[0])) if candidates else None


def main():
    run = ROOT / "runs/c6_30ms_b_s3407"
    own = (run / ".supervisor.lock").open("a")
    fcntl.flock(own, fcntl.LOCK_EX | fcntl.LOCK_NB)
    child = None

    def state(status, **extra):
        data = {"status": status, "updated_utc": datetime.now(timezone.utc).isoformat(),
                "training_total_steps": STEPS, "startup_idle_required": False,
                "sharing_authorized": True, "launch_free_MiB": 8192,
                "runtime_resource_poll": False, "automatic_retry": False,
                "supervisor": "scripts/supervise_c6_30ms_shared.py", **extra}
        tmp = run / "supervisor_state.tmp"
        tmp.write_text(json.dumps(data, indent=2) + "\n")
        tmp.replace(run / "supervisor_state.json")
        print(json.dumps(data), flush=True)

    def interrupted(signum, frame):
        if child is not None:
            stop_own_pipeline(child)
        state("interrupted", signal=signum)
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGINT, interrupted)
    signal.signal(signal.SIGTERM, interrupted)
    if (run / "PIPELINE_COMPLETE").exists():
        state("complete")
        return
    announced = False
    while True:
        candidate = choose_gpu() if shutil.disk_usage(ROOT).free >= 10 * 2**30 else None
        if candidate is not None:
            break
        if not announced:
            state("waiting_for_shared_gpu_capacity", reason="free>=8192MiB,disk>=10GiB; other PIDs allowed; preserve all existing jobs")
            announced = True
        time.sleep(30)
    gpu, free, pids = candidate
    command = [str(ROOT / ".venv-codec/bin/python"), "-u", "scripts/run_c6_30ms_experiment.py", "b_s3407", str(gpu)]
    state("running", gpu=gpu, observed_launch_free_MiB=free, existing_gpu_pids=pids, command=command)
    child = subprocess.Popen(command, cwd=ROOT, start_new_session=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONNOUSERSITE": "1", "OMP_NUM_THREADS": "4", "PYTHONUNBUFFERED": "1"})
    # No GPU/disk queries or retry after dispatch. Existing C12 GPU locks stay untouched.
    child.wait()
    if child.returncode:
        state("failed", gpu=gpu, exit_code=child.returncode, reason="preserve and diagnose actual exit; no automatic retry")
        raise SystemExit(child.returncode if child.returncode > 0 else 1)
    state("complete" if (run / "PIPELINE_COMPLETE").exists() else "needs_attention", gpu=gpu)


if __name__ == "__main__":
    main()
