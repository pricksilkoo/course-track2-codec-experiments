# Structural residual-VQ seed confirmation plan

Date: 2026-10-24

## Why this experiment comes next

The controlled structured-quantizer study established a large and consistent
advantage for projected residual VQ over product VQ. It did not yet establish
whether the smaller difference between uniform `64/64/64` allocation and
later-heavy `48/64/80` allocation is reproducible.

The first-seed fixed-200 scores were:

| Family | Seed | Score |
|---|---:|---:|
| A: residual uniform | 20261024 | 46.683654 |
| B: residual later-heavy | 20261024 | 46.746343 |

The B-minus-A margin is only 0.062689. That is too small to treat as an
architectural result from one seed.

## Pre-registered runs

| GPU | Run | Family | Seed | Steps |
|---:|---|---|---:|---:|
| 0 | `struct4_seed_a_uniform_3407` | A | 3407 | 100000 |
| 1 | `struct4_seed_a_uniform_8128` | A | 8128 | 100000 |
| 2 | `struct4_seed_b_later_3407` | B | 3407 | 100000 |
| 3 | `struct4_seed_b_later_8128` | B | 8128 | 100000 |

All runs independently warm-start from the frozen `strong_baseline_v1`
checkpoint. They retain the same data, batch size, segment length, losses,
optimizer schedule, 5000-step quantizer-only adaptation, 100000-step budget,
and fixed 200-file development evaluation.

## Decision rule

For each family, combine seeds `20261024`, `3407`, and `8128` and report:

1. mean and sample standard deviation of the course objective score;
2. mean and sample standard deviation of PESQ, ESTOI, SI-SNR, and UTMOS;
3. the paired B-minus-A score difference for every seed;
4. worst-seed score and the number of seeds that beat the frozen 45.847260
   baseline;
5. codebook occupancy, perplexity, per-stage error reduction, and partial-stage
   reconstruction for every run.

The family with the higher three-seed mean is the leading architecture. A
single unusually high run cannot decide the family. If the mean difference is
small and the paired sign is inconsistent, the result is recorded as a tie and
the lower-variance family is preferred for subsequent work.

No candidate is evaluated on the sealed LibriTTS confirmation set in this
study. Promotion of the frozen strong-baseline marker is a separate decision
after the seed analysis is complete.
