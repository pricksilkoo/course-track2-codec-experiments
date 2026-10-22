#!/usr/bin/env python3
"""Create a balanced, deterministic 16-kHz confirmation set from LibriTTS test splits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly


def select(root: Path, count: int, rng: np.random.Generator) -> list[Path]:
    files = sorted(path.resolve() for path in root.rglob("*.wav") if path.is_file())
    if len(files) < count:
        raise ValueError(f"{root} contains {len(files)} WAV files, need {count}")
    indices = sorted(rng.choice(len(files), size=count, replace=False))
    return [files[index] for index in indices]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test-clean", type=Path, required=True)
    parser.add_argument("--test-other", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--per-split", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20261022)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    chosen = [("test-clean", path) for path in select(args.test_clean, args.per_split, rng)]
    chosen += [("test-other", path) for path in select(args.test_other, args.per_split, rng)]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    items = []
    for index, (split, source) in enumerate(chosen):
        audio, sample_rate = sf.read(source, dtype="float32", always_2d=True)
        mono = audio.mean(axis=1)
        if sample_rate != 16000:
            factor = np.gcd(sample_rate, 16000)
            mono = resample_poly(mono, 16000 // factor, sample_rate // factor).astype(np.float32)
        target = args.output_dir / f"item_{index:04d}.wav"
        sf.write(target, mono, 16000, subtype="PCM_16")
        items.append({"id": target.stem, "split": split, "source": str(source), "source_sr": sample_rate})

    summary = {
        "purpose": "sealed confirmation only; never use for checkpoint or hyperparameter selection",
        "seed": args.seed,
        "files": len(items),
        "per_split": args.per_split,
        "splits": ["LibriTTS/test-clean", "LibriTTS/test-other"],
        "items": items,
    }
    (args.output_dir / "selection.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"Prepared {len(items)} files in {args.output_dir}")


if __name__ == "__main__":
    main()
