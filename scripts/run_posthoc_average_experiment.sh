#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -ne 4 ]]; then
  echo "usage: $0 RUN_NAME GPU_ID CONFIG_PATH SOURCE_RUN" >&2
  exit 2
fi

RUN_NAME="$1"
GPU_ID="$2"
CONFIG_PATH="$3"
SOURCE_RUN="$4"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

RUN_DIR="$REPO_ROOT/runs/$RUN_NAME"
SOURCE_DIR="$REPO_ROOT/runs/$SOURCE_RUN"
MANIFEST_DIR="$REPO_ROOT/data/manifests/vctk_libritts"
VALIDATION_DIR="$REPO_ROOT/runs/fast_b64_2s_v1/validation_200"
EVAL_DIR="$RUN_DIR/evaluation"
PIPELINE_LOG="$RUN_DIR/pipeline.log"
PYTHON="$REPO_ROOT/.venv-codec/bin/python"
export PYTHONNOUSERSITE=1

mkdir -p "$RUN_DIR/checkpoints" "$EVAL_DIR"
exec > >(tee -a "$PIPELINE_LOG") 2>&1

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

record() {
  local status="$1"
  local note="${2:-}"
  local args=(
    --name "$RUN_NAME" --status "$status"
    --config "$REPO_ROOT/$CONFIG_PATH" --run-dir "$RUN_DIR"
    --dataset-summary "$MANIFEST_DIR/summary.json"
    --evaluation-summary "$EVAL_DIR/metrics/summary.json"
    --complexity-summary "$EVAL_DIR/complexity.json"
    --output "$REPO_ROOT/EXPERIMENT_LOG.md"
  )
  [[ -n "$note" ]] && args+=(--note "$note")
  ( flock -x 9; "$PYTHON" scripts/record_experiment.py "${args[@]}"; ) \
    9>"$REPO_ROOT/.experiment_log.lock" || true
}

on_error() {
  local code="$1"
  local line="$2"
  trap - ERR
  log "Experiment failed with exit code $code at line $line"
  record failed "Exit code $code at line $line; see $PIPELINE_LOG"
  exit "$code"
}
trap 'on_error $? $LINENO' ERR

if [[ -f "$RUN_DIR/PIPELINE_COMPLETE" ]]; then
  log "Pipeline already complete"
  exit 0
fi

test -x "$PYTHON"
test -d "$SOURCE_DIR"
test -d "$VALIDATION_DIR"
AVAILABLE_KB="$(df -Pk "$REPO_ROOT" | awk 'NR==2 {print $4}')"
if (( AVAILABLE_KB < 20 * 1024 * 1024 )); then
  log "Disk-safety stop: less than 20 GiB remains"
  record failed "Disk-safety stop before evaluation"
  exit 1
fi

log "Preflight complexity validation for $CONFIG_PATH"
"$PYTHON" scripts/complexity.py \
  --config "$CONFIG_PATH" --output "$RUN_DIR/preflight_complexity.json"
"$PYTHON" -c '
import json, sys
r = json.load(open(sys.argv[1]))
assert r["bitrate_bps"] == 2400, r
assert r["algorithmic_lookahead_ms"] <= 30, r
assert r["total_mflop_per_s"] <= 700, r
assert r["decoder_mflop_per_s"] <= 300, r
' "$RUN_DIR/preflight_complexity.json"

record running "post-hoc decoder-only average of stable checkpoints"
if [[ ! -f "$RUN_DIR/AVERAGE_COMPLETE" ]]; then
  inputs=(
    "$SOURCE_DIR/checkpoints/step_00020000.pt"
    "$SOURCE_DIR/checkpoints/step_00025000.pt"
    "$SOURCE_DIR/checkpoints/step_00030000.pt"
  )
  for checkpoint in "${inputs[@]}"; do test -f "$checkpoint"; done
  "$PYTHON" scripts/average_selected_parameters.py \
    --checkpoints "${inputs[@]}" \
    --base-checkpoint "$SOURCE_DIR/checkpoints/step_00030000.pt" \
    --include-prefix decoder. \
    --output "$RUN_DIR/checkpoints/best.pt"
  cp "$SOURCE_DIR/metrics.jsonl" "$RUN_DIR/metrics.jsonl"
  touch "$RUN_DIR/AVERAGE_COMPLETE"
fi

CHECKPOINT="$RUN_DIR/checkpoints/best.pt"
log "Encoding and decoding the fixed 200-file development set"
CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/encode.py \
  --checkpoint "$CHECKPOINT" --input-dir "$VALIDATION_DIR" \
  --output-dir "$EVAL_DIR/bitstreams" --device cuda
CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/decode.py \
  --checkpoint "$CHECKPOINT" --bitstream-dir "$EVAL_DIR/bitstreams" \
  --output-dir "$EVAL_DIR/reconstructed" --device cuda
"$PYTHON" scripts/validate_submission.py \
  --input-dir "$VALIDATION_DIR" --bitstream-dir "$EVAL_DIR/bitstreams" \
  --output-dir "$EVAL_DIR/reconstructed"

CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/evaluate.py \
  --reference-dir "$VALIDATION_DIR" --reconstructed-dir "$EVAL_DIR/reconstructed" \
  --output-dir "$EVAL_DIR/metrics" --device cuda
"$PYTHON" scripts/complexity.py \
  --checkpoint "$CHECKPOINT" --output "$EVAL_DIR/complexity.json"
CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/diagnose_rvq.py \
  --checkpoint "$CHECKPOINT" --input-dir "$VALIDATION_DIR" \
  --output "$RUN_DIR/rvq_diagnostics.json" --device cuda

record complete "post-hoc decoder-only stable-window average completed"
touch "$RUN_DIR/PIPELINE_COMPLETE"
log "Experiment complete"
