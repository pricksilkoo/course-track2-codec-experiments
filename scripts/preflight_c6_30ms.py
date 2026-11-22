#!/usr/bin/env python3
"""Once-only untrained C6B initialization with the future-tap4 removed."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,copy,subprocess
import torch,yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from ssp_codec.config import load_config
from ssp_codec.model import CourseCodec
from ssp_codec.checkpoint_io import save_checkpoint_atomic
from run_champion7_experiment import digest,record
CELLS=('b_s3407',)
STEPS=500000
ENDPOINTS=(500000,)
REFERENCE=ROOT/'runs/fast_b64_2s_v1/validation_200'
def read(p):return json.loads(Path(p).read_text())

def main():
    torch.set_num_threads(4)
    out=ROOT/'runs/c6_30ms_setup';run=ROOT/'runs/c6_30ms_b_s3407'
    assert not (ROOT/'C6_30MS_SETUP.audit').exists() and not (out/'step0.pt').exists()
    assert not (run/'run_metadata.json').exists() and not (run/'checkpoints/last.pt').exists()
    log=(out/'cpu_tests.log').read_text();assert 'passed' in log and 'FAILED' not in log
    prior=read(ROOT/'CHAMPION6_SETUP.audit');cell=prior['cells']['b_s3407_fourier_gru']
    source=ROOT/'runs/champion6_setup/step0_b_s3407_fourier_gru.pt'
    assert digest(source)==cell['snapshot_sha256']
    original=torch.load(source,map_location='cpu',weights_only=False)
    assert original['global_step']==0 and original.get('trained') is False
    cfg=load_config(ROOT/'configs/c6_30ms/b_s3407.yaml')
    old=load_config(ROOT/'configs/champion6/b_s3407_fourier_gru.yaml')
    expected=copy.deepcopy(old);expected['model']['encoder_lookahead_frames']=2
    expected['training'].update(output_dir='runs/c6_30ms_b_s3407',checkpoint_keep_last=20,recovery_checkpoint_interval_steps=1000)
    assert cfg==expected and original['model_config']==old['model']
    assert original['model']['quantizer.update_count'].item()==0
    assert all(not bool(v) for k,v in original['model'].items() if k.endswith('initialized'))
    src=copy.deepcopy(original['model'])
    key='analysis_temporal.lookahead.depthwise.weight'
    assert src[key].shape==(160,1,4)
    src[key]=src[key][...,:3].clone()
    model=CourseCodec(**cfg['model']).eval();model.load_state_dict(src,strict=True)
    assert all(torch.equal(v,original['model'][k]) for k,v in model.state_dict().items() if k!=key)
    old_model=CourseCodec(**old['model']).eval();old_model.load_state_dict(original['model'],strict=True)
    torch.manual_seed(3407);x=torch.randn(1,1,1607)
    assert model.analysis_temporal.lookahead.project.weight.count_nonzero().item()==0
    assert model.analysis_temporal.lookahead.project.bias.count_nonzero().item()==0
    with torch.inference_mode():
        padded,_=model.pad_to_frame(x)
        old_latent=old_model.analysis_gru(old_model.analysis_temporal(old_model.latent_norm(old_model.encoder(padded))))
        new_latent=model.analysis_gru(model.analysis_temporal(model.latent_norm(model.encoder(padded))))
        torch.testing.assert_close(old_latent,new_latent,atol=0,rtol=0)
        aa,ai,_=old_model(x);bb,bi,_=model(x)
    torch.testing.assert_close(aa,bb,atol=0,rtol=0);assert torch.equal(ai,bi)
    state=copy.deepcopy(original);state['model_config']=cfg['model'];state['model']=model.state_dict()
    state['global_step']=0;state['trained']=False
    for k in ['optimizer','discriminator_optimizer']:state.pop(k,None)
    assert 'discriminator' in state
    snap=out/'step0.pt';save_checkpoint_atomic(state,snap)
    run.mkdir(exist_ok=True);cfg['training']['output_dir']=str(run)
    (run/'effective_config.yaml').write_text(yaml.safe_dump(cfg,sort_keys=False))
    subprocess.run([str(ROOT/'.venv-codec/bin/python'),'scripts/complexity.py','--checkpoint',str(snap),
        '--output',str(run/'preflight_complexity.json')],check=True,cwd=ROOT,stdout=subprocess.DEVNULL)
    cost=read(run/'preflight_complexity.json')
    assert cost['algorithmic_lookahead_ms']==20 and cost['total_mflop_per_s']<=700
    assert cost['decoder_mflop_per_s']<=300 and cost['unclassified_mmac_per_s']==0
    assert abs(cost['total_mflop_per_s']-666.2752)<1e-7 and cost['parameters']==1867904
    latency={'frame_collection_ms':10,'lookahead_ms':20,'additional_decoder_future_buffer_ms':0,
             'total_delay_ms':30,'dependency_boundary_samples':480,
             'proof':'forced nonzero future branch + prefix and real-byte CPU tests'}
    (run/'latency_audit.json').write_text(json.dumps(latency,indent=2)+'\n')
    protected=read(ROOT/'CHAMPION12_SETUP.audit')['unchanged_historical_sha256']
    assert all(digest(ROOT/p)==h for p,h in protected.items())
    for p,h in prior['data_hashes'].items():assert digest(ROOT/p)==h
    for p,h in prior['fixed200_sha256'].items():assert digest(REFERENCE/p)==h
    lineage={'trained_initialization':False,'global_step':0,'original_untrained_source':str(source),
     'source_sha256':cell['snapshot_sha256'],'snapshot':str(snap),'snapshot_sha256':digest(snap),
     'sole_changed_tensor':key,'change':'first3 taps of original4; no rescale',
     'all_other_tensors_exact':True,'discriminator_exact':True,'paired_initial_audio_codes_exact':True,
     'fresh_optimizers':True,'seed':3407,'data_order_seed':3407}
    (run/'lineage.json').write_text(json.dumps(lineage,indent=2)+'\n')
    paths=['C6_30MS_PLAN.md','configs/c6_30ms/b_s3407.yaml','scripts/preflight_c6_30ms.py',
     'scripts/run_c6_30ms_experiment.py','scripts/supervise_c6_30ms.py','scripts/launch_c6_30ms.py',
     'tests/test_c6_30ms.py','src/ssp_codec/model.py','src/ssp_codec/champion_synthesis.py',
     'scripts/train.py','scripts/complexity.py','scripts/diagnose_rvq.py','scripts/run_champion7_experiment.py',
     'scripts/supervise_champion7.py','scripts/record_experiment.py','src/ssp_codec/checkpoint_io.py']
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'seed':3407,'training_steps':STEPS,
     'primary_endpoint':STEPS,'scientific_model_change_only':'encoder_lookahead_frames3to2',
     'operational_IO_only_changes':{'checkpoint_keep_last':20,'recovery_checkpoint_interval_steps':1000},
     'trained':False,'global_step':0,'lineage':lineage,'latency':latency,
     'cpu_tests':log.strip().splitlines()[-1],'cpu_test_log_sha256':digest(out/'cpu_tests.log'),
     'no_GPU_smoke_or_profile':True,'new_fullGAN_peak_not_measured':True,
     'data_hashes':prior['data_hashes'],'fixed200_sha256':prior['fixed200_sha256'],
     'unchanged_historical_sha256':protected,'code_sha256':{p:digest(ROOT/p) for p in paths},
     'cells':{'b_s3407':{'snapshot':str(snap.relative_to(ROOT)),'snapshot_sha256':digest(snap),
       'effective_config':cfg,'config_sha256':digest(run/'effective_config.yaml'),'complexity':cost,
       'encoder_channels':cfg['model']['encoder_channels'],'fourier_hidden':160}}}
    record(run,run.name,'planned',checkpoint=snap,note='User-approved C6B30ms single seed3407 scratch repeat; only lookahead3to2; original UNTRAINED C6B initialization exact except removed future tap. 500k sole endpoint, no learned parent. C6_30MS_PLAN.md.')
    (ROOT/'C6_30MS_SETUP.audit').write_text(json.dumps(report,indent=2)+'\n')
    (out/'PREFLIGHT_COMPLETE').touch()
    print('PREFLIGHT_COMPLETE',cost['total_mflop_per_s'],cost['decoder_mflop_per_s'],cost['parameters'],flush=True)
if __name__=='__main__':main()
