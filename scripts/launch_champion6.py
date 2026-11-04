#!/usr/bin/env python3
"""Launch exactly the four preregistered confirmation runs after safe preflight."""
from pathlib import Path
import hashlib
import json
import shlex
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SESSION="codec_champion6_v1"
assert (ROOT/"runs/champion6_setup/PREFLIGHT_COMPLETE").is_file()
assert (ROOT/"runs/champion6_setup/PROFILE_COMPLETE").is_file()
if subprocess.run(["tmux","has-session","-t",SESSION],capture_output=True).returncode==0:
    raise RuntimeError("session exists; inspect/recover instead of duplicating")
CELLS=("a_s3407_control","b_s3407_fourier_gru","c_s8128_control","d_s8128_fourier_gru")
setup=json.loads((ROOT/"runs/champion6_setup/preflight_report.json").read_text())
for cell in CELLS:
    run=ROOT/"runs"/f"champion6_{cell}"
    assert not (run/"PIPELINE_COMPLETE").exists() and not (run/"run_metadata.json").exists()
    snapshot=ROOT/"runs/champion6_setup"/f"step0_{cell}.pt"
    assert hashlib.sha256(snapshot.read_bytes()).hexdigest()==setup["cells"][cell]["snapshot_sha256"]
for gpu,cell in enumerate(CELLS):
    run=ROOT/"runs"/f"champion6_{cell}"
    command=shlex.join([str(ROOT/".venv-codec/bin/python"),"-u","scripts/supervise_champion6.py",run.name,str(gpu),
        f"configs/champion6/{cell}.yaml","--allow-shared","--steps","500000"])
    shell=f"cd {shlex.quote(str(ROOT))} && {command} > {shlex.quote(str(run/'supervisor.log'))} 2>&1"
    args=["tmux","new-session","-d","-s",SESSION,"-n",cell,shell] if gpu==0 else ["tmux","new-window","-t",SESSION,"-n",cell,shell]
    subprocess.run(args,check=True)
    subprocess.run(["tmux","set-window-option","-t",f"{SESSION}:{cell}","remain-on-exit","on"],check=True)
print("Four new-seed matched confirmation workers launched")
