#!/usr/bin/env python3
"""Download the single official Mimi tokenizer checkpoint."""

from pathlib import Path

from huggingface_hub import hf_hub_download


ROOT = Path("/storage1/hehaoran/project/course-track2-codec-experiments")
TARGET = ROOT / "third_party/checkpoints/mimi"


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    path = hf_hub_download(
        repo_id="kyutai/moshiko-pytorch-bf16",
        filename="tokenizer-e351c8d8-checkpoint125.safetensors",
        local_dir=TARGET,
    )
    print(Path(path).resolve(), flush=True)


if __name__ == "__main__":
    main()
