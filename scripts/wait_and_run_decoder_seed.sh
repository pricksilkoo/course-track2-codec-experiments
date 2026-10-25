#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -lt 3 || $# -gt 5 ]]; then
  echo "usage: $0 RUN_NAME GPU_ID CONFIG_PATH [FINETUNE_STEPS] [MIN_FREE_MIB]" >&2
  exit 2
fi

RUN_NAME="$1"
GPU_ID="$2"
CONFIG_PATH="$3"
FINETUNE_STEPS="${4:-30000}"
MIN_FREE_MIB="${5:-12000}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
RUN_DIR="$REPO_ROOT/runs/$RUN_NAME"
QUEUE_LOG="$RUN_DIR/queue.log"
mkdir -p "$RUN_DIR"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$QUEUE_LOG"
}

while true; do
  available_kb="$(df -Pk "$REPO_ROOT" | awk 'NR==2 {print $4}')"
  if (( available_kb < 20 * 1024 * 1024 )); then
    log "Disk-safety stop while queued: less than 20 GiB remains"
    exit 1
  fi

  free_mib="$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i "$GPU_ID" | tr -d ' ')"
  if (( free_mib >= MIN_FREE_MIB )); then
    log "GPU $GPU_ID has ${free_mib} MiB free; starting $RUN_NAME"
    break
  fi
  log "GPU $GPU_ID has ${free_mib} MiB free; waiting for ${MIN_FREE_MIB} MiB"
  sleep 30
done

exec "$REPO_ROOT/scripts/run_decoder4_experiment.sh" \
  "$RUN_NAME" "$GPU_ID" "$CONFIG_PATH" "$FINETUNE_STEPS"
