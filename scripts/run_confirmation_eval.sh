#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: $0 NAME GPU_ID CHECKPOINT" >&2
  exit 2
fi
NAME="$1"
GPU_ID="$2"
CHECKPOINT="$3"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
PYTHON="$REPO_ROOT/.venv-codec/bin/python"
REFERENCE="$REPO_ROOT/runs/confirmation_libritts_test_400/reference"
OUTPUT="$REPO_ROOT/runs/confirmation_libritts_test_400/$NAME"
export PYTHONNOUSERSITE=1
export TORCH_HOME="${TORCH_HOME:-$REPO_ROOT/data/torch-cache}"
mkdir -p "$OUTPUT"
exec > >(tee -a "$OUTPUT/pipeline.log") 2>&1
test -f "$REFERENCE/CONFIRMATION_SET_READY"
test -f "$CHECKPOINT"
if [[ -f "$OUTPUT/EVALUATION_COMPLETE" ]]; then
  echo "$NAME already complete"
  exit 0
fi
CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/encode.py --checkpoint "$CHECKPOINT" \
  --input-dir "$REFERENCE" --output-dir "$OUTPUT/bitstreams" --device cuda
CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/decode.py --checkpoint "$CHECKPOINT" \
  --bitstream-dir "$OUTPUT/bitstreams" --output-dir "$OUTPUT/reconstructed" --device cuda
"$PYTHON" scripts/validate_submission.py --input-dir "$REFERENCE" \
  --bitstream-dir "$OUTPUT/bitstreams" --output-dir "$OUTPUT/reconstructed"
CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/evaluate.py --reference-dir "$REFERENCE" \
  --reconstructed-dir "$OUTPUT/reconstructed" --output-dir "$OUTPUT/metrics" --device cuda
"$PYTHON" scripts/complexity.py --checkpoint "$CHECKPOINT" --output "$OUTPUT/complexity.json"
sha256sum "$CHECKPOINT" > "$OUTPUT/checkpoint.sha256"
touch "$OUTPUT/EVALUATION_COMPLETE"
echo "$NAME confirmation evaluation complete"
