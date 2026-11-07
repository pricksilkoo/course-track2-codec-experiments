#!/usr/bin/env python3
"""Archive the diagnosed memory stop and queue only four saved-checkpoint resumes."""
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess

import torch
from run_champion7_experiment import CELLS, PARENT, PARENT_SHA, digest, record

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = dict(zip(CELLS, (75000, 76000, 73000, 73000)))


def tail(path, size=65536):
    with path.open("rb") as stream:
        stream.seek(max(0, os.fstat(stream.fileno()).st_size-size))
        return stream.read().decode(errors="replace")


def tensors_finite(value):
    if isinstance(value, torch.Tensor):
        return not value.is_floating_point() or bool(torch.isfinite(value).all())
    if isinstance(value, dict): return all(tensors_finite(x) for x in value.values())
    if isinstance(value, (list, tuple)): return all(tensors_finite(x) for x in value)
    return True


def main():
    torch.set_num_threads(4)
    output = ROOT / "CHAMPION7_RECOVERY04.audit"
    if output.exists(): raise RuntimeError("Already queued; do not duplicate")
    assert digest(PARENT) == PARENT_SHA
    report = {"created_utc": datetime.now(timezone.utc).isoformat(),
        "cause": "2026-11-06T17:07:51-53Z external task memory surge caused GPUfree4600/2561MiB, below8192MiB guard",
        "not_an_exclusive_pid_stop": True,
        "policy": "user-authorized shared capacity waiting;>=20GiB launch,8GiB runtime,disk10GiB; no forced launch while current free8-12GiB",
        "no_blind_oom_retry": True, "parent_sha256": PARENT_SHA,
        "resume_not_parent_restart": True, "worker_crop_rng_replay_bitwise": False,
        "model_loss_seed_batch_budget_search_unchanged": True,
        "new_gpu_tests": False, "cells": {}}
    locks = []
    for gpu, c in enumerate(CELLS):
        run = ROOT / f"runs/champion7_{c}"
        state = json.loads((run/"supervisor_state.json").read_text())
        assert state["status"] == "safety_stop" and state["free_MiB"] < 8192
        assert not (run/"TRAINING_COMPLETE").exists() and not (run/"PIPELINE_COMPLETE").exists()
        assert subprocess.check_output(["tmux", "display-message", "-p", "-t",
            f"codec_champion7_v1:{c}", "#{pane_dead}"], text=True).strip() == "1"
        for path in (run/".pipeline.lock", run/".supervisor.lock", ROOT/"runs"/f".champion4_gpu{gpu}.lock"):
            lock = path.open("a"); fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB); locks.append(lock)
        last = run/"checkpoints/last.pt"
        ck = torch.load(last, map_location="cpu", weights_only=False)
        step = int(ck["global_step"])
        assert step == EXPECTED[c] and step < 100000
        assert len(ck["model"]) == 211 and ck["discriminator"]
        assert ck["optimizer"]["state"] and ck["discriminator_optimizer"]["state"]
        assert tensors_finite(ck), "Checkpoint integrity failure; do not queue"
        raw = tail(run/"pipeline.log")
        assert not any(x in raw for x in ("Traceback", "OutOfMemoryError", "nonfinite training"))
        matches = re.findall(r"epoch (\d+)/1000:.*?(\d+)/12343", raw)
        epoch,batch = map(int, matches[-1])
        visible_step = (epoch-1)*12343+batch
        archive = run/"attempts/attempt04_shared_memory_guard"
        archive.mkdir(parents=True, exist_ok=False)
        names = ["supervisor_state.json", "supervisor.log", "pipeline.log", "run_metadata.json",
                 "effective_config.yaml", "lineage.json", "recovery_policy.json",
                 "recovery_checkpoints.jsonl", "metrics.jsonl"]
        hashes = {}
        for name in names:
            shutil.copy2(run/name, archive/name); hashes[name] = digest(archive/name)
        (archive/"checkpoints").mkdir()
        shutil.copy2(last, archive/"checkpoints/last.pt")
        sha = digest(last)
        assert digest(archive/"checkpoints/last.pt") == sha
        vals = [json.loads(line) for line in (run/"metrics.jsonl").read_text().splitlines()]
        assert [x["global_step"] for x in vals] == ([25000,50000,75000] if c in CELLS[:2] else [25000,50000])
        report["cells"][c] = {"gpu": gpu, "prior_state": state,
            "archive": str(archive.relative_to(ROOT)), "archive_sha256": hashes,
            "resume_checkpoint": str(last), "resume_checkpoint_sha256": sha,
            "archived_checkpoint_sha256": sha, "resume_global_step": step,
            "resume_cumulative_parent_step": 500000+step,
            "checkpoint_kind": ck.get("checkpoint_kind", "validated"),
            "epoch": ck["epoch"], "batch_in_epoch": ck["batch_in_epoch"],
            "complete_optimizer_and_ema_state_verified_finite": True,
            "last_visible_step_approx": visible_step,
            "unsaved_visible_updates_discarded_approx": max(0,visible_step-step),
            "actual_validation_steps": [v["global_step"] for v in vals],
            "existing_step_snapshots_sha256": {p.name:digest(p) for p in sorted((run/"checkpoints").glob("step_*.pt"))}}
        del ck
    output.write_text(json.dumps(report,indent=2)+"\n")
    (ROOT/"runs/champion7_setup/recovery04_report.json").write_text(output.read_text())
    for lock in locks: lock.close()
    for gpu,c in enumerate(CELLS):
        run = ROOT/f"runs/champion7_{c}"
        cell = report["cells"][c]
        record(run, f"champion7_{c}", "planned", checkpoint=run/"checkpoints/last.pt", note=(
            f"Diagnosed shared memory guard17:07UTC. Retained genuine last local{cell['resume_global_step']} "
            f"SHA256 {cell['resume_checkpoint_sha256']}; will RESUME it, not original parent/smoke. "
            "Wait>=20GiB capacity with user-authorized sharing,8GiB floor. Complete G/D optimizers/EMA preserved; "
            "worker/crop/RNG replay non-bitwise. CHAMPION7_RECOVERY04.audit, immutable attempt04 archive. "
            "Same100k total stage/16 declared score nodes; no new tests or blind launch."))
        command = [str(ROOT/".venv-codec/bin/python"),"-u","scripts/supervise_champion7.py",
            f"champion7_{c}",str(gpu),f"configs/champion7/{c}.yaml","--allow-shared","--steps","100000"]
        shell=shlex.join(command)+" >> "+shlex.quote(str(run/"supervisor.log"))+" 2>&1"
        subprocess.run(["tmux","respawn-pane","-t",f"codec_champion7_v1:{c}","-c",str(ROOT),shell],check=True)
        print(f"Queued capacity-based resume {c} local{cell['resume_global_step']}, same GPU{gpu}",flush=True)


if __name__ == "__main__": main()
