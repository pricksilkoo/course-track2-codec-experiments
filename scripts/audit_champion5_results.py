#!/usr/bin/env python3
"""Audit the prospectively fixed CHAMPION5 endpoint; never select a checkpoint."""
from __future__ import annotations
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import soundfile as sf
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
CELLS = ("a_control", "b_encoder_gru", "c_fourier", "d_fourier_gru")
METRICS = ("PESQ", "ESTOI", "SI_SNR", "UTMOS")

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def main():
    torch.set_num_threads(2)
    setup = json.loads((ROOT / "runs/champion5_setup/preflight_report.json").read_text())
    source = ROOT / "runs/lookahead4_scratch_init/step0.pt"
    assert digest(source) == setup["source_step0_sha256"]
    origin = torch.load(source, map_location="cpu", weights_only=False)
    assert origin["trained"] is False and origin["global_step"] == 0
    baseline = json.loads((ROOT / "model_registry/strong_baseline_v2.json").read_text())
    assert digest(ROOT / baseline["checkpoint"]) == baseline["checkpoint_sha256"]
    reference = ROOT / "runs/fast_b64_2s_v1/validation_200"
    fixed_hashes = {p.name: digest(p) for p in sorted(reference.glob("*.wav"))}
    historical = json.loads((ROOT / "runs/champion4_setup/preflight_report.json").read_text())
    assert fixed_hashes == historical["fixed200_sha256"] and len(fixed_hashes) == 200
    for relative, expected_hash in historical["input_sha256"].items():
        assert digest(ROOT / relative) == expected_hash, relative
    data_hashes = {str(p.relative_to(ROOT)): digest(p) for p in sorted((ROOT / "data/manifests/vctk_libritts").glob("*")) if p.is_file()}
    data_counts = {kind: sum(bool(line.strip()) for line in (ROOT / f"data/manifests/vctk_libritts/{kind}.scp").read_text().splitlines()) for kind in ("train", "valid")}
    assert data_counts == {"train": 394988, "valid": 14596}
    report = {"created_utc": datetime.now(timezone.utc).isoformat(), "selection": "pre-fixed 500000-step last.pt; primary", "baseline": baseline,
        "data_hashes": data_hashes, "data_counts": data_counts, "fixed200_sha256": fixed_hashes,
        "source_step0_sha256": digest(source), "cells": {}, "effects": {}, "guardrails": {}}
    scores = {}
    paths = None
    for cell in CELLS:
        run = ROOT / "runs" / f"champion5_{cell}"
        output = run / "evaluation"
        for marker in (run / "TRAINING_COMPLETE", run / "PIPELINE_COMPLETE", output / "ROUNDTRIP_COMPLETE"):
            assert marker.exists(), marker
        assert json.loads((run / "supervisor_state.json").read_text())["status"] == "complete"
        config = yaml.safe_load((run / "effective_config.yaml").read_text())
        init = ROOT / "runs/champion5_setup" / f"step0_{cell}.pt"
        assert digest(init) == setup["cells"][cell]["snapshot_sha256"]
        initial = torch.load(init, map_location="cpu", weights_only=False)
        assert initial["trained"] is False and initial["global_step"] == 0
        assert all(torch.equal(tensor, initial["discriminator"][key]) for key, tensor in origin["discriminator"].items())
        metadata = json.loads((run / "run_metadata.json").read_text())
        assert Path(metadata["init_checkpoint"]) == init and metadata["resume_checkpoint"] is None
        assert config["seed"] == config["training"]["data_order_seed"] == 20261024
        assert config["model"]["synthesis_initialization_seed"] == 20261103
        assert config["training"]["reset_rng_after_init"] and config["training"]["fail_on_nonfinite"]
        training = [json.loads(line) for line in (run / "metrics.jsonl").read_text().splitlines()]
        assert [row["global_step"] for row in training] == list(range(25000, 500001, 25000))
        assert all(np.isfinite(row["train_loss"]) and all(np.isfinite(value) for value in row["validation"].values()) for row in training)
        for row in training:
            expected = max(0., min(1., (row["global_step"] - 100000 + 1) / 50000))
            assert abs(row["validation"]["adversarial_factor"] - expected) < 1e-6
        checkpoint = run / "checkpoints/last.pt"
        checkpoint_hash = digest(checkpoint)
        assert (output / "checkpoint.sha256").read_text().split()[0] == checkpoint_hash
        state = torch.load(checkpoint, map_location="cpu", weights_only=False)
        best = torch.load(run / "checkpoints/best.pt", map_location="cpu", weights_only=False)
        assert state["global_step"] == 500000
        summary = json.loads((output / "metrics/summary.json").read_text())
        complexity = json.loads((output / "complexity.json").read_text())
        rvq = json.loads((run / "rvq_diagnostics.json").read_text())
        assert summary["files"] == rvq["files"] == 200 and not summary["utmos_skipped"]
        assert rvq["checkpoint_global_step"] == 500000 and Path(rvq["checkpoint"]) == checkpoint
        assert abs(rvq["partial_reconstruction"][-1]["si_snr_db_mean_per_file"] - summary["means"]["SI_SNR"]) < 1e-4
        assert complexity["sample_rate_hz"] == 16000 and complexity["frame_samples"] == 160
        assert complexity["bitrate_bps"] == 2400 and complexity["algorithmic_lookahead_ms"] == 30
        assert complexity["total_mflop_per_s"] <= 700 and complexity["decoder_mflop_per_s"] <= 300
        assert complexity["unclassified_mmac_per_s"] == 0
        rows = list(csv.DictReader((output / "metrics/per_file.csv").open()))
        current_paths = [row["file"] for row in rows]
        assert len(rows) == 200 and (paths is None or paths == current_paths)
        paths = current_paths
        values = np.array([[float(row[key]) for key in METRICS] for row in rows])
        assert np.isfinite(values).all()
        score = 25*(np.clip((values[:,0]-1)/3.5,0,1)+np.clip(values[:,1],0,1)+np.clip((values[:,2]+10)/40,0,1)+np.clip((values[:,3]-1)/4,0,1))
        assert abs(score.mean() - summary["objective_quality_score"]) < 1e-9
        assert all(abs(values[:, index].mean() - summary["means"][key]) < 1e-9 for index, key in enumerate(METRICS))
        scores[cell] = score
        bitstreams = list((output / "bitstreams").glob("*.bin"))
        assert len(bitstreams) == 200
        total_bytes = total_samples = 0
        for bitstream in bitstreams:
            side = json.loads(bitstream.with_suffix(".json").read_text())
            audio = reference / bitstream.with_suffix(".wav").name
            reconstructed = output / "reconstructed" / audio.name
            original_info, decoded_info = sf.info(audio), sf.info(reconstructed)
            assert original_info.samplerate == decoded_info.samplerate == 16000
            assert original_info.channels == decoded_info.channels == 1
            assert original_info.frames == decoded_info.frames == side["num_samples"]
            assert bitstream.stat().st_size == 3*((original_info.frames+159)//160)
            total_bytes += bitstream.stat().st_size
            total_samples += original_info.frames
        assert total_samples == rvq["samples"] and total_bytes == 3*rvq["frames"]
        report["cells"][cell] = {"summary": summary, "complexity": complexity, "rvq": rvq,
            "effective_config": config, "metadata": metadata, "training_curve": training,
            "initialization_sha256": digest(init), "checkpoint": str(checkpoint.relative_to(ROOT)),
            "checkpoint_sha256": checkpoint_hash, "checkpoint_step": state["global_step"],
            "diagnostic_best_step": best["global_step"], "roundtrip": {"files": 200, "bytes": total_bytes, "samples": total_samples, "audio_lengths_and_format_verified": True},
            "training_components_note": "No separate training_components.jsonl was enabled; original validation component metrics at every 25k and raw pipeline logs retained. Do not fabricate per-minibatch component history."}
    a,b,c,d = [report["cells"][cell]["summary"]["objective_quality_score"] for cell in CELLS]
    report["effects"] = {"B_minus_A": b-a, "C_minus_A": c-a, "D_minus_A": d-a, "D_minus_B": d-b, "D_minus_C": d-c,
        "GRU_main_effect": ((b-a)+(d-c))/2, "synthesis_main_effect": ((c-a)+(d-b))/2, "interaction": d-c-b+a}
    rng = np.random.default_rng(20261104)
    samples = rng.integers(0,200,(5000,200))
    report["paired_file_bootstrap"] = {}
    for candidate, reference_cell in ((CELLS[1],CELLS[0]),(CELLS[2],CELLS[0]),(CELLS[3],CELLS[0]),(CELLS[3],CELLS[1]),(CELLS[3],CELLS[2])):
        differences = scores[candidate] - scores[reference_cell]
        report["paired_file_bootstrap"][candidate+"_minus_"+reference_cell] = {"mean": float(differences.mean()), "CI95": np.quantile(differences[samples].mean(axis=1),[.025,.975]).tolist(), "caveat": "Conditional file uncertainty only, not training-seed uncertainty; no promotion test."}
    report["guardrails"]["control_gate_pass"] = a >= 46.25
    for cell in CELLS[1:]:
        candidate = report["cells"][cell]["summary"]
        report["guardrails"][cell] = {}
        for label, reference_summary in (("A",report["cells"][CELLS[0]]["summary"]),("v2",{"means":baseline["selection_metrics"],"objective_quality_score":baseline["selection_metrics"]["objective_quality_score"]})):
            delta = {key:candidate["means"][key]-reference_summary["means"][key] for key in METRICS}
            gain = candidate["objective_quality_score"]-reference_summary["objective_quality_score"]
            report["guardrails"][cell][label] = {"score_gain":gain,"component_deltas":delta,"passes":gain>=.15 and all(delta[key]>=-limit for key,limit in zip(METRICS,(.02,.003,.15,.03)))}
    report["input_hashes"] = {name:digest(ROOT/name) for name in ("CHAMPION5_PLAN.md","scripts/train.py","scripts/diagnose_rvq.py","src/ssp_codec/model.py","src/ssp_codec/champion_synthesis.py")}
    (ROOT/"CHAMPION5_RESULTS.audit").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"effects":report["effects"],"guardrails":report["guardrails"],"summaries":{cell:data["summary"] for cell,data in report["cells"].items()}},indent=2))

if __name__ == "__main__":
    main()
