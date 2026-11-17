#!/usr/bin/env python3
"""One-shot launch of the three newly registered scratch cells; refuse duplicates."""
import shlex
import subprocess
from preflight_champion11 import ROOT,CELLS,GPU_ASSIGNMENTS,read,digest


def main():
    session="codec_champion11_v1"
    assert (ROOT/"runs/champion11_setup/PREFLIGHT_COMPLETE").exists()
    if subprocess.run(["tmux","has-session","-t",session],capture_output=True).returncode==0:
        raise RuntimeError("Existing session: inspect rather than duplicate")
    audit=read(ROOT/"CHAMPION11_SETUP.audit")
    assert all(digest(ROOT/p)==h for p,h in audit["code_sha256"].items())
    for c in CELLS:
        run=ROOT/f"runs/champion11_{c}"
        assert not (run/"run_metadata.json").exists() and not (run/"checkpoints/last.pt").exists()
        assert not (run/"PIPELINE_COMPLETE").exists()
        assert digest(ROOT/audit["cells"][c]["snapshot"])==audit["cells"][c]["snapshot_sha256"]
    for index,(c,gpu) in enumerate(GPU_ASSIGNMENTS.items()):
        run=ROOT/f"runs/champion11_{c}"
        command=shlex.join([str(ROOT/".venv-codec/bin/python"),"-u","scripts/supervise_champion11.py",c,str(gpu)])
        shell=f"cd {shlex.quote(str(ROOT))} && {command} >> {shlex.quote(str(run/'supervisor.log'))} 2>&1"
        args=["tmux","new-session","-d","-s",session,"-n",c,shell] if index==0 else ["tmux","new-window","-t",session,"-n",c,shell]
        subprocess.run(args,check=True)
        subprocess.run(["tmux","set-window-option","-t",f"{session}:{c}","remain-on-exit","on"],check=True)
    print("Three CHAMPION11 scratch supervisors launched; sharing/startup-only capacity, no GPU smoke")


if __name__=="__main__":main()
