"""Reconstruction losses for the course codec baseline."""

from __future__ import annotations

import torch
import torch.nn.functional as F
from functools import lru_cache


@lru_cache(maxsize=24)
def _mel_filters(n_fft: int, n_mels: int, sample_rate: int) -> torch.Tensor:
    """HTK triangular magnitude-mel filters; cached on CPU."""
    mel_max = 2595.0 * torch.log10(torch.tensor(1.0 + sample_rate / 2 / 700))
    mel = torch.linspace(0, float(mel_max), n_mels + 2)
    hz = 700.0 * (10.0 ** (mel / 2595.0) - 1.0)
    frequencies = torch.linspace(0, sample_rate / 2, n_fft // 2 + 1)
    rising = (frequencies[None] - hz[:-2, None]) / (hz[1:-1] - hz[:-2])[:, None]
    falling = (hz[2:, None] - frequencies[None]) / (hz[2:] - hz[1:-1])[:, None]
    filters = torch.minimum(rising, falling).clamp_min(0)
    return filters / filters.sum(dim=1, keepdim=True).clamp_min(1e-8)


def multiscale_mel_loss(
    estimate: torch.Tensor, reference: torch.Tensor,
    fft_sizes: tuple[int, ...] = (256, 512, 1024),
    mel_bins: tuple[int, ...] = (32, 64, 80), sample_rate: int = 16000,
) -> torch.Tensor:
    """L1 log1p magnitude-mel error; used only in training, never inference."""
    if estimate.shape != reference.shape or len(fft_sizes) != len(mel_bins) or not fft_sizes:
        raise ValueError("incompatible mel loss inputs/resolutions")
    loss = estimate.new_zeros(())
    for n_fft, n_mels in zip(fft_sizes, mel_bins):
        window = torch.hann_window(n_fft, device=estimate.device, dtype=estimate.dtype)
        filters = _mel_filters(n_fft, n_mels, sample_rate).to(estimate)
        spectra = []
        for waveform in (estimate, reference):
            magnitude = torch.stft(waveform.squeeze(1), n_fft, hop_length=n_fft // 4,
                                   window=window, return_complex=True).abs()
            spectra.append(torch.log1p(torch.matmul(filters, magnitude)))
        loss = loss + F.l1_loss(spectra[0], spectra[1])
    return loss / len(fft_sizes)


def negative_si_snr_loss(
    estimate: torch.Tensor,
    reference: torch.Tensor,
    eps: float = 1e-8,
) -> torch.Tensor:
    """Return negative scale-invariant SNR in dB, averaged over the batch."""
    if estimate.shape != reference.shape:
        raise ValueError("estimate and reference must have the same shape")
    estimate = estimate.flatten(start_dim=1)
    reference = reference.flatten(start_dim=1)
    estimate = estimate - estimate.mean(dim=-1, keepdim=True)
    reference = reference - reference.mean(dim=-1, keepdim=True)
    reference_energy = reference.square().sum(dim=-1, keepdim=True).clamp_min(eps)
    projection = (
        (estimate * reference).sum(dim=-1, keepdim=True) * reference / reference_energy
    )
    noise = estimate - projection
    ratio = projection.square().sum(dim=-1) / noise.square().sum(dim=-1).clamp_min(eps)
    return -(10.0 * torch.log10(ratio.clamp_min(eps))).mean()


def multiscale_spectral_loss(
    estimate: torch.Tensor,
    reference: torch.Tensor,
    fft_sizes: list[int],
    spectral_convergence_weight: float = 0.0,
    linear_magnitude_weight: float = 0.0,
) -> torch.Tensor:
    """Configurable magnitude loss at several STFT resolutions."""
    if estimate.shape != reference.shape:
        raise ValueError("estimate and reference must have the same shape")
    estimate = estimate.squeeze(1)
    reference = reference.squeeze(1)
    loss = estimate.new_zeros(())
    for n_fft in fft_sizes:
        window = torch.hann_window(n_fft, device=estimate.device, dtype=estimate.dtype)
        estimated_stft = torch.stft(
            estimate, n_fft=n_fft, hop_length=n_fft // 4, window=window, return_complex=True
        )
        reference_stft = torch.stft(
            reference, n_fft=n_fft, hop_length=n_fft // 4, window=window, return_complex=True
        )
        estimated_magnitude = estimated_stft.abs()
        reference_magnitude = reference_stft.abs()
        resolution_loss = F.l1_loss(
            torch.log1p(estimated_magnitude), torch.log1p(reference_magnitude)
        )
        if linear_magnitude_weight:
            resolution_loss = resolution_loss + linear_magnitude_weight * F.l1_loss(
                estimated_magnitude, reference_magnitude
            )
        if spectral_convergence_weight:
            difference = torch.linalg.vector_norm(estimated_magnitude - reference_magnitude)
            scale = torch.linalg.vector_norm(reference_magnitude).clamp_min(1e-8)
            resolution_loss = resolution_loss + spectral_convergence_weight * difference / scale
        loss = loss + resolution_loss
    return loss / len(fft_sizes)
