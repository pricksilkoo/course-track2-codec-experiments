#!/usr/bin/env python3
"""Create the shared, never-trained initialization for the lookahead study."""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ssp_codec.adversarial import MultiResolutionSTFTDiscriminator  # noqa: E402
from ssp_codec.config import load_config  # noqa: E402
from ssp_codec.model import CourseCodec  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    seed = int(config["seed"])
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    model = CourseCodec(**config["model"])
    discriminator = MultiResolutionSTFTDiscriminator(
        config["adversarial"]["resolutions"],
        config["adversarial"].get("periods", ()),
    )
    state = {
        "global_step": 0,
        "trained": False,
        "seed": seed,
        "model_config": config["model"],
        "model": model.state_dict(),
        "discriminator": discriminator.state_dict(),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(state, output)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"created untrained step-0 initialization: {output}")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
