from pathlib import Path
import torch
from ssp_codec.model import CourseCodec, CausalConv2FormerUnit
from ssp_codec.champion_synthesis import CausalResidualGRU, CausalFourierDecoder
from ssp_codec.config import load_config
from ssp_codec.io import write_bitstream, read_bitstream

ROOT = Path(__file__).resolve().parents[1]


def test_forward_gru_identity_and_past_independence():
    block = CausalResidualGRU(8)
    x = torch.randn(2, 12, 8)
    assert torch.equal(block(x), x)
    torch.nn.init.normal_(block.project.weight, std=.1)
    changed = x.clone()
    changed[:, 6:] += 20
    torch.testing.assert_close(block(x)[:, :6], block(changed)[:, :6])
    block(x).square().mean().backward()
    assert block.gru.weight_ih_l0.grad.abs().sum() > 0


def test_fourier_synthesis_causal_frames_and_finite_backward():
    decoder = CausalFourierDecoder(8, 16, 8, 2, 320, CausalConv2FormerUnit)
    x = torch.randn(2, 10, 8, requires_grad=True)
    changed = x.detach().clone()
    changed[:, 5:] += 20
    output = decoder(x)
    assert output.shape == (2, 1, 1600)
    torch.testing.assert_close(output[..., :800], decoder(changed)[..., :800])
    # Appending future latent frames cannot change already committed samples.
    torch.testing.assert_close(decoder(x[:, :5]), output[..., :800])
    output.square().mean().backward()
    assert torch.isfinite(x.grad).all() and x.grad.abs().sum() > 0
    assert torch.isfinite(decoder.head.weight.grad).all()


def test_fourier_gru_codec_actual_bitstream_roundtrip(tmp_path):
    config = load_config(ROOT / "configs/champion5/d_fourier_gru.yaml")
    model = CourseCodec(**config["model"]).eval()
    waveform = torch.randn(1, 1, 1607)
    with torch.no_grad():
        output, indices, _ = model(waveform)
        assert output.shape == waveform.shape and indices.shape == (1, 11, 3)
        path = tmp_path / "audio.bin"
        write_bitstream(path, indices[0], waveform.shape[-1])
        decoded_indices, metadata = read_bitstream(path)
        assert path.stat().st_size == 33 and metadata["bitrate_bps"] == 2400
        torch.testing.assert_close(output, model.decode(decoded_indices[None], length=1607))
        assert model.algorithmic_lookahead_frames == 3


def test_fourier_initialization_matches_across_gru_factor():
    c = CourseCodec(**load_config(ROOT / "configs/champion5/c_fourier.yaml")["model"])
    d = CourseCodec(**load_config(ROOT / "configs/champion5/d_fourier_gru.yaml")["model"])
    assert all(torch.equal(value, d.decoder.state_dict()[key]) for key, value in c.decoder.state_dict().items())
