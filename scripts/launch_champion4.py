#!/usr/bin/env python3
"""Launch exactly the four preflighted cells into independent tmux windows."""
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SESSION = "codec_champion4_v1"
assert (ROOT / "runs/champion4_setup/PREFLIGHT_COMPLETE").is_file()
assert (ROOT / "runs/champion4_setup/PROFILE_COMPLETE").is_file()
if subprocess.run(["tmux", "has-session", "-t", SESSION], capture_output=True).returncode == 0:
    raise RuntimeError("study session already exists; inspect and resume instead of duplicating")
for gpu, cell in enumerate(("a_control", "b_training", "c_conv2former", "d_combined")):
    run = f"champion4_{cell}"
    run_dir = ROOT / "runs" / run
    if (run_dir / "PIPELINE_COMPLETE").exists():
        raise RuntimeError(f"completed cell already exists: {run}")
    command = shlex.join([str(ROOT / ".venv-codec/bin/python"), "-u",
        "scripts/supervise_champion4.py", run, str(gpu), f"configs/champion4/{cell}.yaml",
        "--allow-shared"])
    shell_command = f"cd {shlex.quote(str(ROOT))} && {command} > {shlex.quote(str(run_dir / 'supervisor.log'))} 2>&1"
    if gpu == 0:
        args = ["tmux", "new-session", "-d", "-s", SESSION, "-n", cell, shell_command]
    else:
        args = ["tmux", "new-window", "-t", SESSION, "-n", cell, shell_command]
    subprocess.run(args, check=True)
    subprocess.run(["tmux", "set-window-option", "-t", f"{SESSION}:{cell}", "remain-on-exit", "on"], check=True)
print(f"Launched {SESSION}: four shared-GPU guarded workers")
