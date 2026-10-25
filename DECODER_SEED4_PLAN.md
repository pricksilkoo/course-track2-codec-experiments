# Decoder distillation seed and composition plan

Date: 2026-10-25

## Motivation

The decoder study found two positive effects relative to its continuation
control: training-only waveform/spectral distillation improved the fixed-200
score by 0.1283 without deployment cost, and the causal multiscale refiner
improved it by 0.0797 with 6.912 additional decoder MFLOP/s. Both observations
come from one seed. This study tests the stability of distillation and whether
the two gains compose.

The seed-20261025 references are:

- distillation with the unchanged deployment graph: 47.322666;
- multiscale refinement without distillation: 47.274055.

## Runs

| GPU | Run | Seed | Deployment | Training-only signal |
|---:|---|---:|---|---|
| 0 | `decoder_seed4_a_distill_3407` | 3407 | unchanged v2 graph | waveform + spectral distillation |
| 1 | `decoder_seed4_b_distill_8128` | 8128 | unchanged v2 graph | waveform + spectral distillation |
| 2 | `decoder_seed4_c_multiscale_distill_3407` | 3407 | causal multiscale refiner | waveform + spectral distillation |
| 3 | `decoder_seed4_d_multiscale_distill_8128` | 8128 | causal multiscale refiner | waveform + spectral distillation |

Every run warm-starts codec and discriminator state from the same
`strong_baseline_v2` source checkpoint. The frozen teacher is
`struct4_seed_a_uniform_8128`; it is used only while training and is not saved
in the student deployment graph.

## Budget and selection

Earlier decoder runs all selected their best checkpoint at 10000 new steps and
degraded afterward. These confirmations therefore use a 30000-step upper bound
and validate every 5000 steps. This preserves the complete useful training
window while avoiding another uninformative 100000-step tail.

All candidates use the same data and fixed 200-file development evaluation.
The sealed LibriTTS set remains untouched. Valid results must preserve exactly
2400 bps, at most 30 ms lookahead, at most 700 total MFLOP/s, and at most 300
decoder MFLOP/s.

## Decision rule

Combine the two new pure-distillation seeds with the existing seed-20261025 D
reference to obtain a three-seed mean and sample standard deviation. Combine
the two new multiscale-plus-distillation seeds with a new seed-20261025
composition run only if the composition cannot be inferred from the registered
runs; until then, compare paired 3407/8128 composition results against pure
distillation and use the existing multiscale-only result as the structural
reference.

Prefer pure distillation unless the composition wins both paired seeds by a
margin larger than normal seed noise and does not materially regress ESTOI or
UTMOS. Do not promote a new strong baseline or use the sealed set until the
seed analysis is complete.
