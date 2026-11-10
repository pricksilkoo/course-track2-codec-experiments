from pathlib import Path
import pytest
import torch
from ssp_codec.config import load_config
from ssp_codec.model import CourseCodec
from ssp_codec.io import read_bitstream,write_bitstream
ROOT=Path(__file__).resolve().parents[1]
CELLS=('a_base','b_enc','c_dec','d_both')

@pytest.mark.parametrize('cell',CELLS)
def test_capacity_shapes_real_bytes_and_causality(cell,tmp_path):
    cfg=load_config(ROOT/f'configs/champion10/{cell}.yaml')
    torch.manual_seed(20261110)
    model=CourseCodec(**cfg['model']).eval()
    assert len(model.analysis_temporal.blocks)==0 and len(model.synthesis_temporal.blocks)==2
    assert model.total_algorithmic_delay_ms==30 and model.algorithmic_lookahead_frames==2
    x=torch.randn(1,1,1607)
    with torch.no_grad():
        y,idx,loss=model(x)
        assert y.shape==x.shape and idx.shape==(1,11,3) and torch.isfinite(y).all() and torch.isfinite(loss)
        assert idx.min()>=0 and idx.max()<=255
        path=tmp_path/'bytes.bin';write_bitstream(path,idx[0],1607)
        v,meta=read_bitstream(path)
        assert path.stat().st_size==33 and meta['bits_per_frame']==24
        torch.testing.assert_close(y,model.decode(v[None],length=1607))
        # Force nonzero future branch, rather than testing an identity adapter.
        look=model.analysis_temporal.lookahead
        look.depthwise.weight.zero_();look.depthwise.weight[...,-1]=1
        look.project.weight.zero_();look.project.bias.zero_()
        for c in range(160):look.project.weight[c,c,0]=1
        def analysis(z):return model.analysis_gru(model.analysis_temporal(model.latent_norm(model.encoder(z))))
        changed=x.clone();changed[...,480:]+=10
        within=x.clone();within[...,320:480]+=10
        z=analysis(x)
        torch.testing.assert_close(z[:,:1],analysis(changed)[:,:1])
        torch.testing.assert_close(z[:,:1],analysis(x[...,:480])[:,:1])
        assert not torch.allclose(z[:,:1],analysis(within)[:,:1])
        torch.testing.assert_close(model(x)[0][...,:160],model(changed)[0][...,:160])
        codes=idx.clone();codes[:,1:]=(codes[:,1:]+1)%256
        torch.testing.assert_close(model.decode(idx,length=1607)[...,:160],model.decode(codes,length=1607)[...,:160])

@pytest.mark.parametrize('cell',CELLS)
def test_capacity_finite_cpu_gradient(cell):
    cfg=load_config(ROOT/f'configs/champion10/{cell}.yaml')
    model=CourseCodec(**cfg['model']).train();x=torch.randn(1,1,1600,requires_grad=True)
    y,idx,commit=model(x);objective=y.square().mean()+commit
    objective.backward();assert torch.isfinite(x.grad).all() and x.grad.abs().sum()>0
    assert all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters())
