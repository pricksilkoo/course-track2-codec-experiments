#!/usr/bin/env python3
"""Create matched never-trained snapshots and validate all four architectures."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ssp_codec.model import CourseCodec
from ssp_codec.config import load_config
from ssp_codec.adversarial import MultiResolutionSTFTDiscriminator

CELLS = ("a_control", "b_encoder_gru", "c_fourier", "d_fourier_gru")


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    torch.set_num_threads(2)
    source = ROOT / "runs/lookahead4_scratch_init/step0.pt"
    assert sha256(source) == "3488d8448d523d5db57aa4afe99c65f6bd9089092db661ab8ed4dcc97fd9196e"
    origin = torch.load(source, map_location="cpu", weights_only=False)
    assert origin["trained"] is False and origin["global_step"] == 0
    report = {"source_step0_sha256": sha256(source), "trained": False, "cells": {}}
    models = {}
    out = ROOT / "runs/champion5_setup"
    out.mkdir(exist_ok=True)
    if any((ROOT / "runs" / f"champion5_{cell}" / "run_metadata.json").exists() for cell in CELLS):
        raise RuntimeError("formal training already started; do not regenerate preflight records")
    for cell in CELLS:
        config_file = ROOT / "configs/champion5" / f"{cell}.yaml"
        config = load_config(config_file)
        torch.manual_seed(config["seed"])
        model = CourseCodec(**config["model"]).eval()
        compatible = {key: value for key, value in origin["model"].items()
                      if key in model.state_dict() and model.state_dict()[key].shape == value.shape
                      and not (config["model"]["synthesis_type"] == "fourier" and key.startswith("decoder."))}
        missing = model.load_state_dict(compatible, strict=False).missing_keys
        discriminator = MultiResolutionSTFTDiscriminator(config["adversarial"]["resolutions"], config["adversarial"].get("periods", ()))
        discriminator.load_state_dict(origin["discriminator"], strict=True)
        snapshot = out / f"step0_{cell}.pt"
        state = {"global_step": 0, "trained": False, "seed": config["seed"],
            "model_config": config["model"], "model": model.state_dict(),
            "discriminator": discriminator.state_dict(), "source_untrained_initialization": str(source)}
        if snapshot.exists():
            previous = torch.load(snapshot, map_location="cpu", weights_only=False)
            assert previous["trained"] is False and previous["global_step"] == 0
            assert previous["model_config"] == state["model_config"]
            assert all(torch.equal(value, previous["model"][key]) for key, value in state["model"].items())
        else:
            torch.save(state, snapshot)
        run = ROOT / "runs" / f"champion5_{cell}"
        run.mkdir(exist_ok=True)
        (run / "effective_config.yaml").write_text(yaml.safe_dump(config, sort_keys=False))
        complexity_path = run / "preflight_complexity.json"
        subprocess.run([sys.executable, "scripts/complexity.py", "--config", str(config_file), "--output", str(complexity_path)],
                       cwd=ROOT, env={**os.environ, "OMP_NUM_THREADS": "2"}, check=True, stdout=subprocess.DEVNULL)
        complexity = json.loads(complexity_path.read_text())
        assert complexity["bitrate_bps"] == 2400 and complexity["frame_samples"] == 160
        assert complexity["algorithmic_lookahead_ms"] == 30 and complexity["total_mflop_per_s"] <= 700
        assert complexity["decoder_mflop_per_s"] <= 300 and complexity["unclassified_mmac_per_s"] == 0
        report["cells"][cell] = {"snapshot_sha256": sha256(snapshot), "loaded_tensors": len(compatible),
            "new_tensors": missing, "complexity": complexity, "effective_config": config}
        subprocess.run([sys.executable, "scripts/record_experiment.py", "--name", run.name,
            "--status", "planned", "--config", str(run / "effective_config.yaml"),
            "--run-dir", str(run), "--dataset-summary", "data/manifests/vctk_libritts/summary.json",
            "--complexity-summary", str(complexity_path), "--output", "EXPERIMENT_LOG.md",
            "--note", "Matched never-trained initialization SHA256=" + sha256(snapshot)
                + ";500000-step scratch course, fixed final endpoint primary; no learned checkpoint inherited"],
            cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        models[cell] = model
    for cell, model in models.items():
        for key, value in models["a_control"].state_dict().items():
            if key.startswith(("encoder.", "analysis_temporal.", "quantizer.")):
                assert torch.equal(value, model.state_dict()[key]), (cell, key)
    for key, value in models["c_fourier"].decoder.state_dict().items():
        assert torch.equal(value, models["d_fourier_gru"].decoder.state_dict()[key])
    for key, value in models["b_encoder_gru"].analysis_gru.state_dict().items():
        assert torch.equal(value, models["d_fourier_gru"].analysis_gru.state_dict()[key])
    x = torch.randn(1, 1, 3200)
    with torch.inference_mode():
        results = {cell: model(x) for cell, model in models.items()}
    for cell in CELLS:
        assert torch.equal(results[cell][1], results["a_control"][1])
    torch.testing.assert_close(results["a_control"][0], results["b_encoder_gru"][0], rtol=0, atol=0)
    torch.testing.assert_close(results["c_fourier"][0], results["d_fourier_gru"][0], rtol=0, atol=0)
    report["shared_encoder_rvq_discriminator_verified"] = True
    report["within_synthesis_family_initial_outputs_equal"] = True
    (out / "preflight_report.json").write_text(json.dumps(report, indent=2) + "\n")
    (out / "PREFLIGHT_COMPLETE").touch()
    print(json.dumps({cell: data["complexity"] for cell, data in report["cells"].items()}, indent=2))


if __name__ == "__main__":
    main()
