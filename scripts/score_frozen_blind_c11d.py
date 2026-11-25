#!/usr/bin/env python3
"""User-approved once-only quality scoring of an already frozen blind reconstruction."""
from pathlib import Path
import csv, datetime, fcntl, hashlib, json, math, os, subprocess
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/track2_blind_20261125'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    lock=(RUN/'.score.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if (RUN/'SCORING_COMPLETE').exists():return
    plan=json.loads((ROOT/'BLIND_C11D_SCORE_PLAN.audit').read_text())
    assert sha(RUN/'self_check.audit.json')==plan['self_check_audit_sha256']
    checked=json.loads((RUN/'self_check.audit.json').read_text())
    assert sha(checked['checkpoint'])==plan['checkpoint_sha256']
    for x in checked['per_file']:
        assert sha(Path(plan['reference_dir'])/x['file'])==x['sha256']
        assert sha(Path(plan['reconstructed_dir'])/x['file'])==x['reconstructed_sha256']
    env={**os.environ,'PYTHONPATH':str(ROOT/'src'),'PYTHONNOUSERSITE':'1','OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4','TORCH_HOME':plan['torch_home']}
    summary=Path(plan['output_dir'])/'summary.json'
    if not summary.exists():
        subprocess.run([str(ROOT/'.venv-codec/bin/python'),'scripts/evaluate.py','--reference-dir',plan['reference_dir'],'--reconstructed-dir',plan['reconstructed_dir'],'--output-dir',plan['output_dir'],'--device','cpu'],cwd=ROOT,env=env,check=True)
    s=json.loads(summary.read_text());assert s['files']==50 and not s['utmos_skipped']
    rows=list(csv.DictReader(summary.with_name('per_file.csv').open()));assert len(rows)==50
    keys=['PESQ','ESTOI','SI_SNR','UTMOS'];means={k:sum(float(x[k]) for x in rows)/len(rows) for k in keys}
    comps=[]
    for x in rows:
        values=[(float(x['PESQ'])-1)/3.5,float(x['ESTOI']),(float(x['SI_SNR'])+10)/40,(float(x['UTMOS'])-1)/4]
        assert all(map(math.isfinite,values));comps.append([min(1,max(0,v)) for v in values])
    normalized={k:sum(x[i] for x in comps)/50 for i,k in enumerate(keys)};score=25*sum(normalized.values())
    assert abs(score-s['objective_quality_score'])<1e-10 and all(abs(means[k]-s['means'][k])<1e-10 for k in keys)
    result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':plan['scope'],'model':'C11D fixed500k','checkpoint_sha256':plan['checkpoint_sha256'],'summary':s,'CSV_reaggregated_score':score,'normalized_components':normalized,'summary_sha256':sha(summary),'CSV_sha256':sha(summary.with_name('per_file.csv')),'blind_model_selection_performed':False,'no_checkpoint_or_reconstruction_changed':True,'official_teacher_score':False}
    (ROOT/'BLIND_C11D_SCORE_RESULTS.audit').write_text(json.dumps(result,indent=2)+'\n')
    (RUN/'SCORING_COMPLETE').touch();print('SCORING_COMPLETE',json.dumps(result),flush=True)
if __name__=='__main__':main()
