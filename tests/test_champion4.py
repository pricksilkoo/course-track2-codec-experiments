import importlib.util
from pathlib import Path
import torch
from ssp_codec.config import load_config
from ssp_codec.model import CourseCodec, CausalConv2FormerUnit
from ssp_codec.losses import multiscale_mel_loss
from ssp_codec.io import read_bitstream, write_bitstream

ROOT = Path(__file__).resolve().parents[1]


def test_conv2former_identity_causality_and_gradient():
    block = CausalConv2FormerUnit(8, 4, 7)
    x = torch.randn(2, 20, 8)
    assert torch.equal(block(x), x)
    torch.nn.init.normal_(block.project.weight, std=0.1)
    future_changed = x.clone()
    future_changed[:, 10:] += 10
    torch.testing.assert_close(block(x)[:, :10], block(future_changed)[:, :10])
    block(x).square().mean().backward()
    assert block.depthwise.weight.grad.abs().sum() > 0


def test_training_only_bypass_skips_ema_and_validation_rejects_it():
    config = load_config(ROOT / "configs/champion4/a_control.yaml")
    model = CourseCodec(**config["model"]).train()
    before = {key: value.clone() for key, value in model.quantizer.named_buffers()}
    output, indices, loss = model(torch.randn(1, 1, 1600), quantizer_bypass=True)
    assert output.shape == (1, 1, 1600) and indices.shape == (1, 10, 3)
    assert loss.item() == 0
    assert all(torch.equal(value, before[key]) for key, value in model.quantizer.named_buffers())
    model.eval()
    try:
        model(torch.randn(1, 1, 1600), quantizer_bypass=True)
    except ValueError:
        pass
    else:
        raise AssertionError("inference must never bypass the transmitted RVQ indices")


def test_quantized_codec_roundtrip_and_checkpoint_compatibility(tmp_path):
    a = load_config(ROOT / "configs/champion4/a_control.yaml")["model"]
    c = load_config(ROOT / "configs/champion4/c_conv2former.yaml")["model"]
    control = CourseCodec(**a).eval()
    candidate = CourseCodec(**c).eval()
    missing = candidate.load_state_dict(control.state_dict(), strict=False).missing_keys
    assert missing and all(key.startswith("synthesis_conv2former.") for key in missing)
    waveform = torch.randn(1, 1, 1601)
    with torch.no_grad():
        expected, indices, _ = control(waveform)
        actual, candidate_indices, _ = candidate(waveform)
        torch.testing.assert_close(actual, expected, rtol=0, atol=0)
        assert torch.equal(indices, candidate_indices)
        assert indices.shape == (1, 11, 3)
        assert int(indices.min()) >= 0 and int(indices.max()) <= 255
        torch.testing.assert_close(actual, candidate.decode(indices, length=1601))
        bitstream = tmp_path / "example.bin"
        write_bitstream(bitstream, indices[0], 1601)
        transmitted, metadata = read_bitstream(bitstream)
        assert bitstream.stat().st_size == 3 * 11
        assert metadata["bitrate_bps"] == 2400 and metadata["frame_samples"] == 160
        torch.testing.assert_close(actual, candidate.decode(transmitted[None], length=1601))


def test_mel_loss_finite_and_differentiable():
    reference = torch.randn(2, 1, 1600)
    estimate = (reference + 0.1 * torch.randn_like(reference)).requires_grad_()
    assert multiscale_mel_loss(reference, reference).item() == 0
    loss = multiscale_mel_loss(estimate, reference)
    assert torch.isfinite(loss) and loss > 0
    loss.backward()
    assert torch.isfinite(estimate.grad).all() and estimate.grad.abs().sum() > 0


def test_champion_schedule_is_step_addressed_and_keeps_global_rng():
    spec = importlib.util.spec_from_file_location("codec_train", ROOT / "scripts/train.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    config = load_config(ROOT / "configs/champion4/b_training.yaml")
    assert module.champion_training_settings(config, 1)[1] == 1
    assert abs(module.champion_training_settings(config, 85000)[1] - 1 / 15) < 1e-10
    import random
    before = random.getstate()
    values = [module.champion_training_settings(config, step)[0] for step in range(1, 10001)]
    assert before == random.getstate()
    assert 0.48 < sum(values) / len(values) < 0.52
