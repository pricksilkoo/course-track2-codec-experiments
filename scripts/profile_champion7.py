#!/usr/bin/env python3
"""Two full-batch/full-GAN updates on disposable state, never a formal parent."""
import argparse
import json
import os
from pathlib import Path
import runpy
import sys

import torch

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    os.chdir(ROOT)
    output = (ROOT / args.output).resolve()
    if not output.is_relative_to(ROOT / "runs"):
        raise ValueError("profile output must be under runs")
    if (output / "run_metadata.json").exists():
        raise RuntimeError("profile attempt already started; preserve it, use a new explicit attempt path")
    assert torch.cuda.is_available()
    torch.set_num_threads(4)
    torch.cuda.reset_peak_memory_stats()
    sys.argv = ["scripts/train.py", "--config", args.config,
        "--train-manifest", "data/manifests/vctk_libritts/train.scp",
        "--valid-manifest", "data/manifests/vctk_libritts/valid.scp",
        "--init-checkpoint", "runs/champion6_b_s3407_fourier_gru/checkpoints/last.pt",
        "--output-dir", str(output), "--device", "cuda", "--max-total-steps", "2",
        "--max-valid-steps", "1", "--num-workers", "2", "--set", "training.warmup_steps=0"]
    runpy.run_path(str(ROOT / "scripts/train.py"), run_name="__main__")
    torch.cuda.synchronize()
    state = torch.load(output / "checkpoints/last.pt", map_location="cpu", weights_only=False)
    assert state["global_step"] == 2
    report = {"batch_size": 32, "segment_samples": 32000, "full_GAN": True,
        "config": args.config, "trained_profile_not_for_formal_initialization": True,
        "allocated_peak_MiB": torch.cuda.max_memory_allocated()/2**20,
        "reserved_peak_MiB": torch.cuda.max_memory_reserved()/2**20,
        "validation": state["validation_metrics"]}
    assert report["reserved_peak_MiB"] < 10000
    (output / "profile.json").write_text(json.dumps(report, indent=2) + "\n")
    (output / "PROFILE_COMPLETE").touch()
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
