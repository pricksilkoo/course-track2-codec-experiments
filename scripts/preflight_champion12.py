#!/usr/bin/env python3
"""Create four frozen genuinely untrained factorial sources exactly once."""
from datetime import datetime,timezone
import copy,json,subprocess,sys,re
from pathlib import Path
import torch,yaml
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from ssp_codec.model import CourseCodec
from ssp_codec.config import load_config
from ssp_codec.adversarial import MultiResolutionSTFTDiscriminator
from ssp_codec.checkpoint_io import save_checkpoint_atomic
from run_champion7_experiment import record,digest
CELLS=('a_control','b_norm','c_front','d_both')
GPU_ASSIGNMENTS=dict(zip(CELLS,range(4)))
SEED=20261121
STEPS=500000
ENDPOINTS=(250000,500000)
REFERENCE=ROOT/'runs/fast_b64_2s_v1/validation_200'
def read(p):return json.loads(Path(p).read_text())

def main():
    torch.set_num_threads(4)
    out=ROOT/'runs/champion12_setup'
    assert out.is_dir() and not (ROOT/'CHAMPION12_SETUP.audit').exists()
    assert not any((ROOT/f'runs/champion12_{c}/run_metadata.json').exists() for c in CELLS)
    assert not any((out/f'step0_{c}.pt').exists() for c in CELLS)
    tests=(out/'cpu_tests.log').read_text()
    assert 'passed' in tests and 'FAILED' not in tests
    prior=read(ROOT/'CHAMPION11_SETUP.audit')
    protected={ROOT/k:v for k,v in prior['unchanged_historical_sha256'].items()}
    for c,v in prior['cells'].items():
        protected[ROOT/v['snapshot']]=v['snapshot_sha256']
        for name in [*(f'step_{s:08d}.pt' for s in range(25000,STEPS+1,25000)),'best.pt','last.pt']:
            p=ROOT/f'runs/champion11_{c}/checkpoints'/name
            protected[p]=digest(p)
    for name in ['CHAMPION11_PLAN.md','CHAMPION11_SETUP.audit','CHAMPION11_RESULTS.md','CHAMPION11_RESULTS.audit']:
        protected[ROOT/name]=digest(ROOT/name)
    assert all(digest(p)==h for p,h in protected.items())
    assert all(digest(ROOT/p)==h for p,h in prior['data_hashes'].items())
    assert all(digest(REFERENCE/p)==h for p,h in prior['fixed200_sha256'].items())
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'trained':False,'global_step':0,
      'initialization':'fresh codec/RVQ/D; identical non-varied tensors; C reverses A untrained stage projection/codebook order',
      'seed':SEED,'data_order_seed':SEED,'training_steps':STEPS,'endpoints':list(ENDPOINTS),
      'primary_endpoint':STEPS,'data_counts':prior['data_counts'],'data_hashes':prior['data_hashes'],
      'fixed200_sha256':prior['fixed200_sha256'],
      'unchanged_historical_sha256':{str(p.relative_to(ROOT)):h for p,h in protected.items()},
      'initial_cpu_environment_misroute_log_sha256':digest(out/'cpu_tests_environment_misroute.log'),
      'initial_cpu_check_note':'first invocation imported old editable installation; corrected explicit source path and pytest pythonpath; no GPU or optimization was involved',
      'float32_audio_assertion_log_sha256':digest(out/'cpu_tests_float32_roundoff.log'),
      'float32_audio_assertion_note':'STE versus direct lookup addition roundoff <6e-8; codes/bytes exact, audio checked with established 1e-6 absolute tolerance; no model change',
      'cpu_test_log_sha256':digest(out/'cpu_tests.log'),'cpu_test_summary':tests.strip().splitlines()[-1],
      'no_gpu_smoke_or_profile_per_user':True,'fullGAN_memory_peak_not_measured':True,
      'factor_design':'post-GRU nonaffine frame LN x projected RVQ dimensions 48/64/80 versus 80/64/48',
      'cells':{},'matched_pairs':{}}
    states={};models={}
    for c in CELLS:
        cfg=load_config(ROOT/f'configs/champion12/{c}.yaml');mc=cfg['model']
        assert cfg['seed']==cfg['training']['data_order_seed']==SEED
        assert mc['encoder_groups']==8 and mc['encoder_channels']==[8,24,40,80,160]
        assert mc['encoder_temporal_layers']==0 and mc['decoder_temporal_layers']==2
        assert mc['encoder_lookahead_frames']==2 and mc['decoder_lookahead_frames']==0
        assert mc['fourier_hidden']==184 and mc['synthesis_initialization_seed']==SEED+200000
        torch.manual_seed(SEED);model=CourseCodec(**mc).eval()
        if states:
            base=states['a_control']
            if c in ('c_front','d_both'):
                remapped={}
                for k,v in base.items():
                    m=re.match(r'(quantizer\.(?:input_projections|output_projections|stages)\.)([012])(\..*)',k)
                    key=m[1]+str(2-int(m[2]))+m[3] if m else k
                    remapped[key]=v
                model.load_state_dict(remapped,strict=True)
            else:model.load_state_dict(base,strict=True)
        states[c]=copy.deepcopy(model.state_dict());models[c]=model
        torch.manual_seed(SEED+100000)
        disc=MultiResolutionSTFTDiscriminator(cfg['adversarial']['resolutions'],cfg['adversarial'].get('periods',()))
        assert model.quantizer.update_count.item()==0
        assert all(not bool(v) for k,v in model.quantizer.named_buffers() if k.endswith('initialized'))
        state={'global_step':0,'trained':False,'seed':SEED,'model_config':mc,
            'model':model.state_dict(),'discriminator':disc.state_dict(),
            'initialization_kind':'fresh constructor; paired untrained projection order; never learned parent'}
        snap=out/f'step0_{c}.pt';save_checkpoint_atomic(state,snap)
        if c==CELLS[0]:save_checkpoint_atomic(state,out/'source_step0.pt')
        run=ROOT/f'runs/champion12_{c}';run.mkdir(exist_ok=True);cfg['training']['output_dir']=str(run)
        (run/'effective_config.yaml').write_text(yaml.safe_dump(cfg,sort_keys=False))
        subprocess.run([str(ROOT/'.venv-codec/bin/python'),'scripts/complexity.py','--checkpoint',str(snap),
            '--output',str(run/'preflight_complexity.json')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
        cost=read(run/'preflight_complexity.json')
        assert cost['total_mflop_per_s']<=700 and cost['decoder_mflop_per_s']<=300
        assert cost['unclassified_mmac_per_s']==0 and cost['total_algorithmic_delay_ms']==30
        assert cost['algorithmic_lookahead_ms']==20 and cost['bitrate_bps']==2400
        lineage={'trained_initialization':False,'global_step':0,'seed':SEED,'discriminator_seed':SEED+100000,
          'GRU_Fourier_seed':SEED+200000,'snapshot':str(snap),'snapshot_sha256':digest(snap),
          'matched_source':str(out/'source_step0.pt'),'source_trained':False,'initial_optimizers':'fresh; no saved optimizer state',
          'composition':'A fresh; B tensor-identical to A; C/D reverse A untrained stage2/1/0, all nonquantizer tensors exact'}
        (run/'lineage.json').write_text(json.dumps(lineage,indent=2)+'\n')
        report['cells'][c]={'encoder_channels':mc['encoder_channels'],'fourier_hidden':mc['fourier_hidden'],
          'snapshot':str(snap.relative_to(ROOT)),'snapshot_sha256':digest(snap),'effective_config':cfg,
          'config_sha256':digest(run/'effective_config.yaml'),'complexity':cost,'lineage':lineage}
        record(run,run.name,'planned',checkpoint=snap,note=f'CHAMPION12 scratch 2x2, postGRU norm={mc["quantizer_input_normalization"]}, dims={mc["projected_stage_dims"]}; fixed D backbone, fresh seed20261121, 500k primary, 250k diagnostic; CHAMPION12_PLAN.md.')
        print('PREPARED',c,cost['total_mflop_per_s'],cost['decoder_mflop_per_s'],cost['parameters'],flush=True)
    for x,y in [('a_control','b_norm'),('c_front','d_both')]:
        assert all(torch.equal(v,states[y][k]) for k,v in states[x].items())
        report['matched_pairs'][y+'-'+x]={'all_tensors_identical':True,'only_change':'stateless frame-local post-GRU LN'}
    for x,y in [('a_control','c_front'),('b_norm','d_both')]:
        assert all(torch.equal(v,states[y][k]) for k,v in states[x].items() if not k.startswith('quantizer.'))
        for i in range(3):
            for attr in ['input_projections','output_projections','stages']:
                prefix=f'quantizer.{attr}.{i}.'
                for k,v in states[x].items():
                    if k.startswith(prefix):
                        target=f'quantizer.{attr}.{2-i}.'+k[len(prefix):]
                        assert torch.equal(v,states[y][target])
        report['matched_pairs'][y+'-'+x]={'all_nonquantizer_tensors_identical':True,'stage_initialization_permutation':[2,1,0],
            'same_untrained_projection_row_set':True}
    d0=None
    for c,v in report['cells'].items():
        saved=torch.load(ROOT/v['snapshot'],map_location='cpu',weights_only=False)
        assert saved['global_step']==0 and saved['trained'] is False and 'optimizer' not in saved
        assert saved['model']['quantizer.update_count'].item()==0
        assert all(not bool(v) for k,v in saved['model'].items() if k.endswith('initialized'))
        if d0 is None:d0=saved['discriminator']
        else:assert all(torch.equal(v,d0[k]) for k,v in saved['discriminator'].items())
    assert all(digest(p)==h for p,h in protected.items())
    report['source_step0_sha256']=digest(out/'source_step0.pt')
    paths=['src/ssp_codec/model.py','src/ssp_codec/champion_analysis.py','src/ssp_codec/champion_synthesis.py',
      'pyproject.toml','scripts/complexity.py','scripts/diagnose_rvq.py','scripts/train.py','src/ssp_codec/checkpoint_io.py',
      'scripts/preflight_champion12.py','scripts/run_champion12_experiment.py','scripts/supervise_champion12.py',
      'scripts/launch_champion12.py','scripts/capture_champion12_launch.py','scripts/record_experiment.py','scripts/run_champion7_experiment.py',
      'scripts/supervise_champion7.py','tests/test_champion12.py','CHAMPION12_PLAN.md',
      *[f'configs/champion12/{c}.yaml' for c in CELLS]]
    report['code_sha256']={k:digest(ROOT/k) for k in paths}
    (ROOT/'CHAMPION12_SETUP.audit').write_text(json.dumps(report,indent=2)+'\n')
    (out/'PREFLIGHT_COMPLETE').touch();print('PREFLIGHT_COMPLETE',flush=True)
if __name__=='__main__':main()
