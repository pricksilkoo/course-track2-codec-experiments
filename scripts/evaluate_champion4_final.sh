#!/usr/bin/env bash
set -Eeuo pipefail
RUN="$1"
GPU="$2"
cd -- "$(dirname -- "$0")/.."
[[ "$RUN" == champion4_* ]] || exit 2
DIR="runs/$RUN"
OUT="$DIR/evaluation_final100k"
PYTHON=".venv-codec/bin/python"
REF="runs/fast_b64_2s_v1/validation_200"
CKPT="$DIR/checkpoints/last.pt"
export CUDA_VISIBLE_DEVICES="$GPU" PYTHONUNBUFFERED=1 PYTHONNOUSERSITE=1
export TORCH_HOME="$PWD/data/torch-cache"
mkdir -p "$OUT"
exec 8>"$OUT/.pipeline.lock"
flock -n 8 || exit 73
[[ -f "$OUT/DIAGNOSTIC_COMPLETE" ]] && exit 0
exec > >(tee -a "$OUT/pipeline.log") 2>&1
test -f "$DIR/TRAINING_COMPLETE"
"$PYTHON" -c 'import torch,sys; s=torch.load(sys.argv[1],map_location="cpu",weights_only=False); assert s["global_step"]==100000; print("Fixed endpoint",s["global_step"])' "$CKPT"
sha256sum "$CKPT" > "$OUT/checkpoint.sha256"
if [[ ! -f "$OUT/ROUNDTRIP_COMPLETE" ]]; then
  "$PYTHON" scripts/encode.py --checkpoint "$CKPT" --input-dir "$REF" --output-dir "$OUT/bitstreams" --device cuda
  "$PYTHON" scripts/decode.py --checkpoint "$CKPT" --bitstream-dir "$OUT/bitstreams" --output-dir "$OUT/reconstructed" --device cuda
  "$PYTHON" scripts/validate_submission.py --input-dir "$REF" --bitstream-dir "$OUT/bitstreams" --output-dir "$OUT/reconstructed"
  touch "$OUT/ROUNDTRIP_COMPLETE"
fi
if [[ ! -f "$OUT/metrics/summary.json" ]]; then
  "$PYTHON" scripts/evaluate.py --reference-dir "$REF" --reconstructed-dir "$OUT/reconstructed" --output-dir "$OUT/metrics" --device cuda
fi
"$PYTHON" scripts/complexity.py --checkpoint "$CKPT" --output "$OUT/complexity.json"
"$PYTHON" -c 'import json,sys; r=json.load(open(sys.argv[1])); assert r["bitrate_bps"]==2400 and r["algorithmic_lookahead_ms"]<=30 and r["total_mflop_per_s"]<=700 and r["decoder_mflop_per_s"]<=300' "$OUT/complexity.json"
if [[ ! -f "$OUT/rvq_diagnostics.json" ]]; then
  "$PYTHON" scripts/diagnose_rvq.py --checkpoint "$CKPT" --input-dir "$REF" --output "$OUT/rvq_diagnostics.json" --device cuda
fi
touch "$OUT/DIAGNOSTIC_COMPLETE"
