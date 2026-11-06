#!/usr/bin/env python3
"""Audit CHAMPION6's registered endpoints without training or checkpoint search."""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
CELLS = ("a_s3407_control", "b_s3407_fourier_gru", "c_s8128_control", "d_s8128_fourier_gru")
METRICS = ("PESQ", "ESTOI", "SI_SNR", "UTMOS")
LIMITS = dict(zip(METRICS, (.02, .003, .15, .03)))


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def normalized(config):
    result = copy.deepcopy(config)
    result.pop("seed")
    result["training"].pop("output_dir")
    result["training"].pop("data_order_seed")
    result["model"].pop("synthesis_initialization_seed")
    return result


def comparison(candidate, reference):
    delta = {key: candidate["means"][key] - reference["means"][key] for key in METRICS}
    gain = candidate["objective_quality_score"] - reference["objective_quality_score"]
    return {"score_gain": gain, "component_deltas": delta,
            "score_gate_pass": gain >= .15,
            "component_guard_pass": {key: delta[key] >= -LIMITS[key] for key in METRICS},
            "passes": gain >= .15 and all(delta[key] >= -LIMITS[key] for key in METRICS)}


def mean_range(values):
    return {"mean": float(np.mean(values)), "min": min(values), "max": max(values), "n": len(values)}


