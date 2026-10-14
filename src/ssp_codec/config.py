"""Composable YAML configuration helpers for codec experiments."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge dictionaries without mutating either input."""
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def load_config(path: str | Path, _seen: set[Path] | None = None) -> dict[str, Any]:
    """Load YAML with an optional relative ``_base_`` configuration."""
    path = Path(path).resolve()
    seen = set() if _seen is None else _seen
    if path in seen:
        raise ValueError(f"cyclic config inheritance involving {path}")
    seen.add(path)
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(config, dict):
        raise ValueError(f"configuration root must be a mapping: {path}")
    base_reference = config.pop("_base_", None)
    if base_reference is None:
        return config
    base_path = (path.parent / str(base_reference)).resolve()
    return deep_merge(load_config(base_path, seen), config)


def apply_overrides(config: dict[str, Any], overrides: list[str]) -> dict[str, Any]:
    """Apply repeatable ``dotted.path=value`` CLI overrides."""
    result = deepcopy(config)
    for expression in overrides:
        if "=" not in expression:
            raise ValueError(f"override must be key=value: {expression}")
        dotted_key, raw_value = expression.split("=", 1)
        keys = [part for part in dotted_key.split(".") if part]
        if not keys:
            raise ValueError(f"invalid override key: {expression}")
        current: dict[str, Any] = result
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                raise KeyError(f"unknown config path: {dotted_key}")
            current = current[key]
        if keys[-1] not in current:
            raise KeyError(f"unknown config key: {dotted_key}")
        current[keys[-1]] = yaml.safe_load(raw_value)
    return result
