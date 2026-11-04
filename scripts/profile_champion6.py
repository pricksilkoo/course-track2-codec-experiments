#!/usr/bin/env python3
"""Full-size full-GAN backward smoke, no quality-based checkpoint selection."""
import json
import os
from pathlib import Path
import runpy
import sys
import torch

ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
assert torch.cuda.is_available()
torch.set_num_threads(4)
reports=[]
for cell in ("a_s3407_control","b_s3407_fourier_gru"):
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    output=ROOT/f"runs/_smoke_champion6_{cell}"
    if (output/"checkpoints/last.pt").exists():
        raise RuntimeError("smoke already exists; do not duplicate")
    sys.argv=["scripts/train.py","--config",f"configs/champion6/{cell}.yaml",
        "--train-manifest","data/manifests/vctk_libritts/train.scp","--valid-manifest","data/manifests/vctk_libritts/valid.scp",
        "--init-checkpoint",f"runs/champion6_setup/step0_{cell}.pt","--output-dir",str(output),"--device","cuda",
        "--max-total-steps","2","--max-valid-steps","1","--num-workers","2",
        "--set","adversarial.start_step=0","--set","adversarial.warmup_steps=0"]
    runpy.run_path(str(ROOT/"scripts/train.py"),run_name="__main__")
    torch.cuda.synchronize()
    reports.append({"cell":cell,"full_GAN":True,"batch_size":32,"segment_samples":32000,
        "allocated_peak_MiB":torch.cuda.max_memory_allocated()/2**20,"reserved_peak_MiB":torch.cuda.max_memory_reserved()/2**20})
    print(json.dumps(reports[-1]),flush=True)
out=ROOT/"runs/champion6_setup"
(out/"backward_peak_profile.json").write_text(json.dumps(reports,indent=2)+"\n")
assert all(row["reserved_peak_MiB"]<10000 for row in reports)
(out/"PROFILE_COMPLETE").touch()
