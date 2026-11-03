#!/usr/bin/env python3
"""Launch exactly four preflighted from-scratch structural cells."""
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SESSION = "codec_champion5_v1"
assert (ROOT / "runs/champion5_setup/PREFLIGHT_COMPLETE").is_file()
assert (ROOT / "runs/champion5_setup/PROFILE_COMPLETE").is_file()
if subprocess.run(["tmux", "has-session", "-t", SESSION], capture_output=True).returncode == 0:
    raise RuntimeError("session exists; inspect/recover instead of duplicating")
for gpu, cell in enumerate(("a_control", "b_encoder_gru", "c_fourier", "d_fourier_gru")):
    run = ROOT / "runs" / f"champion5_{cell}"
    assert not (run / "PIPELINE_COMPLETE").exists()
    command = shlex.join([str(ROOT / ".venv-codec/bin/python"), "-u",
        "scripts/supervise_champion5.py", run.name, str(gpu), f"configs/champion5/{cell}.yaml",
        "--allow-shared", "--steps", "500000"])
    shell = f"cd {shlex.quote(str(ROOT))} && {command} > {shlex.quote(str(run / 'supervisor.log'))} 2>&1"
    args = ["tmux", "new-session", "-d", "-s", SESSION, "-n", cell, shell] if gpu == 0 else [
        "tmux", "new-window", "-t", SESSION, "-n", cell, shell]
    subprocess.run(args, check=True)
    subprocess.run(["tmux", "set-window-option", "-t", f"{SESSION}:{cell}", "remain-on-exit", "on"], check=True)
print("Four matched scratch workers launched")