def main():
    torch.set_num_threads(2)
    setup = read_json(ROOT / "runs/champion6_setup/preflight_report.json")
    assert setup["trained"] is False and setup["global_step"] == 0
    baseline = read_json(ROOT / "model_registry/strong_baseline_v2.json")
    assert digest(ROOT / baseline["checkpoint"]) == baseline["checkpoint_sha256"]
    reference = ROOT / "runs/fast_b64_2s_v1/validation_200"
    fixed_hashes = {p.name: digest(p) for p in sorted(reference.glob("*.wav"))}
    assert fixed_hashes == setup["fixed200_sha256"] and len(fixed_hashes) == 200
    assert fixed_hashes == read_json(ROOT / "CHAMPION5_RESULTS.audit")["fixed200_sha256"]
    assert all(digest(ROOT / path) == sha for path, sha in setup["data_hashes"].items())
    counts = {kind: sum(bool(line.strip()) for line in (ROOT / f"data/manifests/vctk_libritts/{kind}.scp").read_text().splitlines()) for kind in ("train", "valid")}
    assert counts == {"train": 394988, "valid": 14596}
    report = {"created_utc": datetime.now(timezone.utc).isoformat(),
              "git_commit_at_audit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "design": "Two new-seed matched control/candidate pairs, not a 2x2 factorial; CHAMPION5 excluded from confirmation statistics.",
              "selection": "Prospectively fixed 500000-step last.pt, primary. No checkpoint search or extension.",
              "baseline": baseline, "baseline_registry_sha256": digest(ROOT / "model_registry/strong_baseline_v2.json"),
              "data_counts": counts, "data_hashes": setup["data_hashes"], "fixed200_sha256": fixed_hashes,
              "initialization": setup["initialization"], "pair_sources": {}, "cells": {}, "comparisons": {}, "guardrails": {}}
    pytest_log = ROOT / "runs/champion6_setup/final_pytest.log"
    assert "35 passed" in pytest_log.read_text()
    report["final_regression_tests"] = {"command": "CUDA_VISIBLE_DEVICES='' .venv-codec/bin/python -m pytest -q tests/test_codec.py tests/test_champion4.py tests/test_champion5.py", "result": pytest_log.read_text().strip(), "log_sha256": digest(pytest_log)}
    origins = {}
    for seed, pair in setup["pairs"].items():
        source = ROOT / pair["source"]
        assert digest(source) == pair["source_sha256"]
        origin = torch.load(source, map_location="cpu", weights_only=False)
        assert origin["trained"] is False and origin["global_step"] == 0 and origin["seed"] == int(seed)
        assert origin["discriminator"]
        origins[int(seed)] = origin
        report["pair_sources"][seed] = {**pair, "trained": False, "global_step": 0}
    scores, metric_paths = {}, None
    experiment_log = (ROOT / "EXPERIMENT_LOG.md").read_text()
    for index, cell in enumerate(CELLS):
        run = ROOT / "runs" / f"champion6_{cell}"
        output = run / "evaluation"
        expected = setup["cells"][cell]
        seed, candidate = expected["seed"], expected["candidate"]
        assert seed == (3407 if index < 2 else 8128) and candidate == (index % 2 == 1)
        for marker in (run / "TRAINING_COMPLETE", run / "PIPELINE_COMPLETE", output / "ROUNDTRIP_COMPLETE"):
            assert marker.exists(), marker
        supervisor = read_json(run / "supervisor_state.json")
        assert supervisor["status"] == "complete"
        supervisor_events = [json.loads(line) for line in (run / "supervisor.log").read_text().splitlines() if line.startswith('{"status"')]
        assert [event["status"] for event in supervisor_events] == ["running", "complete"]
        raw = (run / "pipeline.log").read_text().lower()
        failure_counts = {token: raw.count(token) for token in ("traceback (most recent call last)", "out of memory", "resuming training", "non-finite loss")}
        assert not any(failure_counts.values())
        del raw
        config = yaml.safe_load((run / "effective_config.yaml").read_text())
        preflight_config = copy.deepcopy(expected["effective_config"])
        assert (ROOT / preflight_config["training"]["output_dir"]).resolve() == run
        preflight_config["training"]["output_dir"] = str(run)
        assert config == preflight_config  # train.py resolves only the output directory.
        previous = ROOT / "runs" / ("champion5_d_fourier_gru" if candidate else "champion5_a_control") / "effective_config.yaml"
        assert normalized(config) == normalized(yaml.safe_load(previous.read_text()))
        init = ROOT / "runs/champion6_setup" / f"step0_{cell}.pt"
        assert digest(init) == expected["snapshot_sha256"]
        initial = torch.load(init, map_location="cpu", weights_only=False)
        assert initial["trained"] is False and initial["global_step"] == 0 and initial["seed"] == seed
        origin = origins[seed]
        assert Path(initial["source_untrained_initialization"]) == ROOT / setup["pairs"][str(seed)]["source"]
        shared = expected["shared_or_source_tensors"]
        assert set(shared) == {key for key in origin["model"] if not candidate or not key.startswith(("decoder.", "analysis_gru."))}
        assert all(torch.equal(initial["model"][key], origin["model"][key]) for key in shared)
        assert initial["discriminator"].keys() == origin["discriminator"].keys()
        assert all(torch.equal(value, initial["discriminator"][key]) for key, value in origin["discriminator"].items())
        metadata = read_json(run / "run_metadata.json")
        assert Path(metadata["init_checkpoint"]) == init and metadata["resume_checkpoint"] is None
        assert config["seed"] == config["training"]["data_order_seed"] == seed
        assert config["model"]["synthesis_initialization_seed"] == seed + 200000
        assert config["training"]["reset_rng_after_init"] and config["training"]["fail_on_nonfinite"]
        training = [json.loads(line) for line in (run / "metrics.jsonl").read_text().splitlines()]
        assert [row["global_step"] for row in training] == list(range(25000, 500001, 25000))
        for row in training:
            assert np.isfinite(row["train_loss"]) and all(np.isfinite(value) for value in row["validation"].values())
            factor = max(0., min(1., (row["global_step"] - 99999) / 50000))
            assert abs(row["validation"]["adversarial_factor"] - factor) < 1e-6
        checkpoint = run / "checkpoints/last.pt"
        sha = digest(checkpoint)
        assert (output / "checkpoint.sha256").read_text().split()[0] == sha
        state = torch.load(checkpoint, map_location="cpu", weights_only=False)
        best = torch.load(run / "checkpoints/best.pt", map_location="cpu", weights_only=False)
        assert state["global_step"] == 500000 and state["model_config"] == initial["model_config"] == config["model"]
        assert state["validation_metrics"] == training[-1]["validation"]
        summary = read_json(output / "metrics/summary.json")
        complexity = read_json(output / "complexity.json")
        rvq = read_json(run / "rvq_diagnostics.json")
        assert summary["files"] == rvq["files"] == 200 and not summary["utmos_skipped"]
        assert rvq["checkpoint_global_step"] == 500000 and Path(rvq["checkpoint"]) == checkpoint
        assert abs(rvq["partial_reconstruction"][-1]["si_snr_db_mean_per_file"] - summary["means"]["SI_SNR"]) < 1e-4
        assert complexity == expected["complexity"]
        assert complexity["sample_rate_hz"] == 16000 and complexity["frame_samples"] == 160
        assert complexity["bitrate_bps"] == 2400 and complexity["algorithmic_lookahead_ms"] == 30
        assert complexity["total_mflop_per_s"] <= 700 and complexity["decoder_mflop_per_s"] <= 300 and complexity["unclassified_mmac_per_s"] == 0
        rows = list(csv.DictReader((output / "metrics/per_file.csv").open()))
        paths = [row["file"] for row in rows]
        assert len(rows) == 200 and (metric_paths is None or metric_paths == paths)
        metric_paths = paths
        assert {Path(path).name for path in paths} == set(fixed_hashes)
        values = np.array([[float(row[key]) for key in METRICS] for row in rows])
        assert np.isfinite(values).all()
        score = 25 * (np.clip((values[:, 0]-1)/3.5, 0, 1) + np.clip(values[:, 1], 0, 1) + np.clip((values[:, 2]+10)/40, 0, 1) + np.clip((values[:, 3]-1)/4, 0, 1))
        assert abs(score.mean() - summary["objective_quality_score"]) < 1e-9
        assert all(abs(values[:, i].mean() - summary["means"][key]) < 1e-9 for i, key in enumerate(METRICS))
        scores[cell] = score
        bitstreams = list((output / "bitstreams").glob("*.bin"))
        assert len(bitstreams) == len(list((output / "reconstructed").glob("*.wav"))) == 200
        assert {p.with_suffix(".wav").name for p in bitstreams} == set(fixed_hashes)
        total_bytes = total_samples = 0
        for bitstream in bitstreams:
            side = read_json(bitstream.with_suffix(".json"))
            original = sf.info(reference / bitstream.with_suffix(".wav").name)
            decoded = sf.info(output / "reconstructed" / bitstream.with_suffix(".wav").name)
            assert original.samplerate == decoded.samplerate == 16000 and original.channels == decoded.channels == 1
            assert original.frames == decoded.frames == side["num_samples"]
            assert bitstream.stat().st_size == 3 * ((original.frames + 159) // 160)
            total_bytes += bitstream.stat().st_size
            total_samples += original.frames
        assert total_samples == rvq["samples"] == 16197971 and total_bytes == 3 * rvq["frames"] == 303858
        record = experiment_log.split(f"<!-- experiment:champion6_{cell}:start -->")[1].split(f"<!-- experiment:champion6_{cell}:end -->")[0]
        assert "Status: `complete`" in record and sha in record and "Selected checkpoint global step: `500000`" in record
        assert str(checkpoint) in record and "Training files | 394988" in record and "Validation files | 14596" in record
        assert expected["snapshot_sha256"] in record and "trained=false" in record and "global_step=0" in record
        assert "CHAMPION6_RESULTS.audit" in record and setup["pairs"][str(seed)]["source_sha256"] in record
        report["cells"][cell] = {"seed": seed, "candidate": candidate, "summary": summary, "complexity": complexity, "rvq": rvq,
            "effective_config": config, "metadata": metadata, "supervisor": supervisor, "training_curve": training,
            "supervisor_events": supervisor_events, "raw_log_failure_token_counts": failure_counts,
            "preflight_config_note": "Only output_dir changed from relative to equivalent absolute path at launch; all hyperparameters identical.",
            "initialization_sha256": digest(init), "shared_tensors_verified": len(shared), "discriminator_pair_identity_verified": True,
            "checkpoint": str(checkpoint.relative_to(ROOT)), "checkpoint_sha256": sha, "checkpoint_step": state["global_step"],
            "diagnostic_best_step": best["global_step"], "diagnostic_best_sha256": digest(run / "checkpoints/best.pt"),
            "roundtrip": {"files": 200, "bytes": total_bytes, "samples": total_samples, "frames": rvq["frames"], "audio_lengths_and_format_verified": True},
            "artifact_sha256": {name: digest(run / name) for name in ("pipeline.log", "supervisor.log", "metrics.jsonl", "effective_config.yaml", "run_metadata.json", "rvq_diagnostics.json", "evaluation/metrics/summary.json", "evaluation/metrics/per_file.csv", "evaluation/complexity.json")},
            "training_components_note": "No separate minibatch training_components.jsonl was enabled. Actual 20 validation component records and raw pipeline retained; no fabricated history."}
        print(f"audited {cell}: {summary['objective_quality_score']:.10f}, step500k SHA {sha}", flush=True)
        del state, best, initial
    summaries = [report["cells"][cell]["summary"] for cell in CELLS]
    v2 = {"means": baseline["selection_metrics"], "objective_quality_score": baseline["selection_metrics"]["objective_quality_score"]}
    for label, ci, ri in (("B_minus_A", 1, 0), ("D_minus_C", 3, 2)):
        report["comparisons"][label] = comparison(summaries[ci], summaries[ri])
        report["comparisons"][CELLS[ci]+"_minus_v2"] = comparison(summaries[ci], v2)
        report["guardrails"][str(report["cells"][CELLS[ri]]["seed"])] = {
            "control_score": summaries[ri]["objective_quality_score"],
            "control_gate_pass": summaries[ri]["objective_quality_score"] >= 46.25,
            "candidate_quality_gate_pass": report["comparisons"][label]["passes"] and report["comparisons"][CELLS[ci]+"_minus_v2"]["passes"]}
    report["confirmation_pass"] = all(item["control_gate_pass"] and item["candidate_quality_gate_pass"] for item in report["guardrails"].values())
    report["conclusion"] = "Not a preregistered confirmation pass: seed3407 control failed46.25. Both candidates passed numeric quality/component gates versus matched controls and frozen v2; control failure prevents clean confirmation. No promotion, sealed evaluation, extension or seed replacement."
    report["next_action_decision"] = "Batch complete. Stop automatic new training and remove the existing monitor after scoped archival/push. No CHAMPION7 registered. Retain promising candidates and all checkpoints; any future work needs a preregistered control-stability protocol before mechanism/capacity attribution."
    report["two_new_seed_statistics"] = {}
    for label, indices in (("control", (0, 2)), ("candidate", (1, 3))):
        report["two_new_seed_statistics"][label] = {"score": mean_range([summaries[i]["objective_quality_score"] for i in indices]), **{key: mean_range([summaries[i]["means"][key] for i in indices]) for key in METRICS}}
    contrasts = [report["comparisons"][label] for label in ("B_minus_A", "D_minus_C")]
    report["two_new_seed_statistics"]["matched_gains"] = {"score": mean_range([item["score_gain"] for item in contrasts]), **{key: mean_range([item["component_deltas"][key] for item in contrasts]) for key in METRICS}}
    report["uncertainty_note"] = "Descriptive mean/range of two new training seeds only, not a confidence interval or general seed-distribution estimate. No factorial effects; CHAMPION5 remains separate discovery."
    report["diagnostic_path"] = "encoder -> latent_norm -> analysis_temporal -> analysis_gru -> quantizer; partial codewords -> synthesis_temporal -> synthesis_conv2former -> decoder -> decoder_refinement -> original-length trim (scripts/diagnose_rvq.py inspected)."
    report["input_hashes"] = {name: digest(ROOT / name) for name in ("CHAMPION6_PLAN.md", "CHAMPION6_SETUP.audit", "CHAMPION6_PROFILE.audit", "CHAMPION5_RESULTS.audit", "scripts/preflight_champion6.py", "scripts/train.py", "scripts/diagnose_rvq.py", "scripts/run_champion6_experiment.sh", "scripts/supervise_champion6.py", "src/ssp_codec/model.py", "src/ssp_codec/champion_synthesis.py", "scripts/audit_champion6_results.py")}
    (ROOT / "CHAMPION6_RESULTS.audit").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({key: report[key] for key in ("comparisons", "guardrails", "confirmation_pass", "two_new_seed_statistics")}, indent=2))


if __name__ == "__main__":
    main()
