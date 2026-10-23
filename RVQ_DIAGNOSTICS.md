# RVQ Diagnostics

## Selected final-D checkpoint before codebook experiments

- Checkpoint: `runs/seed_confirm_d_combo_seed8128/checkpoints/best.pt`
- Evaluation set: fixed 200-file development set
- Files / samples / latent frames: 200 / 16,197,971 / 101,286
- Diagnostic JSON: `runs/rvq_diagnostic_best/report.json`

### Occupancy

| RVQ stage | Active codes | Perplexity | Marginal entropy (bit) | Top-1 share | Top-10 share | Codes covering 95% mass |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 256 | 140.432 | 7.134 | 6.97% | 27.54% | 187 |
| 2 | 255 | 132.598 | 7.051 | 5.82% | 30.18% | 181 |
| 3 | 252 | 137.687 | 7.105 | 6.36% | 27.68% | 183 |

The sum of marginal entropies is 21.290 bit per 10-ms frame versus the
24-bit fixed representation. This indicates skewed use rather than classic
dead-code collapse: almost every entry appears, but selection frequencies are
far from uniform.

Sparse plug-in joint entropy is downward-biased and bounded by the finite
number of observed frames. It must not be used to claim that `24 - empirical
joint entropy` bits are unused. The marginal statistics and stagewise ablation
below are the robust evidence used for experiment design.

### Residual quantization gain

| Stage | Residual MSE before | Residual MSE after | Relative reduction | Residual / original latent energy |
|---:|---:|---:|---:|---:|
| 1 | 1.958833 | 0.274257 | 85.999% | 14.001% |
| 2 | 0.274257 | 0.159438 | 41.866% | 8.139% |
| 3 | 0.159438 | 0.108539 | 31.924% | 5.541% |

### Partial-stage reconstruction

These are diagnostic ablations, not valid 2.4-kbps submissions.

| Active RVQ stages | Nominal payload | Waveform L1 | Spectral loss | SI-SNR (dB) |
|---:|---:|---:|---:|---:|
| 1 | 800 bps | 0.024985 | 0.197370 | -1.5700 |
| 2 | 1600 bps | 0.018606 | 0.144685 | 3.2119 |
| 3 | 2400 bps | 0.016374 | 0.128974 | 4.7768 |

Stages two and three remain useful. The next study therefore does not remove
them; it tests whether more balanced assignments and stronger later-stage
encoder pressure can improve full-rate reconstruction.

## Planned 2x2 codebook study

All four runs warm-start the selected final-D seed-8128 checkpoint, use the
same seed and data order, train for 30,000 steps, and preserve the identical
inference graph and submission constraints.

| Run | Assignment balancing | Stage commitment weights |
|---|---:|---|
| `codebook4_a_control` | 0 | `[1.0, 1.0, 1.0]` |
| `codebook4_b_balance` | 0.001 | `[1.0, 1.0, 1.0]` |
| `codebook4_c_later_stages` | 0 | `[1.0, 1.5, 2.0]` |
| `codebook4_d_combined` | 0.001 | `[1.0, 1.5, 2.0]` |

The balancing term uses scale-normalized soft assignments and
`KL(mean_assignment || uniform)` at temperature 1.0. It is training-only.
The stage weights only alter the commitment objective. Neither modification
changes transmitted indices, decoder architecture, bitrate, lookahead, or
inference complexity.
