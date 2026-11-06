#!/usr/bin/env python3
"""Capture completed GPU preflights and the initial formal launch, once."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELLS = ("a_continue", "b_si", "c_gan", "d_both")


def main():
    output = ROOT / "CHAMPION7_PROFILE.audit"
    if output.exists():
        raise RuntimeError("Preserve the first launch snapshot; do not overwrite")
    setup = json.loads((ROOT / "CHAMPION7_SETUP.audit").read_text())
    report = {"captured_utc": datetime.now(timezone.utc).isoformat(),
        "parent_sha256": setup["parent_sha256"], "formal_stage": "warm-start from trained500k, not scratch or smoke", "cells": {}}
    for cell in CELLS:
        run = ROOT / f"runs/champion7_{cell}"
        profile = ROOT / f"runs/_smoke_champion7_{cell}/profile.json"
        assert profile.with_name("PROFILE_COMPLETE").exists()
        data = json.loads(profile.read_text())
        assert data["batch_size"] == 32 and data["segment_samples"] == 32000 and data["full_GAN"]
        assert data["validation"]["adversarial_factor"] == 1
        metadata = json.loads((run / "run_metadata.json").read_text())
        assert Path(metadata["init_checkpoint"]) == ROOT / setup["parent"] and metadata["resume_checkpoint"] is None
        report["cells"][cell] = {"profile": data, "profile_sha256": hashlib.sha256(profile.read_bytes()).hexdigest(),
            "formal_initial_metadata": metadata, "initial_supervisor_snapshot": json.loads((run / "supervisor_state.json").read_text())}
    output.write_text(json.dumps(report, indent=2)+"\n")
    print("Captured four full-batch full-GAN profiles and learned-parent formal launches")


if __name__ == "__main__":
    main()
