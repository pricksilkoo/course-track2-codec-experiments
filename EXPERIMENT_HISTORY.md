# Codec Modeling Experiment History

This document records why the current model looks the way it does, which ideas
worked, which did not, and how each round informed the next one. Scores below
are from the fixed 200-file development set unless explicitly marked as sealed
confirmation results.

## 1. Starting point: official course baseline

The supplied model is a causal waveform convolutional autoencoder with a
100-Hz latent sequence, three 256-entry residual codebooks, and a causal
transposed-convolution decoder. Each 10-ms frame transmits three bytes, giving
exactly 2400 bps.

- Fixed-200 score: `37.4414` (`37.4339` in the separately generated baseline
  report; the small difference comes from the recorded evaluation instance).
- Sealed LibriTTS confirmation score: `36.9167`.
- Complexity: 608.768 total and 244.480 decoder MFLOP/s.

An early fast-training run scored only `24.9042`. This established that a low
score was not automatically evidence against the architecture: training
schedule, segment length, batch size, EMA codebook updates, and GAN staging had
to be fixed before architecture conclusions were meaningful.

## 2. First controlled ablations

| Experiment | Main change | Score | Conclusion |
|---|---|---:|---|
| A train fix | batch 32, 2-s segments, EMA 0.95, improved schedule | 37.9104 | A reliable training recipe recovered and slightly exceeded the reference. |
| B perceptual | spectral convergence, linear magnitude, period critics | 37.9566 | Perceptual losses alone gave only a small gain. |
| C temporal | encoder 2-layer and decoder 1-layer causal TCN, 30-ms lookahead | **40.3124** | Temporal latent modeling was the first large architectural gain. |
| D factorized TCN | 32-D shared RVQ projection plus deeper TCN | 37.7866 | Naively shrinking all codebooks into one low-dimensional space destroyed useful detail. |

The main lesson was that temporal context mattered much more than simple
codebook compression. The 30-ms future allowance was spent once in the encoder;
the remaining temporal stacks stayed causal.

## 3. MiniMimi-inspired rebuild

Four small SEANet/Transformer variants were trained for 200k steps:

| Variant | Score |
|---|---:|
| Plain RVQ | 32.8036 |
| Split semantic/acoustic RVQ | 32.9588 |
| Decoder-heavy Transformer | 33.8339 |
| Hybrid temporal block | 34.7105 |

These were deliberately small, constraint-compliant interpretations of Mimi,
not the original large pretrained Mimi model. They underperformed because the
course compute ceiling forced narrow analysis/synthesis networks and small
Transformers, while the quantizer and decoder had to be learned from the
available course data. The result ruled out continuing to imitate the full
Mimi topology at this scale.

## 4. Long-TCN architecture selection

All four candidates started from the successful temporal model and received
170k additional steps.

| Experiment | Main change | Score |
|---|---|---:|
| A | unchanged temporal control | 42.9513 |
| B | 4 encoder + 2 decoder expansion-one TCN blocks | **43.7272** |
| C | WavLM guidance on RVQ stage zero | 42.5750 |
| D | bounded local Transformer | 42.5003 |

The long dilated TCN was both more effective and more compute-efficient than
the local Transformer. Directly forcing codebook zero toward WavLM features
hurt waveform reconstruction, so semantic supervision was not retained.

## 5. Loss and GAN refinement

Starting from long-TCN B:

| Experiment | Score |
|---|---:|
| Low-LR continuation | 43.8558 |
| Feature matching 2.0 | 44.6625 |
| SI-SNR weight 0.01 | 44.1082 |
| Adversarial weight 0.05 | **45.2681** |

The original GAN term was too strong. Reducing it improved every independently
checked component metric. On the sealed 400-file LibriTTS set, the sequence
official baseline → long TCN → stronger feature matching → weaker GAN scored
`36.9167 → 42.0528 → 42.9356 → 43.5903`, confirming that the development-set
ordering generalized.

## 6. Small loss factorial and seed confirmation

With adversarial weight fixed at 0.05, a 2x2 study tested feature matching 1.5
and SI-SNR 0.003:

| Profile | Score |
|---|---:|
| continuation control | 45.1760 |
| feature matching 1.5 | 45.4786 |
| SI-SNR 0.003 | 45.2666 |
| both | **45.5554** |

Across seeds 2026, 3407, and 8128, feature matching alone averaged `45.4586 ±
0.0360`, while the combination averaged `45.5392 ± 0.0294` and won all three
paired comparisons. The selected seed-8128 checkpoint scored `45.5569` on
development and `43.9842` in the single final sealed confirmation.

## 7. RVQ utilization study

