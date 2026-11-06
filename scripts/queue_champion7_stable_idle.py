#!/usr/bin/env python3
"""Archive attempt02 and rearm only the four safety-stopped idle waiters once."""
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import shlex
import shutil
import subprocess

from run_champion7_experiment import CELLS, PARENT, PARENT_SHA, digest, record

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT / "CHAMPION7_RECOVERY02.audit"
    if output.exists():
        raise RuntimeError("Second recovery already queued, do not duplicate")
    assert digest(PARENT) == PARENT_SHA
    report = {"created_utc": datetime.now(timezone.utc).isoformat(),
        "cause": "Old outside job ended, brief idle gap triggered loading; new outside multi-GPU job2016678 appeared, so exclusive supervisors stopped own groups even though memory was ample.",
        "new_policy": "no unrelated GPU PID and>=20GiB free continuously observed600s; any ineligible observation resets timer; runtime8GiB/disk10GiB unchanged",
        "parent_sha256": PARENT_SHA, "new_optimization_iterations_observed": False, "cells": {}}
    locks = []
    for cell in CELLS:
        run = ROOT / f"runs/champion7_{cell}"
        state = json.loads((run / "supervisor_state.json").read_text())
        assert state["status"] == "safety_stop" and not (run / "PIPELINE_COMPLETE").exists()
        assert not list((run / "checkpoints").glob("*.pt"))
        for name in (".pipeline.lock", ".supervisor.lock"):
            lock = (run / name).open("a")
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            locks.append(lock)
        tail = (run / "pipeline.log").read_text().rsplit("RUN scripts/train.py", 1)[-1]
        assert "epoch 1/1000" not in tail
        archive = run / "attempts/attempt02_external_job_arrival"
        archive.mkdir(parents=True, exist_ok=False)
        hashes = {}
        for name in ("supervisor_state.json", "supervisor.log", "pipeline.log", "run_metadata.json", "effective_config.yaml", "lineage.json"):
            shutil.copy2(run / name, archive / name)
            hashes[name] = digest(archive / name)
        report["cells"][cell] = {"prior_state": state, "archive": str(archive.relative_to(ROOT)), "archive_sha256": hashes,
            "formal_checkpoint_count": 0, "new_epoch_progress_observed": False,
            "next_start": "original trained500k parent, not resume of lost attempt01 steps"}
    output.write_text(json.dumps(report, indent=2)+"\n")
    (ROOT / "runs/champion7_setup/recovery02_report.json").write_text(output.read_text())
    for lock in locks:
        lock.close()
    for gpu, cell in enumerate(CELLS):
        run = ROOT / f"runs/champion7_{cell}"
        target = f"codec_champion7_v1:{cell}"
        dead = subprocess.check_output(["tmux", "display-message", "-p", "-t", target, "#{pane_dead}"], text=True).strip()
        assert dead == "1", "Never replace a live waiter or healthy worker"
        record(run, f"champion7_{cell}", "planned", note=(
            "Waiting for a continuously idle GPU600s, no --allow-shared. Old-job/new-job handoff briefly started loading, "
            "new external PID caused exclusive guard stop before new epoch progress; no formal checkpoint. "
            "Preserve attempt01 unsaved~6000-step history and attempt02 archived logs. "
            f"Will load trained500k parent SHA256 {PARENT_SHA}, same100k stage/seed/config; NOT checkpoint resume. "
            "Evidence CHAMPION7_RECOVERY01.audit and CHAMPION7_RECOVERY02.audit.16 declared dev score nodes unchanged."))
        command = [str(ROOT / ".venv-codec/bin/python"), "-u", "scripts/supervise_champion7.py",
            f"champion7_{cell}", str(gpu), f"configs/champion7/{cell}.yaml", "--steps", "100000"]
        shell = shlex.join(command)+" >> "+shlex.quote(str(run/"supervisor.log"))+" 2>&1"
        subprocess.run(["tmux", "respawn-pane", "-t", target, "-c", str(ROOT), shell], check=True)
        print(f"Rearmed {cell}: idle-only600s continuous eligibility, no GPU training yet", flush=True)


if __name__ == "__main__":
    main()
