#!/usr/bin/env python3
"""Create genuinely new scratch sources and frozen capacity-only2x2 evidence, once."""
from datetime import datetime,timezone
import copy,json,os,subprocess,sys
from pathlib import Path
import torch,yaml
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from ssp_codec.model import CourseCodec
from ssp_codec.config import load_config
from ssp_codec.adversarial import MultiResolutionSTFTDiscriminator
from ssp_codec.checkpoint_io import save_checkpoint_atomic
from run_champion7_experiment import record,digest
CELLS=('a_base','b_enc','c_dec','d_both')
SEED=20261110
STEPS=500000
ENDPOINTS=(250000,500000)
REFERENCE=ROOT/'runs/fast_b64_2s_v1/validation_200'
def read(p):return json.loads(Path(p).read_text())

def main():
    torch.set_num_threads(4)
    out=ROOT/'runs/champion10_setup';out.mkdir(exist_ok=True)
    assert not (ROOT/'CHAMPION10_SETUP.audit').exists()
    assert not any((ROOT/f'runs/champion10_{c}/run_metadata.json').exists() for c in CELLS)
    tests=(out/'cpu_tests.log').read_text();assert 'passed' in tests and 'FAILED' not in tests
    prior=read(ROOT/'CHAMPION9_SETUP.audit');final=read(ROOT/'CHAMPION9_RESULTS.audit')
    protected={ROOT/k:v for k,v in prior['unchanged_historical_sha256'].items()}
    for c,v in final['cells'].items():
        for k,w in v['weights'].items():
            filename=f'step_{int(k):08d}.pt' if k.isdigit() else k+'.pt'
            protected[ROOT/f'runs/champion9_{c}/checkpoints'/filename]=w['sha256']
        protected[ROOT/prior['cells'][c]['snapshot']]=prior['cells'][c]['snapshot_sha256']
    for name in ['CHAMPION9_SETUP.audit','CHAMPION9_LAUNCH.audit','CHAMPION9_RESULTS.audit']:
        protected[ROOT/name]=digest(ROOT/name)
    for p,h in protected.items():assert digest(p)==h
    for p,h in prior['data_hashes'].items():assert digest(ROOT/p)==h
    for name,h in prior['fixed200_sha256'].items():assert digest(REFERENCE/name)==h
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'trained':False,'global_step':0,
      'initialization':'fresh constructor codec/RVQ/D; no learned checkpoint or smoke; paired untrained tensors',
      'seed':SEED,'data_order_seed':SEED,'training_steps':STEPS,'endpoints':list(ENDPOINTS),
      'data_counts':prior['data_counts'],'data_hashes':prior['data_hashes'],'fixed200_sha256':prior['fixed200_sha256'],
      'unchanged_historical_sha256':{str(p.relative_to(ROOT)):h for p,h in protected.items()},
      'cpu_test_log_sha256':digest(out/'cpu_tests.log'),'cpu_test_summary':tests.strip().splitlines()[-1],
      'no_gpu_smoke_or_profile_per_user':True,'new_architecture_fullGAN_memory_peak_not_measured':True,
      'factor_design':'encoder narrow/wide X decoder hidden160/184, groups8 decoderTCN2 fixed',
      'cells':{},'matched_pairs':{}}
    sources={};models={}
    for c in CELLS:
        cfg=load_config(ROOT/f'configs/champion10/{c}.yaml');mc=cfg['model']
        assert cfg['seed']==cfg['training']['data_order_seed']==SEED
        assert mc['encoder_groups']==8 and mc['decoder_temporal_layers']==2 and mc['encoder_temporal_layers']==0
        assert mc['encoder_lookahead_frames']==2 and mc['decoder_lookahead_frames']==0
        assert mc['encoder_channels'][-1]==160 and mc['synthesis_initialization_seed']==SEED+200000
        torch.manual_seed(SEED);model=CourseCodec(**mc).eval();shared=[];new=[]
        if sources:
            src=sources['c_dec'] if c=='d_both' else sources['a_base']
            target=model.state_dict();common={k:v for k,v in src.items() if k in target and target[k].shape==v.shape}
            new=model.load_state_dict(common,strict=False).missing_keys;shared=sorted(common)
            assert all(k.startswith(('encoder.','decoder.')) for k in new),new
            if c=='d_both':
                encoder={k:v for k,v in sources['b_enc'].items() if k.startswith('encoder.')}
                model.load_state_dict(encoder,strict=False)
            assert all(torch.equal(model.state_dict()[k],v) for k,v in common.items() if not (c=='d_both' and k.startswith('encoder.')))
        sources[c]=copy.deepcopy(model.state_dict());models[c]=model
        torch.manual_seed(SEED+100000)
        disc=MultiResolutionSTFTDiscriminator(cfg['adversarial']['resolutions'],cfg['adversarial'].get('periods',()))
        assert model.quantizer.update_count.item()==0 and all(not bool(v) for k,v in model.quantizer.named_buffers() if k.endswith('initialized'))
        state={'global_step':0,'trained':False,'seed':SEED,'model_config':mc,'model':model.state_dict(),'discriminator':disc.state_dict(),
               'initialization_kind':'fresh constructor, paired untrained tensor sharing; never learned parent'}
        snap=out/f'step0_{c}.pt';assert not snap.exists();save_checkpoint_atomic(state,snap)
        if c==CELLS[0]:save_checkpoint_atomic(state,out/'source_step0.pt')
        run=ROOT/f'runs/champion10_{c}';run.mkdir(exist_ok=True);cfg['training']['output_dir']=str(run)
        (run/'effective_config.yaml').write_text(yaml.safe_dump(cfg,sort_keys=False))
        subprocess.run([str(ROOT/'.venv-codec/bin/python'),'scripts/complexity.py','--checkpoint',str(snap),'--output',str(run/'preflight_complexity.json')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
        cost=read(run/'preflight_complexity.json')
        assert cost['total_mflop_per_s']<=680 and cost['decoder_mflop_per_s']<=290 and cost['unclassified_mmac_per_s']==0
        assert cost['total_algorithmic_delay_ms']==30 and cost['algorithmic_lookahead_ms']==20 and cost['bitrate_bps']==2400
        lineage={'trained_initialization':False,'global_step':0,'seed':SEED,'discriminator_seed':SEED+100000,'GRU_Fourier_seed':SEED+200000,
          'snapshot':str(snap),'snapshot_sha256':digest(snap),'matched_source':str(out/'source_step0.pt'),'source_trained':False,
          'shared_keys':shared,'fresh_different_shape_keys':new,'composition':'D encoder from new B; D nonencoder from new C' if c=='d_both' else 'new A same-shape tensors shared'}
        (run/'lineage.json').write_text(json.dumps(lineage,indent=2)+'\n')
        report['cells'][c]={'groups':8,'decoder_tcn_layers':2,'encoder_channels':mc['encoder_channels'],'fourier_hidden':mc['fourier_hidden'],
          'snapshot':str(snap.relative_to(ROOT)),'snapshot_sha256':digest(snap),'effective_config':cfg,'config_sha256':digest(run/'effective_config.yaml'),
          'complexity':cost,'lineage':lineage}
        record(run,run.name,'planned',checkpoint=snap,note=f'CHAMPION10 scratch capacity2x2, encoder{mc["encoder_channels"]}, decoderhidden{mc["fourier_hidden"]}; groups8/decoderTCN2, encoderTCN0, 30msTOTAL. Newly untrained seed20261110, fresh initial optimizers;500kTOTAL, score ONLY250k/500k. CHAMPION10_PLAN.md.')
        print('PREPARED',c,cost['total_mflop_per_s'],cost['decoder_mflop_per_s'],cost['parameters'],flush=True)
    for x,y,factor in [('a_base','b_enc','encoder.'),('c_dec','d_both','encoder.'),('a_base','c_dec','decoder.'),('b_enc','d_both','decoder.')]:
        aa=sources[x];bb=sources[y];assert all(torch.equal(v,bb[k]) for k,v in aa.items() if not k.startswith(factor))
        report['matched_pairs'][y+'-'+x]={'only_changed_factor':factor,'all_other_tensors_identical':True}
    for x,y in [('a_base','c_dec'),('b_enc','d_both')]:
        torch.manual_seed(SEED);sample=torch.randn(1,1,1607)
        with torch.inference_mode():aa,ai,_=models[x](sample);bb,bi,_=models[y](sample)
        torch.testing.assert_close(aa,bb,rtol=0,atol=0);assert torch.equal(ai,bi)
        report['matched_pairs'][y+'-'+x]['zero_output_wider_decoder_step0_audio_codes_identical']=True
    d0=None
    for c,v in report['cells'].items():
        saved=torch.load(ROOT/v['snapshot'],map_location='cpu',weights_only=False)
        assert saved['global_step']==0 and saved['trained'] is False and 'optimizer' not in saved
        assert saved['model']['quantizer.update_count'].item()==0 and all(not bool(v) for k,v in saved['model'].items() if k.endswith('initialized'))
        if d0 is None:d0=saved['discriminator']
        else:assert all(torch.equal(v,d0[k]) for k,v in saved['discriminator'].items())
    assert all(digest(p)==h for p,h in protected.items())
    report['source_step0_sha256']=digest(out/'source_step0.pt')
    paths=['src/ssp_codec/model.py','src/ssp_codec/champion_analysis.py','src/ssp_codec/champion_synthesis.py','scripts/complexity.py','scripts/train.py','src/ssp_codec/checkpoint_io.py',
           'scripts/preflight_champion10.py','scripts/run_champion10_experiment.py','scripts/supervise_champion10.py','scripts/launch_champion10.py','scripts/capture_champion10_launch.py','tests/test_champion10.py']
    report['code_sha256']={k:digest(ROOT/k) for k in paths}
    (ROOT/'CHAMPION10_SETUP.audit').write_text(json.dumps(report,indent=2)+'\n')
    (out/'PREFLIGHT_COMPLETE').touch();print('PREFLIGHT_COMPLETE',flush=True)
if __name__=='__main__':main()
