# Decoder stability and causal-control results

Date: 2026-10-26

## Outcome

The matched controls establish that the registered waveform/spectral teacher
signal has a causal development-set benefit beyond ordinary continuation.
Early-window checkpoint averaging does not preserve that benefit and is
rejected by a wide margin.

| Seed | Continuation control | Raw distillation | Distill - control | Early-window SWA | SWA - raw |
|---:|---:|---:|---:|---:|---:|
| 3407 | 46.3005 | 46.8630 | +0.5625 | 44.5262 | -2.3368 |
| 8128 | 46.3444 | 46.8433 | +0.4988 | 45.0291 | -1.8142 |
| Paired mean | 46.3225 | 46.8532 | **+0.5307** | 44.7777 | **-2.0755** |

Raw distillation wins both matched seeds, so it satisfies the pre-registered
causal criterion. SWA loses both seeds, and each loss is far larger than the
allowed 0.05 regression, so it fails both registered retention routes.

## Component metrics

| Seed / variant | PESQ | ESTOI | SI-SNR (dB) | UTMOS | Objective |
|---|---:|---:|---:|---:|---:|
| 3407 control | 2.0628 | 0.7411 | 5.5573 | 2.6732 | 46.3005 |
| 3407 raw distill | 2.0738 | 0.7419 | 5.5447 | 2.7488 | 46.8630 |
| 3407 SWA distill | 1.9013 | 0.7188 | 4.5612 | 2.7628 | 44.5262 |
| 8128 control | 2.0708 | 0.7432 | 5.5871 | 2.6599 | 46.3444 |
| 8128 raw distill | 2.0540 | 0.7419 | 5.5996 | 2.7627 | 46.8433 |
| 8128 SWA distill | 1.9481 | 0.7211 | 4.6429 | 2.7726 | 45.0291 |

The raw teacher signal consistently raises UTMOS by about 0.076--0.103. The
other components move only slightly and in mixed directions, but without a
material regression. This is consistent with a perceptual synthesis benefit,
not a broad reconstruction-metric improvement.

SWA behaves differently: UTMOS remains slightly above raw distillation, while
PESQ, ESTOI, and SI-SNR all fall sharply. The objective loss is therefore not
metric noise or an isolated MOS-model effect; averaging damaged waveform and
spectral fidelity.

## Selection and RVQ diagnostics

The controls selected their step-5000 checkpoints. The registered SWA models
average steps 2500, 5000, 7500, and 10000 after the complete 30000-step runs.
All codebooks remain nominally active, but the averaged models show a clear
distribution shift:

| Variant | Active codes by stage | Perplexity by stage | Sum marginal entropy (bits) |
|---|---|---|---:|
| control 3407 | 256 / 256 / 254 | 135.4 / 124.5 / 127.8 | 21.0385 |
| control 8128 | 256 / 256 / 256 | 142.9 / 129.0 / 128.0 | 21.1704 |
| SWA 3407 | 256 / 256 / 256 | 88.8 / 110.0 / 119.0 | 20.1484 |
| SWA 8128 | 255 / 256 / 256 | 82.1 / 137.3 / 132.6 | 20.5119 |

Stage-one perplexity and total marginal entropy fall after averaging even
though active-code counts remain high. Full three-stage diagnostic SI-SNR
also drops from 5.56/5.59 dB in the controls to 4.56/4.64 dB in SWA. This
supports a trajectory-incompatibility interpretation: directly averaging the
encoder, codebook, decoder, and associated quantizer state across the early
GAN transition does not preserve a coherent discrete representation.
Occupancy alone would have missed the failure.

## Constraints and artifacts

All four evaluated candidates use the same 200-file development set and meet
the deployment limits:

- bitrate: exactly 2400 bps;
- algorithmic lookahead: 30 ms;
- total complexity: 650.2272 MFLOP/s;
- decoder complexity: 277.44 MFLOP/s.

Checkpoint SHA-256 values:

- control 3407: `f425fdc28ea735cad302c17acc353f43278bef17efdc5cc3411e936a6e10cf20`;
- control 8128: `4c249f0392bc4b1780aee2ac501b4884596e4c6d53c3b55f233590b602a94bca`;
- SWA distill 3407: `18c7b06c3245c2b46e84217ed476678bb1fab01494f89276fc52d3afac7e5935`;
- SWA distill 8128: `33a751885cdb61ecc11f97b4873691d95e942db6ee19b77df312a2ba9c136e94`.

The sealed LibriTTS confirmation set was not used.

## Decision

1. Accept training-only waveform/spectral distillation as a real causal gain
   over matched continuation, with paired mean improvement +0.5307.
2. Reject early-window parameter SWA for this codec. Do not use the averaged
   checkpoints and do not spend more seeds on the same averaging rule.
3. Keep `strong_baseline_v2` frozen. The three-seed raw-distillation mean is
   still 47.0097 +/- 0.2713, so the original 47.3227 run remains a favorable
   seed rather than a sufficiently stable promotion candidate.
4. If optimization stability is pursued again, prefer function-preserving
   methods such as EMA during training, late-window averaging after the GAN
   regime has stabilized, or snapshot selection/ensembling for analysis. Any
   new method should first be screened on the two matched seeds and must not
   touch the sealed set.
