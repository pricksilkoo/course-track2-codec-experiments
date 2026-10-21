#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
BASE_PYTHON="${CODEC_BASE_PYTHON:-/storage1/hehaoran/miniconda3/envs/arktrain/bin/python}"
VENV="$REPO_ROOT/.venv-codec"

test -x "$BASE_PYTHON"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PYTHON" -m venv --system-site-packages "$VENV"
fi

"$VENV/bin/python" -m pip install -e "$REPO_ROOT" --no-deps
"$VENV/bin/python" -m pip install -r "$REPO_ROOT/requirements-evaluation.txt" pytest

"$VENV/bin/python" - <<'PY'
import torch

print(
    "torch", torch.__version__,
    "cuda", torch.version.cuda,
    "cudnn", torch.backends.cudnn.version(),
)
x = torch.randn(1, 1, 16_000, device="cuda")
print("cuda_conv", torch.nn.Conv1d(1, 8, 7).cuda()(x).shape)
PY

