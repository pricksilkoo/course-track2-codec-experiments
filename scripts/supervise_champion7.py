#!/usr/bin/env python3
"""Wait for GPU capacity and supervise one resumable experiment.

Uses a private process group for our pipeline. Never sends signals to any
process found through nvidia-smi. Sharing requires the explicit --allow-shared
flag, used only after user authorization and full-backward peak profiling.
"""
from __future__ import annotations
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def gpu_state(index: int) -> tuple[int, int, list[int]]:
    text = subprocess.check_output(["nvidia-smi", f"--id={index}",
        "--query-gpu=uuid,memory.total,memory.free", "--format=csv,noheader,nounits"], text=True)
    uuid, total, free = [part.strip() for part in text.strip().split(",")]
    processes = subprocess.check_output(["nvidia-smi", "--query-compute-apps=gpu_uuid,pid",
                                        "--format=csv,noheader,nounits"], text=True)
    pids = [int(parts[1].strip()) for line in processes.splitlines()
            if len(parts := line.split(",")) == 2 and parts[0].strip() == uuid]
    return int(total), int(free), pids


def stop_own_pipeline(child: subprocess.Popen) -> None:
    if child.poll() is None:
        os.killpg(child.pid, signal.SIGTERM)
        try:
            child.wait(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run")
    parser.add_argument("gpu", type=int)
    parser.add_argument("config")
    parser.add_argument("--steps", type=int, default=100000)
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--allow-shared", action="store_true")
    args = parser.parse_args()
    allowed = {"champion7_a_continue", "champion7_b_si", "champion7_c_gan", "champion7_d_both"}
    if args.run not in allowed or args.gpu not in range(4) or args.steps != 100000:
        raise ValueError("supervisor is restricted to the registered study")
    run = ROOT / "runs" / args.run
    run.mkdir(parents=True, exist_ok=True)
    lock = (run / ".supervisor.lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    gpu_lock = (ROOT / "runs" / f".champion4_gpu{args.gpu}.lock").open("w")
    fcntl.flock(gpu_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    state_path = run / "supervisor_state.json"
    completion = run / "PIPELINE_COMPLETE"

    def record(status: str, **extra) -> None:
        data = {"status": status, "gpu": args.gpu,
                "updated_utc": datetime.now(timezone.utc).isoformat(), **extra}
        temporary = state_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(data, indent=2) + "\n")
        temporary.replace(state_path)
        print(json.dumps(data), flush=True)

    child = None

    def interrupted(signum, frame):
        if child is not None:
            stop_own_pipeline(child)
        record("interrupted", reason=f"signal {signum}; latest checkpoint preserved")
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    previous_status = None
    while not completion.is_file():
        if shutil.disk_usage(ROOT).free < 10 * 2**30:
            record("safety_stop", reason="/storage1 below 10 GiB; no launch")
            return
        total, free, pids = gpu_state(args.gpu)
        if (pids and not args.allow_shared) or free < 20480:
            if previous_status != "waiting_for_gpu_capacity":
                record("waiting_for_gpu_capacity", other_gpu_pids=pids, free_MiB=free,
                       sharing_authorized=args.allow_shared)
            previous_status = "waiting_for_gpu_capacity"
            time.sleep(args.poll_seconds)
            continue
        # Two consecutive idle samples avoid acquiring a momentary gap between
        # someone else's restarts. GPU lock prevents our own duplicate workers.
        time.sleep(5)
        _, free, pids = gpu_state(args.gpu)
        if (pids and not args.allow_shared) or free < 20480:
            continue
        command = [str(ROOT / ".venv-codec/bin/python"), "scripts/run_champion7_experiment.py", args.run,
                   str(args.gpu), args.config, str(args.steps)]
        record("running", command=command, free_MiB=free,
               sharing_authorized=args.allow_shared, existing_gpu_pids=pids)
        child = subprocess.Popen(command, cwd=ROOT, start_new_session=True,
                                 env={**os.environ, "PYTHONUNBUFFERED": "1", "OMP_NUM_THREADS": "4"})
        while child.poll() is None:
            time.sleep(min(2, args.poll_seconds))
            if child.poll() is not None:
                break
            if shutil.disk_usage(ROOT).free < 10 * 2**30:
                stop_own_pipeline(child)
                record("safety_stop", reason="/storage1 below 10 GiB; latest checkpoint preserved")
                return
            try:
                total, free, pids = gpu_state(args.gpu)
            except (subprocess.SubprocessError, ValueError) as error:
                stop_own_pipeline(child)
                record("needs_attention", reason=f"cannot verify GPU safety: {error}")
                return
            unrelated = []
            for pid in pids:
                try:
                    if os.getpgid(pid) != child.pid:
                        unrelated.append(pid)
                except ProcessLookupError:
                    pass
            if free < 8192 or (unrelated and not args.allow_shared):
                stop_own_pipeline(child)
                record("safety_stop", reason="GPU memory risk or external workload appeared",
                       free_MiB=free, other_gpu_pids=unrelated)
                return
        if child.returncode != 0:
            record("failed", exit_code=child.returncode,
                   reason="diagnose before resuming only this run; no automatic retry loop")
            return
        if not completion.is_file():
            record("needs_attention", reason="runner exited zero without completion marker")
            return
    record("complete")


if __name__ == "__main__":
    main()
