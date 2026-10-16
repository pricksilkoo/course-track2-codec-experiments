#!/usr/bin/env python3
"""Run the official Kyutai Mimi checkpoint on fixed local validation audio."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import soundfile as sf
import torch
import torchaudio
from moshi.models import loaders


ROOT = Path("/storage1/hehaoran/project/course-track2-codec-experiments")
DEFAULT_MANIFEST = ROOT / "data/manifests/vctk_libritts/valid.scp"
DEFAULT_WEIGHT = ROOT / "third_party/checkpoints/mimi/tokenizer-e351c8d8-checkpoint125.safetensors"
DEFAULT_OUTPUT = ROOT / "third_party/outputs/mimi_eval"
REFERENCE_RATE = 16_000
MIMI_RATE = 24_000
CODEBOOK_BINS = 2048


def resample(waveform: torch.Tensor, source_rate: int, target_rate: int) -> torch.Tensor:
    if source_rate == target_rate:
        return waveform
    return torchaudio.functional.resample(waveform, source_rate, target_rate)


def exact_length(waveform: torch.Tensor, length: int) -> torch.Tensor:
    if waveform.shape[-1] < length:
        waveform = torch.nn.functional.pad(waveform, (0, length - waveform.shape[-1]))
    return waveform[..., :length]


def select_paths(manifest: Path, count: int) -> list[Path]:
    paths = [Path(line.strip()) for line in manifest.read_text().splitlines() if line.strip()]
    if len(paths) < count:
        raise ValueError(f"manifest has only {len(paths)} files, requested {count}")
    # Even spacing avoids selecting only one speaker from a sorted manifest.
    indices = [round(i * (len(paths) - 1) / (count - 1)) for i in range(count)] if count > 1 else [0]
    selected = [paths[index] for index in indices]
    missing = [str(path) for path in selected if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing selected audio: {missing[:3]}")
    return selected


def save_wav(path: Path, waveform: torch.Tensor, sample_rate: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    audio = waveform.squeeze().clamp(-1.0, 1.0).cpu().numpy()
    sf.write(path, audio, sample_rate, subtype="PCM_16")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--weight", type=Path, default=DEFAULT_WEIGHT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--num-files", type=int, default=20)
    parser.add_argument("--codebooks", type=int, nargs="+", default=[8, 17])
    parser.add_argument("--device", default="cuda:0")
    args = parser.parse_args()

    if not args.weight.is_file():
        raise FileNotFoundError(args.weight)
    if args.num_files < 1:
        raise ValueError("num-files must be positive")
    if any(value < 1 or value > 32 for value in args.codebooks):
        raise ValueError("Mimi supports between 1 and 32 codebooks")

    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA is unavailable")
    # This server's torch 2.11 / cuDNN 9.19 pairing cannot create cuDNN
    # handles. Native CUDA convolution kernels work correctly and were also
    # used by the course codec experiments on this host.
    if device.type == "cuda":
        torch.backends.cudnn.enabled = False

    paths = select_paths(args.manifest, args.num_files)
    args.output.mkdir(parents=True, exist_ok=True)
    model = loaders.get_mimi(args.weight, device=device)
    model.eval()

    rows: list[dict] = []
    total_source_seconds = 0.0
    total_encode_seconds = {value: 0.0 for value in args.codebooks}
    total_decode_seconds = {value: 0.0 for value in args.codebooks}
    total_frames = {value: 0 for value in args.codebooks}

    with torch.inference_mode():
        for item_index, source_path in enumerate(paths):
            waveform, source_rate = torchaudio.load(source_path)
            waveform = waveform.mean(dim=0, keepdim=True)
            reference = resample(waveform, source_rate, REFERENCE_RATE)
            mimi_input = resample(reference, REFERENCE_RATE, MIMI_RATE).unsqueeze(0).to(device)
            source_seconds = reference.shape[-1] / REFERENCE_RATE
            total_source_seconds += source_seconds
            name = f"{item_index:03d}_{source_path.stem}.wav"
            save_wav(args.output / "reference" / name, reference, REFERENCE_RATE)

            row = {
                "index": item_index,
                "source": str(source_path),
                "source_rate": source_rate,
                "seconds": source_seconds,
                "output_name": name,
            }
            for num_codebooks in args.codebooks:
                model.set_num_codebooks(num_codebooks)
                if device.type == "cuda":
                    torch.cuda.synchronize(device)
                started = time.perf_counter()
                codes = model.encode(mimi_input)
                if device.type == "cuda":
                    torch.cuda.synchronize(device)
                encoded_at = time.perf_counter()
                decoded = model.decode(codes)
                if device.type == "cuda":
                    torch.cuda.synchronize(device)
                decoded_at = time.perf_counter()

                decoded = exact_length(decoded, mimi_input.shape[-1])
                reconstructed = resample(decoded.squeeze(0).cpu(), MIMI_RATE, REFERENCE_RATE)
                reconstructed = exact_length(reconstructed, reference.shape[-1])
                save_wav(
                    args.output / f"reconstructed_{num_codebooks}q" / name,
                    reconstructed,
                    REFERENCE_RATE,
                )
                code_path = args.output / f"codes_{num_codebooks}q" / f"{Path(name).stem}.pt"
                code_path.parent.mkdir(parents=True, exist_ok=True)
                torch.save(codes.cpu(), code_path)

                encode_seconds = encoded_at - started
                decode_seconds = decoded_at - encoded_at
                total_encode_seconds[num_codebooks] += encode_seconds
                total_decode_seconds[num_codebooks] += decode_seconds
                total_frames[num_codebooks] += codes.shape[-1]
                row[f"frames_{num_codebooks}q"] = int(codes.shape[-1])
                row[f"encode_seconds_{num_codebooks}q"] = encode_seconds
                row[f"decode_seconds_{num_codebooks}q"] = decode_seconds
            rows.append(row)
            print(f"[{item_index + 1}/{len(paths)}] {source_path.name}", flush=True)

    bits_per_index = math.ceil(math.log2(CODEBOOK_BINS))
    variants = {}
    for num_codebooks in args.codebooks:
        variants[f"{num_codebooks}q"] = {
            "num_codebooks": num_codebooks,
            "codebook_bins": CODEBOOK_BINS,
            "bits_per_index": bits_per_index,
            "frame_rate_hz": loaders.FRAME_RATE,
            "nominal_bitrate_bps": num_codebooks * bits_per_index * loaders.FRAME_RATE,
            "encoded_frames": total_frames[num_codebooks],
            "encode_seconds": total_encode_seconds[num_codebooks],
            "decode_seconds": total_decode_seconds[num_codebooks],
            "encode_realtime_factor": total_encode_seconds[num_codebooks] / total_source_seconds,
            "decode_realtime_factor": total_decode_seconds[num_codebooks] / total_source_seconds,
        }

    checkpoint_sha256 = hashlib.sha256(args.weight.read_bytes()).hexdigest()
    summary = {
        "model": "Kyutai Mimi",
        "source_repository": "https://github.com/kyutai-labs/moshi",
        "checkpoint_repository": "kyutai/moshiko-pytorch-bf16",
        "checkpoint": str(args.weight),
        "checkpoint_sha256": checkpoint_sha256,
        "device": str(device),
        "mimi_sample_rate": MIMI_RATE,
        "reference_sample_rate": REFERENCE_RATE,
        "files": len(paths),
        "source_seconds": total_source_seconds,
        "variants": variants,
        "items": rows,
    }
    (args.output / "run_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (args.output / "selected_files.txt").write_text("\n".join(str(path) for path in paths) + "\n")
    print(json.dumps({key: value for key, value in summary.items() if key != "items"}, indent=2))


if __name__ == "__main__":
    main()
