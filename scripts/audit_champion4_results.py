#!/usr/bin/env python3
"""Verify primary and fixed-endpoint results without choosing a new checkpoint."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone
import numpy as np
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
CELLS = ("a_control", "b_training", "c_conv2former", "d_combined")


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def per_file_scores(path):
    rows = list(csv.DictReader(path.open()))
    scores = []
    for row in rows:
        scores.append(25 * (np.clip((float(row["PESQ"]) - 1) / 3.5, 0, 1)
            + np.clip(float(row["ESTOI"]), 0, 1)
            + np.clip((float(row["SI_SNR"]) + 10) / 40, 0, 1)
            + np.clip((float(row["UTMOS"]) - 1) / 4, 0, 1)))
    return [r["file"] for r in rows], np.array(scores)


def main():
    setup = json.loads((ROOT / "runs/champion4_setup/preflight_report.json").read_text())
    for relative, expected in setup["input_sha256"].items():
        assert digest(ROOT / relative) == expected
    reference = ROOT / "runs/fast_b64_2s_v1/validation_200"
    for file, expected in setup["fixed200_sha256"].items():
        assert digest(reference / file) == expected
    assert len(list(reference.glob("*.wav"))) == 200
    baseline = json.loads((ROOT / "model_registry/strong_baseline_v2.json").read_text())
    assert digest(ROOT / baseline["checkpoint"]) == baseline["checkpoint_sha256"]
    report = {"created_utc": datetime.now(timezone.utc).isoformat(), "baseline": baseline,
              "data_hashes_verified": True, "cells": {}, "effects": {}, "guardrails": {}}
    scores_by_kind = {}
    for cell in CELLS:
        run = ROOT / "runs" / f"champion4_{cell}"
        assert (run / "PIPELINE_COMPLETE").exists()
        assert (run / "evaluation_final100k/DIAGNOSTIC_COMPLETE").exists()
        config = yaml.safe_load((run / "effective_config.yaml").read_text())
        training = [json.loads(x) for x in (run / "metrics.jsonl").read_text().splitlines()]
        components = [json.loads(x) for x in (run / "training_components.jsonl").read_text().splitlines()]
        metadata = json.loads((run / "run_metadata.json").read_text())
        assert training[-1]["global_step"] == 100000 and len(training) == 20
        assert metadata["resume_checkpoint"] is None
        assert config["seed"] == config["training"]["data_order_seed"] == 20261102
        result = {"effective_config": config, "metadata": metadata,
            "training_curve": training, "phase_samples": [x for x in components if x["global_step"] in (5000, 15000, 80000, 82500, 85000, 100000)]}
        for kind, folder, checkpoint in (("primary", "evaluation", "best.pt"),
                                          ("final100k", "evaluation_final100k", "last.pt")):
            output = run / folder
            ckpt = run / "checkpoints" / checkpoint
            state = torch.load(ckpt, map_location="cpu", weights_only=False)
            summary = json.loads((output / "metrics/summary.json").read_text())
            complexity = json.loads((output / "complexity.json").read_text())
            diagnostics_path = run / "rvq_diagnostics.json" if kind == "primary" else output / "rvq_diagnostics.json"
            diagnostics = json.loads(diagnostics_path.read_text())
            assert summary["files"] == diagnostics["files"] == 200 and not summary["utmos_skipped"]
            assert complexity["bitrate_bps"] == 2400 and complexity["frame_samples"] == 160
            assert complexity["algorithmic_lookahead_ms"] == 30
            assert complexity["total_mflop_per_s"] <= 700 and complexity["decoder_mflop_per_s"] <= 300
            assert complexity["unclassified_mmac_per_s"] == 0
            assert state["global_step"] == diagnostics["checkpoint_global_step"]
            if kind == "final100k":
                assert state["global_step"] == 100000
            paths, scores = per_file_scores(output / "metrics/per_file.csv")
            assert abs(scores.mean() - summary["objective_quality_score"]) < 1e-9
            scores_by_kind[kind, cell] = (paths, scores)
            for path in (output / "bitstreams").glob("*.bin"):
                side = json.loads(path.with_suffix(".json").read_text())
                assert path.stat().st_size == 3 * ((side["num_samples"] + 159) // 160)
            assert len(list((output / "bitstreams").glob("*.bin"))) == 200
            result[kind] = {"summary": summary, "complexity": complexity,
                "rvq": diagnostics, "checkpoint_step": state["global_step"],
                "checkpoint_sha256": digest(ckpt), "checkpoint": str(ckpt.relative_to(ROOT))}
            record_name = run.name if kind == "primary" else run.name + "_final100k_diagnostic"
            args = [sys.executable, "scripts/record_experiment.py", "--name", record_name,
                "--status", "complete", "--config", str(run / "effective_config.yaml"),
                "--run-dir", str(run), "--dataset-summary", "data/manifests/vctk_libritts/summary.json",
                "--evaluation-summary", str(output / "metrics/summary.json"),
                "--complexity-summary", str(output / "complexity.json"), "--output", "EXPERIMENT_LOG.md",
                "--note", "100000 training steps completed. " + (
                    "Pre-registered reconstruction-selected checkpoint; primary control gate failed; see CHAMPION4_RESULTS.md."
                    if kind == "primary" else "Post-primary fixed100000 endpoint diagnostic; no additional training or checkpoint reselection; see CHAMPION4_FINAL_DIAGNOSTIC_PLAN.md.")]
            if kind != "primary":
                args += ["--checkpoint", str(ckpt)]
            subprocess.run(args, cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        report["cells"][cell] = result
    for kind in ("primary", "final100k"):
        values = {cell: report["cells"][cell][kind]["summary"]["objective_quality_score"] for cell in CELLS}
        a, b, c, d = [values[cell] for cell in CELLS]
        effects = {"B_minus_A": b-a, "C_minus_A": c-a, "D_minus_A": d-a,
            "D_minus_B": d-b, "D_minus_C": d-c, "training_main_effect": ((b-a)+(d-c))/2,
            "model_main_effect": ((c-a)+(d-b))/2, "interaction": d-c-b+a}
        paths, reference_scores = scores_by_kind[kind, "a_control"]
        rng = np.random.default_rng(20261103)
        sample_indices = rng.integers(0, 200, size=(5000, 200))
        effects["paired_file_bootstrap"] = {}
        for cell in CELLS[1:]:
            candidate_paths, candidate_scores = scores_by_kind[kind, cell]
            assert paths == candidate_paths
            differences = candidate_scores - reference_scores
            lo, hi = np.quantile(differences[sample_indices].mean(axis=1), [0.025, 0.975])
            effects["paired_file_bootstrap"][cell] = {"mean_difference": float(differences.mean()),
                "CI95_conditional_on_fixed_seed": [float(lo), float(hi)],
                "caveat": "File uncertainty only; not training-seed uncertainty or a promotion test."}
        report["effects"][kind] = effects
        guards = {"control_gate_pass": a >= 46.25, "cells": {}}
        for cell in CELLS[1:]:
            summary = report["cells"][cell][kind]["summary"]
            refs = {"A": report["cells"]["a_control"][kind]["summary"],
                "v2": {"objective_quality_score": baseline["selection_metrics"]["objective_quality_score"],
                       "means": baseline["selection_metrics"]}}
            cell_guard = {}
            for label, ref in refs.items():
                delta = {metric: summary["means"][metric]-ref["means"][metric] for metric in ("PESQ", "ESTOI", "SI_SNR", "UTMOS")}
                gain = summary["objective_quality_score"] - ref["objective_quality_score"]
                cell_guard[label] = {"score_gain": gain, "component_deltas": delta,
                    "passes": gain >= .15 and all(delta[key] >= -limit for key, limit in
                        (("PESQ", .02), ("ESTOI", .003), ("SI_SNR", .15), ("UTMOS", .03)))}
            guards["cells"][cell] = cell_guard
        report["guardrails"][kind] = guards
    destination = ROOT / "CHAMPION4_RESULTS.audit"
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"effects": report["effects"], "guardrails": report["guardrails"],
        "results": {cell: {kind: {"step": data[kind]["checkpoint_step"], **data[kind]["summary"]} for kind in ("primary", "final100k")}
                    for cell, data in report["cells"].items()}}, indent=2))


if __name__ == "__main__":
    main()
