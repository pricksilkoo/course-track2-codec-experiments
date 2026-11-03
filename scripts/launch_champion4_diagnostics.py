#!/usr/bin/env python3
"""Launch only the four registered fixed100k checkpoint evaluations."""
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SESSION = "codec_champion4_finaldiag_v1"
if subprocess.run(["tmux", "has-session", "-t", SESSION], capture_output=True).returncode == 0:
    raise RuntimeError("diagnostic session exists; inspect it before recovery")
for gpu, cell in enumerate(("a_control", "b_training", "c_conv2former", "d_combined")):
    run = ROOT / "runs" / f"champion4_{cell}"
    assert (run / "PIPELINE_COMPLETE").is_file()
    command = shlex.join([str(ROOT / ".venv-codec/bin/python"), "-u",
        "scripts/supervise_champion4.py", run.name, str(gpu), f"configs/champion4/{cell}.yaml",
        "--allow-shared", "--final-diagnostic"])
    shell = f"cd {shlex.quote(str(ROOT))} && {command} > {shlex.quote(str(run / 'final_diagnostic_supervisor.log'))} 2>&1"
    args = ["tmux", "new-session", "-d", "-s", SESSION, "-n", cell, shell] if gpu == 0 else [
        "tmux", "new-window", "-t", SESSION, "-n", cell, shell]
    subprocess.run(args, check=True)
    subprocess.run(["tmux", "set-window-option", "-t", f"{SESSION}:{cell}", "remain-on-exit", "on"], check=True)
print("Four fixed-endpoint diagnostics launched; no training")
