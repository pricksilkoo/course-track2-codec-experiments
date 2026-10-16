"""Low-resource codec architectures adapted to the fixed course interface.

These modules intentionally share a 100-Hz latent contract.  They are not
paper-reproduction checkpoints: each design is adapted to exactly three
8-bit RVQ stages and to the course complexity and delay limits.
"""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F
from torch import nn


class SafeGRU(nn.GRU):
    """GRU fallback for hosts whose mixed environment cannot initialize cuDNN RNNs."""

    def flatten_parameters(self) -> None:
        # Avoid the eager cuDNN flatten call triggered by Module.to(cuda).
        return None

    def forward(self, input: torch.Tensor, hx: torch.Tensor | None = None):
        # The native PyTorch path remains differentiable and preserves the GRU
        # architecture, while avoiding the server's incompatible cuDNN RNN ABI.
        with torch.backends.cudnn.flags(enabled=False):
            return super().forward(input, hx)


class SnakeBeta(nn.Module):
    """Learnable periodic activation used by several neural audio codecs."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.alpha = nn.Parameter(torch.ones(1, channels, 1))
        self.beta = nn.Parameter(torch.ones(1, channels, 1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        alpha = self.alpha.abs().clamp_min(1e-4)
        beta = self.beta.abs().clamp_min(1e-4)
        return x + torch.sin(alpha * x).square() / beta


class CausalFrameBlock(nn.Module):
    """ConvNeXt-style causal temporal block over ``[batch, frames, channels]``."""

    def __init__(self, channels: int, expansion: int = 2, kernel_size: int = 7) -> None:
        super().__init__()
        self.left_padding = kernel_size - 1
        self.depthwise = nn.Conv1d(
            channels, channels, kernel_size, groups=channels
        )
        self.norm = nn.LayerNorm(channels)
        self.expand = nn.Linear(channels, channels * expansion * 2)
        self.project = nn.Linear(channels * expansion, channels)
        self.scale = nn.Parameter(torch.full((channels,), 1e-3))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        hidden = x.transpose(1, 2)
        hidden = self.depthwise(F.pad(hidden, (self.left_padding, 0))).transpose(1, 2)
        hidden = self.norm(hidden)
        value, gate = self.expand(hidden).chunk(2, dim=-1)
        hidden = self.project(F.gelu(value) * torch.sigmoid(gate))
        return x + hidden * self.scale


class LargeKernelAttentionBlock(nn.Module):
    """NanoCodec-inspired large-kernel gated channel attention."""

    def __init__(self, channels: int, expansion: int = 2, kernel_size: int = 15) -> None:
        super().__init__()
        self.left_padding = kernel_size - 1
        self.norm = nn.LayerNorm(channels)
        self.depthwise = nn.Conv1d(
            channels, channels, kernel_size, groups=channels
        )
        hidden = channels * expansion
        self.value = nn.Linear(channels, hidden)
        self.gate = nn.Linear(channels, hidden)
        self.project = nn.Linear(hidden, channels)
        self.scale = nn.Parameter(torch.full((channels,), 1e-3))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = self.norm(x)
        context = residual.transpose(1, 2)
        context = self.depthwise(F.pad(context, (self.left_padding, 0))).transpose(1, 2)
        hidden = F.silu(self.value(residual)) * torch.sigmoid(self.gate(context))
        return x + self.project(hidden) * self.scale


class CausalLocalAttention(nn.Module):
    """Small bounded causal self-attention block used as a PosNet analogue."""

    def __init__(self, channels: int, heads: int = 4, context: int = 8) -> None:
        super().__init__()
        if channels % heads:
            raise ValueError("attention channels must be divisible by heads")
        self.heads = heads
        self.context = context
        self.head_dim = channels // heads
        self.norm = nn.LayerNorm(channels)
        self.qkv = nn.Linear(channels, channels * 3, bias=False)
        self.output = nn.Linear(channels, channels, bias=False)
        self.scale = nn.Parameter(torch.full((channels,), 1e-3))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, frames, channels = x.shape
        qkv = self.qkv(self.norm(x)).reshape(
            batch, frames, 3, self.heads, self.head_dim
        )
        query, key, value = qkv.unbind(dim=2)
        positions = torch.arange(frames, device=x.device)
        distance = positions[:, None] - positions[None, :]
        mask = (distance < 0) | (distance >= self.context)
        scores = torch.einsum("bthd,bshd->bhts", query, key) / math.sqrt(self.head_dim)
        scores = scores.masked_fill(mask.unsqueeze(0).unsqueeze(0), -torch.inf)
        attention = scores.softmax(dim=-1)
        hidden = torch.einsum("bhts,bshd->bthd", attention, value)
        hidden = hidden.reshape(batch, frames, channels)
        return x + self.output(hidden) * self.scale


class CausalSpectralAnalysis(nn.Module):
    """Causal 30-ms analysis window with a 10-ms hop and no future access."""

    def __init__(self, n_fft: int = 512, win_length: int = 480, hop_length: int = 160) -> None:
        super().__init__()
        if win_length != 480 or hop_length != 160 or n_fft < win_length:
            raise ValueError("spectral analysis must use 30-ms/10-ms causal framing")
        self.n_fft = n_fft
        self.win_length = win_length
        self.hop_length = hop_length
        self.bins = n_fft // 2 + 1
        self.register_buffer("window", torch.hann_window(win_length), persistent=False)

    def spectrum(self, waveform: torch.Tensor) -> torch.Tensor:
        padded = F.pad(waveform[:, 0], (self.win_length - self.hop_length, 0))
        frames = padded.unfold(-1, self.win_length, self.hop_length)
        windowed = frames * self.window.to(dtype=waveform.dtype)
        return torch.fft.rfft(windowed, n=self.n_fft, dim=-1)

    def features(self, waveform: torch.Tensor, mode: str) -> torch.Tensor:
        spectrum = self.spectrum(waveform)
        magnitude = spectrum.abs().clamp_min(1e-5)
        if mode == "vocodec":
            unit = spectrum / magnitude
            return torch.cat((magnitude.log(), unit.real, unit.imag), dim=-1)
        if mode in {"nanocodec", "phoenix"}:
            energy = magnitude.square().mean(dim=-1, keepdim=True).sqrt().clamp_min(1e-5)
            normalized = magnitude / energy
            return torch.cat((normalized.log(), energy.log()), dim=-1)
        raise ValueError(f"unsupported spectral feature mode: {mode}")


class SpectralEncoder(nn.Module):
    def __init__(
        self,
        channels: int,
        layers: int,
        mode: str,
        expansion: int = 2,
        attention_every: int = 0,
        use_gru: bool = False,
    ) -> None:
        super().__init__()
        self.analysis = CausalSpectralAnalysis()
        self.mode = mode
        bins = self.analysis.bins
        input_dim = bins * 3 if mode == "vocodec" else bins + 1
        self.input = nn.Linear(input_dim, channels)
        block_type = LargeKernelAttentionBlock if mode == "nanocodec" else CausalFrameBlock
        self.blocks = nn.ModuleList(
            block_type(channels, expansion=expansion) for _ in range(layers)
        )
        self.attention = nn.ModuleDict(
            {
                str(index): CausalLocalAttention(channels)
                for index in range(layers)
                if attention_every and (index + 1) % attention_every == 0
            }
        )
        self.gru = SafeGRU(channels, channels, batch_first=True) if use_gru else None

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        hidden = self.input(self.analysis.features(waveform, self.mode))
        for index, block in enumerate(self.blocks):
            hidden = block(hidden)
            if str(index) in self.attention:
                hidden = self.attention[str(index)](hidden)
        if self.gru is not None:
            hidden, _ = self.gru(hidden)
        return hidden


class SpectralDecoder(nn.Module):
    """Predict a causal synthesis spectrum and emit exactly one hop per frame."""

    def __init__(
        self,
        channels: int,
        layers: int,
        style: str = "vocodec",
        expansion: int = 2,
        attention_every: int = 0,
    ) -> None:
        super().__init__()
        self.n_fft = 512
        self.win_length = 480
        self.hop_length = 160
        self.bins = self.n_fft // 2 + 1
        block_type = LargeKernelAttentionBlock if style == "nanocodec" else CausalFrameBlock
        self.blocks = nn.ModuleList(
            block_type(channels, expansion=expansion) for _ in range(layers)
        )
        self.attention = nn.ModuleDict(
            {
                str(index): CausalLocalAttention(channels)
                for index in range(layers)
                if attention_every and (index + 1) % attention_every == 0
            }
        )
        self.output = nn.Linear(channels, self.bins * 2)

    def forward(self, embeddings: torch.Tensor) -> torch.Tensor:
        hidden = embeddings
        for index, block in enumerate(self.blocks):
            hidden = block(hidden)
            if str(index) in self.attention:
                hidden = self.attention[str(index)](hidden)
        real, imaginary = self.output(hidden).chunk(2, dim=-1)
        spectrum = torch.complex(real, imaginary)
        frames = torch.fft.irfft(spectrum, n=self.n_fft, dim=-1)[..., : self.win_length]
        hops = frames[..., -self.hop_length :]
        return torch.tanh(hops.reshape(hops.size(0), 1, -1))


class SnakeResidualUnit(nn.Module):
    def __init__(self, channels: int, dilation: int) -> None:
        super().__init__()
        self.activation1 = SnakeBeta(channels)
        self.conv1 = nn.Conv1d(channels, channels, 3, dilation=dilation)
        self.activation2 = SnakeBeta(channels)
        self.conv2 = nn.Conv1d(channels, channels, 1)
        self.padding = dilation * 2

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        hidden = self.activation1(x)
        hidden = self.conv1(F.pad(hidden, (self.padding, 0)))
        hidden = self.conv2(self.activation2(hidden))
        return x + hidden


class HybridWaveformEncoder(nn.Module):
    """Winner-inspired waveform encoder with dilated SnakeBeta residual units."""

    def __init__(self, channels: int, strides: tuple[int, ...] = (2, 4, 4, 5)) -> None:
        super().__init__()
        # Keep high-sample-rate stages narrow: their residual units dominate
        # the analytical budget even though the 100-Hz latent can stay wide.
        stage_channels = (8, 16, 32, 64, channels)
        self.input = nn.Conv1d(1, stage_channels[0], 7)
        self.blocks = nn.ModuleList()
        for in_channels, out_channels, stride in zip(
            stage_channels[:-1], stage_channels[1:], strides
        ):
            self.blocks.append(
                nn.ModuleDict(
                    {
                        "residuals": nn.Sequential(
                            SnakeResidualUnit(in_channels, 1),
                            SnakeResidualUnit(in_channels, 3),
                            SnakeResidualUnit(in_channels, 9),
                        ),
                        "downsample": nn.Conv1d(
                            in_channels, out_channels, 2 * stride, stride=stride
                        ),
                    }
                )
            )
        self.gru = SafeGRU(channels, channels, batch_first=True)

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        hidden = self.input(F.pad(waveform, (6, 0)))
        for block in self.blocks:
            hidden = block["residuals"](hidden)
            stride = block["downsample"].stride[0]
            kernel = block["downsample"].kernel_size[0]
            hidden = block["downsample"](F.pad(hidden, (kernel - stride, 0)))
        hidden, _ = self.gru(hidden.transpose(1, 2))
        return hidden


class WaveformSnakeDecoder(nn.Module):
    """Phoenix/BigCodec-inspired causal SnakeBeta waveform decoder."""

    def __init__(self, channels: int, use_gru: bool = True) -> None:
        super().__init__()
        self.gru = SafeGRU(channels, channels, batch_first=True) if use_gru else None
        # The first two synthesis stages dominate decoder compute.  These
        # widths keep the Phoenix adaptation below 300 MFLOP/s.
        stage_channels = (channels, 48, 24, 12, 8)
        strides = (5, 4, 4, 2)
        self.blocks = nn.ModuleList()
        for in_channels, out_channels, stride in zip(
            stage_channels[:-1], stage_channels[1:], strides
        ):
            self.blocks.append(
                nn.ModuleDict(
                    {
                        "activation": SnakeBeta(in_channels),
                        "upsample": nn.ConvTranspose1d(
                            in_channels, out_channels, 2 * stride, stride=stride
                        ),
                        "residuals": nn.Sequential(
                            SnakeResidualUnit(out_channels, 1),
                            SnakeResidualUnit(out_channels, 3),
                        ),
                    }
                )
            )
        self.output_activation = SnakeBeta(stage_channels[-1])
        self.output = nn.Conv1d(stage_channels[-1], 1, 7)

    def forward(self, embeddings: torch.Tensor) -> torch.Tensor:
        hidden = embeddings
        if self.gru is not None:
            hidden, _ = self.gru(hidden)
        hidden = hidden.transpose(1, 2)
        for block in self.blocks:
            hidden = block["activation"](hidden)
            hidden = block["upsample"](hidden)
            stride = block["upsample"].stride[0]
            # A 2*stride kernel creates one hop of causal overlap. Crop it so
            # that one latent frame still maps to exactly 160 output samples.
            hidden = hidden[..., stride :]
            hidden = block["residuals"](hidden)
        hidden = self.output(self.output_activation(F.pad(hidden, (6, 0))))
        return torch.tanh(hidden)
