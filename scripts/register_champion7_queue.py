#!/usr/bin/env python3
"""Register four planned learned-parent cells before their supervisors launch."""
import json
from pathlib import Path

from run_champion7_experiment import CELLS, PARENT_SHA, record

ROOT = Path(__file__).resolve().parents[1]


def main():
    report = json.loads((ROOT / "CHAMPION7_SETUP.audit").read_text())
    assert report["parent_sha256"] == PARENT_SHA
    for cell in CELLS:
        run = ROOT / f"runs/champion7_{cell}"
        if (run / "run_metadata.json").exists() or (run / "PIPELINE_COMPLETE").exists():
            raise RuntimeError("Do not downgrade or duplicate an initialized/completed cell")
    for cell in CELLS:
        run = ROOT / f"runs/champion7_{cell}"
        record(run, f"champion7_{cell}", "planned", note=(
            "Queued for GPU capacity, not yet formal training. Explicit learned-parent fine-tuning, NOT scratch: "
            f"CHAMPION6 B score51.624336, parent500000-step SHA256 {PARENT_SHA}; inherit codec/RVQ EMA/discriminator, "
            "reset optimizers,100000 extra steps, seed/data-order20261106. Four declared25k/50k/75k/100k "
            "fixed200 development score-search nodes; best score not reconstruction-best. "
            "Lineage/config/data hash evidence CHAMPION7_SETUP.audit and run/lineage.json. "
            "One requested shared capacity probe was stopped at8GiB free floor; no OOM. "
            "Formal full-batch GPU backward profile remains pending safe capacity."))


if __name__ == "__main__":
    main()
