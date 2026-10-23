# Current Strong Baseline

`strong_baseline_v1` is the frozen reference for all structural experiments
after 2026-10-23.

| Item | Value |
|---|---|
| Run | `runs/codebook4_d_combined` |
| Checkpoint | `runs/codebook4_d_combined/checkpoints/best.pt` |
| SHA-256 | `e0ab196eab8963a3dd178f7fa3b6fc72e233b70824a0a0d04c87163c03be1b89` |
| Fixed-200 objective | **45.8473** |
| PESQ / ESTOI / SI-SNR / UTMOS | 1.9629 / 0.7203 / 4.8426 / 2.8697 |
| Bitrate / delay | 2400 bps / 30 ms |
| Total / decoder complexity | 676.032 / 265.152 MFLOP/s |
| Parameters | 723,549 |

The machine-readable record is `model_registry/strong_baseline_v1.yaml`. On the
experiment server, `runs/strong_baseline_current` is a stable symbolic link to
the run directory. New experiments must state explicitly whether they warm
start from this checkpoint and compare against `45.8473` on the fixed-200 set.

This checkpoint was selected on the repeatedly used development set. It has
not been evaluated on the sealed confirmation set. Its parent D-family model
was independently confirmed at `43.9842`; the sealed set must not be reused
for structural tuning.
