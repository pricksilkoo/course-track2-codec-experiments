# Residual-VQ stage-allocation seed confirmation

Date: 2026-10-24

## Question and protocol

The first structured-quantizer study clearly favored projected residual VQ over
product VQ, but its `48/64/80` later-heavy allocation exceeded the uniform
`64/64/64` allocation by only 0.062689 score on one seed. This follow-up used
the pre-registered protocol in `STRUCTURAL_SEED_PLAN.md` to test whether that
small allocation difference was reproducible.

Each family was trained from the same frozen `strong_baseline_v1` checkpoint
with seeds `20261024`, `3407`, and `8128`. Data, losses, optimizer, 100000-step
budget, 5000-step quantizer-only adaptation, fixed 200-file development set,
and deployed waveform model were held constant. The sealed LibriTTS
confirmation set was not accessed.

All six runs satisfy exactly 2400 bit/s, 30 ms algorithmic lookahead, 650.2272
total MFLOP/s, 277.44 decoder MFLOP/s, and 662109 deployed parameters.

## Per-seed objective results

| Family | Seed | PESQ | ESTOI | SI-SNR | UTMOS | Score | B minus A |
|---|---:|---:|---:|---:|---:|---:|---:|
| A residual uniform `64/64/64` | 20261024 | 1.98547 | 0.72928 | 5.16467 | 2.90956 | 46.68365 | — |
| B residual later-heavy `48/64/80` | 20261024 | 1.99815 | 0.72878 | 5.17889 | 2.90565 | 46.74634 | +0.06269 |
| A residual uniform `64/64/64` | 3407 | 1.98889 | 0.72963 | 5.08702 | 2.90775 | 46.65699 | — |
| B residual later-heavy `48/64/80` | 3407 | 1.99866 | 0.72760 | 5.13919 | 2.90165 | 46.67069 | +0.01370 |
| A residual uniform `64/64/64` | 8128 | 2.00511 | 0.72978 | 5.15942 | 2.91367 | **46.85894** | — |
| B residual later-heavy `48/64/80` | 8128 | 1.99410 | 0.72889 | 5.11579 | 2.89975 | 46.64381 | -0.21513 |

The paired direction is inconsistent: later-heavy wins two seeds by only
0.063 and 0.014, while uniform wins seed 8128 by 0.215. Every run beats the
frozen 45.847260 baseline.

## Three-seed aggregate

Values are mean ± sample standard deviation.

| Family | Score | PESQ | ESTOI | SI-SNR | UTMOS | Worst seed | Seeds above baseline |
|---|---:|---:|---:|---:|---:|---:|---:|
| A residual uniform | **46.73319 ± 0.10971** | 1.99316 ± 0.01049 | **0.72956 ± 0.00026** | 5.13703 ± 0.04340 | **2.91032 ± 0.00303** | **46.65699** | 3 / 3 |
| B residual later-heavy | 46.68695 ± 0.05317 | **1.99697 ± 0.00250** | 0.72843 ± 0.00071 | **5.14462 ± 0.03190** | 2.90235 ± 0.00301 | 46.64381 | 3 / 3 |

Uniform has the higher mean by 0.04625, but that difference is small relative
to seed variation and the paired signs conflict. Later-heavy has about half the
score standard deviation. Following the pre-registered decision rule, this is
recorded as a practical tie; `48/64/80` is the lower-variance preference for
subsequent work, not a demonstrated quality winner.

## Codebook diagnostics

All stages remain active, so the result is not driven by dead codes. The table
reports each run's stage-1 / stage-2 / stage-3 values.

