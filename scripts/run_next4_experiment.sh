#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -lt 3 || $# -gt 4 ]]; then
  echo "usage: $0 RUN_NAME GPU_ID CONFIG_PATH [ADDITIONAL_STEPS]" >&2
  exit 2
fi

RUN_NAME="$1"
GPU_ID="$2"
CONFIG_PATH="$3"
ADDITIONAL_STEPS="${4:-170000}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

RUN_DIR="$REPO_ROOT/runs/$RUN_NAME"
MANIFEST_DIR="$REPO_ROOT/data/manifests/vctk_libritts"
VALIDATION_DIR="$REPO_ROOT/runs/fast_b64_2s_v1/validation_200"
EVAL_DIR="$RUN_DIR/evaluation"
PIPELINE_LOG="$RUN_DIR/pipeline.log"
PYTHON="$REPO_ROOT/.venv/bin/python"
INIT_CHECKPOINT="$REPO_ROOT/runs/ablation_c_temporal/checkpoints/last.pt"
export PYTHONNOUSERSITE=1
export TORCH_HOME="${TORCH_HOME:-$REPO_ROOT/data/torch-cache}"

mkdir -p "$RUN_DIR" "$EVAL_DIR" "$TORCH_HOME"
exec > >(tee -a "$PIPELINE_LOG") 2>&1

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

record() {
  local status="$1"
  local note="${2:-}"
  local config="$REPO_ROOT/$CONFIG_PATH"
  [[ -f "$RUN_DIR/effective_config.yaml" ]] && config="$RUN_DIR/effective_config.yaml"
  local args=(
    --name "$RUN_NAME"
    --status "$status"
    --config "$config"
    --run-dir "$RUN_DIR"
    --dataset-summary "$MANIFEST_DIR/summary.json"
    --evaluation-summary "$EVAL_DIR/metrics/summary.json"
    --complexity-summary "$EVAL_DIR/complexity.json"
    --output "$REPO_ROOT/EXPERIMENT_LOG.md"
  )
  [[ -n "$note" ]] && args+=(--note "$note")
  (
    flock -x 9
    "$PYTHON" scripts/record_experiment.py "${args[@]}"
  ) 9>"$REPO_ROOT/.experiment_log.lock" || true
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

test -x "$PYTHON"
test -f "$INIT_CHECKPOINT"
test -f "$MANIFEST_DIR/train.scp"
test -f "$MANIFEST_DIR/valid.scp"
test -d "$VALIDATION_DIR"

AVAILABLE_KB="$(df -Pk "$REPO_ROOT" | awk 'NR==2 {print $4}')"
if (( AVAILABLE_KB < 20 * 1024 * 1024 )); then
  log "Disk-safety stop: less than 20 GiB remains"
  record failed "Disk-safety stop before training"
  exit 1
fi

log "Preflight complexity validation for $CONFIG_PATH"
"$PYTHON" scripts/complexity.py \
  --config "$CONFIG_PATH" --output "$RUN_DIR/preflight_complexity.json"
"$PYTHON" -c '
import json, sys
report = json.load(open(sys.argv[1]))
assert report["bitrate_bps"] == 2400, report
assert report["algorithmic_lookahead_ms"] <= 30, report
assert report["total_mflop_per_s"] <= 700, report
assert report["decoder_mflop_per_s"] <= 300, report
' "$RUN_DIR/preflight_complexity.json"

log "Starting $RUN_NAME on physical GPU $GPU_ID for $ADDITIONAL_STEPS additional steps"
record running "$ADDITIONAL_STEPS-step continuation from the common 30k-step C checkpoint on GPU $GPU_ID"

if [[ ! -f "$RUN_DIR/TRAINING_COMPLETE" ]]; then
  train_args=(
    --config "$CONFIG_PATH"
    --train-manifest "$MANIFEST_DIR/train.scp"
    --valid-manifest "$MANIFEST_DIR/valid.scp"
    --output-dir "$RUN_DIR"
    --device cuda
    --max-total-steps "$ADDITIONAL_STEPS"
  )
  if [[ -f "$RUN_DIR/checkpoints/last.pt" ]]; then
    log "Resuming from $RUN_DIR/checkpoints/last.pt"
    train_args+=(--resume "$RUN_DIR/checkpoints/last.pt")
  else
    log "Warm-starting codec and discriminator from $INIT_CHECKPOINT"
    train_args+=(--init-checkpoint "$INIT_CHECKPOINT")
  fi
  CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/train.py "${train_args[@]}"
  touch "$RUN_DIR/TRAINING_COMPLETE"
fi

CHECKPOINT="$RUN_DIR/checkpoints/best.pt"
test -f "$CHECKPOINT"

log "Encoding the fixed 200-file validation set"
CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/encode.py \
  --checkpoint "$CHECKPOINT" --input-dir "$VALIDATION_DIR" \
  --output-dir "$EVAL_DIR/bitstreams" --device cuda

log "Decoding the fixed validation set"
CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/decode.py \
  --checkpoint "$CHECKPOINT" --bitstream-dir "$EVAL_DIR/bitstreams" \
  --output-dir "$EVAL_DIR/reconstructed" --device cuda

"$PYTHON" scripts/validate_submission.py \
  --input-dir "$VALIDATION_DIR" --bitstream-dir "$EVAL_DIR/bitstreams" \
  --output-dir "$EVAL_DIR/reconstructed"

log "Computing PESQ, ESTOI, SI-SNR and UTMOS"
CUDA_VISIBLE_DEVICES="$GPU_ID" "$PYTHON" scripts/evaluate.py \
  --reference-dir "$VALIDATION_DIR" --reconstructed-dir "$EVAL_DIR/reconstructed" \
  --output-dir "$EVAL_DIR/metrics" --device cuda

"$PYTHON" scripts/complexity.py \
  --checkpoint "$CHECKPOINT" --output "$EVAL_DIR/complexity.json"

record complete "$ADDITIONAL_STEPS additional steps from common C checkpoint and fixed evaluation completed"
touch "$RUN_DIR/PIPELINE_COMPLETE"
log "Experiment complete"

