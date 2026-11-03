"""Causal GRU analysis and learned Fourier/overlap-add waveform synthesis."""
from __future__ import annotations
import math
import torch
from torch import nn
import torch.nn.functional as F


class CausalResidualGRU(nn.Module):
    """One forward GRU at100Hz, initially an identity residual adapter."""
    def __init__(self, channels: int) -> None:
        super().__init__()
        self.norm = nn.LayerNorm(channels)
        self.gru = nn.GRU(channels, channels, num_layers=1, batch_first=True)
        self.project = nn.Linear(channels, channels)
        nn.init.zeros_(self.project.weight)
        nn.init.zeros_(self.project.bias)

    def forward(self, embeddings: torch.Tensor) -> torch.Tensor:
        hidden, _ = self.gru(self.norm(embeddings))
        return embeddings + self.project(hidden)


class CausalFourierDecoder(nn.Module):
    """Predict320-point real Fourier frames every160samples, then causal OLA.

    Frame t starts at output sample160t and forecasts320 samples. Thus each
    committed output hop combines frame t and the already-known frame t-1;
    never frame t+1. This differs from centered torch.istft buffering.
    """
    def __init__(self, channels: int, width: int, hidden: int, layers: int,
                 n_fft: int, block_factory) -> None:
        super().__init__()
        if n_fft != 320 or width < 1 or hidden < 1 or layers < 1:
            raise ValueError("Fourier synthesis requires n_fft320 and positive dimensions")
        self.n_fft = n_fft
        self.hop = 160
        self.input_projection = nn.Linear(channels, width)
        self.blocks = nn.Sequential(*(block_factory(width, hidden, 7) for _ in range(layers)))
        self.norm = nn.LayerNorm(width)
        #161 real bins +159 non-DC/non-Nyquist imaginary bins =320 real scalars.
        self.head = nn.Linear(width, n_fft)
        window = torch.sin(math.pi * (torch.arange(n_fft) + .5) / n_fft).square()
        self.register_buffer("window", window)

    def forward(self, embeddings: torch.Tensor) -> torch.Tensor:
        hidden = self.blocks(self.input_projection(embeddings))
        coefficients = self.head(self.norm(hidden))
        real = coefficients[..., :self.n_fft // 2 + 1]
        imag = F.pad(coefficients[..., self.n_fft // 2 + 1:], (1, 1))
        frames = torch.fft.irfft(torch.complex(real, imag), n=self.n_fft, dim=-1)
        count = frames.shape[1]
        window = self.window.to(frames)
        output_samples = (count - 1) * self.hop + self.n_fft
        numerator = F.fold((frames * window).transpose(1, 2),
            output_size=(1, output_samples), kernel_size=(1, self.n_fft), stride=(1, self.hop))
        denominator = F.fold(window.view(1, self.n_fft, 1).expand(1, self.n_fft, count),
            output_size=(1, output_samples), kernel_size=(1, self.n_fft), stride=(1, self.hop))
        # Sum-of-window normalization is a weighted average of predicted
        # unwindowed Fourier frames, not a squared-window STFT inverse.
        waveform = (numerator / denominator.clamp_min(1e-8)).squeeze(2)
        return torch.tanh(waveform[..., :count * self.hop])

    def extra_flops(self, frames: int) -> int:
        # Conservative complex-FFT upper estimate for real IRFFT, plus window,
        # fold accumulation and envelope normalization. Excludes activations/LN
        # consistently with the existing analytical competition convention.
        return frames * self.n_fft * (5 * math.ceil(math.log2(self.n_fft)) + 4)
