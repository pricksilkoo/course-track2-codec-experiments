#!/usr/bin/env python3
"""One warm-start cell, four prospectively declared score-search endpoints."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv-codec/bin/python"
PARENT = ROOT / "runs/champion6_b_s3407_fourier_gru/checkpoints/last.pt"
PARENT_SHA = "c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23"
CELLS = ("a_continue", "b_si", "c_gan", "d_both")
STEPS = (25000, 50000, 75000, 100000)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()


def checkpoint_step(path):
    import torch
    state = torch.load(path, map_location="cpu", weights_only=False)
    return int(state["global_step"])


def select_endpoint(candidates):
    return max(candidates, key=lambda item: (item["summary"]["objective_quality_score"], -item["additional_step"]))


def execute(*arguments):
    print("RUN", " ".join(str(x) for x in arguments), flush=True)
    subprocess.run([str(PYTHON), *map(str, arguments)], cwd=ROOT, check=True)


def record(run, name, status, checkpoint=None, evaluation=None, note=""):
    arguments = ["scripts/record_experiment.py", "--name", name, "--status", status,
        "--config", run / "effective_config.yaml", "--run-dir", run,
        "--dataset-summary", ROOT / "data/manifests/vctk_libritts/summary.json",
        "--checkpoint", checkpoint or run / "checkpoints/not_yet_score_selected.pt",
        "--output", ROOT / "EXPERIMENT_LOG.md", "--note", note]
    if evaluation:
        arguments += ["--evaluation-summary", evaluation / "metrics/summary.json",
            "--complexity-summary", evaluation / "complexity.json"]
    else:
        arguments += ["--complexity-summary", run / "preflight_complexity.json"]
    with (ROOT / ".experiment_log.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        execute(*arguments)


def verify_roundtrip(reference, output):
    import soundfile as sf
    import math
    originals = sorted(reference.glob("*.wav"))
    assert len(originals) == 200
    assert len(list((output / "bitstreams").glob("*.bin"))) == 200
    assert len(list((output / "reconstructed").glob("*.wav"))) == 200
    samples = total_bytes = 0
    for original in originals:
        reconstructed = output / "reconstructed" / original.name
        bitstream = output / "bitstreams" / original.with_suffix(".bin").name
        side = json.loads(bitstream.with_suffix(".json").read_text())
        a, b = sf.info(original), sf.info(reconstructed)
        assert a.samplerate == b.samplerate == 16000 and a.channels == b.channels == 1
        assert a.frames == b.frames == side["num_samples"]
        assert bitstream.stat().st_size == 3 * math.ceil(a.frames / 160)
        samples += a.frames
        total_bytes += bitstream.stat().st_size
    assert samples == 16197971 and total_bytes == 303858
    return {"files": 200, "samples": samples, "actual_bytes": total_bytes, "frames": total_bytes // 3, "audio_lengths_verified": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run")
    parser.add_argument("gpu", type=int)
    parser.add_argument("config")
    parser.add_argument("steps", type=int)
    args = parser.parse_args()
    cell = args.run.removeprefix("champion7_")
    if cell not in CELLS or args.run != f"champion7_{cell}" or args.steps != 100000 or args.gpu not in range(4):
        raise ValueError("Restricted to four registered100k fine-tuning cells")
    assert Path(args.config) == Path(f"configs/champion7/{cell}.yaml")
    run = ROOT / "runs" / args.run
    run.mkdir(parents=True, exist_ok=True)
    lock = (run / ".pipeline.lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if (run / "PIPELINE_COMPLETE").exists():
        return
    log = (run / "pipeline.log").open("a", buffering=1)
    os.dup2(log.fileno(), 1)
    os.dup2(log.fileno(), 2)
    os.environ.update(CUDA_VISIBLE_DEVICES=str(args.gpu), PYTHONNOUSERSITE="1",
        TORCH_HOME=str(ROOT / "data/torch-cache"), PYTHONUNBUFFERED="1")
    note = (f"Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 "
        f"SHA256 {PARENT_SHA}; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; "
        "select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/"+args.run+"/lineage.json; CHAMPION7_SETUP.audit.")
    try:
        assert digest(PARENT) == PARENT_SHA
        lineage = json.loads((run / "lineage.json").read_text())
        assert lineage["parent_sha256"] == PARENT_SHA and lineage["parent_global_step"] == 500000
        # Previous full-batch profile is preserved. This cell also proves finite
        # backward on disposable state only after the protected GPU launch.
        profile = ROOT / "runs" / f"_smoke_champion7_{cell}"
        if not (profile / "PROFILE_COMPLETE").exists():
            if (profile / "run_metadata.json").exists():
                raise RuntimeError("Incomplete full-batch profile; diagnose explicitly, do not blindly retry")
            execute("scripts/profile_champion7.py", "--config", args.config,
                "--output", str(profile.relative_to(ROOT)))
        record(run, args.run, "running", note=note)
        last = run / "checkpoints/last.pt"
        if not (run / "TRAINING_COMPLETE").exists():
            completed_step = checkpoint_step(last) if last.exists() else 0
            if completed_step > 100000:
                raise ValueError("Checkpoint beyond registered budget")
            if completed_step < 100000:
                train = ["scripts/train.py", "--config", args.config,
                    "--train-manifest", ROOT / "data/manifests/vctk_libritts/train.scp",
                    "--valid-manifest", ROOT / "data/manifests/vctk_libritts/valid.scp",
                    "--output-dir", run, "--device", "cuda", "--max-total-steps", "100000"]
                train += ["--resume", last] if last.exists() else ["--init-checkpoint", PARENT]
                execute(*train)
            assert checkpoint_step(last) == 100000
            (run / "TRAINING_COMPLETE").touch()
        reference = ROOT / "runs/fast_b64_2s_v1/validation_200"
        selection = []
        for step in STEPS:
            checkpoint = run / "checkpoints" / f"step_{step:08d}.pt"
            assert checkpoint_step(checkpoint) == step
            output = run / "evaluation" / f"step_{step:08d}"
            output.mkdir(parents=True, exist_ok=True)
            sha = digest(checkpoint)
            evidence = output / "checkpoint.sha256"
            if evidence.exists():
                assert evidence.read_text().split()[0] == sha
            else:
                evidence.write_text(f"{sha}  {checkpoint}\n")
            if not (output / "ROUNDTRIP_COMPLETE").exists():
                execute("scripts/encode.py", "--checkpoint", checkpoint, "--input-dir", reference,
                    "--output-dir", output / "bitstreams", "--device", "cuda")
                execute("scripts/decode.py", "--checkpoint", checkpoint,
                    "--bitstream-dir", output / "bitstreams", "--output-dir", output / "reconstructed", "--device", "cuda")
                execute("scripts/validate_submission.py", "--input-dir", reference,
                    "--bitstream-dir", output / "bitstreams", "--output-dir", output / "reconstructed")
                (output / "ROUNDTRIP_COMPLETE").touch()
            actual = verify_roundtrip(reference, output)
            if not (output / "metrics/summary.json").exists():
                execute("scripts/evaluate.py", "--reference-dir", reference,
                    "--reconstructed-dir", output / "reconstructed", "--output-dir", output / "metrics", "--device", "cuda")
            execute("scripts/complexity.py", "--checkpoint", checkpoint, "--output", output / "complexity.json")
            summary = json.loads((output / "metrics/summary.json").read_text())
            cost = json.loads((output / "complexity.json").read_text())
            assert summary["files"] == 200 and not summary["utmos_skipped"]
            import math
            assert all(math.isfinite(x) for x in summary["means"].values()) and math.isfinite(summary["objective_quality_score"])
            assert cost["total_mflop_per_s"] <= 700 and cost["decoder_mflop_per_s"] <= 300
            assert cost["algorithmic_lookahead_ms"] <= 30 and cost["bitrate_bps"] == 2400 and cost["unclassified_mmac_per_s"] == 0
            (output / "roundtrip_audit.json").write_text(json.dumps(actual, indent=2)+"\n")
            record(run, f"{args.run}_step{step:06d}", "complete", checkpoint, output,
                note + f" This searched endpoint extra step{step}, cumulative parent+stage={500000+step}.")
            selection.append({"additional_step": step, "cumulative_step": 500000+step,
                "checkpoint": str(checkpoint), "checkpoint_sha256": sha,
                "evaluation": str(output), "summary": summary})
        selected = select_endpoint(selection)
        selected["gain_vs_parent"] = selected["summary"]["objective_quality_score"] - 51.62433613863932
        selected["selection_kind"] = "exploratory fixed four-node development score search, not confirmation"
        (run / "selection.json").write_text(json.dumps({"candidates": selection, "selected": selected}, indent=2)+"\n")
        output = Path(selected["evaluation"])
        if not (output / "rvq_diagnostics.json").exists():
            execute("scripts/diagnose_rvq.py", "--checkpoint", selected["checkpoint"],
                "--input-dir", reference, "--output", output / "rvq_diagnostics.json", "--device", "cuda")
        record(run, args.run, "complete", Path(selected["checkpoint"]), output,
            note + f" Selected extra step{selected['additional_step']} by actual score; gain_vs_parent={selected['gain_vs_parent']:+.8f}.")
        (run / "PIPELINE_COMPLETE").touch()
        print("PIPELINE_COMPLETE", args.run, flush=True)
    except Exception as error:
        try:
            record(run, args.run, "failed", note=note+" Error: "+repr(error))
        except Exception:
            pass
        raise


if __name__ == "__main__":
    main()