The selected checkpoint used almost every code but had stage perplexities
`140.4 / 132.6 / 137.7`, corresponding to 21.29 summed marginal bits rather
than 24 perfectly uniform bits. Crucially, stages two and three still reduced
residual MSE by 41.9% and 31.9%, so they were not dead.

A 2x2 study tested stable assignment balancing and stronger commitment on the
later residual stages:

| Profile | Score | Delta vs input checkpoint |
|---|---:|---:|
| A continuation | 45.6565 | +0.0996 |
| B assignment balance | 45.6244 | +0.0675 |
| C later-stage commitment | 45.8099 | +0.2530 |
| D both | **45.8473** | **+0.2904** |

Uniform occupancy was not the objective by itself: balancing alone did not
beat continued training. The useful signal was stronger residual-error
reduction, especially in later stages. D is now registered as
`strong_baseline_v1`.

## 8. Current modeling principles

The retained design choices are:

1. A causal waveform encoder/decoder is a stronger use of the compute budget
   than the small MiniMimi replica tested here.
2. Four encoder and two decoder expansion-one dilated TCN blocks provide the
   best temporal context found under the limit.
3. The encoder consumes the entire three-frame lookahead allowance once; the
   decoder remains causal.
4. Three 8-bit codebooks at 100 Hz guarantee the exact 2400-bps payload.
5. A weaker GAN, moderate feature matching, and very small SI-SNR term balance
   perceptual texture and waveform fidelity.
6. Codebook perplexity is diagnostic, not a target. A change is useful only if
   it improves residual reduction and final reconstruction.

Repeated micro-tuning of loss coefficients, adding more steps to the same
checkpoint, direct semantic forcing, and replacing the TCN with a tiny
Transformer are now considered exhausted directions.

## 9. Next structural question

The next study keeps the encoder, TCN, decoder, bitrate, delay, and validated
loss recipe fixed. It changes only how the three transmitted bytes divide the
latent representation:

- projected residual VQ: every stage owns an independent learned subspace but
  still encodes the remaining common-space residual;
- product VQ: the three bytes encode complementary learned subspaces in
  parallel;
- uniform `64/64/64` versus later-heavy `48/64/80` projection dimensions.

This 2x2 design tests sequential residual coding against independent product
coding and tests whether allocating more representation dimension to later
bytes helps. All four retain exactly three uint8 indices per frame and use a
separate higher learning rate plus a short quantizer-only adaptation phase for
the newly initialized projection layers. The analytical preflight is identical
for all four: 650.227 total MFLOP/s, 277.440 decoder MFLOP/s, 30-ms lookahead,
and 662,109 deployed parameters.
# Structural quantizer conclusion (2026-10-24)

The controlled projected-quantizer 2 x 2 study is complete; full tables and diagnostics are in `STRUCTURAL_RESULTS.md`.

- Projected residual VQ, 64/64/64: 46.683654.
- Projected residual VQ, 48/64/80: **46.746343**.
- Product VQ, 64/64/64: 46.361507.
- Product VQ, 48/64/80: 46.359523.
- Frozen pre-study strong baseline: 45.847260.

This changes the diagnosis of the plateau. The surrounding long-TCN waveform codec still had headroom, but the useful direction was a learned lower-dimensional residual hierarchy rather than independent product partitions. Residual VQ improved the score by about 0.35 over product VQ under matched compute and projected dimensions. Later-heavy allocation added a smaller +0.063 within the residual family. All variants used almost every code, so occupancy was not the deciding signal; partial-stage reconstruction showed that product VQ's early partitions carried very little standalone information.

The current strong-baseline marker remains frozen pending multi-seed confirmation. `struct4_b_residual_later` is the leading candidate for that confirmation.

## 10. Residual stage-allocation seed confirmation

The one-seed `64/64/64` versus `48/64/80` comparison was repeated with seeds
3407 and 8128, giving three matched seeds per family:

| Family | Three-seed score | Worst seed | Paired wins |
|---|---:|---:|---:|
| Residual uniform `64/64/64` | **46.7332 ± 0.1097** | **46.6570** | 1 / 3 |
| Residual later-heavy `48/64/80` | 46.6869 ± 0.0532 | 46.6438 | 2 / 3 |

Later-heavy minus uniform was `+0.0627`, `+0.0137`, and `-0.2151` across the
three paired seeds. Uniform has the slightly higher mean, later-heavy has about
half the variance, and the paired direction conflicts. Under the pre-registered
rule this is a practical tie, with later-heavy retained only as the
lower-variance continuation branch. All six runs beat `strong_baseline_v1`, so
the robust finding is the projected residual hierarchy itself, not the exact
stage-dimension split.

This closes fine-grained stage allocation as the immediate search axis. The
next useful experiment should keep projected residual VQ fixed and change a
larger causal synthesis factor, such as multi-scale decoder refinement or a
lightweight sub-band synthesis head, under the decoder-compute limit. The
frozen strong-baseline marker was not changed and the sealed set was not used.

