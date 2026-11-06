#!/usr/bin/env python3
"""CPU lineage/config preflight for an explicitly warm-started score search."""
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
from ssp_codec.adversarial import MultiResolutionSTFTDiscriminator

CELLS = ("a_continue", "b_si", "c_gan", "d_both")
PARENT = ROOT / "runs/champion6_b_s3407_fourier_gru/checkpoints/last.pt"
PARENT_SHA = "c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23"


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    torch.set_num_threads(2)
    assert digest(PARENT) == PARENT_SHA
    state = torch.load(PARENT, map_location="cpu", weights_only=False)
    assert state["global_step"] == 500000 and state["discriminator"]
    prior = json.loads((ROOT / "CHAMPION6_RESULTS.audit").read_text())
    ref = ROOT / "runs/fast_b64_2s_v1/validation_200"
    hashes = {p.name: digest(p) for p in sorted(ref.glob("*.wav"))}
    assert hashes == prior["fixed200_sha256"]
    assert all(digest(ROOT / p) == h for p, h in prior["data_hashes"].items())
    report = {"study": "CHAMPION7 exploratory warm-start fine-tuning, NOT from scratch",
        "parent": str(PARENT.relative_to(ROOT)), "parent_sha256": PARENT_SHA,
        "parent_trained_global_step": 500000, "parent_score": 51.62433613863932,
        "new_stage_steps": 100000, "optimizer_state_inherited": False,
        "codec_discriminator_and_RVQ_EMA_inherited": True,
        "selection": "best actual fixed200 objective score among four declared extra-step endpoints per cell;16 searched checkpoints total, plus unchanged parent fallback; exploratory not confirmation",
        "endpoints": [25000, 50000, 75000, 100000], "data_counts": prior["data_counts"],
        "data_hashes": prior["data_hashes"], "fixed200_sha256": hashes,
        "cells": {}, "capacity_probe": json.loads((ROOT / "runs/champion7_setup/shared_capacity_probe.json").read_text())}
    for index, cell in enumerate(CELLS):
        config_path = ROOT / f"configs/champion7/{cell}.yaml"
        config = load_config(config_path)
        assert config["model"] == state["model_config"]
        assert config["seed"] == config["training"]["data_order_seed"] == 20261106
        assert config["training"]["batch_size"] == 32 and config["audio"]["segment_samples"] == 32000
        assert config["training"]["checkpoint_keep_last"] == 4
        assert config["training"]["validation_checkpoint_interval_steps"] == 25000
        assert config["training"]["learning_rate"] == config["training"]["quantizer_learning_rate"] == .00005
        assert config["adversarial"]["learning_rate"] == .00005
        assert config["adversarial"]["start_step"] == config["adversarial"]["warmup_steps"] == 0
        assert config["loss"]["si_snr_weight"] == (.01 if index in (1, 3) else .003)
        assert config["loss"]["adversarial_weight"] == (.1 if index in (2, 3) else .05)
        assert config["loss"]["feature_matching_weight"] == 1.5
        run = ROOT / f"runs/champion7_{cell}"
        if (run / "run_metadata.json").exists():
            raise RuntimeError("Formal cell already initialized; do not regenerate preflight")
        run.mkdir(exist_ok=True)
        config["training"]["output_dir"] = str(run)
        model = CourseCodec(**config["model"])
        model.load_state_dict(state["model"], strict=True)
        assert all(torch.equal(v, model.state_dict()[k]) for k, v in state["model"].items())
        disc = MultiResolutionSTFTDiscriminator(config["adversarial"]["resolutions"], config["adversarial"]["periods"])
        disc.load_state_dict(state["discriminator"], strict=True)
        assert all(torch.equal(v, disc.state_dict()[k]) for k, v in state["discriminator"].items())
        subprocess.run([sys.executable, "scripts/complexity.py", "--config", str(config_path),
            "--output", str(run / "preflight_complexity.json")], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        complexity = json.loads((run / "preflight_complexity.json").read_text())
        assert abs(complexity["total_mflop_per_s"] - 666.3072) < 1e-8
        assert abs(complexity["decoder_mflop_per_s"] - 257.632) < 1e-8
        assert complexity["total_mflop_per_s"] <= 700 and complexity["decoder_mflop_per_s"] <= 300
        assert complexity["algorithmic_lookahead_ms"] == 30 and complexity["bitrate_bps"] == 2400
        assert complexity["unclassified_mmac_per_s"] == 0
        (run / "effective_config.yaml").write_text(yaml.safe_dump(config, sort_keys=False))
        lineage = {"parent_checkpoint": str(PARENT), "parent_sha256": PARENT_SHA,
            "parent_global_step": 500000, "stage_local_start_step": 0,
            "trained_parent_not_untrained_initialization": True, "optimizer_reset": True,
            "all_codec_and_discriminator_tensors_verified_identical_to_parent": True}
        (run / "lineage.json").write_text(json.dumps(lineage, indent=2)+"\n")
        report["cells"][cell] = {"effective_config": config, "config_sha256": digest(config_path),
            "lineage": lineage, "complexity": complexity}
        print(f"preflight {cell} inherited trained500k parent, all tensors/EMA identical", flush=True)
    setup = ROOT / "runs/champion7_setup"
    report["CPU_regression_tests"] = (setup / "pytest.log").read_text().strip()
    report["orchestration_tests"] = (setup / "tools_pytest.log").read_text().strip()
    assert "35 passed" in report["CPU_regression_tests"] and "7 passed" in report["orchestration_tests"]
    report["GPU_preflight_status"] = "pending capacity; each protected pipeline must complete its full-batch two-step profile before formal optimization; shared probe was safety-stopped, not a pass"
    content = json.dumps(report, indent=2, ensure_ascii=False)+"\n"
    (setup / "preflight_report.json").write_text(content)
    (ROOT / "CHAMPION7_SETUP.audit").write_text(content)


if __name__ == "__main__":
    main()
