from pathlib import Path
import pytest
import torch

from ssp_codec.champion_analysis import GroupedWaveformEncoder, SnakeBeta
from ssp_codec.config import load_config
from ssp_codec.io import read_bitstream, write_bitstream
from ssp_codec.model import CourseCodec

ROOT=Path(__file__).resolve().parents[1]
CELLS=("a_g4_d0","b_g8_d0","c_g4_d2","d_g8_d2")


@pytest.mark.parametrize("cell",CELLS)
def test_registered_shapes_and_real_roundtrip(cell,tmp_path):
    cfg=load_config(ROOT/f"configs/champion9/{cell}.yaml")
    model=CourseCodec(**cfg["model"]).eval()
    assert len(model.analysis_temporal.blocks)==0
    assert len(model.synthesis_temporal.blocks)==cfg["model"]["decoder_temporal_layers"]
    assert model.algorithmic_lookahead_frames==2 and model.total_algorithmic_delay_ms==30
    x=torch.randn(1,1,1607)
    with torch.no_grad():
        output,indices,loss=model(x)
        assert output.shape==x.shape and indices.shape==(1,11,3)
        assert torch.isfinite(output).all() and torch.isfinite(loss)
        assert indices.min()>=0 and indices.max()<=255
        path=tmp_path/"test.bin";write_bitstream(path,indices[0],1607)
        values,side=read_bitstream(path)
        assert path.stat().st_size==33 and side["frame_samples"]==160 and side["bits_per_frame"]==24
        torch.testing.assert_close(output,model.decode(values[None],length=1607))


@pytest.mark.parametrize("groups",(4,8))
def test_grouped_frontend_packet_causality_and_gradient(groups):
    model=GroupedWaveformEncoder((8,16,32,64,160),(2,4,4,5),groups)
    x=torch.randn(1,1,1600,requires_grad=True)
    original=model(x)
    changed=x.detach().clone();changed[...,480:]+=10
    torch.testing.assert_close(original[:,:3],model(changed)[:,:3])
    torch.testing.assert_close(original[:,:3],model(x[...,:480]))
    original.square().mean().backward()
    assert torch.isfinite(x.grad).all() and x.grad.abs().sum()>0
    assert model.blocks[0]["residual"][0].snake1.log_alpha.grad.abs().sum()>0


@pytest.mark.parametrize("cell",CELLS)
def test_exercised_lookahead_never_crosses_total30ms(cell):
    model=CourseCodec(**load_config(ROOT/f"configs/champion9/{cell}.yaml")["model"]).eval()
    look=model.analysis_temporal.lookahead
    with torch.no_grad():
        look.depthwise.weight.zero_();look.depthwise.weight[..., -1]=1
        look.project.weight.zero_();look.project.bias.zero_()
        for c in range(160):look.project.weight[c,c,0]=1
    def analysis(x):return model.analysis_gru(model.analysis_temporal(model.latent_norm(model.encoder(x))))
    x=torch.randn(1,1,1600)
    beyond=x.clone();beyond[...,480:]+=10
    within=x.clone();within[...,320:480]+=10
    with torch.no_grad():
        a=analysis(x)
        torch.testing.assert_close(a[:,:1],analysis(beyond)[:,:1])
        torch.testing.assert_close(a[:,:1],analysis(x[...,:480])[:,:1])
        assert not torch.allclose(a[:,:1],analysis(within)[:,:1])
        output=model(x)[0]
        torch.testing.assert_close(output[...,:160],model(beyond)[0][...,:160])


def test_snake_accounting_and_finite_backward():
    block=SnakeBeta(8);x=torch.randn(2,8,20,requires_grad=True)
    y=block(x)
    torch.testing.assert_close(y,x+torch.sin(x).square())
    assert block.extra_flops(x.numel())==36*x.numel()+65*8
    y.square().mean().backward();assert torch.isfinite(x.grad).all()


def test_grouped_model_rejects_extra_tcn_or_delay():
    cfg=load_config(ROOT/"configs/champion9/a_g4_d0.yaml")["model"]
    with pytest.raises(ValueError):CourseCodec(**{**cfg,"encoder_temporal_layers":1})
    with pytest.raises(ValueError):CourseCodec(**{**cfg,"encoder_lookahead_frames":3})
    with pytest.raises(ValueError):CourseCodec(**{**cfg,"decoder_lookahead_frames":1})
