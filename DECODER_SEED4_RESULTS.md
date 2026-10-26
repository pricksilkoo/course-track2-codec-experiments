# Decoder distillation seed and composition study

Date: 2026-10-26

## Question

The preceding decoder study found training-only waveform/spectral distillation
to be the best single-seed variant, while a small causal multiscale refiner
gave a smaller independent gain. This registered follow-up asks:

1. whether pure distillation is stable across three seeds; and
2. whether the multiscale refiner composes with distillation.

All candidates warm-start from frozen `strong_baseline_v2`, train to 30000
total fine-tuning steps, use the same validation selection rule, and are
evaluated on the same fixed 200-file development set. The sealed LibriTTS set
was not used.

## Pure-distillation three-seed result

| Seed | Score | PESQ | ESTOI | SI-SNR | UTMOS | Selected step |
|---:|---:|---:|---:|---:|---:|---:|
| 20261025 | 47.3227 | 2.0216 | 0.7319 | 5.3972 | 2.9368 | 10000 |
| 3407 | 46.8630 | 2.0738 | 0.7419 | 5.5447 | 2.7488 | 5000 |
| 8128 | 46.8433 | 2.0540 | 0.7419 | 5.5996 | 2.7627 | 5000 |
| Mean +/- sample SD | **47.0097 +/- 0.2713** | - | - | - | - | - |

The range is 46.8433--47.3227. The original seed is the high member of the
three-seed distribution, and the two added seeds are close to one another.
Consequently, the single-seed 47.3227 result should not be treated as a stable
promotion over `strong_baseline_v2`.

## Matched composition test

| Seed | Pure distillation | Multiscale + distillation | Composition minus pure |
|---:|---:|---:|---:|
| 3407 | 46.8630 | 46.6964 | **-0.1666** |
| 8128 | 46.8433 | 46.7856 | **-0.0577** |
| Paired mean | 46.8532 | 46.7410 | **-0.1121** |

Component changes for composition minus pure were:

| Seed | PESQ | ESTOI | SI-SNR | UTMOS |
|---:|---:|---:|---:|---:|
| 3407 | -0.0151 | -0.0015 | +0.0160 | -0.0050 |
| 8128 | +0.0035 | -0.0002 | -0.0533 | -0.0071 |

The composition loses on the course objective in both matched seeds. Its small
and inconsistent waveform changes do not compensate for the consistent ESTOI
and UTMOS losses. A third composition seed is therefore not justified.

## Complexity and validity

| Family | Bitrate | Lookahead | Total MFLOP/s | Decoder MFLOP/s | Valid |
|---|---:|---:|---:|---:|---|
| Pure distillation | 2400 | 30 ms | 650.2272 | 277.440 | yes |
| Multiscale + distillation | 2400 | 30 ms | 657.1392 | 284.352 | yes |

All four new runs evaluated exactly 200 files and remained within every
submission constraint.

Checkpoint SHA-256:

- Pure seed 3407: `27803665ba9a5e6415c77c8b06dc38b55adda737120ca7f9e79d715c20062007`
- Pure seed 8128: `127491647b1636cac27672e59a749806d9ef10b0f0e7f105f937e3d5a53fadbe`
- Composition seed 3407: `38d85c5d7ef467a2952d486cdcc27c6034bd29b791405eabd657e45d17e7e67d`
- Composition seed 8128: `ab501141729a19b3373831d2af814a4c3ca78c44812b8837682d04d4831944ab`

## Selection behavior

The two added pure-distillation runs and both composition runs selected their
5000-step checkpoints. The original seed-20261025 pure-distillation run
selected step 10000. Continuing to 30000 remained useful as a controlled upper
bound, but it did not improve selection after the early window. Future decoder
fine-tuning should validate densely through 5000--10000 steps and treat longer
training as confirmation rather than the default source of gains.

## RVQ diagnostics

There is no codebook collapse in either family. Across the four new runs,
stages use 254--256 of 256 entries, marginal entropy remains about 6.92--7.05
bits, and perplexity remains about 121--133.

| Run | Active codes | Perplexity | Marginal entropy (bits) | Residual MSE reduction | Final/original residual |
|---|---|---|---|---|---:|
| Pure 3407 | 256/254/256 | 126.68/125.52/126.50 | 6.985/6.972/6.983 | 63.91%/48.20%/52.24% | 0.0893 |
| Composition 3407 | 256/254/255 | 130.24/121.99/122.98 | 7.025/6.931/6.942 | 64.06%/48.73%/52.32% | 0.0879 |
| Pure 8128 | 256/256/256 | 132.84/127.51/125.98 | 7.054/6.994/6.977 | 63.87%/48.46%/52.62% | 0.0882 |
| Composition 8128 | 255/256/256 | 128.15/128.75/121.08 | 7.002/7.008/6.920 | 64.29%/48.37%/52.11% | 0.0883 |

The multiscale head does not create a consistent latent-space advantage. The
small diagnostic differences are seed-sized and do not track the objective
score. The negative composition result is therefore best attributed to
synthesis/optimization interference rather than RVQ utilization.

## Recovery note

The initial GPU 0--2 launches shared cards with an unrelated job and reached
5000 steps before a validation/GAN memory peak caused OOM. The unrelated
processes were never altered. All affected runs resumed from their intact
5000-step checkpoints on GPU 3 and completed with the registered
configurations. One recovery command initially referenced the wrong C config
filename; this was corrected before training resumed and did not change model
state or evaluation.

## Decision

- Do not promote the single-seed distillation checkpoint as a new strong
  baseline.
- Do not run a third seed for multiscale plus distillation: both registered
  paired comparisons are negative.
- Keep `strong_baseline_v2` frozen.
- Before attributing a robust causal gain to distillation, the clean next test
  is matched no-distillation continuation controls at seeds 3407 and 8128.
  That comparison separates seed variance and ordinary continued optimization
  from the teacher signal without adding deployment compute.
