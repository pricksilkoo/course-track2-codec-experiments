#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

RUN_NAME="${RUN_NAME:-baseline_full_v1}"
GPU_IDS="${GPU_IDS:-0,1,2,3}"
EVAL_GPU="${EVAL_GPU:-3}"
NUM_GPUS="$(awk -F, '{print NF}' <<<"$GPU_IDS")"
RUN_DIR="$REPO_ROOT/runs/$RUN_NAME"
DATA_ROOT="$REPO_ROOT/data/corpora"
MANIFEST_DIR="$REPO_ROOT/data/manifests/vctk_libritts"
VALIDATION_DIR="$RUN_DIR/validation_200"
EVAL_DIR="$RUN_DIR/evaluation"
PIPELINE_LOG="$RUN_DIR/pipeline.log"
BASE_PYTHON="${BASE_PYTHON:-/storage1/hehaoran/miniconda3/envs/Qwen-ASR/bin/python}"
VENV_DIR="$REPO_ROOT/.venv"
TORCH_HOME="${TORCH_HOME:-$REPO_ROOT/data/torch-cache}"
export TORCH_HOME

mkdir -p "$RUN_DIR" "$EVAL_DIR" "$TORCH_HOME"
exec > >(tee -a "$PIPELINE_LOG") 2>&1

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

record() {
  local status="$1"
  local note="${2:-}"
  local config="$REPO_ROOT/configs/baseline_16k_2p4k.yaml"
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
  "$VENV_DIR/bin/python" scripts/record_experiment.py "${args[@]}" || true
}

on_error() {
  local code="$1"
  local line="$2"
  trap - ERR
  log "Pipeline failed with exit code $code at line $line"
  if [[ -x "$VENV_DIR/bin/python" ]]; then
    record failed "Pipeline exit code $code at line $line; see $PIPELINE_LOG"
  fi
  exit "$code"
}
trap 'on_error $? $LINENO' ERR

log "Starting $RUN_NAME on training GPUs $GPU_IDS at commit $(git rev-parse HEAD)"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  log "Creating project virtual environment from $BASE_PYTHON"
  "$BASE_PYTHON" -m venv --system-site-packages "$VENV_DIR"
fi

log "Installing project and evaluation dependencies"
"$VENV_DIR/bin/python" -m pip install -e . -r requirements-evaluation.txt pytest
record running "Persistent baseline pipeline is active; see $PIPELINE_LOG"

log "Running unit tests"
"$VENV_DIR/bin/python" -m pytest -q

log "Downloading and preparing corpora"
bash scripts/download_datasets.sh "$DATA_ROOT"

if [[ ! -f "$VALIDATION_DIR/selection.json" ]]; then
  log "Preparing deterministic 200-file validation subset"
  "$VENV_DIR/bin/python" scripts/prepare_validation.py \
    --manifest "$MANIFEST_DIR/valid.scp" \
    --output-dir "$VALIDATION_DIR" \
    --limit 200 \
    --seed 42
fi

if [[ ! -f "$RUN_DIR/TRAINING_COMPLETE" ]]; then
  train_args=(
    --config configs/baseline_16k_2p4k.yaml
    --train-manifest "$MANIFEST_DIR/train.scp"
    --valid-manifest "$MANIFEST_DIR/valid.scp"
    --output-dir "$RUN_DIR"
    --device cuda
    --num-workers 4
  )
  if [[ -f "$RUN_DIR/checkpoints/last.pt" ]]; then
    log "Resuming training from last.pt"
    train_args+=(--resume "$RUN_DIR/checkpoints/last.pt")
  else
    log "Starting full baseline training"
  fi
  CUDA_VISIBLE_DEVICES="$GPU_IDS" "$VENV_DIR/bin/python" -m torch.distributed.run \
    --standalone \
    --nproc_per_node="$NUM_GPUS" \
    scripts/train.py "${train_args[@]}"
  touch "$RUN_DIR/TRAINING_COMPLETE"
fi

CHECKPOINT="$RUN_DIR/checkpoints/best.pt"
test -f "$CHECKPOINT"

log "Encoding validation set"
CUDA_VISIBLE_DEVICES="$EVAL_GPU" "$VENV_DIR/bin/python" scripts/encode.py \
  --checkpoint "$CHECKPOINT" \
  --input-dir "$VALIDATION_DIR" \
  --output-dir "$EVAL_DIR/bitstreams" \
  --device cuda

log "Decoding validation set"
CUDA_VISIBLE_DEVICES="$EVAL_GPU" "$VENV_DIR/bin/python" scripts/decode.py \
  --checkpoint "$CHECKPOINT" \
  --bitstream-dir "$EVAL_DIR/bitstreams" \
  --output-dir "$EVAL_DIR/reconstructed" \
  --device cuda

log "Validating submission format"
"$VENV_DIR/bin/python" scripts/validate_submission.py \
  --input-dir "$VALIDATION_DIR" \
  --bitstream-dir "$EVAL_DIR/bitstreams" \
  --output-dir "$EVAL_DIR/reconstructed"

log "Running PESQ, ESTOI, SI-SNR and UTMOS evaluation"
CUDA_VISIBLE_DEVICES="$EVAL_GPU" "$VENV_DIR/bin/python" scripts/evaluate.py \
  --reference-dir "$VALIDATION_DIR" \
  --reconstructed-dir "$EVAL_DIR/reconstructed" \
  --output-dir "$EVAL_DIR/metrics" \
  --device cuda

log "Computing analytical complexity"
"$VENV_DIR/bin/python" scripts/complexity.py \
  --checkpoint "$CHECKPOINT" \
  --output "$EVAL_DIR/complexity.json"

record complete "Full training, format validation, objective evaluation and complexity analysis completed"
touch "$RUN_DIR/PIPELINE_COMPLETE"
log "Pipeline complete"
