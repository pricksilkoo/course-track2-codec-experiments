#!/usr/bin/env python3
"""One-shot persistent queue, without replacing any existing experiment."""
import subprocess,shlex
from preflight_c6_30ms import ROOT,read,digest
def main():
    session='codec_c6_30ms_v1';run=ROOT/'runs/c6_30ms_b_s3407'
    assert (ROOT/'runs/c6_30ms_setup/PREFLIGHT_COMPLETE').exists()
    assert not (ROOT/'runs/c6_30ms_setup/LAUNCHED').exists()
    assert subprocess.run(['tmux','has-session','-t',session],capture_output=True).returncode!=0
    audit=read(ROOT/'C6_30MS_SETUP.audit');cell=audit['cells']['b_s3407']
    assert all(digest(ROOT/p)==h for p,h in audit['code_sha256'].items())
    assert digest(ROOT/cell['snapshot'])==cell['snapshot_sha256']
    assert not (run/'run_metadata.json').exists() and not (run/'checkpoints/last.pt').exists()
    cmd=shlex.join([str(ROOT/'.venv-codec/bin/python'),'-u','scripts/supervise_c6_30ms.py'])
    shell='cd '+shlex.quote(str(ROOT))+' && '+cmd+' >> '+shlex.quote(str(run/'supervisor.log'))+' 2>&1'
    subprocess.run(['tmux','new-session','-d','-s',session,'-n','b_s3407',shell],check=True)
    subprocess.run(['tmux','set-window-option','-t',session+':b_s3407','remain-on-exit','on'],check=True)
    (ROOT/'runs/c6_30ms_setup/LAUNCHED').touch()
    print('ONE_C6_30MS_QUEUE_LAUNCHED')
if __name__=='__main__':main()
