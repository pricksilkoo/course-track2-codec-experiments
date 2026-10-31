# From-scratch lookahead capacity study

## Question and controlled design

This study asks whether the competition's 30 ms algorithmic-lookahead limit is
the dominant quality ceiling. Four residual-later-heavy long-TCN projected-RVQ
codecs were trained for 100000 steps from the same never-trained initialization.
The codec and discriminator therefore both started untrained; no learned model
was inherited.

The shared step-0 checkpoint is
`runs/lookahead4_scratch_init/step0.pt` (SHA-256
`3488d8448d523d5db57aa4afe99c65f6bd9089092db661ab8ed4dcc97fd9196e`).
Shared parameters and step-0 forward outputs were verified identical. A
dedicated data-order seed and post-initialization RNG reset kept stochastic
training matched. The only intended model difference was encoder lookahead:
30, 40, 60, or 80 ms. Decoder lookahead remained zero.

All candidates used the same 394988-file training set, 14596-file validation
set, seed 20261024, losses, discriminator, three 256-entry codebooks, projected
stage dimensions `[48, 64, 80]`, and fixed 200-file development evaluation.
The sealed LibriTTS confirmation set was not used.

## Fixed-200 results

| Cell | Lookahead | Selected step | Score | Delta vs A | PESQ-WB | ESTOI | SI-SNR dB | UTMOS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A control | 30 ms | 100000 | 21.4078 | -- | 1.1707 | 0.4293 | 2.6145 | 1.2516 |
| B future | 40 ms | 100000 | **22.8386** | **+1.4308** | **1.1781** | **0.4859** | 2.5707 | 1.2499 |
| C future | 60 ms | 100000 | 21.7014 | +0.2936 | 1.1718 | 0.4461 | 2.3167 | 1.2488 |
| D future | 80 ms | 90000 | 22.5166 | +1.1088 | 1.1726 | 0.4791 | 2.3641 | **1.2524** |

The objective improvement is not monotonic: 40 ms is best, 60 ms falls close
to the control, and 80 ms recovers only part of the 40 ms advantage. Relative
to A, the score gains are mainly associated with ESTOI (+0.0566, +0.0168, and
+0.0498 for B/C/D). SI-SNR moves in the opposite direction (-0.0438, -0.2978,
and -0.2504 dB), while PESQ and UTMOS change only slightly. Thus additional
future context produces a metric trade-off, not a uniform reconstruction gain.

All four from-scratch scores remain far below the frozen `strong_baseline_v2`
development score of 46.7463. The best research-only cell B is lower by
23.9077 points. This comparison is not an architecture rejection: the study
deliberately removed the long warm-start lineage and shows that 100000 steps
from random initialization do not recover the mature checkpoint. It does mean
that the experiment can support only a matched within-study latency conclusion,
not a new absolute upper bound for the fully optimized model family.

## Constraints and eligibility

| Cell | Bitrate bps | Total MFLOP/s | Decoder MFLOP/s | Parameters | Eligibility |
|---|---:|---:|---:|---:|---|
| A | 2400 | 650.2272 | 277.440 | 662109 | competition-compliant |
| B | 2400 | 650.2592 | 277.440 | 662269 | research only: 40 ms |
| C | 2400 | 650.3232 | 277.440 | 662589 | research only: 60 ms |
| D | 2400 | 650.3872 | 277.440 | 662909 | research only: 80 ms |

Bitrate and compute satisfy the limits in every cell. Only A satisfies the
30 ms delay rule. B/C/D must never be promoted or submitted.

## RVQ diagnostics

| Cell | Active codes by stage | Perplexity by stage | Marginal entropy bits by stage | Sum entropy bits |
|---|---|---|---|---:|
| A | 256 / 256 / 252 | 47.76 / 61.69 / 56.56 | 5.578 / 5.947 / 5.822 | 17.347 |
| B | 256 / 256 / 255 | 47.29 / 53.03 / 60.16 | 5.564 / 5.729 / 5.911 | 17.203 |
| C | 256 / 256 / 256 | 52.74 / 57.70 / 55.60 | 5.721 / 5.851 / 5.797 | 17.368 |
| D | 256 / 256 / 254 | 43.30 / 59.88 / 49.67 | 5.436 / 5.904 / 5.634 | 16.974 |

There is no dead-code collapse and no monotonic increase in utilization with
lookahead. D actually has the lowest total marginal entropy, while B has the
best objective. Codebook usage therefore does not explain the score ordering.

The recorded projected-latent residual MSE increases after each stage in all
four cells (negative reported reductions). Because each stage has learned
analysis and synthesis projections, that raw coordinate-space diagnostic is
not a reliable monotonic energy measure for this model. The functional partial
reconstructions are more informative:

| Cell | SI-SNR with 1 / 2 / 3 stages dB | Spectral loss with 1 / 2 / 3 stages |
|---|---|---|
| A | -3.613 / -0.198 / 2.614 | 0.2859 / 0.2438 / 0.2061 |
| B | -3.459 / -0.014 / 2.571 | 0.2879 / 0.2457 / 0.2010 |
| C | -4.907 / -0.586 / 2.317 | 0.2993 / 0.2431 / 0.2036 |
| D | -3.706 / -0.512 / 2.364 | 0.2890 / 0.2431 / 0.2031 |

Each additional stage improves spectral reconstruction and SI-SNR, confirming
that all three stages contribute despite the coordinate-space MSE caveat.

## Revised decision: failed positive control

The 30 ms control did not recover the identical-architecture mature model:
21.4078 versus 46.7463. This is too large to treat as seed noise. The inherited
recipe was a warm-start adaptation schedule, not a valid scratch curriculum:
it froze the random codec for 5000 quantizer-only steps, introduced the GAN as
the codec first unfroze, and annealed a 2e-5 fine-tuning learning rate to 5e-6
within 100000 steps.

Therefore this study is **inconclusive about the mature latency ceiling**. Its
non-monotonic 30/40/60/80 ms ordering is only an observation in an undertrained
regime and must not support an upper-bound claim. Keep `strong_baseline_v2`
unchanged and do not evaluate or promote B/C/D. The corrected replacement is
pre-registered in `LOOKAHEAD_SCRATCH2_PLAN.md`; it uses joint scratch
pretraining, delayed GAN activation, 500000 steps, and an explicit positive-
control gate before interpreting lookahead.

## Checkpoint identities

| Cell | Best-checkpoint SHA-256 |
|---|---|
| A | `9fab76aac277d5dc1c1df56bb9b59b77bb90b9b1995c87be7def29e745055bef` |
| B | `88183ea9181ef2e076bb75f6e15bffc3dc6bff29cc9068c68087ffc957208c98` |
| C | `d1a9ff9062dcdfb90df122760f94b4f4df95e54feac5c3a414fb53c3415fad8f` |
| D | `064d67d6ac1b25260d649ebf38f6a967914443e373321c691cb7342725258f14` |
