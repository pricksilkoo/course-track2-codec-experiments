#!/usr/bin/env python3
"""One user-authorized capacity probe; 8GiB free floor, signals only own group."""
import json
import os
from pathlib import Path
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def free_memory(gpu):
    return int(subprocess.check_output(["nvidia-smi", f"--id={gpu}",
        "--query-gpu=memory.free", "--format=csv,noheader,nounits"], text=True).strip())


def main():
    setup = ROOT / "runs/champion7_setup"
    setup.mkdir(exist_ok=True, parents=True)
    result_path = setup / "shared_capacity_probe.json"
    if result_path.exists():
        raise RuntimeError("capacity probe already recorded; no blind retries")
    before = {gpu: free_memory(gpu) for gpu in range(4)}
    gpu = max(before, key=before.get)
    report = {"before_free_MiB": before, "gpu": gpu, "minimum_free_MiB": 8192,
        "scope": "one two-step full-batch full-GAN probe, not a formal run"}
    if before[gpu] < 10240:
        report["status"] = "not_launched_insufficient_capacity"
        result_path.write_text(json.dumps(report, indent=2)+"\n")
        return
    log = (setup / "shared_capacity_probe.log").open("w")
    command = [str(ROOT / ".venv-codec/bin/python"), "scripts/profile_champion7.py",
        "--config", "configs/champion7/d_both.yaml", "--output", "runs/_smoke_champion7_shared_probe"]
    child = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
        start_new_session=True, env={**os.environ, "CUDA_VISIBLE_DEVICES": str(gpu), "OMP_NUM_THREADS": "4"})

    def stop():
        if child.poll() is None:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()

    def interrupted(signum, frame):
        report["status"] = "interrupted_probe_only"
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)

    try:
        while child.poll() is None:
            current = free_memory(gpu)
            report["lowest_free_MiB"] = min(report.get("lowest_free_MiB", current), current)
            if current < 8192:
                stop()
                report["status"] = "own_probe_stopped_below_8GiB_free"
                break
            time.sleep(.2)
        else:
            report["status"] = "passed" if child.returncode == 0 else "failed_check_log"
    finally:
        stop()
        report.setdefault("status", "probe_error_check_log")
        report["exit_code"] = child.returncode
        result_path.write_text(json.dumps(report, indent=2)+"\n")
        log.close()
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
