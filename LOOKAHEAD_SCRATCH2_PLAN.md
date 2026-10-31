# Corrected from-scratch lookahead study

## Motivation

The first 100000-step scratch study failed its positive control. Its 30 ms
control scored 21.4078 instead of approaching the identical-architecture
`strong_baseline_v2` score of 46.7463. The cause is a schedule mismatch rather
than a demonstrated architecture limit: the inherited structural fine-tuning
recipe froze a random encoder/decoder for 5000 quantizer-only steps, enabled
the GAN as the codec first unfroze, used a 2e-5 fine-tuning learning rate, and
annealed it to 5e-6 by step 100000.

The earlier study remains an audit record but is inconclusive about the mature
model's latency ceiling. This replacement study trains the same four
architectures from the same untrained initialization with a scratch-specific
curriculum.

## Controlled cells

| Cell | Encoder future context | Eligibility |
|---|---:|---|
| A control | 3 latent frames = 30 ms | competition compliant |
| B | 4 latent frames = 40 ms | research only |
| C | 6 latent frames = 60 ms | research only |
| D | 8 latent frames = 80 ms | research only |

All cells use the residual-later-heavy long-TCN projected-RVQ architecture,
decoder lookahead zero, seed 20261024, identical data order and RNG reset, the
same fixed training and validation manifests, and the same never-trained step-0
codec/discriminator snapshot:

`runs/lookahead4_scratch_init/step0.pt`

SHA-256:
`3488d8448d523d5db57aa4afe99c65f6bd9089092db661ab8ed4dcc97fd9196e`

Expanded future taps are initialized to zero, so all four cells implement the
same function at step 0. The only intended model difference is lookahead.

## Scratch curriculum

Each cell trains for an initial budget of 500000 steps:

1. Steps 0--99999: joint encoder, projected RVQ, and decoder optimization with
   reconstruction, spectral, commitment, usage, and SI-SNR terms. No codec
   module is frozen and the adversarial factor is zero.
2. Steps 100000--149999: the discriminator becomes active and adversarial plus
   feature-matching weights ramp linearly to their configured values.
3. Steps 150000--500000: full codec/GAN training.

The codec learning rate warms to 2e-4 over 5000 steps and then cosine-decays to
1e-5 over the complete 500000-step schedule. The projected RVQ learning rate
is 2e-4 from step 0. Validation and checkpointing occur every 25000 steps.

## Positive-control gate

This study is interpretable as a latency-capacity experiment only if A recovers
the mature architecture. The target is the previous fixed-200 score 46.7463.
The minimum acceptance gate is:

- fixed-200 objective at least 46.25 (within 0.50 of `strong_baseline_v2`);
- no catastrophic component mismatch relative to the previous model;
- exactly 2400 bps, at most 700 total MFLOP/s, at most 300 decoder MFLOP/s,
  and exactly 30 ms lookahead.

If A misses the gate, no conclusion about the 30 ms ceiling is allowed. The
training curves and checkpoint must be diagnosed before any extension. An
extension may resume all four matched cells only if it preserves the controlled
comparison; a single overtrained cell cannot be compared with the others.

## Evaluation and decision rule

All four cells use the fixed 200-file development set only after training. The
sealed LibriTTS confirmation set is prohibited. Report objective, PESQ, ESTOI,
SI-SNR, UTMOS, selected step, complexity, checkpoint SHA-256, and full RVQ
diagnostics.

Only after A passes the positive-control gate:

- monotonic and materially large improvement from 30 to 40/60/80 ms supports
  latency as a real ceiling;
- small, non-monotonic, or component-tradeoff changes reject latency as the
  dominant ceiling;
- B/C/D remain research-only and can never be promoted or submitted.

