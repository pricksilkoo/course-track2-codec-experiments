# Corrected from-scratch lookahead study: results

## Question and validity gate

This study asked whether the competition's 30 ms algorithmic-lookahead limit is
a major quality ceiling for the mature residual-later-heavy long-TCN
projected-RVQ codec. Four codecs were trained from the same never-trained
codec/discriminator state for 500000 steps. The only intended model difference
was encoder future context: 30, 40, 60, or 80 ms. Decoder lookahead remained
zero, seed and data order were shared, expanded future taps were zero
initialized, and the post-initialization RNG state was reset identically.

The interpretation gate required the 30 ms control to score at least 46.25 on
the fixed 200-file development set, remain component-compatible with the mature
46.7463 reference, and satisfy all competition constraints. It scored 46.5503,
so the gate passes. Relative to `strong_baseline_v2`, the control changes PESQ
by -0.0137, ESTOI by +0.0031, SI-SNR by +0.4063 dB, and UTMOS by -0.0689. This
is not a catastrophic component mismatch. The sealed LibriTTS confirmation set
was not used.

## Fixed-200 results

| Encoder lookahead | Selected step | Objective | Delta vs 30 ms | Delta vs strong v2 | PESQ | ESTOI | SI-SNR (dB) | UTMOS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 30 ms control | 475000 | 46.5503 | -- | -0.1961 | 1.9845 | 0.7319 | 5.5852 | 2.8368 |
| 40 ms | 500000 | 47.2073 | +0.6570 | +0.4609 | 2.0250 | 0.7333 | 5.8261 | 2.8659 |
| 60 ms | 500000 | **47.8593** | **+1.3091** | **+1.1130** | **2.0512** | **0.7379** | **5.9574** | **2.9086** |
| 80 ms | 450000 | 46.2402 | -0.3100 | -0.5061 | 1.9786 | 0.7275 | 5.8238 | 2.7877 |

The 40 and 60 ms cells improve every reported component relative to the valid
30 ms control. The 60 ms gain is therefore material rather than a scalar-score
trade-off. However, the response is strongly non-monotonic: increasing context
from 60 to 80 ms loses 1.6191 objective points and regresses PESQ, ESTOI, and
UTMOS below the control. More future context is not automatically better.

## Constraints and eligibility

| Lookahead | Bitrate (bps) | Total MFLOP/s | Decoder MFLOP/s | Parameters | Eligibility |
|---:|---:|---:|---:|---:|---|
| 30 ms | 2400 | 650.2272 | 277.44 | 662109 | competition-compliant |
| 40 ms | 2400 | 650.2592 | 277.44 | 662269 | research only: delay violation |
| 60 ms | 2400 | 650.3232 | 277.44 | 662589 | research only: delay violation |
| 80 ms | 2400 | 650.3872 | 277.44 | 662909 | research only: delay violation |

Every cell satisfies the bitrate and compute limits. Only the 30 ms control
satisfies the delay rule. The 40/60/80 ms models must not be submitted,
promoted, or evaluated on the sealed set.

## Training behavior

The corrected scratch curriculum resolved the failed positive control from the
earlier 100000-step study. Joint codec/RVQ reconstruction training ran through
step 99999; adversarial and feature-matching weights ramped over steps
100000--149999; full GAN training then continued to step 500000 with a 2e-4
peak learning rate and cosine decay.

The 30 ms validation reconstruction improved from 0.18110 at step 100000 to
0.13121 at its selected step 475000, close to the mature reference 0.13151.
The final validation reconstructions at step 500000 were 0.13128, 0.13005,
0.12980, and 0.13162 for 30/40/60/80 ms. The long schedule was therefore
necessary for a valid latency comparison.

## RVQ diagnostics

| Lookahead | Active codes by stage | Perplexity by stage | Marginal entropy sum (bits) | Full-rate SI-SNR (dB) |
|---:|---|---|---:|---:|
| 30 ms | 256 / 256 / 255 | 150.04 / 136.70 / 134.73 | 21.3980 | 5.5852 |
| 40 ms | 256 / 255 / 256 | 144.68 / 144.75 / 134.41 | 21.4246 | 5.8261 |
| 60 ms | 256 / 254 / 256 | 145.96 / 151.18 / 139.49 | 21.5535 | 5.9574 |
| 80 ms | 256 / 256 / 256 | 132.70 / 130.69 / 131.82 | 21.1245 | 5.8238 |

No cell exhibits dead-code collapse. The 60 ms winner has the highest summed
marginal entropy and full-rate SI-SNR, but differences in occupancy are modest
and do not explain the non-monotonic objective response by themselves.

Partial reconstruction is not progressively scalable for every cell. In the
30/40/60 ms models, individual projected stages can increase latent residual
MSE before the third stage compensates; the full three-stage output is the
functional unit. The 80 ms cell has cleaner one- and two-stage partial
reconstructions but worse final objective quality. Consequently, partial-stage
quality is not a reliable proxy for the submitted full-rate codec in this
learned projected-RVQ design.

## Decision

The corrected positive control makes the study interpretable. The evidence
supports a narrow conclusion:

- the 30 ms rule imposes a measurable quality cost at this seed, because 60 ms
  improves the objective by 1.3091 and improves all four component metrics;
- latency is not a simple monotonic or dominant ceiling, because 80 ms is worse
  than the valid control and the best point is an intermediate 60 ms;
- the result is best understood as a context/optimization sweet spot, not as
  evidence that unlimited future context would continue raising quality;
- because the winning cells violate the competition delay rule and this was a
  single-seed diagnostic, no over-limit checkpoint should be promoted and no
  further seed campaign is justified for deployment.

For the competition-compliant branch, continue to optimize causal modeling,
decoder synthesis, losses, or training stability within 30 ms. The over-limit
experiment has served its purpose: the rule costs some attainable quality, but
it is not the only or unbounded bottleneck.

## Checkpoint audit

| Cell | Checkpoint SHA-256 |
|---|---|
| 30 ms | `0a06fd2df88df26b175528291612ca19c4e86d43e756624c02bb256b337b2ed7` |
| 40 ms | `e97c5a93791518f5d63f73559e94b74da70b4bd97572a926d0b721daabc9765f` |
| 60 ms | `44ae8018494476bb66a1c211952ee063c3172678e7d7051fe39acd068f3800d7` |
| 80 ms | `d7041b0391fd4506ac67ac2b8059073094bd22231b5eaf4c9f1935fdc6a4a20e` |

