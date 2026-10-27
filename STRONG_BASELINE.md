# Current Strong Baseline

`strong_baseline_v2` is the frozen, sealed-confirmed reference for subsequent
decoder experiments.

| Item | Value |
|---|---|
| Family | projected residual VQ, later-heavy stage dimensions |
| Run | `runs/struct4_b_residual_later` |
| Checkpoint | `runs/struct4_b_residual_later/checkpoints/best.pt` |
| SHA-256 | `f9c71919519dbda7d02bdfc56d6eb309cf9a45976d733e29b3fd808b7b77cc1a` |
| Fixed-200 development objective | **46.7463** |
| Sealed 400-file objective | **44.9637** |
| Sealed PESQ / ESTOI / SI-SNR / UTMOS | 1.9015 / 0.7561 / 4.0573 / 2.7267 |
| Bitrate / lookahead | 2400 bps / 30 ms |
| Total / decoder complexity | 650.2272 / 277.44 MFLOP/s |
| Parameters | 662,109 |

The checkpoint was selected on the fixed 200-file development set after a
three-seed structural comparison. The later-heavy family tied the uniform
family within seed uncertainty but had lower variance, so it was chosen by the
pre-registered tie rule. Its one-shot sealed result improved the previous
confirmed model from 43.9842 to 44.9637 (+0.9795) while improving all four
component metrics.

The machine-readable marker is `model_registry/strong_baseline_v2.yaml`, and
`runs/strong_baseline_current` identifies the frozen run on the experiment
server. Later decoder studies may warm-start this model, but development-only
gains do not replace this marker automatically. In particular, the
single-seed decoder-distillation peak and the late decoder averages have not
passed the full promotion standard. The sealed LibriTTS set must not be used
for tuning or repeated candidate selection.

## Previous marker

`strong_baseline_v1` was `runs/codebook4_d_combined`, fixed-200 score 45.8473,
checkpoint SHA-256
`e0ab196eab8963a3dd178f7fa3b6fc72e233b70824a0a0d04c87163c03be1b89`.
It remains a reproducible historical milestone but is no longer the current
reference.
