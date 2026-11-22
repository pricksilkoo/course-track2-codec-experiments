#!/usr/bin/env python3
"""Use the frozen supervisor with an idle-only startup gate after two diagnosed OOMs."""
from datetime import datetime,timezone
import json,sys,time
from pathlib import Path
import supervise_champion12 as supervisor

def make_idle_gate(real_gpu_state, run):
    announced=False
    def idle_gpu_state(gpu):
        nonlocal announced
        while True:
            total,free,pids=real_gpu_state(gpu)
            if free>=8192 and not pids:
                return total,free,pids
            if not announced:
                value={'status':'waiting_for_idle_gpu_after_repeated_oom',
                    'updated_utc':datetime.now(timezone.utc).isoformat(),'gpu':gpu,
                    'observed_free_MiB':free,'existing_gpu_pids':pids,
                    'launch_free_MiB':8192,'runtime_resource_poll':False,
                    'startup_idle_requirement_after_two_diagnosed_shared_OOMs':True,
                    'training_total_steps':500000,'next_resume_step':99000,
                    'automatic_retry':False}
                tmp=run/'supervisor_state.tmp'
                tmp.write_text(json.dumps(value,indent=2)+'\n')
                tmp.replace(run/'supervisor_state.json')
                print(json.dumps(value),flush=True);announced=True
            time.sleep(30)
    return idle_gpu_state

def main():
    if len(sys.argv)!=3:
        raise SystemExit('usage: supervise_champion12_idle.py CELL GPU')
    cell,gpu=sys.argv[1],int(sys.argv[2])
    assert cell in supervisor.CELLS and gpu==supervisor.CELLS.index(cell)
    root=supervisor.ROOT;run=root/f'runs/champion12_{cell}'
    audit=json.loads((root/'CHAMPION12_RECOVERY_02.audit').read_text())
    item=audit['cells'][cell]
    assert item['resume_step']==99000 and item['additional_completed_updates']==0
    assert (Path(item['archive'])/'preservation.audit').exists()
    assert not (run/'PIPELINE_COMPLETE').exists()
    # All actual locks, disk threshold, private Popen group, complete-state resume,
    # child.wait and no-retry behavior remain in the frozen original supervisor.
    # This adapter is called only by that supervisor's pre-launch capacity loop.
    supervisor.gpu_state=make_idle_gate(supervisor.gpu_state,run)
    supervisor.main()

if __name__=='__main__':main()