| Family / seed | Active codes | Perplexity | Marginal entropy (bits) | Residual-MSE reduction | Partial SI-SNR at 0.8 / 1.6 / 2.4 kbit/s |
|---|---|---|---|---|---|
| A / 20261024 | 256/256/256 | 143.2/138.3/139.5 | 7.162/7.111/7.125 | 67.6%/40.8%/57.7% | -8.33/-3.01/5.16 dB |
| A / 3407 | 256/255/256 | 151.8/142.1/139.2 | 7.246/7.151/7.121 | 71.4%/35.9%/50.3% | -8.42/-5.20/5.09 dB |
| A / 8128 | 256/256/256 | 144.4/136.7/132.7 | 7.174/7.095/7.052 | 68.0%/58.2%/43.4% | -8.82/-1.37/5.16 dB |
| B / 20261024 | 256/256/256 | 141.9/140.6/143.1 | 7.149/7.136/7.161 | 72.2%/49.0%/44.6% | -8.61/-1.74/5.18 dB |
| B / 3407 | 256/255/256 | 148.7/144.0/147.2 | 7.216/7.170/7.201 | 75.7%/40.0%/46.5% | -7.27/-5.28/5.14 dB |
| B / 8128 | 256/256/256 | 132.8/133.9/140.2 | 7.053/7.066/7.132 | 67.5%/37.5%/71.0% | -4.96/-1.04/5.12 dB |

Family-average diagnostics likewise do not provide evidence that one stage
allocation dominates:

| Family | Perplexity | Marginal entropy | Residual-MSE reduction | Partial SI-SNR |
|---|---|---|---|---|
| A uniform | 146.5/139.1/137.1 | 7.194/7.119/7.099 | 69.0%/45.0%/50.5% | -8.52/-3.19/5.14 dB |
| B later-heavy | 141.1/139.5/143.5 | 7.139/7.124/7.165 | 71.8%/42.2%/54.0% | -6.95/-2.69/5.14 dB |

Later-heavy shifts slightly more organization toward stages 1 and 3, as
intended, but intermediate-stage usefulness varies substantially by seed. The
fully reconstructed SI-SNR is effectively tied. Occupancy, entropy, and
partial reconstructions therefore support the same conclusion as the objective
score: residual composition is robustly useful; fine-grained dimension
allocation is not yet a robust source of gain.

## Checkpoints

| Run | Selected step | SHA-256 |
|---|---:|---|
| A seed 20261024 | 100000 | `64d230d565e0eb3c9f137ae44ac9b88a4bbcf68fc4ff6b0dd3edf552d06ecc4a` |
| A seed 3407 | 100000 | `5ae3236e5d63ba21ae599334529faefeb0ad85f9ba6181b912b404c453c7b218` |
| A seed 8128 | 100000 | `9bdabf9a897ed25ab69d1e344d40e180eb4e7ae5e29229d667c82526cacf192b` |
| B seed 20261024 | 100000 | `f9c71919519dbda7d02bdfc56d6eb309cf9a45976d733e29b3fd808b7b77cc1a` |
| B seed 3407 | 100000 | `8c35191307838d375b704f7dc039cacefecf3bcb47dca10151a219ff07e20f14` |
| B seed 8128 | 10000 | `6ec0f4955fd008d2155b6d8c30fb89caa6b5f44a085ebe1cfdf59b9f88f1f6a5` |

The B seed-8128 run completed all 100000 training steps, but validation-based
selection retained its 10000-step checkpoint. This is another warning that the
small allocation effect is sensitive to optimization and checkpoint selection.

## Decision and next recommendation

1. Projected residual VQ is retained; product VQ remains rejected.
2. `64/64/64` and `48/64/80` are a practical tie. Later-heavy is preferred as
   the lower-variance continuation branch, not promoted as a proven winner.
3. The frozen `strong_baseline_v1` marker remains unchanged and no sealed
   evaluation is run in this tuning study.
4. More seeds or more small reallocations such as `32/64/96` are unlikely to be
   the best use of compute. The next experiment should change a larger causal
   structural factor while keeping the now-validated residual quantizer fixed:
   test multi-scale decoder refinement or a lightweight sub-band synthesis
   head, with a matched control and strict decoder-MFLOP preflight.

