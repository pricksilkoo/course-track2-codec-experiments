"""Time-domain convolutional neural codec used by the course baseline.

The structure uses a compact encoder, RVQ, and decoder at a fixed course
operating point: waveform convolutional encoder, residual vector quantizer,
and waveform transposed-convolution decoder.  It is deliberately fixed to
16 kHz and a 160-sample (10 ms) embedding rate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import torch
import torch.distributed as dist
import torch.nn.functional as F
from torch import nn

from .minimimi import (
    LookaheadFusion,
    MiniSEANetDecoder,
    MiniSEANetEncoder,
    MiniTransformerStack,
)


SAMPLE_RATE = 16_000
FRAME_SAMPLES = 160
BITS_PER_FRAME = 24


class CausalConv1d(nn.Module):
    """A length-preserving causal 1-D convolution."""

    def __init__(self, in_channels: int, out_channels: int, kernel_size: int) -> None:
        super().__init__()
        self.left_padding = kernel_size - 1
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(F.pad(x, (self.left_padding, 0)))


class ResidualUnit(nn.Module):
    """Two causal convolutions with ELU activations and a skip connection."""

    def __init__(self, channels: int, kernel_size: int) -> None:
        super().__init__()
        self.conv1 = CausalConv1d(channels, channels, kernel_size)
        self.conv2 = CausalConv1d(channels, channels, kernel_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = F.elu(self.conv1(x))
        residual = self.conv2(residual)
        return F.elu(x + residual)


class ResidualStack(nn.Module):
    def __init__(self, channels: int, num_blocks: int, kernel_size: int) -> None:
        super().__init__()
        self.blocks = nn.Sequential(
            *(ResidualUnit(channels, kernel_size) for _ in range(num_blocks))
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.blocks(x)


class CausalTemporalUnit(nn.Module):
    """A lightweight depthwise-separable causal block at the latent frame rate."""

    def __init__(
        self,
        channels: int,
        kernel_size: int,
        dilation: int,
        expansion: int,
    ) -> None:
        super().__init__()
        if kernel_size < 2 or dilation < 1 or expansion < 1:
            raise ValueError("invalid temporal block configuration")
        self.left_padding = dilation * (kernel_size - 1)
        self.depthwise = nn.Conv1d(
            channels,
            channels,
            kernel_size,
            dilation=dilation,
            groups=channels,
        )
        hidden = channels * expansion
        self.expand = nn.Conv1d(channels, hidden, kernel_size=1)
        self.project = nn.Conv1d(hidden, channels, kernel_size=1)
        # Start as an exact identity block. This permits stable warm-starting
        # from a codec checkpoint that predates temporal modeling.
        nn.init.zeros_(self.project.weight)
        nn.init.zeros_(self.project.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = self.depthwise(F.pad(x, (self.left_padding, 0)))
        residual = self.project(F.gelu(self.expand(residual)))
        return x + residual


class LimitedLookaheadUnit(nn.Module):
    """Inject at most ``frames`` future latent frames through a residual path."""

    def __init__(self, channels: int, frames: int) -> None:
        super().__init__()
        if frames < 1:
            raise ValueError("lookahead frames must be positive")
        self.frames = frames
        self.depthwise = nn.Conv1d(
            channels,
            channels,
            kernel_size=frames + 1,
            groups=channels,
            bias=False,
        )
        self.project = nn.Conv1d(channels, channels, kernel_size=1)
        nn.init.zeros_(self.project.weight)
        nn.init.zeros_(self.project.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Right padding means output frame t can observe input [t, t + frames]
        # but never anything beyond the configured algorithmic lookahead.
        future = self.depthwise(F.pad(x, (0, self.frames)))
        return x + self.project(F.gelu(future))


class CausalTemporalStack(nn.Module):
    """Optional causal temporal modeling over ``[batch, frames, channels]``."""

    def __init__(
        self,
        channels: int,
        layers: int,
        kernel_size: int = 3,
        expansion: int = 2,
        lookahead_frames: int = 0,
    ) -> None:
        super().__init__()
        if layers < 0:
            raise ValueError("temporal layers must be non-negative")
        if lookahead_frames < 0:
            raise ValueError("lookahead frames must be non-negative")
        self.lookahead = (
            LimitedLookaheadUnit(channels, lookahead_frames)
            if lookahead_frames
            else nn.Identity()
        )
        self.blocks = nn.ModuleList(
            CausalTemporalUnit(
                channels,
                kernel_size=kernel_size,
                dilation=2 ** (index % 8),
                expansion=expansion,
            )
            for index in range(layers)
        )

    def forward(self, embeddings: torch.Tensor) -> torch.Tensor:
        hidden = embeddings.transpose(1, 2)
        hidden = self.lookahead(hidden)
        for block in self.blocks:
            hidden = block(hidden)
        return hidden.transpose(1, 2)


class WaveformEncoder(nn.Module):
    """Four-stage residual convolutional encoder with 160-sample stride."""

    def __init__(
        self,
        channels: Iterable[int],
        strides: Iterable[int],
        residual_blocks: int,
        residual_kernel_size: int,
    ) -> None:
        super().__init__()
        channels = list(channels)
        strides = list(strides)
        if len(channels) != len(strides) + 1:
            raise ValueError("encoder channels must contain one more value than strides")
        self.input_conv = CausalConv1d(1, channels[0], kernel_size=7)
        self.blocks = nn.ModuleList()
        for in_channels, out_channels, stride in zip(channels[:-1], channels[1:], strides):
            self.blocks.append(
                nn.ModuleDict(
                    {
                        "residual": ResidualStack(
                            in_channels, residual_blocks, residual_kernel_size
                        ),
                        "downsample": nn.Conv1d(
                            in_channels,
                            out_channels,
                            kernel_size=stride,
                            stride=stride,
                        ),
                    }
                )
            )

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        x = F.elu(self.input_conv(waveform))
        for block in self.blocks:
            x = block["downsample"](block["residual"](x))
        return x.transpose(1, 2)


class WaveformDecoder(nn.Module):
    """Four-stage transposed-convolution decoder with no implicit overlap-add."""

    def __init__(
        self,
        channels: Iterable[int],
        strides: Iterable[int],
        residual_blocks: int,
        residual_kernel_size: int,
    ) -> None:
        super().__init__()
        channels = list(channels)
        strides = list(strides)
        if len(channels) != len(strides) + 1:
            raise ValueError("decoder channels must contain one more value than strides")
        self.blocks = nn.ModuleList()
        for in_channels, out_channels, stride in zip(channels[:-1], channels[1:], strides):
            self.blocks.append(
                nn.ModuleDict(
                    {
                        "upsample": nn.ConvTranspose1d(
                            in_channels,
                            out_channels,
                            kernel_size=stride,
                            stride=stride,
                        ),
                        "residual": ResidualStack(
                            out_channels, residual_blocks, residual_kernel_size
                        ),
                    }
                )
            )
        self.output_conv = CausalConv1d(channels[-1], 1, kernel_size=7)

    def forward(self, embeddings: torch.Tensor) -> torch.Tensor:
        x = embeddings.transpose(1, 2)
        for block in self.blocks:
            x = F.elu(block["upsample"](x))
            x = block["residual"](x)
        return torch.tanh(self.output_conv(x))


class ResidualVectorQuantizer(nn.Module):
    """EMA residual VQ with k-means initialization and dead-code replacement."""

    def __init__(
        self,
        embedding_dim: int,
        num_codebooks: int = 3,
        codebook_size: int = 256,
        codebook_dim: int = 160,
        commitment_weight: float = 0.25,
        usage_loss_weight: float = 0.0,
        usage_temperature: float = 0.1,
        ema_decay: float = 0.99,
        dead_code_threshold: float = 0.5,
        dead_code_after_updates: int = 100,
        kmeans_iterations: int = 10,
    ) -> None:
        super().__init__()
        if num_codebooks < 1 or codebook_size != 256:
            raise ValueError("RVQ requires one or more 256-entry codebooks")
        if codebook_dim < 1:
            raise ValueError("codebook_dim must be positive")
        if not 0.0 < ema_decay < 1.0:
            raise ValueError("ema_decay must be between zero and one")
        self.embedding_dim = embedding_dim
        self.num_codebooks = num_codebooks
        self.codebook_size = codebook_size
        self.codebook_dim = codebook_dim
        self.commitment_weight = commitment_weight
        # Retained only so older checkpoint configurations can still be loaded.
        # The differentiable usage loss was removed because its low-temperature
        # gradient dominated reconstruction and drove the latent scale upward.
        self.usage_loss_weight = 0.0
        self.ema_decay = ema_decay
        self.dead_code_threshold = dead_code_threshold
        self.dead_code_after_updates = dead_code_after_updates
        self.kmeans_iterations = kmeans_iterations
        # A low-dimensional lookup space is often substantially easier to
        # populate than a large codebook in the full encoder dimension. Keep
        # Identity modules at the baseline setting so old checkpoints remain
        # state-dict compatible.
        self.input_projection: nn.Module = (
            nn.Identity()
            if codebook_dim == embedding_dim
            else nn.Linear(embedding_dim, codebook_dim, bias=False)
        )
        self.output_projection: nn.Module = (
            nn.Identity()
            if codebook_dim == embedding_dim
            else nn.Linear(codebook_dim, embedding_dim, bias=False)
        )
        # EMA VQ codebooks are buffers: they are updated from assignments rather
        # than by Adam gradients. This avoids the early one-codeword collapse seen
        # with the original small, randomly initialized projected codebooks.
        self.register_buffer("codebooks", torch.zeros(num_codebooks, codebook_size, codebook_dim))
        self.register_buffer("ema_cluster_size", torch.zeros(num_codebooks, codebook_size))
        self.register_buffer(
            "ema_embed_sum", torch.zeros(num_codebooks, codebook_size, codebook_dim)
        )
        self.register_buffer("initialized", torch.tensor(False))
        self.register_buffer("update_count", torch.zeros((), dtype=torch.long))

    @property
    def bits_per_frame(self) -> int:
        return self.num_codebooks * 8

    def _distances(self, values: torch.Tensor, stage: int) -> torch.Tensor:
        table = self.codebooks[stage]
        return (
            values.square().sum(dim=-1, keepdim=True)
            - 2 * values @ table.t()
            + table.square().sum(dim=-1)
        )

    def _lookup(self, values: torch.Tensor, stage: int) -> tuple[torch.Tensor, torch.Tensor]:
        distance = self._distances(values, stage)
        indices = distance.argmin(dim=-1)
        return F.embedding(indices, self.codebooks[stage]), indices

    @staticmethod
    def _distributed() -> bool:
        return dist.is_available() and dist.is_initialized()

    @torch.no_grad()
    def _kmeans(self, values: torch.Tensor) -> torch.Tensor:
        """Return ``codebook_size`` centroids from one local first-batch sample."""
        values = values.reshape(-1, self.codebook_dim)
        if values.size(0) == 0:
            raise ValueError("cannot initialize a codebook from an empty batch")
        if values.size(0) < self.codebook_size:
            repeat = (self.codebook_size + values.size(0) - 1) // values.size(0)
            values = values.repeat(repeat, 1)
        values = values[: min(values.size(0), 4096)]
        centroids = values[torch.randperm(values.size(0), device=values.device)[: self.codebook_size]].clone()
        for _ in range(self.kmeans_iterations):
            distance = (
                values.square().sum(dim=-1, keepdim=True)
                - 2 * values @ centroids.t()
                + centroids.square().sum(dim=-1)
            )
            assignments = distance.argmin(dim=-1)
            counts = torch.bincount(assignments, minlength=self.codebook_size)
            sums = torch.zeros_like(centroids)
            sums.index_add_(0, assignments, values)
            nonempty = counts > 0
            centroids[nonempty] = sums[nonempty] / counts[nonempty].unsqueeze(1)
            if (~nonempty).any():
                replacements = torch.randint(
                    values.size(0), (int((~nonempty).sum()),), device=values.device
                )
                centroids[~nonempty] = values[replacements]
        return centroids

    @torch.no_grad()
    def _initialize_codebooks(self, embeddings: torch.Tensor) -> None:
        """Initialize all residual stages before their first assignment."""
        residual = embeddings.detach()
        for stage in range(self.num_codebooks):
            codebook = self._kmeans(residual)
            self.codebooks[stage].copy_(codebook)
            self.ema_cluster_size[stage].fill_(1.0)
            self.ema_embed_sum[stage].copy_(codebook)
            codeword, _ = self._lookup(residual, stage)
            residual = residual - codeword
        self.initialized.fill_(True)
        if self._distributed():
            # Each rank has a different first batch. Rank zero supplies one
            # deterministic initialization to every worker before EMA updates.
            for value in (
                self.codebooks,
                self.ema_cluster_size,
                self.ema_embed_sum,
                self.initialized,
            ):
                dist.broadcast(value, src=0)

    @torch.no_grad()
    def _ema_update(self, stage: int, values: torch.Tensor, indices: torch.Tensor) -> None:
        flat_values = values.reshape(-1, self.codebook_dim)
        flat_indices = indices.reshape(-1)
        counts = torch.bincount(flat_indices, minlength=self.codebook_size).to(flat_values.dtype)
        sums = torch.zeros_like(self.ema_embed_sum[stage])
        sums.index_add_(0, flat_indices, flat_values)
        if self._distributed():
            dist.all_reduce(counts, op=dist.ReduceOp.SUM)
            dist.all_reduce(sums, op=dist.ReduceOp.SUM)
        self.ema_cluster_size[stage].mul_(self.ema_decay).add_(counts, alpha=1 - self.ema_decay)
        self.ema_embed_sum[stage].mul_(self.ema_decay).add_(sums, alpha=1 - self.ema_decay)
        total_count = self.ema_cluster_size[stage].sum()
        smoothed_count = (
            (self.ema_cluster_size[stage] + 1e-5)
            / (total_count + self.codebook_size * 1e-5)
            * total_count
        )
        self.codebooks[stage].copy_(self.ema_embed_sum[stage] / smoothed_count.unsqueeze(1))

        if self.update_count.item() >= self.dead_code_after_updates:
            dead = self.ema_cluster_size[stage] < self.dead_code_threshold
            if dead.any():
                # Use live encoder residuals for replacement, then synchronize
                # the selected values and their EMA state under DDP.
                if not self._distributed() or dist.get_rank() == 0:
                    replacement_indices = torch.arange(
                        int(dead.sum()), device=flat_values.device
                    ) % flat_values.size(0)
                    replacements = flat_values[replacement_indices]
                    self.codebooks[stage, dead] = replacements
                    self.ema_embed_sum[stage, dead] = replacements * self.dead_code_threshold
                    self.ema_cluster_size[stage, dead] = self.dead_code_threshold
                if self._distributed():
                    for value in (
                        self.codebooks[stage],
                        self.ema_cluster_size[stage],
                        self.ema_embed_sum[stage],
                    ):
                        dist.broadcast(value, src=0)

    @torch.no_grad()
    def usage_metrics(self) -> dict[str, list[float] | list[int]]:
        """EMA-smoothed RVQ occupancy, suitable for checkpoint logging."""
        active = (self.ema_cluster_size >= self.dead_code_threshold).sum(dim=1)
        probabilities = self.ema_cluster_size / self.ema_cluster_size.sum(dim=1, keepdim=True).clamp_min(1e-12)
        perplexity = torch.exp(-(probabilities * probabilities.clamp_min(1e-12).log()).sum(dim=1))
        return {
            "active_codes": [int(value) for value in active.cpu()],
            "perplexity": [float(value) for value in perplexity.cpu()],
        }

    def forward(self, embeddings: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if embeddings.ndim != 3:
            raise ValueError("embeddings must have shape [batch, frames, channels]")
        projected = self.input_projection(embeddings)
        if self.training and not bool(self.initialized):
            self._initialize_codebooks(projected)
        residual = projected
        quantized = torch.zeros_like(projected)
        all_indices = []
        commitment = embeddings.new_zeros(())
        first_stage_codeword = None
        for stage in range(self.num_codebooks):
            codeword, indices = self._lookup(residual, stage)
            if stage == 0:
                first_stage_codeword = codeword
            commitment = commitment + F.mse_loss(residual, codeword.detach())
            if self.training:
                self._ema_update(stage, residual.detach(), indices)
            quantized = quantized + codeword
            residual = projected - quantized
            all_indices.append(indices)
        if self.training:
            self.update_count.add_(1)
        indices = torch.stack(all_indices, dim=-1)
        loss = self.commitment_weight * commitment
        straight_through = projected + (quantized - projected).detach()
        if first_stage_codeword is None:
            raise RuntimeError("RVQ must contain at least one codebook")
        # A straight-through view of codebook zero lets a training-only
        # semantic teacher shape the encoder while preserving the exact RVQ
        # lookup and the three-byte inference bitstream.
        self.last_first_stage_latent = projected + (
            first_stage_codeword - projected
        ).detach()
        # Split-RVQ semantic distillation consumes this projected latent only
        # during training. It is neither transmitted nor required at inference.
        self.last_quantized_latent = straight_through
        return self.output_projection(straight_through), indices, loss

    def decode(self, indices: torch.Tensor) -> torch.Tensor:
        if indices.ndim != 3 or indices.size(-1) != self.num_codebooks:
            raise ValueError("indices must have shape [batch, frames, 3]")
        quantized = torch.zeros(
            *indices.shape[:-1], self.codebook_dim, device=indices.device, dtype=self.codebooks.dtype
        )
        for stage in range(self.num_codebooks):
            quantized = quantized + F.embedding(indices[..., stage], self.codebooks[stage])
        return self.output_projection(quantized)

    def search_macs(self, frames: int) -> int:
        """Approximate nearest-neighbour search cost used by complexity.py."""
        return frames * self.num_codebooks * self.codebook_size * self.codebook_dim * 3


class SplitResidualVectorQuantizer(nn.Module):
    """One semantic codebook plus two acoustic residual codebooks.

    Both branches reconstruct the common latent dimension and are fused by a
    learned projection. Only their three uint8 indices cross the bitstream.
    """

    def __init__(
        self,
        embedding_dim: int,
        semantic_dim: int = 32,
        acoustic_dim: int = 64,
        commitment_weight: float = 0.1,
        ema_decay: float = 0.99,
        dead_code_threshold: float = 0.5,
        dead_code_after_updates: int = 100,
        kmeans_iterations: int = 10,
    ) -> None:
        super().__init__()
        common = dict(
            embedding_dim=embedding_dim,
            codebook_size=256,
            commitment_weight=commitment_weight,
            ema_decay=ema_decay,
            dead_code_threshold=dead_code_threshold,
            dead_code_after_updates=dead_code_after_updates,
            kmeans_iterations=kmeans_iterations,
        )
        self.semantic = ResidualVectorQuantizer(
            num_codebooks=1, codebook_dim=semantic_dim, **common
        )
        self.acoustic = ResidualVectorQuantizer(
            num_codebooks=2, codebook_dim=acoustic_dim, **common
        )
        self.fusion = nn.Linear(2 * embedding_dim, embedding_dim, bias=False)
        self.semantic_dim = semantic_dim

    @property
    def bits_per_frame(self) -> int:
        return 24

    def forward(self, embeddings: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        semantic, semantic_indices, semantic_loss = self.semantic(embeddings)
        acoustic, acoustic_indices, acoustic_loss = self.acoustic(embeddings)
        self.last_semantic_latent = self.semantic.last_quantized_latent
        fused = self.fusion(torch.cat((semantic, acoustic), dim=-1))
        return (
            fused,
            torch.cat((semantic_indices, acoustic_indices), dim=-1),
            semantic_loss + acoustic_loss,
        )

    def decode(self, indices: torch.Tensor) -> torch.Tensor:
        if indices.ndim != 3 or indices.shape[-1] != 3:
            raise ValueError("split RVQ indices must have shape [batch, frames, 3]")
        semantic = self.semantic.decode(indices[..., :1])
        acoustic = self.acoustic.decode(indices[..., 1:])
        return self.fusion(torch.cat((semantic, acoustic), dim=-1))

    @torch.no_grad()
    def usage_metrics(self) -> dict[str, list[float] | list[int]]:
        semantic = self.semantic.usage_metrics()
        acoustic = self.acoustic.usage_metrics()
        return {
            "active_codes": semantic["active_codes"] + acoustic["active_codes"],
            "perplexity": semantic["perplexity"] + acoustic["perplexity"],
        }

    def search_macs(self, frames: int) -> int:
        return self.semantic.search_macs(frames) + self.acoustic.search_macs(frames)


class FiniteScalarQuantizer(nn.Module):
    """A fixed 24-bit FSQ bottleneck packed into three transmitted bytes.

    The product of ``levels`` must be exactly 2**24. For example, eight
    dimensions with eight levels each use 8 * 3 = 24 bits per frame.
    """

    def __init__(self, embedding_dim: int, levels: Iterable[int]) -> None:
        super().__init__()
        parsed = tuple(int(level) for level in levels)
        if not parsed or any(level < 2 for level in parsed):
            raise ValueError("FSQ levels must contain integers >= 2")
        product = 1
        basis = []
        for level in parsed:
            basis.append(product)
            product *= level
        if product != 2**BITS_PER_FRAME:
            raise ValueError("FSQ levels must define exactly 24 bits per frame")
        self.embedding_dim = embedding_dim
        self.level_values = parsed
        self.input_projection = nn.Linear(embedding_dim, len(parsed), bias=False)
        self.output_projection = nn.Linear(len(parsed), embedding_dim, bias=False)
        self.register_buffer("levels", torch.tensor(parsed, dtype=torch.long))
        self.register_buffer("basis", torch.tensor(basis, dtype=torch.long))

    @property
    def bits_per_frame(self) -> int:
        return BITS_PER_FRAME

    def _quantize(self, values: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        levels = self.levels.to(device=values.device, dtype=values.dtype)
        scaled = (torch.tanh(values) + 1.0) * 0.5 * (levels - 1.0)
        rounded = scaled + (scaled.round() - scaled).detach()
        normalized = 2.0 * rounded / (levels - 1.0) - 1.0
        return normalized, rounded.detach().to(torch.long)

    def _pack(self, digits: torch.Tensor) -> torch.Tensor:
        code = (digits * self.basis.to(digits.device)).sum(dim=-1)
        return torch.stack(
            (code & 255, (code >> 8) & 255, (code >> 16) & 255), dim=-1
        )

    def _unpack(self, indices: torch.Tensor) -> torch.Tensor:
        if indices.ndim != 3 or indices.size(-1) != 3:
            raise ValueError("indices must have shape [batch, frames, 3]")
        code = indices[..., 0] | (indices[..., 1] << 8) | (indices[..., 2] << 16)
        return (code.unsqueeze(-1) // self.basis.to(code.device)) % self.levels.to(code.device)

    def forward(self, embeddings: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        projected = self.input_projection(embeddings)
        quantized, digits = self._quantize(projected)
        reconstructed = self.output_projection(quantized)
        return reconstructed, self._pack(digits), embeddings.new_zeros(())

    def decode(self, indices: torch.Tensor) -> torch.Tensor:
        digits = self._unpack(indices)
        levels = self.levels.to(device=indices.device, dtype=self.output_projection.weight.dtype)
        normalized = 2.0 * digits.to(levels.dtype) / (levels - 1.0) - 1.0
        return self.output_projection(normalized)

    @torch.no_grad()
    def usage_metrics(self) -> dict[str, list[float] | list[int]]:
        return {"active_codes": [], "perplexity": []}

    @staticmethod
    def search_macs(frames: int) -> int:
        del frames
        return 0


@dataclass(frozen=True)
class CodecSpecification:
    sample_rate: int = SAMPLE_RATE
    frame_samples: int = FRAME_SAMPLES
    bits_per_frame: int = BITS_PER_FRAME


class CourseCodec(nn.Module):
    """The complete fixed-16-kHz / fixed-2.4-kbps neural codec baseline."""

    def __init__(
        self,
        sample_rate: int = SAMPLE_RATE,
        frame_samples: int = FRAME_SAMPLES,
        encoder_channels: Iterable[int] = (8, 16, 32, 64, 160),
        encoder_strides: Iterable[int] = (2, 4, 4, 5),
        decoder_channels: Iterable[int] = (160, 48, 24, 12, 8),
        decoder_strides: Iterable[int] = (5, 4, 4, 2),
        residual_blocks: int = 3,
        residual_kernel_size: int = 3,
        rvq_num_codebooks: int = 3,
        rvq_codebook_size: int = 256,
        rvq_codebook_dim: int = 160,
        commitment_weight: float = 0.25,
        rvq_usage_loss_weight: float = 0.0,
        rvq_usage_temperature: float = 0.1,
        rvq_ema_decay: float = 0.99,
        rvq_dead_code_threshold: float = 0.5,
        rvq_dead_code_after_updates: int = 100,
        rvq_kmeans_iterations: int = 10,
        quantizer_type: str = "rvq",
        fsq_levels: Iterable[int] = (8, 8, 8, 8, 8, 8, 8, 8),
        encoder_temporal_layers: int = 0,
        decoder_temporal_layers: int = 0,
        temporal_kernel_size: int = 3,
        temporal_expansion: int = 2,
        encoder_lookahead_frames: int = 0,
        decoder_lookahead_frames: int = 0,
        temporal_model: str = "tcn",
        temporal_transformer_heads: int = 4,
        temporal_transformer_ffn_dim: int = 128,
        encoder_history_frames: int = 16,
        decoder_history_frames: int = 16,
        architecture: str = "baseline",
        minimimi_encoder_channels: Iterable[int] = (12, 24, 48, 96, 192),
        minimimi_decoder_channels: Iterable[int] = (128, 64, 32, 16, 8),
        minimimi_latent_dim: int = 128,
        minimimi_residual_compression: int = 2,
        minimimi_downsample_overlap: int = 2,
        minimimi_upsample_overlap: int = 1,
        minimimi_encoder_transformer_layers: int = 3,
        minimimi_decoder_transformer_layers: int = 3,
        minimimi_transformer_heads: int = 4,
        minimimi_transformer_ffn_dim: int = 256,
        minimimi_encoder_history_frames: int = 128,
        minimimi_decoder_history_frames: int = 128,
        minimimi_hybrid_kernel_size: int = 0,
        minimimi_semantic_dim: int = 32,
        minimimi_acoustic_dim: int = 64,
    ) -> None:
        super().__init__()
        encoder_channels = tuple(encoder_channels)
        encoder_strides = tuple(encoder_strides)
        decoder_channels = tuple(decoder_channels)
        decoder_strides = tuple(decoder_strides)
        if sample_rate != SAMPLE_RATE or frame_samples != FRAME_SAMPLES:
            raise ValueError("this baseline is fixed to 16 kHz and 160 samples per frame")
        if torch.tensor(encoder_strides).prod().item() != frame_samples:
            raise ValueError("encoder strides must multiply to 160 samples")
        if torch.tensor(decoder_strides).prod().item() != frame_samples:
            raise ValueError("decoder strides must multiply to 160 samples")
        if encoder_channels[-1] != decoder_channels[0]:
            raise ValueError("encoder output and decoder input dimensions must agree")
        if encoder_lookahead_frames < 0 or decoder_lookahead_frames < 0:
            raise ValueError("lookahead frames must be non-negative")
        if encoder_lookahead_frames + decoder_lookahead_frames > 3:
            raise ValueError("total codec lookahead cannot exceed three 10-ms frames")
        self.specification = CodecSpecification()
        self.architecture = architecture
        self.temporal_model = temporal_model
        self.algorithmic_lookahead_frames = (
            encoder_lookahead_frames + decoder_lookahead_frames
        )
        if architecture == "minimimi":
            if decoder_lookahead_frames:
                raise ValueError("MiniMimi decoder must remain strictly causal")
            if tuple(encoder_strides) != (2, 4, 4, 5):
                raise ValueError("MiniMimi encoder strides must remain [2, 4, 4, 5]")
            if tuple(decoder_strides) != (5, 4, 4, 2):
                raise ValueError("MiniMimi decoder strides must remain [5, 4, 4, 2]")
            self.encoder = MiniSEANetEncoder(
                minimimi_encoder_channels,
                encoder_strides,
                minimimi_latent_dim,
                residual_compression=minimimi_residual_compression,
                downsample_overlap=minimimi_downsample_overlap,
            )
            self.latent_norm = nn.LayerNorm(minimimi_latent_dim, elementwise_affine=False)
            self.lookahead_fusion = LookaheadFusion(
                minimimi_latent_dim, encoder_lookahead_frames
            )
            self.analysis_transformer = MiniTransformerStack(
                minimimi_latent_dim,
                minimimi_encoder_transformer_layers,
                minimimi_transformer_heads,
                minimimi_transformer_ffn_dim,
                minimimi_encoder_history_frames,
                minimimi_hybrid_kernel_size,
            )
            if quantizer_type == "rvq":
                self.quantizer = ResidualVectorQuantizer(
                    embedding_dim=minimimi_latent_dim,
                    num_codebooks=rvq_num_codebooks,
                    codebook_size=rvq_codebook_size,
                    codebook_dim=rvq_codebook_dim,
                    commitment_weight=commitment_weight,
                    usage_loss_weight=rvq_usage_loss_weight,
                    usage_temperature=rvq_usage_temperature,
                    ema_decay=rvq_ema_decay,
                    dead_code_threshold=rvq_dead_code_threshold,
                    dead_code_after_updates=rvq_dead_code_after_updates,
                    kmeans_iterations=rvq_kmeans_iterations,
                )
            elif quantizer_type == "split_rvq":
                self.quantizer = SplitResidualVectorQuantizer(
                    embedding_dim=minimimi_latent_dim,
                    semantic_dim=minimimi_semantic_dim,
                    acoustic_dim=minimimi_acoustic_dim,
                    commitment_weight=commitment_weight,
                    ema_decay=rvq_ema_decay,
                    dead_code_threshold=rvq_dead_code_threshold,
                    dead_code_after_updates=rvq_dead_code_after_updates,
                    kmeans_iterations=rvq_kmeans_iterations,
                )
            else:
                raise ValueError("MiniMimi supports rvq or split_rvq quantization")
            self.quantizer_type = quantizer_type
            self.synthesis_transformer = MiniTransformerStack(
                minimimi_latent_dim,
                minimimi_decoder_transformer_layers,
                minimimi_transformer_heads,
                minimimi_transformer_ffn_dim,
                minimimi_decoder_history_frames,
                minimimi_hybrid_kernel_size,
            )
            self.decoder = MiniSEANetDecoder(
                minimimi_decoder_channels,
                decoder_strides,
                minimimi_latent_dim,
                residual_compression=minimimi_residual_compression,
                upsample_overlap=minimimi_upsample_overlap,
            )
            return
        if architecture != "baseline":
            raise ValueError(f"unsupported codec architecture: {architecture}")
        self.encoder = WaveformEncoder(
            encoder_channels, encoder_strides, residual_blocks, residual_kernel_size
        )
        # Fixed per-frame normalization prevents the encoder and EMA codebooks
        # from reducing loss by inflating their absolute scale. With no affine
        # parameters, each latent frame remains centered with unit variance.
        self.latent_norm = nn.LayerNorm(
            encoder_channels[-1], elementwise_affine=False
        )
        if temporal_model == "tcn":
            self.analysis_temporal = CausalTemporalStack(
                encoder_channels[-1],
                layers=encoder_temporal_layers,
                kernel_size=temporal_kernel_size,
                expansion=temporal_expansion,
                lookahead_frames=encoder_lookahead_frames,
            )
        elif temporal_model == "transformer":
            if decoder_lookahead_frames:
                raise ValueError("Transformer decoder must remain strictly causal")
            self.lookahead_fusion = LookaheadFusion(
                encoder_channels[-1], encoder_lookahead_frames
            )
            self.analysis_transformer = MiniTransformerStack(
                encoder_channels[-1],
                encoder_temporal_layers,
                temporal_transformer_heads,
                temporal_transformer_ffn_dim,
                encoder_history_frames,
            )
        else:
            raise ValueError(f"unsupported temporal_model: {temporal_model}")
        if quantizer_type == "rvq":
            self.quantizer: nn.Module = ResidualVectorQuantizer(
                embedding_dim=encoder_channels[-1],
                num_codebooks=rvq_num_codebooks,
                codebook_size=rvq_codebook_size,
                codebook_dim=rvq_codebook_dim,
                commitment_weight=commitment_weight,
                usage_loss_weight=rvq_usage_loss_weight,
                usage_temperature=rvq_usage_temperature,
                ema_decay=rvq_ema_decay,
                dead_code_threshold=rvq_dead_code_threshold,
                dead_code_after_updates=rvq_dead_code_after_updates,
                kmeans_iterations=rvq_kmeans_iterations,
            )
        elif quantizer_type == "fsq":
            self.quantizer = FiniteScalarQuantizer(encoder_channels[-1], fsq_levels)
        else:
            raise ValueError(f"unsupported quantizer_type: {quantizer_type}")
        self.quantizer_type = quantizer_type
        if temporal_model == "tcn":
            self.synthesis_temporal = CausalTemporalStack(
                encoder_channels[-1],
                layers=decoder_temporal_layers,
                kernel_size=temporal_kernel_size,
                expansion=temporal_expansion,
                lookahead_frames=decoder_lookahead_frames,
            )
        else:
            self.synthesis_transformer = MiniTransformerStack(
                encoder_channels[-1],
                decoder_temporal_layers,
                temporal_transformer_heads,
                temporal_transformer_ffn_dim,
                decoder_history_frames,
            )
        self.decoder = WaveformDecoder(
            decoder_channels, decoder_strides, residual_blocks, residual_kernel_size
        )

    @staticmethod
    def pad_to_frame(waveform: torch.Tensor) -> tuple[torch.Tensor, int]:
        samples = waveform.size(-1)
        padding = (-samples) % FRAME_SAMPLES
        return F.pad(waveform, (0, padding)), padding

    def encode(self, waveform: torch.Tensor) -> torch.Tensor:
        if waveform.ndim == 2:
            waveform = waveform.unsqueeze(1)
        if waveform.ndim != 3 or waveform.size(1) != 1:
            raise ValueError("waveform must have shape [batch, 1, samples]")
        padded, _ = self.pad_to_frame(waveform)
        if self.architecture == "minimimi" or self.temporal_model == "transformer":
            embeddings = self.analysis_transformer(
                self.lookahead_fusion(self.latent_norm(self.encoder(padded)))
            )
        else:
            embeddings = self.analysis_temporal(self.latent_norm(self.encoder(padded)))
        _, indices, _ = self.quantizer(embeddings)
        return indices

    def decode(self, indices: torch.Tensor, length: int | None = None) -> torch.Tensor:
        embeddings = self.quantizer.decode(indices)
        if self.architecture == "minimimi" or self.temporal_model == "transformer":
            embeddings = self.synthesis_transformer(embeddings)
        else:
            embeddings = self.synthesis_temporal(embeddings)
        waveform = self.decoder(embeddings)
        return waveform[..., :length] if length is not None else waveform

    def forward(
        self, waveform: torch.Tensor, return_aux: bool = False
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor] | tuple[
        torch.Tensor, torch.Tensor, torch.Tensor, dict[str, torch.Tensor]
    ]:
        if waveform.ndim == 2:
            waveform = waveform.unsqueeze(1)
        if waveform.ndim != 3 or waveform.size(1) != 1:
            raise ValueError("waveform must have shape [batch, 1, samples]")
        original_length = waveform.size(-1)
        padded, _ = self.pad_to_frame(waveform)
        if self.architecture == "minimimi" or self.temporal_model == "transformer":
            embeddings = self.analysis_transformer(
                self.lookahead_fusion(self.latent_norm(self.encoder(padded)))
            )
        else:
            embeddings = self.analysis_temporal(self.latent_norm(self.encoder(padded)))
        quantized, indices, quantizer_loss = self.quantizer(embeddings)
        if self.architecture == "minimimi" or self.temporal_model == "transformer":
            reconstructed = self.decoder(self.synthesis_transformer(quantized))[
                ..., :original_length
            ]
        else:
            reconstructed = self.decoder(self.synthesis_temporal(quantized))[
                ..., :original_length
            ]
        if return_aux:
            auxiliary: dict[str, torch.Tensor] = {}
            if isinstance(self.quantizer, SplitResidualVectorQuantizer):
                auxiliary["semantic"] = self.quantizer.last_semantic_latent
            elif isinstance(self.quantizer, ResidualVectorQuantizer):
                auxiliary["semantic"] = self.quantizer.last_first_stage_latent
            return reconstructed, indices, quantizer_loss, auxiliary
        return reconstructed, indices, quantizer_loss
