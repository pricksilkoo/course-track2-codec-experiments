#!/usr/bin/env python3
"""User-confirmed fixed-model comparison; no tuning, extra weights or auto-retry."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv,datetime,fcntl,hashlib,json,math,os,subprocess,time,traceback
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'runs/track2_blind_20261125'
PLAN=ROOT/'BLIND_CONFIRMED_COMPARISON_PLAN.audit'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,data):
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');tmp.replace(p)
def run_one(m,plan,original):
    out=Path(plan['output_root'])/m['label'];out.mkdir(parents=True,exist_ok=True)
    with (out/'.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if (out/'COMPLETE').exists():return json.loads((out/'audit.json').read_text())
        m=dict(m);ck=Path(m['checkpoint'])
        if m['wait_for_original_pipeline_complete']:
            r=Path(m['run'])
            while not (r/'PIPELINE_COMPLETE').exists():
                if (r/'pipeline_phase.json').exists() and json.loads((r/'pipeline_phase.json').read_text()).get('phase')=='failed':raise RuntimeError('original C12C pipeline failed; no retry or alternate checkpoint')
                write(out/'status.json',{'status':'waiting_for_original_500k_pipeline','updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});time.sleep(30)
            selected=json.loads((r/'selection.json').read_text())['selected'];assert selected['step']==500000 and Path(selected['checkpoint']).resolve()==ck.resolve()
            m['checkpoint_sha256']=selected['checkpoint_sha256'];m['public200dev_score']=selected['summary']['objective_quality_score'];write(out/'resolved_fixed_checkpoint.json',m)
        assert sha(ck)==m['checkpoint_sha256']
        assert sha(ROOT/'scripts/evaluate.py')==plan['quality_scoring_script_sha256']
        write(out/'status.json',{'status':'running','checkpoint':m,'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
        env={**os.environ,'PYTHONPATH':str(ROOT/'src'),'PYTHONNOUSERSITE':'1','OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4','TORCH_HOME':str(ROOT/'runs/c6_30ms_setup/torch-cache')}
        with (out/'pipeline.log').open('a',buffering=1) as log:
            def command(*args):
                log.write('RUN '+' '.join(map(str,args))+'\n');log.flush();subprocess.run([str(ROOT/'.venv-codec/bin/python'),*map(str,args)],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
            command('scripts/encode.py','--checkpoint',ck,'--input-dir',original['reference_dir'],'--output-dir',out/'bitstreams','--device','cpu')
            command('scripts/decode.py','--checkpoint',ck,'--bitstream-dir',out/'bitstreams','--output-dir',out/'reconstructed','--device','cpu')
            command('scripts/validate_submission.py','--input-dir',original['reference_dir'],'--bitstream-dir',out/'bitstreams','--output-dir',out/'reconstructed')
            command('scripts/evaluate.py','--reference-dir',original['reference_dir'],'--reconstructed-dir',out/'reconstructed','--output-dir',out/'metrics','--device','cpu')
            command('scripts/complexity.py','--checkpoint',ck,'--output',out/'complexity.json')
        import numpy as np,soundfile as sf
        evidence=[];expected={x['file'] for x in original['files']}
        assert {x.name for x in (out/'reconstructed').glob('*.wav')}==expected
        assert {x.stem for x in (out/'bitstreams').glob('*.bin')}=={Path(x).stem for x in expected}
        for x in original['files']:
            f=out/'reconstructed'/x['file'];bits=out/'bitstreams'/Path(x['file']).with_suffix('.bin');y,sr=sf.read(f,always_2d=True)
            assert sr==16000 and y.shape==(x['samples'],1) and np.isfinite(y).all() and bits.stat().st_size==x['expected_bytes']
            assert json.loads(bits.with_suffix('.json').read_text())=={'sample_rate':16000,'num_samples':x['samples'],'frame_samples':160,'bits_per_frame':24,'bitrate_bps':2400}
            evidence.append({**x,'actual_bytes':bits.stat().st_size,'bitstream_sha256':sha(bits),'reconstructed_sha256':sha(f)})
        summary=json.loads((out/'metrics/summary.json').read_text());rows=list(csv.DictReader((out/'metrics/per_file.csv').open()));assert len(rows)==50 and summary['files']==50 and not summary['utmos_skipped']
        clip=lambda v:min(1,max(0,v));points=[]
        for x in rows:
            v=[(float(x['PESQ'])-1)/3.5,float(x['ESTOI']),(float(x['SI_SNR'])+10)/40,(float(x['UTMOS'])-1)/4];assert all(map(math.isfinite,v));points.append([25*clip(z) for z in v])
        score=sum(sum(x) for x in points)/50;assert abs(score-summary['objective_quality_score'])<1e-10
        for k in ['PESQ','ESTOI','SI_SNR','UTMOS']:assert abs(sum(float(x[k]) for x in rows)/50-summary['means'][k])<1e-10
        cost=json.loads((out/'complexity.json').read_text());assert cost['total_mflop_per_s']<=700 and cost['decoder_mflop_per_s']<=300
        result={'model':m,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'summary':summary,'CSV_reaggregated_score':score,'CSV_sha256':sha(out/'metrics/per_file.csv'),'files':50,'samples':sum(x['samples'] for x in evidence),'frames':sum(x['actual_bytes'] for x in evidence)//3,'actual_bytes':sum(x['actual_bytes'] for x in evidence),'complexity':cost,'output_dir':str(out),'per_file':evidence,'no_model_or_submission_change':True}
        assert result['samples']==4204525 and result['frames']==26300 and result['actual_bytes']==78900
        write(out/'audit.json',result);(out/'COMPLETE').touch();write(out/'status.json',{'status':'complete','score':score});return result

def publish(done,plan):
    entries=[]
    for path,label,delay in [('BLIND_OFFICIAL_BASELINE_RESULTS.audit','official_baseline',10),('BLIND_C11D_SCORE_RESULTS.audit','c11d',30)]:
        a=json.loads((ROOT/path).read_text());entries.append({'label':label,'total_delay_ms':delay,'summary':a['summary'],'reused':True})
    entries += [{'label':a['model']['label'],'total_delay_ms':a['model']['total_delay_ms'],'summary':a['summary'],'reused':False,'checkpoint_sha256':a['model']['checkpoint_sha256'],'output_dir':a['output_dir']} for a in done]
    pending=[m['label'] for m in plan['models'] if m['label'] not in {a['model']['label'] for a in done}]
    write(ROOT/'BLIND_CONFIRMED_COMPARISON_RESULTS.audit',{'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan_sha256':sha(PLAN),'complete':not pending,'pending':pending,'entries':entries,'scope':'fixed user-confirmed research contrasts only; no checkpoint search/tuning or submission replacement','C6B_40ms_not_course_delay_compliant':True})
    lines=['# 用户确认的固定模型盲测对照','', '仅40ms历史模型C6B，其余新测为30ms固定500k；官方baseline/C11D复用审计结果。提交候选不据本表改变。C6B不符合总30ms限制；自测分非教师官方成绩。','', '| 模型 | 总延迟ms | 总分 | PESQ | ESTOI | SI-SNR dB | UTMOS |','|---|---:|---:|---:|---:|---:|---:|']
    for e in entries:
        s=e['summary'];v=s['means'];lines.append(f"| {e['label']} | {e['total_delay_ms']} | {s['objective_quality_score']:.6f} | {v['PESQ']:.6f} | {v['ESTOI']:.6f} | {v['SI_SNR']:.6f} | {v['UTMOS']:.6f} |")
    lines += ['', '待完成：'+(', '.join(pending) if pending else '无'),'', '输出根目录：`'+plan['output_root']+'`。每模型含bitstreams、reconstructed、metrics/per_file.csv、summary.json、复杂度、逐文件SHA审计。逐文件原长/有限音频/元数据/3ceil(samples/160)字节及CSV独立复算通过后才标记完成。']
    (ROOT/'BLIND_CONFIRMED_COMPARISON_RESULTS.md').write_text('\n'.join(lines)+'\n')

def main():
    lock=(BASE/'.confirmed_comparison.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    plan=json.loads(PLAN.read_text());original=json.loads((BASE/'frozen_plan.json').read_text());assert sha(BASE/'frozen_plan.json')==plan['source_frozen_plan_sha256']
    for x in original['files']:assert sha(Path(original['reference_dir'])/x['file'])==x['sha256']
    done=[];publish(done,plan)
    try:
        # Two independent CPU workers, four threads each; no GPU/disk resource query.
        with ThreadPoolExecutor(max_workers=2) as pool:
            jobs={pool.submit(run_one,m,plan,original):m for m in plan['models']}
            for future in as_completed(jobs):
                result=future.result();done.append(result);publish(done,plan);print('MODEL_COMPLETE',result['model']['label'],result['summary'],flush=True)
        (BASE/'CONFIRMED_COMPARISON_COMPLETE').touch();print('BATCH_COMPLETE',flush=True)
    except Exception:
        traceback.print_exc();write(BASE/'confirmed_comparison_failure.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':traceback.format_exc(),'no_automatic_retry':True});raise
if __name__=='__main__':main()
