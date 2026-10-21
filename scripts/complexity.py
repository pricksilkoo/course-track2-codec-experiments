#!/usr/bin/env python3
"""Report analytical Conv/Linear MAC counts for the course baseline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
from torch import nn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ssp_codec.model import CourseCodec  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", help="optional checkpoint; model configuration is read from it")
    parser.add_argument("--config", help="optional YAML config for a model that has not been trained yet")
    parser.add_argument("--duration", type=float, default=1.0)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    if args.checkpoint and args.config:
        parser.error("provide at most one of --checkpoint and --config")
    if args.duration <= 0:
        raise ValueError("duration must be positive")
    if args.checkpoint:
        state = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
        model = CourseCodec(**state["model_config"])
    elif args.config:
        from ssp_codec.config import load_config

        model = CourseCodec(**load_config(args.config)["model"])
    else:
        model = CourseCodec()
    macs: dict[str, int] = {}
    handles = []

    def hook(name: str):
        def count(module: nn.Module, inputs: tuple[torch.Tensor], output: torch.Tensor) -> None:
            if isinstance(module, nn.Conv1d):
                kernel = module.kernel_size[0]
                per_output = (module.in_channels // module.groups) * kernel
            elif isinstance(module, nn.ConvTranspose1d):
                kernel = module.kernel_size[0]
                per_output = (module.in_channels // module.groups) * kernel
            elif isinstance(module, nn.Linear):
                per_output = module.in_features
            else:
                return
            macs[name] = macs.get(name, 0) + output.numel() * per_output
        return count

    for name, module in model.named_modules():
        if isinstance(module, (nn.Conv1d, nn.ConvTranspose1d, nn.Linear)):
            handles.append(module.register_forward_hook(hook(name)))
    samples = round(args.duration * 16_000)
    with torch.inference_mode():
        model(torch.zeros(1, 1, samples))
    for handle in handles:
        handle.remove()
    encoder = sum(
        value
        for name, value in macs.items()
        if name.startswith(
            ("encoder.", "analysis_temporal.", "lookahead_fusion.", "analysis_transformer.")
        )
    )
    decoder = sum(
        value
        for name, value in macs.items()
        if name.startswith(("decoder.", "synthesis_temporal.", "synthesis_transformer."))
    )
    quantizer_projections = sum(value for name, value in macs.items() if name.startswith("quantizer."))
    frames = (samples + 159) // 160
    encoder_attention = 0
    decoder_attention = 0
    for name, module in model.named_modules():
        if module.__class__.__name__ != "LocalCausalSelfAttention":
            continue
        window = min(frames, int(module.history_frames))
        # QK^T and attention-value products, each with dimension d_model.
        attention_macs = 2 * frames * window * int(module.dimension)
        if name.startswith("analysis_transformer."):
            encoder_attention += attention_macs
        elif name.startswith("synthesis_transformer."):
            decoder_attention += attention_macs
    encoder += encoder_attention
    decoder += decoder_attention
    # RVQ reports its approximate squared-distance lookup cost. FSQ has no
    # nearest-neighbour search and therefore returns zero here.
    quantizer_search = model.quantizer.search_macs(frames)
    accounted_linear_conv = (
        encoder - encoder_attention
        + decoder - decoder_attention
        + quantizer_projections
    )
    unclassified = sum(macs.values()) - accounted_linear_conv
    report = {
        "sample_rate_hz": 16000,
        "duration_seconds": args.duration,
        "frame_samples": 160,
        "bitrate_bps": 2400,
        "encoder_mmac_per_s": encoder / args.duration / 1e6,
        "decoder_mmac_per_s": decoder / args.duration / 1e6,
        "quantizer_mmac_per_s": (quantizer_projections + quantizer_search) / args.duration / 1e6,
        "unclassified_mmac_per_s": unclassified / args.duration / 1e6,
        "total_mflop_per_s": 2
        * (
            sum(macs.values())
            + quantizer_search
            + encoder_attention
            + decoder_attention
        )
        / args.duration
        / 1e6,
        "decoder_mflop_per_s": 2 * decoder / args.duration / 1e6,
        # EMA codebooks are inference state stored as buffers rather than Adam
        # parameters, but must still count toward the deployed model size.
        "parameters": sum(parameter.numel() for parameter in model.parameters())
        + sum(
            value.numel()
            for name, value in model.quantizer.named_buffers()
            if name.endswith("codebooks")
        ),
        "quantizer_type": model.quantizer_type,
        "algorithmic_lookahead_ms": int(
            10 * getattr(model, "algorithmic_lookahead_frames", 0)
        ),
        "notes": "Counts Conv1d, ConvTranspose1d, Linear, bounded attention QK/AV and approximate RVQ nearest-neighbour search. FSQ scalar rounding is reported as zero MACs. Excludes activations, normalization, padding and file I/O.",
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
