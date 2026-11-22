#!/usr/bin/env python3
"""One C6-30ms job, waiting for a truly idle unreserved GPU; no runtime polling."""
from datetime import datetime,timezone
import fcntl,json,os,signal,subprocess,time,shutil
from preflight_c6_30ms import ROOT,STEPS,read
from supervise_champion7 import gpu_state,stop_own_pipeline

def choose_gpu(shared_runs):
    for gpu in range(4):
        lock=(shared_runs/f'.champion4_gpu{gpu}.lock').open('r')
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:lock.close();continue
        total,free,pids=gpu_state(gpu)
        if free>=8192 and not pids:return gpu,lock,free
        lock.close()
    return None

def main():
    run=ROOT/'runs/c6_30ms_b_s3407'
    own=(run/'.supervisor.lock').open('a');fcntl.flock(own,fcntl.LOCK_EX|fcntl.LOCK_NB)
    child=None
    def state(status,**extra):
        v={'status':status,'updated_utc':datetime.now(timezone.utc).isoformat(),
           'training_total_steps':STEPS,'startup_idle_required':True,'runtime_resource_poll':False,
           'automatic_retry':False,**extra}
        p=run/'supervisor_state.tmp';p.write_text(json.dumps(v,indent=2)+'\n');p.replace(run/'supervisor_state.json')
        print(json.dumps(v),flush=True)
    def interrupted(signum,frame):
        if child is not None:stop_own_pipeline(child)
        state('interrupted',signal=signum);raise SystemExit(128+signum)
    signal.signal(signal.SIGINT,interrupted);signal.signal(signal.SIGTERM,interrupted)
    if (run/'PIPELINE_COMPLETE').exists():state('complete');return
    shared_runs=(ROOT/'runs/champion10_setup').resolve().parent
    announced=False
    while True:
        candidate=choose_gpu(shared_runs) if shutil.disk_usage(ROOT).free>=10*2**30 else None
        if candidate is not None:break
        if not announced:
            state('waiting_for_unreserved_idle_gpu',reason='preserve existing project GPU reservations; require no compute PID,free>=8192MiB,disk>=10GiB')
            announced=True
        time.sleep(30)
    gpu,gpu_lock,free=candidate
    command=[str(ROOT/'.venv-codec/bin/python'),'-u','scripts/run_c6_30ms_experiment.py','b_s3407',str(gpu)]
    state('running',gpu=gpu,observed_launch_free_MiB=free,existing_gpu_pids=[],command=command)
    child=subprocess.Popen(command,cwd=ROOT,start_new_session=True,
      env={**os.environ,'PYTHONPATH':str(ROOT/'src'),'PYTHONNOUSERSITE':'1','OMP_NUM_THREADS':'4','PYTHONUNBUFFERED':'1'})
    child.wait()
    if child.returncode:
        state('failed',gpu=gpu,exit_code=child.returncode,reason='preserve and diagnose actual exit; no automatic retry')
        raise SystemExit(child.returncode if child.returncode>0 else 1)
    state('complete' if (run/'PIPELINE_COMPLETE').exists() else 'needs_attention',gpu=gpu)

if __name__=='__main__':main()
