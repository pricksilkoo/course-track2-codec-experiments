"""Champion-inspired grouped waveform analysis; no independent latent TCN."""
from __future__ import annotations

import torch
from torch import nn
import torch.nn.functional as F


class SnakeBeta(nn.Module):
    """Positive per-channel periodic activation; temporal positions never mix."""
    def __init__(self, channels: int) -> None:
        super().__init__()
        self.log_alpha = nn.Parameter(torch.zeros(1, channels, 1))
        self.log_beta = nn.Parameter(torch.zeros(1, channels, 1))
        self.channels = channels

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + torch.sin(self.log_alpha.exp() * x).square() * (-self.log_beta).exp()

    def extra_flops(self, elements: int) -> int:
        # Explicit conservative transcendental-operation convention, not MACs:
        # sin32 + multiply/square/multiply/add4 per element; exp32 twice and
        # parameter negation1 per channel per call. Other existing activations
        # remain excluded by the historical analytical convention.
        return 36 * elements + 65 * self.channels


class GroupedResidualUnit(nn.Module):
    def __init__(self, channels: int, groups: int, dilation: int) -> None:
        super().__init__()
        if channels % groups:
            raise ValueError("group count must divide every residual width")
        self.snake1 = SnakeBeta(channels)
        self.spatial = nn.Conv1d(channels, channels, 3, dilation=dilation, groups=groups)
        self.snake2 = SnakeBeta(channels)
        self.mix = nn.Conv1d(channels, channels, 1)
        self.left_padding = 2 * dilation

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = self.spatial(F.pad(self.snake1(x), (self.left_padding, 0)))
        return x + self.mix(self.snake2(residual))


class GroupedWaveformEncoder(nn.Module):
    """Four packet-aligned causal stages, with dilation1/3/9 at each stage."""
    def __init__(self, channels, strides, groups: int) -> None:
        super().__init__()
        channels, strides = tuple(channels), tuple(strides)
        if len(channels) != len(strides) + 1 or groups not in (4, 8):
            raise ValueError("This registered encoder uses groups4/8 and four stages")
        if len(strides) != 4 or any(c % groups for c in channels):
            raise ValueError("Invalid grouped encoder dimensions")
        self.input_conv = nn.Conv1d(1, channels[0], 7)
        self.blocks = nn.ModuleList()
        for before, after, stride in zip(channels[:-1], channels[1:], strides):
            self.blocks.append(nn.ModuleDict({
                "residual": nn.Sequential(*(GroupedResidualUnit(before, groups, d) for d in (1, 3, 9))),
                "snake": SnakeBeta(before),
                "downsample": nn.Conv1d(before, after, 2 * stride, stride=stride),
            }))
        self.strides = strides

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        x = self.input_conv(F.pad(waveform, (6, 0)))
        for block, stride in zip(self.blocks, self.strides):
            x = block["residual"](x)
            # Output j sees samples through (j+1)*stride-1, not past the
            # current downsampling packet. Left overlap is prior context only.
            x = block["downsample"](F.pad(block["snake"](x), (stride, 0)))
        return x.transpose(1, 2)
