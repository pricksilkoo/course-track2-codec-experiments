#!/usr/bin/env python3
"""Launch only four protected capacity waiters; no direct GPU training launch."""
import json
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CELLS = ("a_continue", "b_si", "c_gan", "d_both")
SESSION = "codec_champion7_v1"


def main():
    if subprocess.run(["tmux", "has-session", "-t", SESSION], capture_output=True).returncode == 0:
        raise RuntimeError("Session already exists; inspect/resume only affected cell, never duplicate")
    report = json.loads((ROOT / "CHAMPION7_SETUP.audit").read_text())
    assert set(report["cells"]) == set(CELLS)
    for cell in CELLS:
        run = ROOT / f"runs/champion7_{cell}"
        if (run / "run_metadata.json").exists() or (run / "PIPELINE_COMPLETE").exists():
            raise RuntimeError("Formal work already exists; do not relaunch all cells")
    for gpu, cell in enumerate(CELLS):
        run = f"champion7_{cell}"
        cmd = [str(ROOT / ".venv-codec/bin/python"), "-u", "scripts/supervise_champion7.py",
            run, str(gpu), f"configs/champion7/{cell}.yaml", "--allow-shared", "--steps", "100000"]
        shell = shlex.join(cmd) + " >> " + shlex.quote(str(ROOT / "runs" / run / "supervisor.log")) + " 2>&1"
        if gpu == 0:
            subprocess.run(["tmux", "new-session", "-d", "-s", SESSION, "-n", cell,
                "-c", str(ROOT), shell], check=True)
            subprocess.run(["tmux", "set-option", "-t", SESSION, "remain-on-exit", "on"], check=True)
        else:
            subprocess.run(["tmux", "new-window", "-t", SESSION, "-n", cell,
                "-c", str(ROOT), shell], check=True)
        subprocess.run(["tmux", "set-window-option", "-t", f"{SESSION}:{cell}",
            "remain-on-exit", "on"], check=True)
        print(f"Started protected capacity waiter {run} on GPU{gpu}", flush=True)


if __name__ == "__main__":
    main()
