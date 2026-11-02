#!/usr/bin/env python3
"""Audit, then optionally prune redundant checkpoints in completed local runs.

Never follows symlinks. Retains every real experiment's selected checkpoint,
all external/tracked weights, unfinished runs and averaging source snapshots.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--audit", required=True)
    args = parser.parse_args()
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    averaging = {
        "decoder_seed4_a_distill_3407": {20000, 25000, 30000},
        "decoder_seed4_b_distill_8128": {20000, 25000, 30000},
        "decoder_stability4_c_distill_swa_3407": {2500, 5000, 7500, 10000},
        "decoder_stability4_d_distill_swa_8128": {2500, 5000, 7500, 10000},
    }
    candidates, retained = [], []
    for run in sorted((ROOT / "runs").iterdir()):
        if run.is_symlink() or not run.is_dir():
            continue
        smoke = run.name.startswith("_smoke")
        complete = (run / "PIPELINE_COMPLETE").is_file()
        for path in sorted((run / "checkpoints").glob("*.pt")):
            if path.is_symlink() or not path.is_file():
                continue
            relative = str(path.relative_to(ROOT))
            step = int(path.stem[5:]) if path.stem.startswith("step_") and path.stem[5:].isdigit() else None
            reason = ""
            if relative in tracked:
                reason = "tracked regression checkpoint"
            elif not smoke and path.name in {"best.pt", "raw_best.pt"}:
                reason = "selected historical comparator / lineage / teacher"
            elif not smoke and not complete:
                reason = "no completion marker: preserve resumability"
            elif step is not None and step in averaging.get(run.name, set()):
                reason = "source for registered SWA or decoder averaging"
            elif not smoke and path.name != "last.pt" and step is None:
                reason = "unrecognized checkpoint: preserve"
            item = {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}
            if reason:
                item["reason"] = reason
                retained.append(item)
            else:
                candidates.append(item)
    # Process check closes the gap between filesystem completion and a still
    # running manual training/resume command. Refuse all deletion if uncertain.
    processes = subprocess.check_output(["ps", "-eo", "args"], text=True).splitlines()
    for item in candidates:
        run_path = str(Path(item["path"]).parent.parent)
        if any(run_path in line and ("train.py" in line or "run_" in line) for line in processes):
            raise RuntimeError(f"candidate has an active process: {run_path}")
    audit = {"created_utc": datetime.now(timezone.utc).isoformat(),
             "mode": "apply" if args.apply else "dry-run", "deleted": False,
             "reclaim_bytes": sum(item["bytes"] for item in candidates),
             "candidates": candidates, "retained": retained,
             "note": "step0.pt, third-party weights, symlinks, metrics/audio/configs are outside deletion scope"}
    audit_path = ROOT / args.audit
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    if audit_path.exists():
        raise FileExistsError("choose a new audit path; do not overwrite a prior deletion record")
    audit_path.write_text(json.dumps(audit, indent=2) + "\n")
    if args.apply:
        for item in candidates:
            target = ROOT / item["path"]
            assert target.parent.parent.parent == ROOT / "runs"
            if target.is_symlink() or target.stat().st_size != item["bytes"] or sha256(target) != item["sha256"]:
                raise RuntimeError(f"checkpoint changed after inventory: {target}")
            target.unlink()
        for item in retained:
            if sha256(ROOT / item["path"]) != item["sha256"]:
                raise RuntimeError(f"retained checkpoint changed: {item['path']}")
        audit["deleted"] = True
        audit_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(json.dumps({"candidates": len(candidates), "retained": len(retained),
                      "reclaim_GiB": audit["reclaim_bytes"] / 2**30,
                      "audit": str(audit_path), "applied": audit["deleted"]}, indent=2))


if __name__ == "__main__":
    main()
