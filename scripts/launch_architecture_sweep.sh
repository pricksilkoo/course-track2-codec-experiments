#!/usr/bin/env bash
set -Eeuo pipefail

SESSION="${1:-codec_architecture_sweep_v1}"
STEPS="${2:-30000}"
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session already exists: $SESSION" >&2
  exit 1
fi

launch=(
  "arch4_a_vocodec_tf|0|configs/architectures/a_vocodec_tf.yaml"
  "arch4_b_nanocodec_tf|1|configs/architectures/b_nanocodec_tf.yaml"
  "arch4_c_winner_hybrid|2|configs/architectures/c_winner_hybrid.yaml"
  "arch4_d_phoenix_hybrid|3|configs/architectures/d_phoenix_hybrid.yaml"
)

for index in "${!launch[@]}"; do
  IFS='|' read -r run gpu config <<<"${launch[$index]}"
  command="cd '$ROOT' && scripts/run_ablation_experiment.sh '$run' '$gpu' '$config' '$STEPS'"
  if [[ "$index" == 0 ]]; then
    tmux new-session -d -s "$SESSION" -n "$run" "$command"
  else
    tmux new-window -t "$SESSION" -n "$run" "$command"
  fi
done

tmux set-option -t "$SESSION" remain-on-exit on
tmux list-windows -t "$SESSION"
