#!/usr/bin/env python3
"""Freeze registered inputs, preflight all cells and verify initial equality."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ssp_codec.config import load_config
from ssp_codec.model import CourseCodec
from ssp_codec.io import load_codec

CELLS = (("a_control", "a_control.yaml"), ("b_training", "b_training.yaml"),
         ("c_conv2former", "c_conv2former.yaml"), ("d_combined", "d_combined.yaml"))


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def main():
    torch.set_num_threads(2)
    parent = ROOT / "runs/struct4_b_residual_later/checkpoints/best.pt"
    assert digest(parent) == "f9c71919519dbda7d02bdfc56d6eb309cf9a45976d733e29b3fd808b7b77cc1a"
    reference, state = load_codec(parent, torch.device("cpu"))
    torch.manual_seed(20261102)
    waveform = torch.randn(1, 1, 3200)
    with torch.inference_mode():
        expected, expected_indices, _ = reference(waveform)
    setup = ROOT / "runs/champion4_setup"
    setup.mkdir(exist_ok=True)
    profile = json.loads((setup / "backward_peak_profile.json").read_text())
    assert len(profile) == 2 and all(item["reserved_peak_MiB"] < 10000 for item in profile)
    report = {"parent_sha256": digest(parent), "cells": {}, "profile": profile,
              "input_sha256": {str(path.relative_to(ROOT)): digest(path) for path in (
                  ROOT / "data/manifests/vctk_libritts/train.scp",
                  ROOT / "data/manifests/vctk_libritts/valid.scp")}}
    for name, file in CELLS:
        config_path = ROOT / "configs/champion4" / file
        config = load_config(config_path)
        candidate = CourseCodec(**config["model"]).eval()
        missing, unexpected = candidate.load_state_dict(state["model"], strict=False)
        assert not unexpected
        assert all(key.startswith("synthesis_conv2former.") for key in missing)
        with torch.inference_mode():
            actual, indices, _ = candidate(waveform)
        torch.testing.assert_close(actual, expected, rtol=0, atol=0)
        assert torch.equal(indices, expected_indices)
        run = ROOT / "runs" / f"champion4_{name}"
        run.mkdir(exist_ok=True)
        (run / "effective_config.yaml").write_text(yaml.safe_dump(config, sort_keys=False))
        subprocess.run([sys.executable, "scripts/complexity.py", "--config", str(config_path),
            "--output", str(run / "preflight_complexity.json")], cwd=ROOT, check=True,
            env={**__import__("os").environ, "OMP_NUM_THREADS": "2"}, stdout=subprocess.DEVNULL)
        complexity = json.loads((run / "preflight_complexity.json").read_text())
        assert complexity["bitrate_bps"] == 2400 and complexity["algorithmic_lookahead_ms"] == 30
        assert complexity["total_mflop_per_s"] <= 700 and complexity["decoder_mflop_per_s"] <= 300
        assert complexity["unclassified_mmac_per_s"] == 0
        report["cells"][name] = {"initial_output_equal": True, "initial_indices_equal": True,
             "loaded_codec_tensors": len(state["model"]), "new_tensors": len(missing),
             "complexity": complexity, "config": config}
        subprocess.run([sys.executable, "scripts/record_experiment.py", "--name", f"champion4_{name}",
            "--status", "planned", "--config", str(run / "effective_config.yaml"),
            "--run-dir", str(run), "--dataset-summary", "data/manifests/vctk_libritts/summary.json",
            "--complexity-summary", str(run / "preflight_complexity.json"),
            "--output", "EXPERIMENT_LOG.md", "--note",
            "Champion-inspired matched100k continuation; user authorized GPU sharing; no quality result yet"],
            cwd=ROOT, check=True)
    report["fixed200_sha256"] = {
        path.name: digest(path) for path in sorted((ROOT / "runs/fast_b64_2s_v1/validation_200").glob("*.wav"))}
    assert len(report["fixed200_sha256"]) == 200
    (setup / "preflight_report.json").write_text(json.dumps(report, indent=2) + "\n")
    (setup / "PREFLIGHT_COMPLETE").touch()
    print(json.dumps({name: data["complexity"]["total_mflop_per_s"] for name, data in report["cells"].items()}))


if __name__ == "__main__":
    main()
