#!/usr/bin/env python3
"""Measure RVQ occupancy, joint entropy, residual energy, and stagewise gains."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import math
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import torch.nn.functional as F


def entropy_from_counts(counts: np.ndarray) -> float:
    counts = np.asarray(counts, dtype=np.float64)
    probabilities = counts[counts > 0] / counts.sum()
    return float(-(probabilities * np.log2(probabilities)).sum())


def entropy_from_counter(counts: Counter) -> float:
    return entropy_from_counts(np.fromiter(counts.values(), dtype=np.int64))


def effective_mass_codes(counts: np.ndarray, mass: float) -> int:
    ordered = np.sort(np.asarray(counts, dtype=np.int64))[::-1]
    return int(np.searchsorted(np.cumsum(ordered), ordered.sum() * mass) + 1)


def si_snr(estimate: torch.Tensor, reference: torch.Tensor) -> torch.Tensor:
    reference = reference - reference.mean(dim=-1, keepdim=True)
    estimate = estimate - estimate.mean(dim=-1, keepdim=True)
    projection = (
        (estimate * reference).sum(dim=-1, keepdim=True)
        * reference
        / reference.square().sum(dim=-1, keepdim=True).clamp_min(1e-8)
    )
    noise = estimate - projection
    return 10.0 * torch.log10(
        projection.square().sum(dim=-1).clamp_min(1e-8)
        / noise.square().sum(dim=-1).clamp_min(1e-8)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--max-files", type=int)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "src"))
    from ssp_codec.io import load_codec
    from ssp_codec.losses import multiscale_spectral_loss
    from ssp_codec.model import ResidualVectorQuantizer

    device = torch.device(args.device)
    model, state = load_codec(args.checkpoint, device)
    if not isinstance(model.quantizer, ResidualVectorQuantizer):
        raise TypeError("diagnostics currently require ResidualVectorQuantizer")
    quantizer = model.quantizer
    files = sorted(
        path
        for path in Path(args.input_dir).rglob("*")
        if path.suffix.lower() in {".wav", ".flac"}
    )
    if args.max_files is not None:
        files = files[: args.max_files]
    if not files:
        raise ValueError("input directory contains no audio files")

    histograms = np.zeros((quantizer.num_codebooks, quantizer.codebook_size), dtype=np.int64)
    pair_counts: Counter = Counter()
    triple_counts: Counter = Counter()
    residual_before = np.zeros(quantizer.num_codebooks, dtype=np.float64)
    residual_after = np.zeros(quantizer.num_codebooks, dtype=np.float64)
    residual_elements = np.zeros(quantizer.num_codebooks, dtype=np.int64)
    partial_l1 = np.zeros(quantizer.num_codebooks, dtype=np.float64)
    partial_spectral = np.zeros(quantizer.num_codebooks, dtype=np.float64)
    partial_si_snr = np.zeros(quantizer.num_codebooks, dtype=np.float64)
    total_samples = 0
    total_frames = 0

    with torch.inference_mode():
        for file_index, path in enumerate(files, start=1):
            audio, sample_rate = sf.read(path, dtype="float32", always_2d=True)
            if sample_rate != 16_000:
                raise ValueError(f"{path}: expected 16 kHz, got {sample_rate}")
            waveform = torch.from_numpy(audio.mean(axis=1).copy()).to(device)[None, None]
            original_length = waveform.shape[-1]
            padded, _ = model.pad_to_frame(waveform)
            if model.architecture == "minimimi" or model.temporal_model == "transformer":
                embeddings = model.analysis_transformer(
                    model.lookahead_fusion(model.latent_norm(model.encoder(padded)))
                )
            else:
                embeddings = model.analysis_temporal(model.latent_norm(model.encoder(padded)))
            projected = quantizer.input_projection(embeddings)
            residual = projected
            cumulative = torch.zeros_like(projected)
            index_columns = []
            stage_codewords = []
            for stage in range(quantizer.num_codebooks):
                codeword, indices = quantizer._lookup(residual, stage)
                residual_before[stage] += float(residual.double().square().sum().cpu())
                residual_elements[stage] += residual.numel()
                cumulative = cumulative + codeword
                residual = projected - cumulative
                residual_after[stage] += float(residual.double().square().sum().cpu())
                index_columns.append(indices)
                stage_codewords.append(codeword)
                flat = indices.reshape(-1).cpu().numpy()
                histograms[stage] += np.bincount(flat, minlength=quantizer.codebook_size)

            stacked = torch.stack(index_columns, dim=-1).reshape(-1, quantizer.num_codebooks)
            index_array = stacked.cpu().numpy()
            pair_counts.update(map(tuple, index_array[:, :2].tolist()))
            triple_counts.update(map(tuple, index_array.tolist()))
            total_frames += index_array.shape[0]

            cumulative = torch.zeros_like(projected)
            for stage, codeword in enumerate(stage_codewords):
                cumulative = cumulative + codeword
                quantized = quantizer.output_projection(cumulative)
                if model.architecture == "minimimi" or model.temporal_model == "transformer":
                    decoded = model.decoder(model.synthesis_transformer(quantized))
                else:
                    decoded = model.decoder(model.synthesis_temporal(quantized))
                decoded = decoded[..., :original_length]
                partial_l1[stage] += float(F.l1_loss(decoded, waveform, reduction="sum").cpu())
                partial_spectral[stage] += float(
                    multiscale_spectral_loss(decoded, waveform, [256, 512, 1024], 0.25, 0.1).cpu()
                )
                partial_si_snr[stage] += float(si_snr(decoded, waveform).mean().cpu())
            total_samples += original_length
            if file_index % 20 == 0 or file_index == len(files):
                print(f"processed {file_index}/{len(files)} files", flush=True)

    marginal_entropy = [entropy_from_counts(row) for row in histograms]
    pair_entropy = entropy_from_counter(pair_counts)
    joint_entropy = entropy_from_counter(triple_counts)
    occupancy = []
    for stage, counts in enumerate(histograms):
        probabilities = counts / counts.sum()
        occupancy.append(
            {
                "stage": stage + 1,
                "active_codes": int((counts > 0).sum()),
                "perplexity": float(2.0 ** marginal_entropy[stage]),
                "entropy_bits": marginal_entropy[stage],
                "top1_fraction": float(probabilities.max()),
                "top10_fraction": float(np.sort(probabilities)[-10:].sum()),
                "codes_for_95pct_mass": effective_mass_codes(counts, 0.95),
                "codes_for_99pct_mass": effective_mass_codes(counts, 0.99),
            }
        )

    before_mse = residual_before / residual_elements
    after_mse = residual_after / residual_elements
    residual_report = [
        {
            "stage": stage + 1,
            "mse_before": float(before_mse[stage]),
            "mse_after": float(after_mse[stage]),
            "relative_reduction": float(1.0 - after_mse[stage] / before_mse[stage]),
            "relative_to_original_after": float(after_mse[stage] / before_mse[0]),
        }
        for stage in range(quantizer.num_codebooks)
    ]
    reconstruction = [
        {
            "stages": stage + 1,
            "nominal_bitrate_bps": (stage + 1) * 800,
            "waveform_l1": float(partial_l1[stage] / total_samples),
            "spectral_loss_mean_per_file": float(partial_spectral[stage] / len(files)),
            "si_snr_db_mean_per_file": float(partial_si_snr[stage] / len(files)),
        }
        for stage in range(quantizer.num_codebooks)
    ]
    report = {
        "checkpoint": str(Path(args.checkpoint).resolve()),
        "files": len(files),
        "samples": total_samples,
        "frames": total_frames,
        "occupancy": occupancy,
        "entropy": {
            "marginal_bits": marginal_entropy,
            "sum_marginal_bits": float(sum(marginal_entropy)),
            "naive_plugin_joint_stage12_bits": pair_entropy,
            "naive_plugin_joint_stage123_bits": joint_entropy,
            "naive_plugin_conditional_stage2_given_stage1_bits": pair_entropy - marginal_entropy[0],
            "naive_plugin_conditional_stage3_given_stage12_bits": joint_entropy - pair_entropy,
            "naive_plugin_interstage_redundancy_bits": float(sum(marginal_entropy) - joint_entropy),
            "joint_entropy_caveat": (
                "Sparse plug-in joint entropy is downward-biased and capped by log2(frames); "
                "do not interpret 24 minus this estimate as unused capacity."
            ),
        },
        "residual_quantization": residual_report,
        "partial_reconstruction": reconstruction,
        "checkpoint_global_step": state.get("global_step"),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
