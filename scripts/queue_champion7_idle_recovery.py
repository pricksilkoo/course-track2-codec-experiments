#!/usr/bin/env python3
"""Archive the diagnosed first safety-stop, then queue only affected cells idle-only.

No private run had reached its first25k checkpoint. Preserve the abandoned
attempt and disclose that the next trajectory must reload the original trained
parent, not pretend to resume the lost progress. Never signal external jobs.
"""
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess

from run_champion7_experiment import CELLS, PARENT, PARENT_SHA, digest, record

ROOT = Path(__file__).resolve().parents[1]
SESSION = "codec_champion7_v1"


def main():
    result = ROOT / "runs/champion7_setup/recovery01_report.json"
    if result.exists():
        raise RuntimeError("Recovery already registered; inspect existing waiters, no duplicate retry")
    assert digest(PARENT) == PARENT_SHA
    report = {"created_utc": datetime.now(timezone.utc).isoformat(),
        "cause": "External GPU memory jumped; all four private groups safety-stopped, no OOM/nonfinite/traceback.",
        "next_policy": "idle-only: no --allow-shared;20GiB launch,8GiB runtime GPUfree floor, no outside processes altered",
        "recovery": "No formal last.pt existed before first25k validation. Restart only affected incomplete stage from original trained500k parent with same seed/config; unsaved steps are lost, not resumed.",
        "parent_sha256": PARENT_SHA, "cells": {}}
    locks = []
    for cell in CELLS:
        run = ROOT / f"runs/champion7_{cell}"
        state = json.loads((run / "supervisor_state.json").read_text())
        if state["status"] != "safety_stop" or (run / "PIPELINE_COMPLETE").exists():
            raise RuntimeError(f"Do not touch healthy/completed/non-diagnosed cell {cell}")
        if list((run / "checkpoints").glob("*.pt")):
            raise RuntimeError("Checkpoint exists: recover from it instead of replaying source")
        for name in (".supervisor.lock", ".pipeline.lock"):
            lock = (run / name).open("a")
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            locks.append(lock)
        raw = (run / "pipeline.log").read_text()
        assert not any(token in raw.lower() for token in ("traceback (most recent call last)", "out of memory", "non-finite loss"))
        visible = re.findall(r"(\d+)/12343", raw)
        archive = run / "attempts/attempt01_safety_stop"
        archive.mkdir(parents=True, exist_ok=False)
        hashes = {}
        for name in ("supervisor_state.json", "supervisor.log", "pipeline.log", "run_metadata.json", "effective_config.yaml", "lineage.json"):
            shutil.copy2(run / name, archive / name)
            hashes[name] = digest(archive / name)
        report["cells"][cell] = {"prior_state": state, "archive": str(archive.relative_to(ROOT)),
            "archive_sha256": hashes, "last_visible_epoch_batch": int(visible[-1]),
            "formal_checkpoint_count": 0, "recovered_local_step": 0,
            "unchanged_stage_budget": 100000, "original_profile_retained": True}
    result.write_text(json.dumps(report, indent=2)+"\n")
    (ROOT / "CHAMPION7_RECOVERY01.audit").write_text(result.read_text())
    for lock in locks:
        lock.close()
    for cell in CELLS:
        run = ROOT / f"runs/champion7_{cell}"
        record(run, f"champion7_{cell}", "planned", note=(
            "Idle-GPU queue after external memory surge caused private safety stop; not currently training. "
            f"No first25k checkpoint existed; approx{report['cells'][cell]['last_visible_epoch_batch']} visible batches lost. "
            "Will reload original learned500k parent, not claim checkpoint resume. Same100k new-stage budget/seed/config; "
            f"parent SHA256 {PARENT_SHA}; no new seed or development outcome selection. "
            "Prior raw metadata/logs archived under run/attempts/attempt01_safety_stop; CHAMPION7_RECOVERY01.audit. "
            "Idle-only/no sharing retries,20GiB launch/8GiB runtime protection; preserve completed GPU profile. "
            "Four declared25k/50k/75k/100k fixed200 score-search nodes unchanged."))
    existing = subprocess.run(["tmux", "has-session", "-t", SESSION], capture_output=True).returncode == 0
    for gpu, cell in enumerate(CELLS):
        cmd = [str(ROOT / ".venv-codec/bin/python"), "-u", "scripts/supervise_champion7.py",
            f"champion7_{cell}", str(gpu), f"configs/champion7/{cell}.yaml", "--steps", "100000"]
        # No --allow-shared: require an actually idle device, not a transient
        # low-memory phase of the same outside multi-GPU task.
        shell = shlex.join(cmd) + " >> " + shlex.quote(str(ROOT / f"runs/champion7_{cell}/supervisor.log")) + " 2>&1"
        if not existing:
            subprocess.run(["tmux", "new-session", "-d", "-s", SESSION, "-n", cell, "-c", str(ROOT)], check=True)
            existing = True
            target = f"{SESSION}:{cell}"
            subprocess.run(["tmux", "set-window-option", "-t", target, "remain-on-exit", "on"], check=True)
            subprocess.run(["tmux", "send-keys", "-t", target, "exec "+shell, "C-m"], check=True)
        elif cell == "a_continue":
            target = f"{SESSION}:{cell}"
            dead = subprocess.check_output(["tmux", "display-message", "-p", "-t", target, "#{pane_dead}"], text=True).strip()
            if dead != "1":
                raise RuntimeError("A pane is not dead; do not duplicate or replace it")
            subprocess.run(["tmux", "set-window-option", "-t", target, "remain-on-exit", "on"], check=True)
            subprocess.run(["tmux", "respawn-pane", "-t", target, "-c", str(ROOT), shell], check=True)
        else:
            subprocess.run(["tmux", "new-window", "-d", "-t", SESSION, "-n", cell, "-c", str(ROOT)], check=True)
            target = f"{SESSION}:{cell}"
            subprocess.run(["tmux", "set-window-option", "-t", target, "remain-on-exit", "on"], check=True)
            subprocess.run(["tmux", "send-keys", "-t", target, "exec "+shell, "C-m"], check=True)
        print(f"Queued {cell} idle-only on GPU{gpu}; no training until device has no other PIDs", flush=True)


if __name__ == "__main__":
    main()
