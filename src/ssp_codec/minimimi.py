"""Compact SEANet and bounded-context Transformer modules for MiniMimi codecs."""

from __future__ import annotations

import math
from typing import Iterable

import torch
import torch.nn.functional as F
from torch import nn


class CausalStridedConv1d(nn.Module):
    """Causal strided convolution that preserves exact divisible lengths."""

    def __init__(self, in_channels: int, out_channels: int, stride: int, overlap: int = 2) -> None:
        super().__init__()
        if stride < 1 or overlap < 1:
            raise ValueError("stride and overlap must be positive")
        kernel_size = stride * overlap
        self.left_padding = kernel_size - stride
        self.conv = nn.Conv1d(
            in_channels,
            out_channels,
            kernel_size=kernel_size,
            stride=stride,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(F.pad(x, (self.left_padding, 0)))


class CausalTransposeConv1d(nn.Module):
    """Causal transposed convolution with deterministic right trimming."""

    def __init__(self, in_channels: int, out_channels: int, stride: int, overlap: int = 1) -> None:
        super().__init__()
        if stride < 1 or overlap < 1:
            raise ValueError("stride and overlap must be positive")
        self.stride = stride
        self.conv = nn.ConvTranspose1d(
            in_channels,
            out_channels,
            kernel_size=stride * overlap,
            stride=stride,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        expected = x.shape[-1] * self.stride
        return self.conv(x)[..., :expected]


class MiniSEANetResidualBlock(nn.Module):
    """Mimi-style bottleneck residual block with a true identity shortcut."""

    def __init__(self, channels: int, compression: int = 2) -> None:
        super().__init__()
        if compression < 1 or channels % compression:
            raise ValueError("channels must be divisible by residual compression")
        hidden = channels // compression
        self.conv = nn.Sequential(
            nn.ELU(),
            nn.Conv1d(channels, hidden, kernel_size=3),
            nn.ELU(),
            nn.Conv1d(hidden, channels, kernel_size=1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Only the kernel-three convolution expands the receptive field.
        return x + self.conv[3](self.conv[2](self.conv[1](F.pad(self.conv[0](x), (2, 0)))))


class MiniSEANetEncoder(nn.Module):
    def __init__(
        self,
        channels: Iterable[int],
        strides: Iterable[int],
        latent_dim: int,
        residual_compression: int = 2,
        downsample_overlap: int = 2,
    ) -> None:
        super().__init__()
        channels = tuple(int(value) for value in channels)
        strides = tuple(int(value) for value in strides)
        if len(channels) != len(strides) + 1:
            raise ValueError("MiniSEANet encoder needs one more channel value than strides")
        self.input_conv = nn.Conv1d(1, channels[0], kernel_size=7)
        self.blocks = nn.ModuleList()
        for in_channels, out_channels, stride in zip(channels[:-1], channels[1:], strides):
            self.blocks.append(
                nn.ModuleDict(
                    {
                        "residual": MiniSEANetResidualBlock(in_channels, residual_compression),
                        "downsample": CausalStridedConv1d(
                            in_channels,
                            out_channels,
                            stride,
                            overlap=downsample_overlap,
                        ),
                    }
                )
            )
        self.output_conv = nn.Conv1d(channels[-1], latent_dim, kernel_size=3)

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        x = self.input_conv(F.pad(waveform, (6, 0)))
        for block in self.blocks:
            x = block["downsample"](block["residual"](x))
        x = self.output_conv(F.pad(F.elu(x), (2, 0)))
        return x.transpose(1, 2)


class MiniSEANetDecoder(nn.Module):
    def __init__(
        self,
        channels: Iterable[int],
        strides: Iterable[int],
        latent_dim: int,
        residual_compression: int = 2,
        upsample_overlap: int = 1,
    ) -> None:
        super().__init__()
        channels = tuple(int(value) for value in channels)
        strides = tuple(int(value) for value in strides)
        if len(channels) != len(strides) + 1:
            raise ValueError("MiniSEANet decoder needs one more channel value than strides")
        self.input_conv = nn.Conv1d(latent_dim, channels[0], kernel_size=7)
        self.blocks = nn.ModuleList()
        for in_channels, out_channels, stride in zip(channels[:-1], channels[1:], strides):
            self.blocks.append(
                nn.ModuleDict(
                    {
                        "upsample": CausalTransposeConv1d(
                            in_channels,
                            out_channels,
                            stride,
                            overlap=upsample_overlap,
                        ),
                        "residual": MiniSEANetResidualBlock(out_channels, residual_compression),
                    }
                )
            )
        self.output_conv = nn.Conv1d(channels[-1], 1, kernel_size=3)

    def forward(self, embeddings: torch.Tensor) -> torch.Tensor:
        x = embeddings.transpose(1, 2)
        x = self.input_conv(F.pad(x, (6, 0)))
        for block in self.blocks:
            x = block["residual"](F.elu(block["upsample"](x)))
        x = self.output_conv(F.pad(F.elu(x), (2, 0)))
        return torch.tanh(x)


class LookaheadFusion(nn.Module):
    """Fuse future frames exactly once before a strictly causal stack."""

    def __init__(self, channels: int, frames: int) -> None:
        super().__init__()
        if frames < 0:
            raise ValueError("lookahead frames must be non-negative")
        self.frames = frames
        if frames:
            self.depthwise = nn.Conv1d(
                channels,
                channels,
                kernel_size=frames + 1,
                groups=channels,
                bias=False,
            )
            self.pointwise = nn.Conv1d(channels, channels, kernel_size=1)
            self.scale = nn.Parameter(torch.full((channels,), 0.01))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if not self.frames:
            return x
        channels_first = x.transpose(1, 2)
        future = self.depthwise(F.pad(channels_first, (0, self.frames)))
        future = self.pointwise(F.gelu(future)).transpose(1, 2)
        return x + future * self.scale


def _apply_rope(x: torch.Tensor) -> torch.Tensor:
    """Apply rotary position encoding to [B, H, T, D]."""

    _, _, length, dim = x.shape
    if dim % 2:
        raise ValueError("attention head dimension must be even for RoPE")
    positions = torch.arange(length, device=x.device, dtype=torch.float32)
    inverse = torch.exp(
        torch.arange(0, dim, 2, device=x.device, dtype=torch.float32)
        * (-math.log(10_000.0) / dim)
    )
    angles = positions[:, None] * inverse[None]
    cos = angles.cos().to(dtype=x.dtype)[None, None]
    sin = angles.sin().to(dtype=x.dtype)[None, None]
    even, odd = x[..., 0::2], x[..., 1::2]
    return torch.stack((even * cos - odd * sin, even * sin + odd * cos), dim=-1).flatten(-2)


class LocalCausalSelfAttention(nn.Module):
    """Actual bounded-window causal attention, not merely a masked dense matrix."""

    def __init__(self, dimension: int, heads: int, history_frames: int) -> None:
        super().__init__()
        if dimension % heads:
            raise ValueError("Transformer dimension must be divisible by its head count")
        if history_frames < 1:
            raise ValueError("history_frames must be positive")
        self.dimension = dimension
        self.heads = heads
        self.head_dim = dimension // heads
        self.history_frames = history_frames
        self.qkv = nn.Linear(dimension, 3 * dimension, bias=False)
        self.output = nn.Linear(dimension, dimension, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, length, _ = x.shape
        qkv = self.qkv(x).view(batch, length, 3, self.heads, self.head_dim)
        q, k, v = (value.permute(0, 2, 1, 3) for value in qkv.unbind(dim=2))
        q = _apply_rope(q)
        k = _apply_rope(k)
        window = min(self.history_frames, length)
        k_windows = F.pad(k, (0, 0, window - 1, 0)).unfold(2, window, 1)
        v_windows = F.pad(v, (0, 0, window - 1, 0)).unfold(2, window, 1)
        scores = (q.unsqueeze(-1) * k_windows).sum(dim=3) / math.sqrt(self.head_dim)
        offsets = torch.arange(window, device=x.device)
        times = torch.arange(length, device=x.device)[:, None]
        valid = times - (window - 1 - offsets[None]) >= 0
        scores = scores.masked_fill(~valid[None, None], torch.finfo(scores.dtype).min)
        weights = scores.softmax(dim=-1)
        attended = (weights.unsqueeze(3) * v_windows).sum(dim=-1)
        attended = attended.permute(0, 2, 1, 3).reshape(batch, length, self.dimension)
        return self.output(attended)


class MiniTransformerBlock(nn.Module):
    def __init__(
        self,
        dimension: int,
        heads: int,
        feedforward_dim: int,
        history_frames: int,
        hybrid_kernel_size: int = 0,
    ) -> None:
        super().__init__()
        self.attention_norm = nn.LayerNorm(dimension)
        self.attention = LocalCausalSelfAttention(dimension, heads, history_frames)
        self.attention_scale = nn.Parameter(torch.full((dimension,), 0.01))
        self.hybrid_kernel_size = hybrid_kernel_size
        if hybrid_kernel_size:
            if hybrid_kernel_size < 2:
                raise ValueError("hybrid kernel size must be at least two")
            self.conv_norm = nn.LayerNorm(dimension)
            self.depthwise = nn.Conv1d(
                dimension,
                dimension,
                kernel_size=hybrid_kernel_size,
                groups=dimension,
            )
            self.pointwise = nn.Conv1d(dimension, dimension, kernel_size=1)
            self.conv_scale = nn.Parameter(torch.full((dimension,), 0.01))
        self.feedforward_norm = nn.LayerNorm(dimension)
        self.feedforward = nn.Sequential(
            nn.Linear(dimension, feedforward_dim),
            nn.GELU(),
            nn.Linear(feedforward_dim, dimension),
        )
        self.feedforward_scale = nn.Parameter(torch.full((dimension,), 0.01))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attention(self.attention_norm(x)) * self.attention_scale
        if self.hybrid_kernel_size:
            local = self.conv_norm(x).transpose(1, 2)
            local = self.depthwise(F.pad(local, (self.hybrid_kernel_size - 1, 0)))
            local = self.pointwise(F.gelu(local)).transpose(1, 2)
            x = x + local * self.conv_scale
        return x + self.feedforward(self.feedforward_norm(x)) * self.feedforward_scale


class MiniTransformerStack(nn.Module):
    def __init__(
        self,
        dimension: int,
        layers: int,
        heads: int,
        feedforward_dim: int,
        history_frames: int,
        hybrid_kernel_size: int = 0,
    ) -> None:
        super().__init__()
        self.history_frames = history_frames
        self.layers = nn.ModuleList(
            MiniTransformerBlock(
                dimension,
                heads,
                feedforward_dim,
                history_frames,
                hybrid_kernel_size,
            )
            for _ in range(layers)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for layer in self.layers:
            x = layer(x)
        return x
