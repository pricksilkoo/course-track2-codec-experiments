#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
DATA_ROOT="$REPO_ROOT/data/corpora"
DOWNLOAD_DIR="$DATA_ROOT/.downloads"
OUTPUT_DIR="$REPO_ROOT/runs/confirmation_libritts_test_400/reference"
PYTHON="$REPO_ROOT/.venv-codec/bin/python"
mkdir -p "$DOWNLOAD_DIR" "$OUTPUT_DIR"

free_gib() {
  df -BG --output=avail "$DATA_ROOT" | awk 'NR == 2 {gsub(/G/, "", $1); print $1}'
}

download_and_extract() {
  local split="$1"
  local checksum="$2"
  local target="$DATA_ROOT/LibriTTS/$split"
  local archive="$DOWNLOAD_DIR/$split.tar.gz"
  local url="https://openslr.magicdatatech.com/resources/60/$split.tar.gz"
  if [[ -n "$(find "$target" -type f -name '*.wav' -print -quit 2>/dev/null)" ]]; then
    echo "Reusing LibriTTS/$split"
    return
  fi
  if (( $(free_gib) < 30 )); then
    echo "Disk-safety stop before $split: less than 30 GiB free" >&2
    exit 70
  fi
  wget --continue --inet4-only --retry-connrefused --read-timeout=30 --timeout=30 \
    --tries=0 --progress=dot:giga --output-document="$archive" "$url"
  printf '%s  %s\n' "$checksum" "$archive" | md5sum --check --status
  tar -xzf "$archive" -C "$DATA_ROOT"
  [[ -n "$(find "$target" -type f -name '*.wav' -print -quit)" ]]
  rm -f -- "$archive"
}

download_and_extract test-clean 7bed3bdb047c4c197f1ad3bc412db59f
download_and_extract test-other ae3258249472a13b5abef2a816f733e4

if [[ ! -f "$OUTPUT_DIR/CONFIRMATION_SET_READY" ]]; then
  "$PYTHON" scripts/prepare_confirmation_set.py \
    --test-clean "$DATA_ROOT/LibriTTS/test-clean" \
    --test-other "$DATA_ROOT/LibriTTS/test-other" \
    --output-dir "$OUTPUT_DIR" --per-split 200 --seed 20261022
  touch "$OUTPUT_DIR/CONFIRMATION_SET_READY"
fi
echo "Confirmation set ready: $OUTPUT_DIR (free space: $(free_gib) GiB)"
