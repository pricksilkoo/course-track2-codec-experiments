#!/usr/bin/env python3
"""Evaluate the official Cisco LRAC 2025 Track-1 generator on 16-kHz WAVs."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import torchaudio.functional as AF
import yaml


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fit_length(audio: torch.Tensor, length: int) -> torch.Tensor:
    if audio.numel() >= length:
        return audio[:length]
    return torch.nn.functional.pad(audio, (0, length - audio.numel()))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--espnet-root", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--bandwidths", type=float, nargs="+", default=[1.0, 3.0, 6.0])
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()

    sys.path.insert(0, str(args.espnet_root))
    from espnet2.gan_codec.lrac.lrac import LRACGenerator

    train_config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    codec_config = train_config["codec_conf"]
    model = LRACGenerator(
        sample_rate=codec_config["sampling_rate"],
        encoder_params=codec_config["encoder_params"],
        decoder_params=codec_config["decoder_params"],
        quantizer_params=codec_config["quantizer_params"],
    )
    released = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    prefix = "codec.generator."
    generator_state = {
        key[len(prefix):]: value for key, value in released.items() if key.startswith(prefix)
    }
    model.load_state_dict(generator_state, strict=True)
    device = torch.device(args.device)
    model = model.to(device).eval()

    inputs = sorted(args.input_dir.rglob("*.wav"))
    if not inputs:
        raise RuntimeError(f"No WAV files under {args.input_dir}")

    metadata = {
        "model": "Cisco LRAC 2025 Track-1 official baseline",
        "checkpoint": str(args.checkpoint),
        "checkpoint_sha256": sha256(args.checkpoint),
        "source_commit": subprocess.check_output(
            ["git", "-C", str(args.espnet_root), "rev-parse", "HEAD"], text=True
        ).strip(),
        "source_sample_rate_hz": 24000,
        "evaluation_sample_rate_hz": 16000,
        "latent_frame_rate_hz": 100,
        "bandwidths_kbps": args.bandwidths,
        "files": len(inputs),
        "adapter": "torchaudio sinc 16k->24k->16k resampling; exact length restored",
    }
    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )

    with torch.inference_mode():
        for bandwidth in args.bandwidths:
            label = f"{bandwidth:g}kbps"
            output_dir = args.output_root / label / "reconstructed"
            output_dir.mkdir(parents=True, exist_ok=True)
            code_shapes = []
            for index, input_path in enumerate(inputs, 1):
                relative = input_path.relative_to(args.input_dir)
                output_path = output_dir / relative
                output_path.parent.mkdir(parents=True, exist_ok=True)
                audio, sample_rate = sf.read(input_path, dtype="float32", always_2d=False)
                if sample_rate != 16000 or audio.ndim != 1:
                    raise RuntimeError(f"Expected mono 16-kHz WAV: {input_path}")
                source = torch.from_numpy(np.asarray(audio)).to(device)
                model_input = AF.resample(source, 16000, 24000)
                codes = model.encode(model_input[None, None], target_bw=bandwidth)
                reconstruction = fit_length(model.decode(codes).reshape(-1), model_input.numel())
                reconstruction = fit_length(AF.resample(reconstruction, 24000, 16000), source.numel())
                sf.write(output_path, reconstruction.cpu().numpy(), 16000, subtype="PCM_16")
                code_shapes.append(list(codes.shape))
                if index % 20 == 0 or index == len(inputs):
                    print(f"{label}: {index}/{len(inputs)}", flush=True)
            stages = int(code_shapes[0][0])
            mode_metadata = {
                "requested_bandwidth_kbps": bandwidth,
                "actual_rvq_stages": stages,
                "nominal_bitrate_bps": stages * 10 * 100,
                "first_code_shape": code_shapes[0],
            }
            (args.output_root / label / "codec_metadata.json").write_text(
                json.dumps(mode_metadata, indent=2) + "\n", encoding="utf-8"
            )


if __name__ == "__main__":
    main()