### One-shot promotion after the study

Following the pre-registered tie rule, the lower-variance later-heavy family
was chosen for one sealed confirmation. Its seed-20261024 checkpoint scored
`44.9637` on the 400-file LibriTTS set versus the previous confirmed `43.9842`,
a gain of `+0.9795`, while improving all four component metrics. The checkpoint
therefore became `strong_baseline_v2`. The following decoder study does not use
the sealed set for candidate comparison.

## 11. Decoder synthesis and training-only distillation

Starting from `strong_baseline_v2`, four matched seed-20261025 continuations
were trained for 100000 steps and evaluated on the fixed 200-file development
set. Full details are in `DECODER4_RESULTS.md`.

| Variant | Score | Delta vs v2 | Total / decoder MFLOP/s |
|---|---:|---:|---:|
| A continuation control | 47.1943 | +0.4480 | 650.227 / 277.440 |
| B causal multiscale refiner | 47.2741 | +0.5277 | 657.139 / 284.352 |
| C Haar subband synthesis | 47.0528 | +0.3064 | 657.075 / 284.288 |
| D training-only distillation | **47.3227** | **+0.5763** | 650.227 / 277.440 |

Most of the gain came from another short continuation: all four selected their
best checkpoint at 10000 new steps, and the control alone gained 0.4480. The
full-band multiscale head added a smaller +0.0797 over control, while the tested
Haar head lost 0.1416. Training-only waveform/spectral distillation was best,
adding +0.1283 over control with no deployment cost. Codebook occupancy and
entropy remained healthy, so this is a synthesis/training effect rather than a
codebook-collapse repair.

D is the leading development candidate but is not promoted from a single seed.
The next registered study should add two seeds for D and for multiscale plus
distillation, then compare three-seed mean and variance before using the sealed
confirmation set again.

## 12. Distillation seed stability and multiscale composition

The decoder follow-up added seeds 3407 and 8128 for pure training-only
distillation and for multiscale refinement plus distillation. Full results are
in `DECODER_SEED4_RESULTS.md`.

Pure distillation scored 47.3227, 46.8630, and 46.8433 across seeds 20261025,
3407, and 8128, for **47.0097 +/- 0.2713** (sample standard deviation). The
original 47.3227 result is the high member of the distribution, so it is not a
robust basis for replacing `strong_baseline_v2`.

The multiscale composition lost to pure distillation at both matched new seeds:
-0.1666 at seed 3407 and -0.0577 at seed 8128, for a paired mean of -0.1121.
All runs satisfy 2400 bps, 30 ms lookahead, 700 total MFLOP/s, and 300 decoder
MFLOP/s limits. RVQ occupancy, entropy, residual reduction, and partial
reconstruction remain healthy and do not explain the composition loss.

The multiscale-plus-distillation branch is closed without a third seed.
`strong_baseline_v2` remains frozen. The next clean causal experiment is a
matched two-seed continuation control versus pure distillation, rather than
another decoder-head change. The sealed confirmation set was not used.

## 13. Decoder causal controls and early-window SWA

Matched no-distillation controls at seeds 3407 and 8128 scored 46.3005 and
46.3444. The corresponding raw distillation runs scored 46.8630 and 46.8433,
giving paired gains of +0.5625 and +0.4988 and a paired mean of **+0.5307**.
Because distillation wins both seeds without a material component regression,
it satisfies the pre-registered causal criterion: the teacher signal adds a
real perceptual synthesis benefit beyond ordinary continuation.

The registered early-window averages of steps 2500/5000/7500/10000 scored
44.5262 and 45.0291. They lose 2.3368 and 1.8142 points against their matched
raw-distillation runs, so SWA decisively fails the retention rule. PESQ,
ESTOI, and SI-SNR all regress despite slightly higher UTMOS. RVQ active-code
counts remain near complete, but stage-one perplexity and total marginal
entropy fall and full-rate reconstruction degrades. This indicates that
averaging across the early GAN/quantizer trajectory breaks functional
alignment even though simple occupancy still looks healthy.

All four candidates remain valid at exactly 2400 bps, 30 ms lookahead,
650.2272 total MFLOP/s, and 277.44 decoder MFLOP/s. Full metrics and hashes are
in `DECODER_STABILITY4_RESULTS.md`. The sealed set was not used and
`strong_baseline_v2` remains unchanged.

The stable conclusion is therefore narrower than the best single-seed score:
training-only distillation is causally useful, but its raw three-seed result
still has substantial variance. Early-window SWA is closed. A future stability
study should use a function-preserving alternative such as training-time EMA
or a late, already-stable averaging window, screened on matched development
seeds before any sealed confirmation.
