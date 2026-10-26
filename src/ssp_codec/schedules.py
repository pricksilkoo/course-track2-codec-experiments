"""Small, testable training schedules shared by experiment scripts."""

from __future__ import annotations


def distillation_factor(global_step: int, config: dict) -> float:
    """Return the delayed, linearly ramped teacher contribution."""
    start = int(config.get("start_step", 0))
    warmup = int(config.get("warmup_steps", 0))
    if global_step < start:
        return 0.0
    if warmup <= 0:
        return 1.0
    return min(1.0, (global_step - start + 1) / warmup)
