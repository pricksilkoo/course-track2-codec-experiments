"""Reconstruction losses for the course codec baseline."""

from __future__ import annotations

import torch
import torch.nn.functional as F


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
