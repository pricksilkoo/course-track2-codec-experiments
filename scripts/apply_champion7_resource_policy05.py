#!/usr/bin/env python3
"""Apply explicit user policy to idle waiters only; never stop a training child."""
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess
import time

from run_champion7_experiment import CELLS, PARENT_SHA, digest, record

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT/"CHAMPION7_RESOURCE_POLICY05.audit"
    if output.exists(): raise RuntimeError("Already applied; do not repeat")
    prior = json.loads((ROOT/"CHAMPION7_RECOVERY04.audit").read_text())
    report = {"created_utc":datetime.now(timezone.utc).isoformat(),
        "authorization":"User: 有空间就训练，不用实时检测，断了再说",
        "launch_free_MiB":8192,"profile_reserved_peak_MiB":6382,
        "runtime_GPU_and_disk_resource_poll":False,
        "no_proactive_8GiB_runtime_stop":True,"disk_floor_prelaunch_GiB":10,
        "recovery_interval_steps":1000,"model_training_budget_unchanged":True,
        "parent_sha256":PARENT_SHA,"cells":{}}
    # Locate only our exact four waiting supervisors. Freeze them during the
    # no-child check to close the race with an old-policy launch.
    supervisors = {}
    for process in Path("/proc").iterdir():
        if not process.name.isdecimal(): continue
        try:
            words=(process/"cmdline").read_bytes().decode().split("\0")
            if len(words)<4 or not Path(words[0]).name.startswith("python"):continue
            if words[1:3]!=["-u","scripts/supervise_champion7.py"]:continue
            for c in CELLS:
                if words[3]==f"champion7_{c}":
                    assert c not in supervisors;supervisors[c]=int(process.name)
        except (FileNotFoundError,ProcessLookupError,PermissionError): pass
    assert set(supervisors)==set(CELLS), "Only replace four confirmed live waiters"
    frozen=[]
    try:
        for c,pid in supervisors.items():
            run=ROOT/f"runs/champion7_{c}"
            state=json.loads((run/"supervisor_state.json").read_text())
            assert state["status"].startswith("waiting_for_")
            os.kill(pid,signal.SIGSTOP);frozen.append(pid)
        for gpu,c in enumerate(CELLS):
            pid=supervisors[c];run=ROOT/f"runs/champion7_{c}"
            children=Path(f"/proc/{pid}/task/{pid}/children").read_text().strip()
            # A short-lived nvidia-smi child is permissible only after it exits;
            # never signal a waiter with any active pipeline or GPU child.
            if children:
                for child in children.split():
                    cmd=Path(f"/proc/{child}/cmdline")
                    if cmd.exists():
                        assert b"nvidia-smi" in cmd.read_bytes(), "Training child active: leave it untouched"
                for _ in range(100):
                    if not any(Path(f"/proc/{x}").exists() and Path(f"/proc/{x}/stat").read_text().split()[2]!="Z" for x in children.split()):break
                    time.sleep(.05)
            assert json.loads((run/"supervisor_state.json").read_text())["status"].startswith("waiting_for_")
            lock=(run/".pipeline.lock").open("a")
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);lock.close()
            assert digest(run/"checkpoints/last.pt")==prior["cells"][c]["resume_checkpoint_sha256"]
            archive=run/"attempts/resource_policy05_prelaunch_waiter"
            archive.mkdir(parents=True,exist_ok=False)
            hashes={}
            for name in ("supervisor_state.json","supervisor.log","run_metadata.json","recovery_policy.json"):
                shutil.copy2(run/name,archive/name);hashes[name]=digest(archive/name)
            report["cells"][c]={"gpu":gpu,"old_waiter_pid":pid,"no_training_child":True,
                "archive":str(archive.relative_to(ROOT)),"archive_sha256":hashes,
                "resume_step":prior["cells"][c]["resume_global_step"],
                "resume_sha256":prior["cells"][c]["resume_checkpoint_sha256"],
                "no_extra_optimization_lost":True}
        output.write_text(json.dumps(report,indent=2)+"\n")
        (ROOT/"runs/champion7_setup/resource_policy05_report.json").write_text(output.read_text())
        for pid in frozen: os.kill(pid,signal.SIGTERM)
    finally:
        for pid in frozen:
            try:os.kill(pid,signal.SIGCONT)
            except ProcessLookupError:pass
    for gpu,c in enumerate(CELLS):
        run=ROOT/f"runs/champion7_{c}";target=f"codec_champion7_v1:{c}"
        for _ in range(100):
            if subprocess.check_output(["tmux","display-message","-p","-t",target,"#{pane_dead}"],text=True).strip()=="1":break
            time.sleep(.1)
        assert subprocess.check_output(["tmux","display-message","-p","-t",target,"#{pane_dead}"],text=True).strip()=="1"
        policy=json.loads((run/"recovery_policy.json").read_text())
        policy.update(launch_free_MiB=8192,runtime_resource_poll=False,user_requested_policy05=True)
        (run/"recovery_policy.json").write_text(json.dumps(policy,indent=2)+"\n")
        record(run,f"champion7_{c}","planned",checkpoint=run/"checkpoints/last.pt",note=(
            f"User policy05: launch with>=8GiB free (measured peak6382MiB), no runtime resource polling/stops. "
            f"Resume saved local{report['cells'][c]['resume_step']}, no model/optimizer reset. "
            "1000-step atomic recovery retained; crash/OOM handled after actual exit, no blind auto-retry. "
            "Only idle waiters replaced, no training child stopped. CHAMPION7_RESOURCE_POLICY05.audit."))
        args=[str(ROOT/".venv-codec/bin/python"),"-u","scripts/supervise_champion7.py",
            f"champion7_{c}",str(gpu),f"configs/champion7/{c}.yaml","--allow-shared","--steps","100000",
            "--launch-free-mib","8192","--no-runtime-resource-poll"]
        shell=shlex.join(args)+" >> "+shlex.quote(str(run/"supervisor.log"))+" 2>&1"
        subprocess.run(["tmux","respawn-pane","-t",target,"-c",str(ROOT),shell],check=True)
        print(f"Applied policy05 {c}: resume when8GiB free, no runtime resource polling",flush=True)


if __name__=="__main__":main()
