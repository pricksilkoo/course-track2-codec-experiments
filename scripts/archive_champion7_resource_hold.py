#!/usr/bin/env python3
"""Preserve attempt03 and mark a resource-policy decision hold; never relaunch."""
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import re
import shutil

from run_champion7_experiment import CELLS, PARENT, PARENT_SHA, digest, record

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT / "CHAMPION7_RECOVERY03.audit"
    if output.exists():
        raise RuntimeError("Third attempt already archived; no duplicate hold registration")
    assert digest(PARENT) == PARENT_SHA
    report = {"created_utc": datetime.now(timezone.utc).isoformat(),
        "cause": "After continuous600s idle, all four ran about1575 batches; new outside PIDs triggered exclusive guard despite about38GiB free. No OOM/nonfinite/Traceback found.",
        "status": "all four training processes stopped; no live capacity waiters; awaiting user resource-policy choice",
        "decision_requested": ["permit sharing with8GiB floor and more frequent recovery checkpoints", "continue waiting for exclusive idle GPU"],
        "parent_sha256": PARENT_SHA, "no_new_evaluation_results": True, "cells": {}}
    for cell in CELLS:
        run = ROOT / f"runs/champion7_{cell}"
        state = json.loads((run / "supervisor_state.json").read_text())
        assert state["status"] == "safety_stop" and not (run / "PIPELINE_COMPLETE").exists()
        assert not list((run / "checkpoints").glob("*.pt"))
        with (run / ".supervisor.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            raw = (run / "pipeline.log").read_text()
            assert not any(x in raw.lower() for x in ("out of memory", "traceback (most recent call last)", "non-finite loss"))
            last = raw.rsplit("RUN scripts/train.py", 1)[-1]
            visible = re.findall(r"(\d+)/12343", last)
            archive = run / "attempts/attempt03_exclusive_guard"
            archive.mkdir(parents=True, exist_ok=False)
            hashes = {}
            for name in ("supervisor_state.json", "supervisor.log", "pipeline.log", "run_metadata.json", "effective_config.yaml", "lineage.json"):
                shutil.copy2(run / name, archive / name)
                hashes[name] = digest(archive / name)
            report["cells"][cell] = {"prior_state": state, "archive": str(archive.relative_to(ROOT)),
                "archive_sha256": hashes, "last_visible_attempt03_batch": int(visible[-1]),
                "formal_checkpoint_count": 0, "progress_recoverable": False,
                "next_initial_model_if_approved": "original trained500k parent, not a resume"}
        record(run, f"champion7_{cell}", "planned", note=(
            "TRAINING STOPPED; awaiting user resource-policy choice, no live GPU waiter. "
            "Third attempt reached about1575 batches after600s idle then exclusive guard saw other PID, "
            "despite ample memory. No formal checkpoint: progress cannot resume. "
            f"Preserve all3 attempt archives; CHAMPION7_RECOVERY03.audit. Parent trained500k SHA256 {PARENT_SHA}. "
            "Do not automatically retry or revert to sharing until user chooses. "
            "No change to model/batch/seed100k-stage/16 fixed200 search nodes; no new quality result."))
    output.write_text(json.dumps(report, indent=2)+"\n")
    (ROOT / "runs/champion7_setup/recovery03_report.json").write_text(output.read_text())
    print("All third-attempt evidence archived; no task restarted or queued")


if __name__ == "__main__":
    main()
