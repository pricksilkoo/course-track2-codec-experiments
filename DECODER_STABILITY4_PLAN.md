# Decoder stability and causal-control plan

Date: 2026-10-26

## Motivation

The seed study showed that the original 47.3227 distillation result was the
high member of a 47.0097 +/- 0.2713 three-seed distribution. It also showed
that multiscale refinement plus distillation loses to pure distillation in both
matched seeds. This study separates ordinary continuation from the teacher
signal and tests trajectory averaging without adding deployment cost.

## Registered runs

| Run | Seed | Training change | Deployment change |
|---|---:|---|---|
| A control | 3407 | No distillation | None |
| B control | 8128 | No distillation | None |
| C distill SWA | 3407 | Waveform/spectral distillation; average steps 2500/5000/7500/10000 | None |
| D distill SWA | 8128 | Waveform/spectral distillation; average steps 2500/5000/7500/10000 | None |

A and B are compared against the already-completed pure-distillation runs at
the same seeds. C and D are compared against both their matched controls and
the already-completed raw pure-distillation runs.

All runs warm-start frozen `strong_baseline_v2`, retain the same 30000-step
upper bound and learning-rate schedule, and use the same fixed 200-file
development set. C and D save checkpoints every 2500 steps solely to construct
the registered early-window average. No sealed data are used.

## Decision rules

1. Attribute a causal benefit to distillation only if it beats continuation in
   both matched seeds or has a positive paired mean without a material
   component-metric regression.
2. Retain early-window SWA only if it improves both raw distillation seeds, or
   if its paired mean gain is at least 0.05 and no seed drops by more than 0.05.
3. Do not alter `strong_baseline_v2` or run sealed confirmation automatically.
4. All valid candidates must remain exactly 2400 bps, at most 30 ms lookahead,
   at most 700 total MFLOP/s, and at most 300 decoder MFLOP/s.

Because GPUs 0--2 currently have insufficient safe free memory, the four runs
are intentionally queued sequentially on GPU 3.
