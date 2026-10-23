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

## Completed 2x2 codebook study

All objective results use the same fixed 200-file development set. The starting
checkpoint scored `45.556887`; deltas in the table are relative to that exact
checkpoint.

| Run | Best step | PESQ | ESTOI | SI-SNR | UTMOS | Objective | Delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| A control | 30,000 | 1.9508 | 0.7216 | 4.8127 | 2.8507 | 45.6565 | +0.0996 |
| B balance | 25,000 | 1.9509 | 0.7202 | 4.8235 | 2.8502 | 45.6244 | +0.0675 |
| C later stages | 20,000 | 1.9558 | 0.7219 | 4.8799 | 2.8616 | 45.8099 | +0.2530 |
| D combined | 30,000 | 1.9629 | 0.7203 | 4.8426 | 2.8697 | **45.8473** | **+0.2904** |

Relative to the continued-training control, B is `-0.0321`, C is `+0.1534`,
and D is `+0.1908`. Stronger later-stage commitment is therefore the main
positive factor in this run. Assignment balancing alone did not improve the
objective, while its interaction with later-stage weighting added `+0.0374`
over C. That interaction is small enough to require a seed confirmation before
being treated as robust.

### Post-training RVQ diagnostics

| Run | Stage perplexities | Sum marginal entropy | Stage residual reductions | Partial-stage SI-SNR |
|---|---|---:|---|---|
| Starting checkpoint | 140.4 / 132.6 / 137.7 | 21.2899 | 86.00% / 41.87% / 31.92% | -1.570 / 3.212 / 4.777 |
| A control | 139.4 / 133.0 / 141.3 | 21.3208 | 86.38% / 41.87% / 31.84% | -1.538 / 3.271 / 4.813 |
| B balance | 138.9 / 136.0 / 137.0 | 21.3023 | 86.41% / 41.89% / 31.93% | -1.581 / 3.341 / 4.824 |
| C later stages | 134.3 / 134.1 / 141.5 | 21.2819 | 87.79% / 43.21% / 32.93% | -1.559 / 3.291 / 4.880 |
| D combined | 131.8 / 142.1 / 142.4 | **21.3460** | 87.75% / 42.96% / 32.78% | -1.583 / 3.318 / 4.843 |

The balancing loss did not simply make every stage uniform. In D it shifted
capacity from stage one toward stages two and three and produced the highest
sum marginal entropy, while the later-stage weighting increased residual-error
reduction at all three stages. The score gain correlates more strongly with
better residual quantization than with perplexity alone, confirming that
uniform occupancy is not itself the target.

All four checkpoints preserve 2400 bps, 30 ms lookahead, 676.032 total
MFLOP/s, 265.152 decoder MFLOP/s, and 723,549 parameters.

| Run | Checkpoint SHA-256 |
|---|---|
| A | `593f2bf7dbdbe332109a607db69e1e114ae9ca7d4fbdcc96a2d0cc1b332601a1` |
| B | `b9096a55e24ce8e44fc474b9e0a24e97e46ad4f1914fb59e021299d793416286` |
| C | `f33810831d161e2f6646b28c3bf1d359d56be2adcd2c8aa4d4b784e3e1197c85` |
| D | `e0ab196eab8963a3dd178f7fa3b6fc72e233b70824a0a0d04c87163c03be1b89` |
