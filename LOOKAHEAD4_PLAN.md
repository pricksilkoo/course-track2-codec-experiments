# Lookahead capacity study

## Question

Is the 30 ms competition lookahead limit a material quality bottleneck for the
confirmed residual-later-heavy codec, or is the current development score mainly
limited by representation, quantization, and synthesis capacity?

This is a diagnostic study, not a submission-candidate search. Models above
30 ms are intentionally ineligible for the competition.

## Controlled design

All four cells inherit `configs/struct4/b_residual_later.yaml`, use seed
20261024, and train both the codec and discriminator from step 0 for the same
100000-step schedule. No trained checkpoint is loaded. Data, batch size,
optimizer, loss weights, long-TCN architecture, projected residual VQ
`[48, 64, 80]`, bitrate, and validation protocol are fixed. Only encoder
lookahead changes.

| Cell | Encoder future context | Eligibility |
|---|---:|---|
| A control | 3 latent frames = 30 ms | competition compliant |
| B | 4 latent frames = 40 ms | research only |
| C | 6 latent frames = 60 ms | research only |
| D | 8 latent frames = 80 ms | research only |

The decoder remains strictly causal in every cell. A single seed-20261024,
never-trained step-0 snapshot supplies the common random initialization for all
shared codec and discriminator parameters. Expanded lookahead kernels copy the
same random 30 ms taps and zero-initialize only newly exposed future taps. Thus
all cells implement the same function at initialization without inheriting any
learned weights.

## Fixed constraints and evaluation

- bitrate must remain exactly 2400 bps;
- total compute must remain at most 700 MFLOP/s;
- decoder compute must remain at most 300 MFLOP/s;
- only B/C/D may violate the 30 ms lookahead limit;
- all cells use the same fixed 200-file development set;
- the sealed LibriTTS confirmation set is not used.

Report objective score, PESQ, ESTOI, SI-SNR, UTMOS, model complexity, RVQ
activity/perplexity/entropy, residual reduction, and partial-stage
reconstruction. Compare every cell with A and with `strong_baseline_v2`.

## Interpretation rule

- A monotonic and practically material gain with 40/60/80 ms is evidence that
  the competition latency limit is a real bottleneck.
- Small, non-monotonic, or component-tradeoff gains mean extra future context is
  not the dominant limitation and architecture/quantization/synthesis remains
  the more plausible ceiling.
- No over-limit model will replace the strong baseline or be evaluated on the
  sealed set.
