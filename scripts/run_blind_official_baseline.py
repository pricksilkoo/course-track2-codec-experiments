#!/usr/bin/env python3
"""Explicitly approved fixed original-course-baseline blind benchmark, CPU only."""
from pathlib import Path
import csv,datetime,fcntl,hashlib,json,math,os,subprocess
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/track2_blind_20261125'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    lock=(RUN/'.baseline.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if (RUN/'BASELINE_COMPLETE').exists():return
    plan=json.loads((ROOT/'BLIND_OFFICIAL_BASELINE_PLAN.audit').read_text());orig=json.loads((RUN/'frozen_plan.json').read_text());ck=Path(plan['checkpoint']);out=Path(plan['output_dir']);out.mkdir(exist_ok=True)
    assert sha(ck)==plan['checkpoint_sha256'] and sha(ROOT/'scripts/evaluate.py')==plan['scoring_code_sha256']
    for x in orig['files']:assert sha(Path(plan['reference_dir'])/x['file'])==x['sha256']
    env={**os.environ,'PYTHONPATH':str(ROOT/'src'),'PYTHONNOUSERSITE':'1','OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4','TORCH_HOME':plan['UTMOS_cache']}
    def command(*args):
        print('RUN',*map(str,args),flush=True);subprocess.run([str(ROOT/'.venv-codec/bin/python'),*map(str,args)],cwd=ROOT,env=env,check=True)
    command('scripts/encode.py','--checkpoint',ck,'--input-dir',plan['reference_dir'],'--output-dir',out/'bitstreams','--device','cpu')
    command('scripts/decode.py','--checkpoint',ck,'--bitstream-dir',out/'bitstreams','--output-dir',out/'reconstructed','--device','cpu')
    command('scripts/validate_submission.py','--input-dir',plan['reference_dir'],'--bitstream-dir',out/'bitstreams','--output-dir',out/'reconstructed')
    command('scripts/evaluate.py','--reference-dir',plan['reference_dir'],'--reconstructed-dir',out/'reconstructed','--output-dir',out/'metrics','--device','cpu')
    command('scripts/complexity.py','--checkpoint',ck,'--output',out/'complexity.json')
    import numpy as np,soundfile as sf
    evidence=[]
    assert len(list((out/'reconstructed').glob('*.wav')))==50 and len(list((out/'bitstreams').glob('*.bin')))==50
    for x in orig['files']:
        wav=out/'reconstructed'/x['file'];bits=out/'bitstreams'/Path(x['file']).with_suffix('.bin');audio,rate=sf.read(wav,always_2d=True)
        assert rate==16000 and audio.shape==(x['samples'],1) and np.isfinite(audio).all() and bits.stat().st_size==x['expected_bytes']
        assert json.loads(bits.with_suffix('.json').read_text())=={'sample_rate':16000,'num_samples':x['samples'],'frame_samples':160,'bits_per_frame':24,'bitrate_bps':2400}
        evidence.append({**x,'actual_bytes':bits.stat().st_size,'reconstructed_sha256':sha(wav),'bitstream_sha256':sha(bits)})
    rows=list(csv.DictReader((out/'metrics/per_file.csv').open()));s=json.loads((out/'metrics/summary.json').read_text());assert len(rows)==50 and s['files']==50 and not s['utmos_skipped']
    clip=lambda v:min(1,max(0,v));scores=[]
    for x in rows:
        v=[(float(x['PESQ'])-1)/3.5,float(x['ESTOI']),(float(x['SI_SNR'])+10)/40,(float(x['UTMOS'])-1)/4];assert all(map(math.isfinite,v));scores.append(25*sum(map(clip,v)))
    recomputed=sum(scores)/50;assert abs(recomputed-s['objective_quality_score'])<1e-10
    for key in ['PESQ','ESTOI','SI_SNR','UTMOS']:assert abs(sum(float(x[key]) for x in rows)/50-s['means'][key])<1e-10
    result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model':plan['model'],'checkpoint_sha256':plan['checkpoint_sha256'],'summary':s,'CSV_reaggregated_score':recomputed,'CSV_sha256':sha(out/'metrics/per_file.csv'),'summary_sha256':sha(out/'metrics/summary.json'),'files':50,'samples':sum(x['samples'] for x in evidence),'frames':sum(x['actual_bytes'] for x in evidence)//3,'actual_bytes':sum(x['actual_bytes'] for x in evidence),'complexity':json.loads((out/'complexity.json').read_text()),'fixed_baseline_reference_only_no_tuning':True,'per_file':evidence,'bitstream_tree_sha256':hashlib.sha256(''.join(x['file']+' '+x['bitstream_sha256']+'\n' for x in evidence).encode()).hexdigest(),'reconstructed_tree_sha256':hashlib.sha256(''.join(x['file']+' '+x['reconstructed_sha256']+'\n' for x in evidence).encode()).hexdigest()}
    (ROOT/'BLIND_OFFICIAL_BASELINE_RESULTS.audit').write_text(json.dumps(result,indent=2)+'\n');(RUN/'BASELINE_COMPLETE').touch();print('BASELINE_COMPLETE',json.dumps({k:v for k,v in result.items() if k not in ['per_file','complexity']}),flush=True)
if __name__=='__main__':main()
