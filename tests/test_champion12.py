from pathlib import Path
import pytest
import torch
from ssp_codec.model import CourseCodec
from ssp_codec.config import load_config
from ssp_codec.io import read_bitstream, write_bitstream

ROOT=Path(__file__).resolve().parents[1]
CELLS=('a_control','b_norm','c_front','d_both')

@pytest.mark.parametrize('cell',CELLS)
def test_quantizer_interface_real_bytes_and_future_boundary(cell,tmp_path):
    cfg=load_config(ROOT/f'configs/champion12/{cell}.yaml')
    model=CourseCodec(**cfg['model'])
    # CPU-only disposable model initialization: formal step0 never comes from this test.
    with torch.no_grad(): model(torch.randn(1,1,6400))
    model.eval()
    x=torch.randn(1,1,1607)
    with torch.no_grad():
        y,codes,loss=model(x)
        assert y.shape==x.shape and codes.shape==(1,11,3)
        assert torch.isfinite(y).all() and torch.isfinite(loss)
        assert torch.equal(codes,model.encode(x))
        path=tmp_path/'payload.bin';write_bitstream(path,codes[0],1607)
        recovered,meta=read_bitstream(path)
        assert path.stat().st_size==33 and meta['bits_per_frame']==24
        # STE reconstruction and direct lookup differ by float32 addition order.
        # Codes/serialized bytes stay exact; audio uses the established 1e-6 tolerance.
        torch.testing.assert_close(y,model.decode(recovered[None],length=1607),rtol=1e-5,atol=1e-6)
        look=model.analysis_temporal.lookahead
        look.depthwise.weight.zero_();look.depthwise.weight[...,-1]=1
        look.project.weight.zero_();look.project.bias.zero_()
        for c in range(160):look.project.weight[c,c,0]=1
        def analysis(z):
            return model.quantizer_input_norm(model.analysis_gru(model.analysis_temporal(model.latent_norm(model.encoder(z)))))
        future=x.clone();future[...,480:]+=10
        allowed=x.clone();allowed[...,320:480]+=10
        z=analysis(x)
        torch.testing.assert_close(z[:,:1],analysis(future)[:,:1],rtol=0,atol=0)
        torch.testing.assert_close(z[:,:1],analysis(x[...,:480])[:,:1],rtol=1e-5,atol=1e-6)
        assert not torch.allclose(z[:,:1],analysis(allowed)[:,:1])
        torch.testing.assert_close(model(x)[0][...,:160],model(future)[0][...,:160],rtol=0,atol=0)
        changed=codes.clone();changed[:,1:]=(changed[:,1:]+1)%256
        torch.testing.assert_close(model.decode(codes)[...,:160],model.decode(changed)[...,:160],rtol=0,atol=0)
        assert model.total_algorithmic_delay_ms==30

@pytest.mark.parametrize('cell',CELLS)
def test_finite_gradients_and_frame_local_normalization(cell):
    cfg=load_config(ROOT/f'configs/champion12/{cell}.yaml')
    model=CourseCodec(**cfg['model']).train()
    x=torch.randn(1,1,1600,requires_grad=True)
    y,_,loss=model(x);(y.square().mean()+loss).backward()
    assert torch.isfinite(x.grad).all() and x.grad.abs().sum()>0
    assert all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters())
    if 'norm' in cell or cell=='d_both':
        z=torch.randn(2,9,160);q=model.quantizer_input_norm(z)
        torch.testing.assert_close(q.mean(-1),torch.zeros(2,9),atol=1e-6,rtol=0)
        changed=z.clone();changed[:,1:]+=100
        torch.testing.assert_close(q[:,:1],model.quantizer_input_norm(changed)[:,:1],rtol=0,atol=0)

def test_disabled_normalization_old_config_state_and_audio_exact():
    cfg=load_config(ROOT/'configs/champion11/d_both.yaml')['model']
    torch.manual_seed(37);old=CourseCodec(**cfg).eval()
    torch.manual_seed(37);new=CourseCodec(**{**cfg,'quantizer_input_normalization':'none'}).eval()
    new.load_state_dict(old.state_dict(),strict=True)
    x=torch.randn(1,1,1607)
    with torch.no_grad():
        a,ai,_=old(x);b,bi,_=new(x)
    torch.testing.assert_close(a,b,rtol=0,atol=0);assert torch.equal(ai,bi)
    with pytest.raises(ValueError,match='quantizer input normalization'):
        CourseCodec(**{**cfg,'quantizer_input_normalization':'batchnorm'})

def test_retained_c11_checkpoint_matches_legacy_implementation():
    import importlib.util, sys
    legacy_path=Path('/var/tmp/hehaoran-codec-champion11.VvwCbAgC/src/ssp_codec/model.py')
    if not legacy_path.exists():
        pytest.skip('remote retained CHAMPION11 source unavailable')
    name='ssp_codec._champion11_legacy_model'
    spec=importlib.util.spec_from_file_location(name,legacy_path)
    legacy=importlib.util.module_from_spec(spec);sys.modules[name]=legacy
    spec.loader.exec_module(legacy)
    state=torch.load(ROOT/'runs/champion11_d_both/checkpoints/step_00500000.pt',map_location='cpu',weights_only=False)
    old=legacy.CourseCodec(**state['model_config']).eval()
    new=CourseCodec(**state['model_config']).eval()
    old.load_state_dict(state['model'],strict=True);new.load_state_dict(state['model'],strict=True)
    x=torch.randn(1,1,1607)
    with torch.no_grad():
        a,ai,al=old(x);b,bi,bl=new(x)
    torch.testing.assert_close(a,b,rtol=0,atol=0);assert torch.equal(ai,bi)
    torch.testing.assert_close(al,bl,rtol=0,atol=0)
