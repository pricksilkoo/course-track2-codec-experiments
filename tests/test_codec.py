import json
from pathlib import Path

import torch

from ssp_codec.adversarial import (
    MultiResolutionSTFTDiscriminator,
    discriminator_hinge_loss,
    feature_matching_loss,
    generator_hinge_loss,
)
from ssp_codec.io import read_bitstream, write_bitstream
from ssp_codec.config import apply_overrides, load_config
from ssp_codec.losses import negative_si_snr_loss
from ssp_codec.model import CausalTemporalStack, CourseCodec


def test_fixed_2p4k_shape_and_indices() -> None:
    model = CourseCodec()
    waveform = torch.randn(2, 1, 16_080)
    reconstructed, indices, _ = model(waveform)
    assert reconstructed.shape == waveform.shape
    assert indices.shape == (2, 101, 3)
    assert indices.dtype == torch.long
    assert int(indices.min()) >= 0
    assert int(indices.max()) < 256


def test_ema_rvq_initializes_and_decode_matches_forward() -> None:
    model = CourseCodec()
    waveform = torch.randn(8, 1, 16_000)
    model.train()
    model(waveform)
    assert bool(model.quantizer.initialized)
    metrics = model.quantizer.usage_metrics()
    assert metrics["active_codes"] == [256, 256, 256]
    model.eval()
    direct, _, _ = model(waveform)
    indices = model.encode(waveform)
    decoded = model.decode(indices, waveform.size(-1))
    assert torch.allclose(direct, decoded, atol=1e-6)


def test_latent_scale_is_fixed_before_quantization() -> None:
    model = CourseCodec()
    waveform = torch.randn(2, 1, 16_000)
    with torch.no_grad():
        latent = model.latent_norm(model.encoder(waveform))
    assert torch.allclose(latent.mean(dim=-1), torch.zeros_like(latent[..., 0]), atol=1e-5)
    assert torch.allclose(
        latent.var(dim=-1, unbiased=False),
        torch.ones_like(latent[..., 0]),
        atol=2e-3,
    )


def test_bitstream_uses_exactly_three_bytes_per_frame(tmp_path) -> None:
    indices = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.long)
    path = tmp_path / "sample.bin"
    write_bitstream(path, indices, num_samples=161)
    assert path.stat().st_size == 6
    assert json.loads(path.with_suffix(".json").read_text())["bitrate_bps"] == 2400
    decoded_indices, metadata = read_bitstream(path)
    assert torch.equal(decoded_indices, indices)
    assert metadata["num_samples"] == 161


def test_multiresolution_discriminator_losses_are_finite() -> None:
    discriminator = MultiResolutionSTFTDiscriminator(
        [[256, 64, 256], [512, 128, 512], [1024, 256, 1024]],
        periods=[2, 3],
    )
    real = torch.randn(2, 1, 4096)
    fake = torch.randn_like(real)
    real_logits, real_features = discriminator(real)
    fake_logits, fake_features = discriminator(fake)
    losses = (
        discriminator_hinge_loss(real_logits, fake_logits),
        generator_hinge_loss(fake_logits),
        feature_matching_loss(real_features, fake_features),
    )
    assert all(torch.isfinite(loss) for loss in losses)
    assert len(real_logits) == 5


def test_negative_si_snr_prefers_a_clean_estimate() -> None:
    reference = torch.randn(4, 1, 1600)
    clean = negative_si_snr_loss(reference + 0.01 * torch.randn_like(reference), reference)
    noisy = negative_si_snr_loss(reference + 0.5 * torch.randn_like(reference), reference)
    assert torch.isfinite(clean)
    assert torch.isfinite(noisy)
    assert clean < noisy


def test_factorized_rvq_round_trip_matches_forward() -> None:
    model = CourseCodec(rvq_codebook_dim=32)
    waveform = torch.randn(4, 1, 3200)
    model.train()
    model(waveform)
    model.eval()
    direct, indices, _ = model(waveform)
    decoded = model.decode(indices, waveform.size(-1))
    assert indices.shape == (4, 20, 3)
    assert torch.allclose(direct, decoded, atol=1e-6)


def test_fsq_packs_exactly_24_bits_and_round_trips() -> None:
    model = CourseCodec(quantizer_type="fsq")
    waveform = torch.randn(2, 1, 1600)
    direct, indices, loss = model(waveform)
    decoded = model.decode(indices, waveform.size(-1))
    assert indices.shape == (2, 10, 3)
    assert int(indices.min()) >= 0
    assert int(indices.max()) <= 255
    assert loss.item() == 0.0
    assert torch.allclose(direct, decoded, atol=1e-6)


def test_latent_temporal_stack_is_causal() -> None:
    stack = CausalTemporalStack(8, layers=4, kernel_size=3, expansion=2)
    original = torch.randn(2, 20, 8)
    changed = original.clone()
    changed[:, 12:] = torch.randn_like(changed[:, 12:])
    assert torch.allclose(stack(original)[:, :12], stack(changed)[:, :12], atol=1e-6)


