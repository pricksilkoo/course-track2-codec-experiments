#!/usr/bin/env python3
"""Average model tensors from checkpoints on one training trajectory."""

from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

import torch


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoints", nargs="+", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if len(args.checkpoints) < 2:
        raise ValueError("at least two checkpoints are required")

    states = [
        torch.load(path, map_location="cpu", weights_only=False)
        for path in args.checkpoints
    ]
    keys = list(states[0]["model"])
    for state, path in zip(states[1:], args.checkpoints[1:]):
        if list(state["model"]) != keys:
            raise ValueError(f"model state keys differ in {path}")

    averaged = {}
    for key in keys:
        values = [state["model"][key] for state in states]
        first = values[0]
        if not all(
            value.shape == first.shape and value.dtype == first.dtype
            for value in values
        ):
            raise ValueError(f"incompatible tensor for {key}")
        if first.is_floating_point():
            mean = torch.stack([value.to(torch.float64) for value in values]).mean(0)
            averaged[key] = mean.to(first.dtype)
        elif first.is_complex():
            mean = torch.stack([value.to(torch.complex128) for value in values]).mean(0)
            averaged[key] = mean.to(first.dtype)
        else:
            averaged[key] = values[-1].clone()

    output = deepcopy(states[-1])
    output["model"] = averaged
    output["averaged_checkpoints"] = [str(path) for path in args.checkpoints]
    output["averaged_global_steps"] = [
        int(state.get("global_step", -1)) for state in states
    ]
    output["global_step"] = max(output["averaged_global_steps"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(output, args.output)
    print(
        f"averaged {len(states)} checkpoints at steps "
        f"{output['averaged_global_steps']} -> {args.output}"
    )


if __name__ == "__main__":
    main()
