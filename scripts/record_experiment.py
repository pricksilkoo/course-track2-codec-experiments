#!/usr/bin/env python3
"""Create or update one reproducible entry in the project experiment log."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def last_jsonl(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return json.loads(lines[-1]) if lines else None


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def fmt(value: Any, digits: int = 6) -> str:
    return f"{value:.{digits}f}" if isinstance(value, float) else str(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument("--status", required=True, choices=("planned", "running", "failed", "complete"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--dataset-summary", type=Path)
    parser.add_argument("--evaluation-summary", type=Path)
    parser.add_argument("--complexity-summary", type=Path)
    parser.add_argument("--note", default="")
    parser.add_argument("--output", type=Path, default=ROOT / "EXPERIMENT_LOG.md")
    args = parser.parse_args()

    dataset = load_json(args.dataset_summary)
    evaluation = load_json(args.evaluation_summary)
    complexity = load_json(args.complexity_summary)
    training = last_jsonl(args.run_dir / "metrics.jsonl")
    checkpoint = args.run_dir / "checkpoints" / "best.pt"
    config_text = args.config.read_text(encoding="utf-8") if args.config.is_file() else "<missing>\n"

    lines = [
        f"<!-- experiment:{args.name}:start -->",
        f"## {args.name}",
        "",
        f"- Status: `{args.status}`",
        f"- Updated (UTC): `{datetime.now(timezone.utc).isoformat()}`",
        f"- Git commit: `{git_commit()}`",
        f"- Run directory: `{args.run_dir}`",
    ]
    if args.note:
        lines.append(f"- Note: {args.note}")
    checkpoint_hash = sha256(checkpoint)
    if checkpoint_hash:
        lines.extend(
            [f"- Best checkpoint: `{checkpoint}`", f"- Checkpoint SHA-256: `{checkpoint_hash}`"]
        )

    if dataset:
        lines.extend(
            [
                "",
                "### Dataset",
                "",
                "| Item | Value |",
                "|---|---:|",
                f"| Training files | {dataset.get('total_train_files', 'n/a')} |",
                f"| Validation files | {dataset.get('total_valid_files', 'n/a')} |",
                f"| VCTK training files | {dataset.get('vctk_train_files', 'n/a')} |",
                f"| VCTK validation files | {dataset.get('vctk_valid_files', 'n/a')} |",
                f"| LibriTTS training files | {dataset.get('libritts_train_files', 'n/a')} |",
                f"| LibriTTS validation files | {dataset.get('libritts_valid_files', 'n/a')} |",
            ]
        )

    if training:
        validation = training.get("validation", {})
        lines.extend(
            [
                "",
                "### Last training validation",
                "",
                "| Item | Value |",
                "|---|---:|",
                f"| Epoch | {training.get('epoch', 'n/a')} |",
                f"| Global step | {training.get('global_step', 'n/a')} |",
                f"| Train loss | {fmt(training.get('train_loss', 'n/a'))} |",
                f"| Reconstruction loss | {fmt(validation.get('reconstruction', 'n/a'))} |",
                f"| Waveform L1 | {fmt(validation.get('waveform_l1', 'n/a'))} |",
                f"| Spectral loss | {fmt(validation.get('spectral', 'n/a'))} |",
                f"| Commitment loss | {fmt(validation.get('commitment', 'n/a'))} |",
            ]
        )

    if evaluation:
        means = evaluation.get("means", {})
        lines.extend(
            [
                "",
                "### Objective evaluation",
                "",
                "| Item | Value |",
                "|---|---:|",
                f"| Files | {evaluation.get('files', 'n/a')} |",
                f"| PESQ-WB | {fmt(means.get('PESQ', 'n/a'), 4)} |",
                f"| ESTOI | {fmt(means.get('ESTOI', 'n/a'), 4)} |",
                f"| SI-SNR (dB) | {fmt(means.get('SI_SNR', 'n/a'), 4)} |",
                f"| UTMOS | {fmt(means.get('UTMOS', 'n/a'), 4)} |",
                f"| Course objective score | {fmt(evaluation.get('objective_quality_score', 'n/a'), 4)} |",
            ]
        )

    if complexity:
        lines.extend(
            [
                "",
                "### Submission constraints",
                "",
                "| Item | Value |",
                "|---|---:|",
                f"| Bitrate (bps) | {complexity.get('bitrate_bps', 'n/a')} |",
                f"| Algorithmic lookahead (ms) | {fmt(complexity.get('algorithmic_lookahead_ms', 'n/a'), 3)} |",
                f"| Total MFLOP/s | {fmt(complexity.get('total_mflop_per_s', 'n/a'), 3)} |",
                f"| Decoder MFLOP/s | {fmt(complexity.get('decoder_mflop_per_s', 'n/a'), 3)} |",
                f"| Parameters | {complexity.get('parameters', 'n/a')} |",
            ]
        )

    lines.extend(["", "### Effective configuration", "", "```yaml", config_text.rstrip(), "```", ""])
    lines.append(f"<!-- experiment:{args.name}:end -->")
    section = "\n".join(lines) + "\n"

    header = "# Experiment Log\n\nThis file is updated by `scripts/record_experiment.py`.\n\n"
    existing = args.output.read_text(encoding="utf-8") if args.output.is_file() else header
    start = f"<!-- experiment:{args.name}:start -->"
    end = f"<!-- experiment:{args.name}:end -->"
    if start in existing and end in existing:
        prefix, remainder = existing.split(start, 1)
        _, suffix = remainder.split(end, 1)
        updated = prefix.rstrip() + "\n\n" + section + suffix.lstrip("\n")
    else:
        updated = existing.rstrip() + "\n\n" + section
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(updated, encoding="utf-8")
    temporary.replace(args.output)
    print(f"updated {args.output} for {args.name}: {args.status}")


if __name__ == "__main__":
    main()