def test_limited_lookahead_observes_no_more_than_three_frames() -> None:
    stack = CausalTemporalStack(
        4, layers=0, kernel_size=3, expansion=2, lookahead_frames=3
    )
    with torch.no_grad():
        stack.lookahead.depthwise.weight.zero_()
        stack.lookahead.depthwise.weight[:, 0, -1] = 1.0
        stack.lookahead.project.weight.zero_()
        for channel in range(4):
            stack.lookahead.project.weight[channel, channel, 0] = 1.0
        stack.lookahead.project.bias.zero_()
    original = torch.randn(2, 20, 4)
    changed = original.clone()
    changed[:, 12:] = torch.randn_like(changed[:, 12:])
    original_output = stack(original)
    changed_output = stack(changed)
    assert torch.allclose(original_output[:, :9], changed_output[:, :9], atol=1e-6)
    assert not torch.allclose(original_output[:, 9:12], changed_output[:, 9:12])


def test_baseline_local_transformer_round_trip_and_semantic_auxiliary() -> None:
    model = CourseCodec(
        temporal_model="transformer",
        encoder_temporal_layers=2,
        decoder_temporal_layers=1,
        temporal_transformer_heads=4,
        temporal_transformer_ffn_dim=56,
        encoder_history_frames=16,
        decoder_history_frames=16,
        encoder_lookahead_frames=3,
    )
    waveform = torch.randn(2, 1, 1600)
    model.train()
    reconstructed, indices, loss, auxiliary = model(waveform, return_aux=True)
    assert reconstructed.shape == waveform.shape
    assert indices.shape == (2, 10, 3)
    assert auxiliary["semantic"].shape == (2, 10, 160)
    assert torch.isfinite(loss)
    model.eval()
    decoded = model.decode(model.encode(waveform), waveform.size(-1))
    assert torch.allclose(model(waveform)[0], decoded, atol=1e-6)


def test_baseline_local_transformer_future_dependency_is_bounded() -> None:
    model = CourseCodec(
        temporal_model="transformer",
        encoder_temporal_layers=2,
        decoder_temporal_layers=1,
        encoder_lookahead_frames=3,
    ).eval()
    original = torch.randn(1, 1, 3200)
    changed = original.clone()
    changed[..., 1600:] = torch.randn_like(changed[..., 1600:])
    with torch.no_grad():
        original_latent = model.analysis_transformer(
            model.lookahead_fusion(model.latent_norm(model.encoder(original)))
        )
        changed_latent = model.analysis_transformer(
            model.lookahead_fusion(model.latent_norm(model.encoder(changed)))
        )
    assert torch.allclose(original_latent[:, :7], changed_latent[:, :7], atol=1e-5)


def test_codec_rejects_more_than_30ms_total_lookahead() -> None:
    try:
        CourseCodec(encoder_lookahead_frames=2, decoder_lookahead_frames=2)
    except ValueError as error:
        assert "three 10-ms frames" in str(error)
    else:
        raise AssertionError("codec accepted more than 30 ms of lookahead")


def test_config_inheritance_and_cli_override() -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_config(root / "configs/experiments/factorized_rvq_32.yaml")
    assert config["model"]["rvq_codebook_dim"] == 32
    assert config["audio"]["sample_rate"] == 16000
    overridden = apply_overrides(config, ["model.rvq_codebook_dim=64"])
    assert overridden["model"]["rvq_codebook_dim"] == 64
    assert config["model"]["rvq_codebook_dim"] == 32


def test_minimimi_plain_rvq_shape_and_round_trip() -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_config(root / "configs/minimimi/a_plain_rvq.yaml")
    model = CourseCodec(**config["model"])
    waveform = torch.randn(2, 1, 1600)
    model.train()
    reconstructed, indices, _ = model(waveform)
    model.eval()
    decoded = model.decode(model.encode(waveform), waveform.size(-1))
    assert reconstructed.shape == waveform.shape
    assert indices.shape == (2, 10, 3)
    assert torch.allclose(model(waveform)[0], decoded, atol=1e-6)


def test_minimimi_split_rvq_exposes_semantic_latent() -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_config(root / "configs/minimimi/b_split_semantic.yaml")
    model = CourseCodec(**config["model"])
    waveform = torch.randn(2, 1, 1600)
    model.train()
    reconstructed, indices, loss, auxiliary = model(waveform, return_aux=True)
    assert reconstructed.shape == waveform.shape
    assert indices.shape == (2, 10, 3)
    assert auxiliary["semantic"].shape == (2, 10, 32)
    assert torch.isfinite(loss)


def test_minimimi_future_dependency_is_limited_to_three_frames() -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_config(root / "configs/minimimi/a_plain_rvq.yaml")
    model = CourseCodec(**config["model"]).eval()
    original = torch.randn(1, 1, 3200)
    changed = original.clone()
    changed[..., 1600:] = torch.randn_like(changed[..., 1600:])
    with torch.no_grad():
        original_latent = model.analysis_transformer(
            model.lookahead_fusion(model.latent_norm(model.encoder(original)))
        )
        changed_latent = model.analysis_transformer(
            model.lookahead_fusion(model.latent_norm(model.encoder(changed)))
        )
    # Input changes at frame 10 can affect frames 7--9 through the one-time
    # lookahead, but never frame 6 or earlier despite the three-layer stack.
    assert torch.allclose(original_latent[:, :7], changed_latent[:, :7], atol=1e-5)
