#!/usr/bin/env python3
"""Persistent setup smoke: full-size GAN backward through both RVQ routes."""
import json
import os
from pathlib import Path
import runpy
import sys
import torch

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
assert torch.cuda.is_available()
reports = []
for probability, name in ((0, "quantized"), (1, "bypass")):
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    output = ROOT / f"runs/_smoke_champion4_{name}"
    if (output / "checkpoints/last.pt").exists():
        raise RuntimeError(f"smoke already ran: {output}; inspect instead of duplicating")
    sys.argv = ["scripts/train.py", "--config", "configs/champion4/d_combined.yaml",
        "--train-manifest", "data/manifests/vctk_libritts/train.scp",
        "--valid-manifest", "data/manifests/vctk_libritts/valid.scp",
        "--init-checkpoint", "runs/struct4_b_residual_later/checkpoints/best.pt",
        "--output-dir", str(output), "--device", "cuda", "--max-total-steps", "2",
        "--max-valid-steps", "1", "--num-workers", "2",
        "--set", "adversarial.start_step=0", "--set", "adversarial.warmup_steps=0",
        "--set", f"champion_training.quantizer_bypass_probability={probability}"]
    runpy.run_path(str(ROOT / "scripts/train.py"), run_name="__main__")
    torch.cuda.synchronize()
    reports.append({"route": name, "batch_size": 32, "segment_samples": 32000,
        "full_GAN": True, "allocated_peak_MiB": torch.cuda.max_memory_allocated() / 2**20,
        "reserved_peak_MiB": torch.cuda.max_memory_reserved() / 2**20})
    print(json.dumps(reports[-1]), flush=True)
destination = ROOT / "runs/champion4_setup"
destination.mkdir(exist_ok=True)
(destination / "backward_peak_profile.json").write_text(json.dumps(reports, indent=2) + "\n")
(destination / "PROFILE_COMPLETE").touch()
