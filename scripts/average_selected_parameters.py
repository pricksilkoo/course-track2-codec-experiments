#!/usr/bin/env python3
"""Average selected floating-point model tensors while preserving base state."""

from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

import torch


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoints", nargs="+", required=True, type=Path)
    parser.add_argument("--base-checkpoint", required=True, type=Path)
    parser.add_argument("--include-prefix", action="append", required=True)
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
    base = torch.load(args.base_checkpoint, map_location="cpu", weights_only=False)
    keys = list(base["model"])
    selected = [key for key in keys if key.startswith(tuple(args.include_prefix))]
    if not selected:
        raise ValueError("no model tensors matched the requested prefixes")

    for state, path in zip(states, args.checkpoints):
        if list(state["model"]) != keys:
            raise ValueError(f"model state keys differ in {path}")

    output = deepcopy(base)
    for key in selected:
        values = [state["model"][key] for state in states]
        first = values[0]
        if not all(
            value.shape == first.shape and value.dtype == first.dtype
            for value in values
        ):
            raise ValueError(f"incompatible tensor for {key}")
        if first.is_floating_point():
            mean = torch.stack([value.to(torch.float64) for value in values]).mean(0)
            output["model"][key] = mean.to(first.dtype)
        elif first.is_complex():
            mean = torch.stack([value.to(torch.complex128) for value in values]).mean(0)
            output["model"][key] = mean.to(first.dtype)
        else:
            output["model"][key] = values[-1].clone()

    output["parameter_average"] = {
        "checkpoints": [str(path) for path in args.checkpoints],
        "global_steps": [int(state.get("global_step", -1)) for state in states],
        "base_checkpoint": str(args.base_checkpoint),
        "include_prefixes": list(args.include_prefix),
        "selected_tensor_count": len(selected),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(output, args.output)
    print(
        f"averaged {len(selected)} selected tensors from steps "
        f"{output['parameter_average']['global_steps']} -> {args.output}"
    )


if __name__ == "__main__":
    main()
