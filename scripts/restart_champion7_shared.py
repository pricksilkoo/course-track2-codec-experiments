#!/usr/bin/env python3
"""One-shot user-approved shared launch of four diagnosed stopped cells."""
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import shlex
import subprocess
import sys

from run_champion7_experiment import CELLS, PARENT, PARENT_SHA, digest, record

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ssp_codec.config import load_config


def main():
    output = ROOT / "CHAMPION7_SHARED_RESTART.audit"
    if output.exists():
        raise RuntimeError("Already launched; never reuse this one-shot script")
    assert digest(PARENT) == PARENT_SHA
    report = {"created_utc": datetime.now(timezone.utc).isoformat(),
        "user_authorization": "share whenever GPU memory suffices; retain8GiB floor; add frequent recovery snapshots",
        "launch_free_MiB": 20480, "runtime_free_MiB": 8192,
        "disk_floor_GiB": 10, "recovery_checkpoint_interval_steps": 1000,
        "parent_sha256": PARENT_SHA, "all_prior_unsaved_updates_lost": True,
        "prior_evidence": [f"CHAMPION7_RECOVERY0{i}.audit" for i in (1, 2, 3)],
        "search_nodes_unchanged": [25000,50000,75000,100000], "cells": {}}
    locks = []
    for gpu, cell in enumerate(CELLS):
        run = ROOT / f"runs/champion7_{cell}"
        state = json.loads((run / "supervisor_state.json").read_text())
        assert state["status"] == "safety_stop"
        assert not (run / "PIPELINE_COMPLETE").exists()
        assert not list((run / "checkpoints").glob("*.pt"))
        assert (ROOT / f"runs/_smoke_champion7_{cell}/PROFILE_COMPLETE").exists()
        assert (run / "attempts/attempt03_exclusive_guard/pipeline.log").exists()
        target = f"codec_champion7_v1:{cell}"
        assert subprocess.check_output(["tmux", "display-message", "-p", "-t", target,
            "#{pane_dead}"], text=True).strip() == "1"
        for path in (run/".pipeline.lock", run/".supervisor.lock", ROOT/"runs"/f".champion4_gpu{gpu}.lock"):
            lock = path.open("a"); fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB); locks.append(lock)
        config_path = ROOT / f"configs/champion7/{cell}.yaml"
        config = load_config(str(config_path))
        assert config["training"].pop("recovery_checkpoint_interval_steps") == 1000
        original = load_config(str(run / "attempts/attempt03_exclusive_guard/effective_config.yaml"))
        assert (ROOT / config["training"]["output_dir"]).resolve() == Path(original["training"]["output_dir"]).resolve()
        config["training"]["output_dir"] = original["training"]["output_dir"]
        assert config == original, "Only I/O recovery cadence may change"
        report["cells"][cell] = {"gpu": gpu, "prior_state": state,
            "initialization": "original trained500k parent; NOT resume of lost updates",
            "effective_config_change_only": {"training.recovery_checkpoint_interval_steps": 1000},
            "config_sha256": digest(config_path)}
    output.write_text(json.dumps(report, indent=2)+"\n")
    (ROOT / "runs/champion7_setup/shared_restart_report.json").write_text(output.read_text())
    for lock in locks: lock.close()
    for gpu, cell in enumerate(CELLS):
        run = ROOT / f"runs/champion7_{cell}"
        (run / "recovery_policy.json").write_text(json.dumps(report["cells"][cell] | {
            "allow_shared": True, "recovery_checkpoint_interval_steps": 1000,
            "not_extra_score_search_nodes": True}, indent=2)+"\n")
        record(run, f"champion7_{cell}", "planned", note=(
            "User approved ample-memory sharing and1000-step atomic resume-only last.pt saves. "
            "Original parent restart, not recovery of unsaved attempts01/03; old archives preserved. "
            "Model/loss/seed/batch/100k budget/16 score nodes unchanged. Full optimizer/EMA recovery; "
            "future worker/crop replay is not bitwise. CHAMPION7_SHARED_RESTART.audit."))
        command = [str(ROOT/".venv-codec/bin/python"), "-u", "scripts/supervise_champion7.py",
            f"champion7_{cell}", str(gpu), f"configs/champion7/{cell}.yaml",
            "--allow-shared", "--steps", "100000"]
        shell = shlex.join(command)+" >> "+shlex.quote(str(run/"supervisor.log"))+" 2>&1"
        subprocess.run(["tmux", "respawn-pane", "-t", f"codec_champion7_v1:{cell}",
            "-c", str(ROOT), shell], check=True)
        print(f"Queued shared {cell} GPU{gpu}:20GiB launch/8GiB runtime/1000-step recovery", flush=True)


if __name__ == "__main__": main()
