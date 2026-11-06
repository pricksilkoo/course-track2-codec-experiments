#!/usr/bin/env python3
"""Disposable full-batch recovery/resume exercise; never a formal initializer."""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs/_smoke_champion7_recovery_io_v1"
sys.path.insert(0, str(ROOT / "src"))


def phase(stop):
    import torch
    torch.set_num_threads(4)
    if stop:
        import ssp_codec.checkpoint_io as io
        save = io.save_recovery_checkpoint
        def save_and_stop(**kwargs):
            save(**kwargs)
            raise SystemExit(0)
        io.save_recovery_checkpoint = save_and_stop
    sys.argv = ["scripts/train.py", "--config", "configs/champion7/a_continue.yaml",
        "--train-manifest", "data/manifests/vctk_libritts/train.scp",
        "--valid-manifest", "data/manifests/vctk_libritts/valid.scp",
        "--output-dir", str(OUT), "--device", "cuda", "--max-total-steps", "2",
        "--max-valid-steps", "1", "--num-workers", "2", "--set", "training.warmup_steps=0",
        "--set", "training.recovery_checkpoint_interval_steps=1"]
    sys.argv += (["--init-checkpoint", "runs/champion6_b_s3407_fourier_gru/checkpoints/last.pt"]
                 if stop else ["--resume", str(OUT / "checkpoints/last.pt")])
    runpy.run_path(str(ROOT / "scripts/train.py"), run_name="__main__")


def main():
    os.chdir(ROOT)
    if len(sys.argv) == 2:
        phase(sys.argv[1] == "stop"); return
    from supervise_champion7 import gpu_state, stop_own_pipeline
    assert not OUT.exists(), "Do not overwrite old smoke evidence"
    assert gpu_state(0)[1] >= 20480
    OUT.mkdir()
    os.environ.update(CUDA_VISIBLE_DEVICES="0", OMP_NUM_THREADS="4",
                      TORCH_HOME=str(ROOT / "data/torch-cache"))
    for name in ("stop", "resume"):
        with (OUT / f"{name}.log").open("w") as log:
            child = subprocess.Popen([sys.executable, __file__, name], cwd=ROOT,
                stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            while child.poll() is None:
                time.sleep(1)
                if gpu_state(0)[1] < 8192:
                    stop_own_pipeline(child)
                    raise RuntimeError("Smoke GPU capacity guard; diagnose, no retry")
            assert child.returncode == 0, f"Check {name}.log"
        import torch
        state = torch.load(OUT / "checkpoints/last.pt", map_location="cpu", weights_only=False)
        assert state["global_step"] == (1 if name == "stop" else 2)
        if name == "stop":
            assert state["checkpoint_kind"] == "recovery_only"
            assert "validation_metrics" not in state and not (OUT/"metrics.jsonl").exists()
            assert state["optimizer"]["state"] and state["discriminator_optimizer"]["state"]
        else:
            assert state["validation_metrics"]
    events = [json.loads(line) for line in (OUT/"recovery_checkpoints.jsonl").read_text().splitlines()]
    assert [event["global_step"] for event in events] == [1, 2]
    assert len((OUT/"metrics.jsonl").read_text().splitlines()) == 1
    report = {"full_batch": 32, "segment_samples": 32000, "full_GAN": True,
        "saved_recovery_step": 1, "resumed_final_step": 2,
        "no_fake_validation_at_recovery": True, "disposable_not_formal_parent": True,
        "finite_final_validation": state["validation_metrics"]}
    (OUT/"report.json").write_text(json.dumps(report, indent=2)+"\n")
    (OUT/"RECOVERY_IO_COMPLETE").touch()
    print(json.dumps(report), flush=True)


if __name__ == "__main__": main()
