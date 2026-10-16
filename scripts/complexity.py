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
from ssp_codec.architectures import CausalLocalAttention, CausalSpectralAnalysis, SpectralDecoder  # noqa: E402


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
            elif isinstance(module, nn.GRU):
                sequence = output[0]
                steps = sequence.numel() // module.hidden_size
                per_output = 3 * (module.input_size + module.hidden_size)
                macs[name] = macs.get(name, 0) + steps * module.hidden_size * per_output
                return
            else:
                return
            macs[name] = macs.get(name, 0) + output.numel() * per_output
        return count

    for name, module in model.named_modules():
        if isinstance(module, (nn.Conv1d, nn.ConvTranspose1d, nn.Linear, nn.GRU)):
            handles.append(module.register_forward_hook(hook(name)))
    samples = round(args.duration * 16_000)
    with torch.inference_mode():
        model(torch.zeros(1, 1, samples))
    for handle in handles:
        handle.remove()
    encoder = sum(
        value
        for name, value in macs.items()
        if name.startswith(("encoder.", "analysis_temporal."))
    )
    decoder = sum(
        value
        for name, value in macs.items()
        if name.startswith(("decoder.", "synthesis_temporal."))
    )
    quantizer_projections = sum(value for name, value in macs.items() if name.startswith("quantizer."))
    frames = (samples + 159) // 160
    # RVQ reports its approximate squared-distance lookup cost. FSQ has no
    # nearest-neighbour search and therefore returns zero here.
    quantizer_search = model.quantizer.search_macs(frames)
    encoder_auxiliary_macs = 0
    decoder_auxiliary_macs = 0
    # Count FFTs and the two attention matrix products that are not exposed as
    # Conv/Linear modules.  A conservative radix-2 estimate is used.
    for name, module in model.named_modules():
        if isinstance(module, CausalSpectralAnalysis):
            encoder_auxiliary_macs += int(frames * 2.5 * module.n_fft * module.n_fft.bit_length())
        elif isinstance(module, SpectralDecoder):
            decoder_auxiliary_macs += int(frames * 2.5 * module.n_fft * module.n_fft.bit_length())
        elif isinstance(module, CausalLocalAttention):
            attention_macs = frames * min(frames, module.context) * module.heads * module.head_dim * 2
            if name.startswith("encoder."):
                encoder_auxiliary_macs += attention_macs
            elif name.startswith("decoder."):
                decoder_auxiliary_macs += attention_macs
    raw_accounted = encoder + decoder + quantizer_projections
    unclassified = sum(macs.values()) - raw_accounted
    encoder += encoder_auxiliary_macs
    decoder += decoder_auxiliary_macs
    total_macs = sum(macs.values()) + encoder_auxiliary_macs + decoder_auxiliary_macs + quantizer_search
    report = {
        "sample_rate_hz": 16000,
        "duration_seconds": args.duration,
        "frame_samples": 160,
        "bitrate_bps": 2400,
        "encoder_mmac_per_s": encoder / args.duration / 1e6,
        "decoder_mmac_per_s": decoder / args.duration / 1e6,
        "quantizer_mmac_per_s": (quantizer_projections + quantizer_search) / args.duration / 1e6,
        "unclassified_mmac_per_s": unclassified / args.duration / 1e6,
        "total_mflop_per_s": 2 * total_macs / args.duration / 1e6,
        "decoder_mflop_per_s": 2 * decoder / args.duration / 1e6,
        # EMA codebooks are inference state stored as buffers rather than Adam
        # parameters, but must still count toward the deployed model size.
        "parameters": sum(parameter.numel() for parameter in model.parameters())
        + (
            model.quantizer.codebooks.numel()
            if hasattr(model.quantizer, "codebooks")
            else 0
        ),
        "quantizer_type": model.quantizer_type,
        "architecture": model.architecture,
        "algorithmic_delay_ms": model.algorithmic_delay_ms,
        "notes": "Counts Conv1d, ConvTranspose1d, Linear, GRU, bounded-attention products, conservative FFT estimates and approximate RVQ search. Excludes activations, normalization, padding and file I/O.",
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
