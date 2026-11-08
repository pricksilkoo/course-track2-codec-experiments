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

## 14. Late decoder averaging and delayed distillation

The registered stabilization follow-up tested two function-preserving ideas at
seeds 3407 and 8128. A/B averaged only decoder parameters from raw-distillation
steps 20000/25000/30000 while retaining step-30000 encoder and quantizer state.
C/D disabled distillation through step 9999 and ramped it to full weight over
steps 10000--14999. Full results are in `DECODER_STABILITY5_RESULTS.md`.

Late decoder averaging scored 46.9762 and 46.9475, improving the matched raw
distillation scores by +0.1132 and +0.1042. However, both gains came from UTMOS
(+0.1730 and +0.1628) while PESQ, ESTOI, and SI-SNR all fell materially. The
method therefore passes the scalar objective threshold but fails the registered
component-metric guardrail and is not retained for deployment.

Delayed distillation scored 46.2324 and 46.1260, a paired mean loss of 0.6739
against raw distillation and 0.1433 against continuation controls. Both runs
selected step 5000, before distillation was enabled, so validation supplied no
evidence that the delayed teacher phase helped. This branch is closed.

All candidates satisfy exactly 2400 bps, 30 ms lookahead, 650.2272 total
MFLOP/s, and 277.44 decoder MFLOP/s. RVQ occupancy remained healthy; the
outcomes are synthesis/optimization trade-offs rather than codebook collapse.
The sealed set was not used, and `strong_baseline_v2` remains frozen.

## 15. From-scratch lookahead capacity study

Four residual-later-heavy long-TCN projected-RVQ codecs were trained for
100000 steps from one verified-identical never-trained codec/discriminator
initialization. The only intended difference was encoder lookahead: 30, 40,
60, or 80 ms. Decoder lookahead remained zero. A matched data-order seed and
post-initialization RNG reset kept stochastic training aligned. The fixed
200-file development scores were:

| Lookahead | Score | Delta vs 30 ms | PESQ | ESTOI | SI-SNR | UTMOS |
|---:|---:|---:|---:|---:|---:|---:|
| 30 ms | 21.4078 | -- | 1.1707 | 0.4293 | 2.6145 | 1.2516 |
| 40 ms | **22.8386** | **+1.4308** | 1.1781 | 0.4859 | 2.5707 | 1.2499 |
| 60 ms | 21.7014 | +0.2936 | 1.1718 | 0.4461 | 2.3167 | 1.2488 |
| 80 ms | 22.5166 | +1.1088 | 1.1726 | 0.4791 | 2.3641 | 1.2524 |

The response is non-monotonic and component-traded: extra context mainly
raises ESTOI, while SI-SNR falls and PESQ/UTMOS barely move. All codebooks stay
near fully active, and utilization does not track the score order. Functional
partial reconstructions confirm that every RVQ stage contributes.

All cells satisfy 2400 bps, total compute below 700 MFLOP/s, and decoder compute
below 300 MFLOP/s. Only the 30 ms control is competition-eligible; the other
three are research-only and must not be promoted. All four from-scratch scores
are also far below `strong_baseline_v2` 46.7463, showing that this 100000-step
scratch schedule does not recover the mature warm-start lineage.

The 30 ms control scored only 21.4078 versus 46.7463 for the identical mature
architecture, so the study failed its positive-control requirement. The
inherited recipe froze a random codec during a 5000-step quantizer-only phase
and used a short, low-learning-rate fine-tuning schedule. The non-monotonic
ordering is therefore only an undertrained-regime observation and cannot
establish the mature latency ceiling. `strong_baseline_v2` remains frozen. A
corrected 500000-step scratch curriculum and explicit control gate are
pre-registered in `LOOKAHEAD_SCRATCH2_PLAN.md`. The sealed set was not used.

## 16. Corrected from-scratch lookahead capacity study

The corrected study trained the same 30/40/60/80 ms cells for 500000 steps
from the same never-trained codec/discriminator state, but used a genuine
scratch curriculum: joint codec and projected-RVQ training from step zero, no
GAN through step 99999, an adversarial ramp through step 149999, and a 2e-4
peak learning rate with cosine decay. Full results are in
`LOOKAHEAD_SCRATCH2_RESULTS.md`.

The 30 ms control scored 46.5503 and therefore passed the registered 46.25
positive-control gate. Its selected validation reconstruction was 0.13121,
close to the mature 0.13151 reference. The latency comparison is consequently
valid:

| Lookahead | Objective | Delta vs 30 ms | PESQ | ESTOI | SI-SNR | UTMOS |
|---:|---:|---:|---:|---:|---:|---:|
| 30 ms | 46.5503 | -- | 1.9845 | 0.7319 | 5.5852 | 2.8368 |
| 40 ms | 47.2073 | +0.6570 | 2.0250 | 0.7333 | 5.8261 | 2.8659 |
| 60 ms | **47.8593** | **+1.3091** | **2.0512** | **0.7379** | **5.9574** | **2.9086** |
| 80 ms | 46.2402 | -0.3100 | 1.9786 | 0.7275 | 5.8238 | 2.7877 |

The 60 ms gain is material and improves every component, so the 30 ms rule has
a measurable cost at this seed. The response is nevertheless non-monotonic:
80 ms falls below the control. The result is an intermediate context sweet
spot, not evidence that future context is the dominant or unbounded quality
ceiling. All codebooks remain essentially fully active, and the 60 ms winner
has the highest summed marginal entropy, but occupancy alone does not explain
the ordering.

All cells satisfy 2400 bps and the 700/300 MFLOP/s limits. Only 30 ms is
competition-compliant; the other checkpoints are research-only, were not
promoted, and were not evaluated on the sealed set. `strong_baseline_v2`
remains frozen.

## 2026-11-02 — Champion-inspired controlled adaptation, first batch

At the user's request, register a four-cell2×2 study of LRAC2025 champion-inspired
causal Conv2Former modulation and training-only RVQ bypass / staged mel loss.
All cells continue the same frozen v2 checkpoint for100000 steps at matched
seed20261102, data order, optimizer schedule, validation and fixed200 evaluation.
Full design, adaptation limits, component guardrails and follow-up rules are in
`CHAMPION4_PLAN.md`. This is an adaptation study; no claim of reproducing the
champion or of receiving quality gains has been made before results exist.

In parallel, the user's checkpoint cleanup authorization was applied through
an audited, hash-verified inventory:301 redundant intermediate/smoke weights
removed,3.8444GiB reclaimed;78 checkpoint-directory files retained, plus the
separately protected scratch initialization and external weights. Every formal
run's selected checkpoint, teachers, parents and averaging sources survive.
See `CHECKPOINT_RETENTION.md` and `checkpoint_audits/20261102_applied.audit`.
Deleted intermediates have no backup; selected-model evaluations remain
reproducible, arbitrary restart from removed intermediate steps does not.

All31 tests and real-parent initial-output/index equality checks passed. Full
GAN profiling of D covered both quantized and bypass routes (reserved peak
7204/7126MiB). The user explicitly authorized sharing the existing GPU workload;
four100k workers launched in `codec_champion4_v1` on GPUs0–3 at13:47Asia/Shanghai.
The guards require20GiB GPU free at launch and stop only our pipeline below8GiB
GPU free or10GiB storage free. Quality comparisons remain pending.

## 2026-11-03 — Champion4 completed; checkpoint-selection diagnosis

All four100k runs completed without interruption. Pre-registered reconstruction
selection picked step5000 in every cell: A46.0115/B46.7819/C45.9936/D46.8959.
A failed the46.25 positive-control gate; early B/D gains cannot establish a
reliable breakthrough, and both fail component guards against frozen v2.

A separate, prospectively fixed-endpoint diagnostic was registered after these
primary scores, before evaluating any final100k quality scores. All four final
checkpoints were then evaluated on the same fixed200 set: A47.2383/B47.2584/
C47.1374/D47.1692. A recovered the reference level, while B-A was only+0.0201,
C-A=-0.1009 and D-A=-0.0691. The main lesson is a mismatch between lowest
reconstruction loss and perceptual quality, not evidence that100k continuation
never converged. Supplementary results do not replace the failed primary gate.

Close this small appended Conv2Former adaptation and the current bypass/mel
training package as deployment upgrades. Preserve best and final weights,
all8 explicit experiment records and frozen v2. Full metrics, phase analysis,
RVQ, hashes and paired-file uncertainty: CHAMPION4_RESULTS.md and its.audit.
Next investigate causal inverse-Fourier synthesis and encoder GRU as separate
architecture factors, only after a new plan and scratch-positive-control
resource/interface preflight. No sealed evaluation or baseline promotion.

## 2026-11-03 — Champion5 registered: GRU × causal Fourier synthesis, scratch

Register four architecture cells: A original waveform control; B encoder
forwardGRU; C causal Fourier/overlap-add synthesis; D both. Every codec and
discriminator starts untrained, with shared encoder/TCN/projected-RVQ/discriminator
states from the retained step0 snapshot, no inherited learned checkpoint.
Use the previously validated500k scratch curriculum and seed/data-order20261024.
Unlike the preceding selection failure, primary evaluation is fixed at500000
steps before any quality results exist. Reconstruction-best remains diagnostic.

All35 tests pass, including Fourier/GRU causality and actual3-byte/frame roundtrip.
Total/decoder MFLOP/s for A/B/C/D:650.2272/277.44,686.1152/277.44,
630.4192/257.632,666.3072/257.632. Conservative FFT/OLA and GRU gate costs included;
all remain16kHz,10ms/24bit frames,2400bps,30ms lookahead. Full-size GAN backward
profiling passed for B and D at reserved7064/6380MiB. Full hypotheses, parameters,
initialization matching, gates and resource rules: CHAMPION5_PLAN.md.

The four guarded workers launched in `codec_champion5_v1` on GPUs0–3 at
2026-11-03 08:53Asia/Shanghai and all started optimizer iterations. The existing
monitor was updated to this actual batch rather than duplicated. No current
quality result or baseline promotion is claimed.

## 2026-11-04 — Champion5 completed: Fourier family warrants seed confirmation

All four matched scratch runs completed500000 steps without recovery. Primary
evaluation used only the prospectively fixed last.pt on the same fixed200 dev
files, not reconstruction-best. A47.000583/B47.330493/C50.370972/D51.412604;
frozen v2 remains46.746343. A passed the46.25 positive-control gate. C and D beat
both A and v2 with all four component guardrails. B failed the v2 UTMOS guard
(-.04352) despite+.32991 over A. D-C=+1.04163 includes SI-SNR-.17052dB, so D
does not dominate C in every component. Synthesis main effect+3.72625, GRU
main effect+.68577, interaction+.71172, conditional on one training seed.

Actual200-file bitstreams/audio lengths,500k checkpoint hashes, finite training
and objective components, constraints and full-path RVQ diagnostics audited.
No separate minibatch training_components log was enabled; original25k validation
components and raw logs are retained. Details and machine-readable evidence:
CHAMPION5_RESULTS.md/.audit; reproducible scripts/audit_champion5_results.py.

No sealed evaluation, v2 promotion or checkpoint pruning. Close GRU-only as a
deployment upgrade, retain C as a lower-compute alternative. Pre-register exactly
four new scratch runs: A versus D at seeds3407 and8128, including new matched
untrained initialization, same500k curriculum/fixed endpoint. This confirms the
whole combined architecture, not individual mechanisms. See CHAMPION6_PLAN.md.

CHAMPION6 preflight passed35 pytest tests and full-size full-GAN backward checks
(control reserved7030MiB/candidate6364MiB). Two fresh initialization pairs and
all data hashes verified; preregistration committed/pushed d78829d before formal
training. Four guarded500k workers launched2026-11-04 17:35Asia/Shanghai in
codec_champion6_v1 and entered optimization. The same monitor now follows this
actual batch; no new confirmation quality result is claimed.

## 2026-11-06 — Champion6 complete: repeated candidate gains, control gate failed

All four new-initialization matched-seed runs finished500000 steps on Nov5,
without OOM, recovery, endpoint substitution or extension. Same fixed200 dev
files and true3-byte/frame bitstreams; no sealed evaluation or v2 promotion.
Seed3407: control45.974350 / Fourier+GRU51.624336, paired gain+5.649986.
Seed8128: control46.376849 / Fourier+GRU50.968929, paired gain+4.592080.
Both candidates improve all four components versus own control and frozen
v2=46.746343, with v2 gains+4.877993/+4.222586. However3407 control is below
the preregistered46.25 gate by.275650: this is NOT a full confirmation pass.
Do not hide this failure with the mean, a favorable seed, or the best candidate.

Two-new-seed descriptive means/ranges only: candidate51.296632
[50.968929,51.624336]; control46.175599[45.974350,46.376849]; paired gain
5.121033[4.592080,5.649986]. n=2 is limited; CHAMPION5 remains separate
discovery, not pooled confirmation. This is two matched pairs, not a new
factorial design; no independent GRU/Fourier effect or interaction claims.

Audit verified genuine untrained source/cell initialization, pairwise shared
model/discriminator tensors, seed/config/manifest hashes and counts,20 finite
validation component records,100k/150k GAN transitions,500k last.pt hashes,
all200 real bitstreams/audio lengths, component means/score and full-path RVQ.
Final35 pytest regressions passed7.05s. No separate minibatch component log
was enabled; raw pipelines and actual validation records are preserved.
No configuration/data/lineage/evaluation fault was identified. Weak control
quality is mainly perceptual/naturalness relative to v2, not SI-SNR collapse;
seed sensitivity is compatible with the observations, not a proven cause.
Late reconstruction changes do not clearly establish insufficient convergence.

Close this batch as confirmation-gate failure with promising experimental
candidates retained. No CHAMPION7, seed replacement, automatic capacity-matched
training or selective extension: a new control-stability protocol is needed
before further claims/training. Keep v2 and all historical/current best/last;
do not repeat the old cleanup. Consolidate and remove the existing monitor,
without creating a duplicate. Full report/audit: CHAMPION6_RESULTS.md/.audit;
reproducible checker: scripts/audit_champion6_results.py. Four complete native
records are in EXPERIMENT_LOG.md; self-contained Chinese review updated in
CODEC_EXPERIMENT_REVIEW.md.

## 2026-11-06 — Champion7 approved: score-oriented warm-start loss search

User explicitly changed the next-batch goal to competition development score
and approved four runs, then requested a trial despite shared GPU occupancy.
Prior CHAMPION6 conclusions remain unchanged; no retroactive confirmation pass.
All four inherit trained CHAMPION6 B500k score51.624336, SHA256
c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23,
including RVQ EMA/discriminator, but reset optimizers. This is NOT scratch.
A original losses; B SI-SNR weight.003→.010; C GAN weight.05→.10; D both.
Same100k additional steps, batch32/2s, new-stage seed/data-order20261106,
G/projection lr5e-5 warmup1k cosine1e-5; D lr5e-5, fullGAN from the start.

Search exactly four extra-step endpoints25k/50k/75k/100k per cell on the same
fixed200 dev files,16 weights total, selecting actual objective score rather
than reconstruction-best. Disclose the development search and all components;
retain the unchanged parent as fallback. No46.25 control veto or old+.15/
component guard promotion rule for this exploratory search, but fixed interface,
complexity/delay, genuine bitstream and audio-length checks remain mandatory.
No sealed evaluation, automatic v2 registry change or further batch launch.

Initially only7.2/11.2GiB free; one requested full-batch probe on GPU1 stopped
its own process group below8GiB free, with no OOM or external-process changes.
After external occupancy independently fell to~22GiB free/card, protected
supervisors launched all four at13:21Asia/Shanghai, after registration push
35e7e05. Full-batch/fullGAN two-step profiles all passed allocated5611.93/
reserved6382MiB and formal optimization began from the original learned parent,
not smoke. All42 CPU tests passed. Current~15GiB free/card; sharing slows initial
throughput to~2.5–2.7steps/s, so the earlier6h reference is not a launch ETA.
Full details CHAMPION7_PLAN.md, CHAMPION7_SETUP.audit/CHAMPION7_PROFILE.audit;
tmux codec_champion7_v1, one new heartbeat only. Private-group8GiB/disk10GiB
safety remains; no downloads/pruning or unrelated-process actions.

### Champion7 first safety-stop: idle-only queue, no saved stage progress

At13:56–13:57Asia/Shanghai the outside multi-GPU task increased its memory,
reducing GPUfree to257MiB on0 and1309MiB on1–3 before our guards terminated
only their private groups. No OOM/Traceback/nonfinite-loss token was found.
Last visible batches A5802/B5991/C6049/D6111 were below the first25k save,
so no formal checkpoint exists and this progress cannot be resumed. Preserve
raw logs/metadata/config/lineage in each run/attempts/attempt01_safety_stop;
SHA/recovery evidence CHAMPION7_RECOVERY01.audit. Original51.624336 parent
and all historical weights remain unchanged, no outcome/seed selection.

All four affected incomplete cells are now queued in the same tmux with
idle-only supervisors (omit --allow-shared), requiring no outside GPU PID
and>=20GiB free. Do not keep exploiting temporary free-memory troughs of
the same external job. At actual restart reload original trained500k parent,
same100k stage/seed/config; disclose the lost~35minutes/unsaved updates, not
claim a last.pt resume. Completed full-GAN profiles remain valid and must
never seed formal training. Future recovery after a saved last must resume
that last. The same monitor was updated, no duplicate automation or new batch.

### Champion7 second handoff stop: require600s continuously idle

At15:09–15:10Asia/Shanghai the outside job exited and the idle-only waiters
began loading. New outside task2016678 arrived at15:11; exclusive guards
stopped only our groups despite ample~44GiB free at the detection instant.
This was outside-PID exclusivity, not OOM or memory exhaustion. No new epoch
optimization progress was observed; no formal checkpoint/validation exists.
Attempt02 logs/metadata preserved separately, hashes CHAMPION7_RECOVERY02.audit;
attempt01 and its unsaved~6000-step disclosure remain unchanged.

Replace the short idle check with600s continuously eligible observations:
no outside GPU PID,>=20GiB free; any ineligible sample resets the timer.
Wait-only polling30s, runtime2s/8GiB/disk10GiB protection unchanged. Five new
pure state/time tests plus7 existing orchestration tests pass before rearming
only stopped incomplete cells. No sharing retries, seed/config/batch/endpoint
changes, duplicate monitor, external signals or historical checkpoint deletion.

### Champion7 third exclusive stop: resource-policy decision required

After600s idle the four cells launched16:40Asia/Shanghai and reached~1575
batches; new outside GPU PIDs triggered exclusive guards16:47 despite~38GiB
free. No OOM/Traceback/nonfinite loss; still before first25k checkpoint.
That~6m40s unsaved trajectory is not recoverable and is separate from the
earlier~6000 lost updates. Evidence/hashes CHAMPION7_RECOVERY03.audit and
run/attempts/attempt03_exclusive_guard; earlier archives/source remain intact.

All4 stopped, NO live capacity waiters, no automatic rearm. User asked to
choose ample-memory sharing with8GiB protection/frequent recovery saves, or
continue exclusive waiting. Until answered do not change resource policy,
checkpoint cadence, batch or training factors. No new quality results and no
batch8; same monitor tracks this decision state without repeated alerts.

### CHAMPION7: user approved memory-capacity sharing and1000-step recovery

User explicitly selected sharing whenever memory suffices, retaining8GiB floor.
This supersedes exclusive-PID/600s-idle and decision-hold policies. Launch threshold20GiB,
runtime2s GPU8GiB/disk10GiB unchanged. Add only recovery_checkpoint_interval_steps1000:
atomic last.pt with complete model/EMA/G+D optimizers and epoch/batch/step, no invented
validation or added search nodes. Existing25k validations and16-node dev search unchanged.
No formal last exists: restart original51.624336 parent, not lost attempts01/03 progress.
Preserve all old archives; evidence CHAMPION7_SHARED_RESTART.audit; no automatic batch8.

56 CPU tests passed11.33s before the user requested no further tests. Disposable full-batch
recovery smoke was cancelled at user request, evidence preserved, NOT a passing smoke.
Four formal shared supervisors rearmed in existing tmux; original trained500k parent only,
not disposable/old unsaved progress. Same monitor updated; no batch8 or quality result yet.

### CHAMPION7 recovery04: memory floor stop, retained real checkpoints

At2026-11-06T17:07:51–53Z external GPU memory rose, free4600/2561MiB, below8GiB.
Only own groups stopped; no OOM/Traceback/nonfinite in log tails, not a PID-exclusivity stop.
Resume last localA75000/B76000/C73000/D73000 with model/EMA/G+D optimizers; no parent reset.
A/B retain3 validations, C/D2. Immutable attempt04 logs/config/metadata/checkpoint copies and
SHA audit CHAMPION7_RECOVERY04.audit. Capacity waiters shared>=20GiB (currently8–12GiB),
no forced launch or new GPU tests. Budget100k total and16 search nodes unchanged; disclose
discarded unsaved updates and non-bitwise worker/crop/RNG replay. No automatic next batch.

### CHAMPION7 user resource policy05: prelaunch capacity only, no runtime polling

User explicitly requested run whenever it fits, no realtime resource detection; handle actual
failure afterwards. Overrides20GiB launch and8GiB runtime stop: opt-in launch>=8192MiB,
profile6382MiB+1810MiB headroom, prelaunch disk>=10GiB, no runtime GPU/disk queries or
proactive resource stop. Shared flag retained. Only four no-training-child waiters replaced;
report CHAMPION7_RESOURCE_POLICY05.audit, original waiter evidence archived. Resume genuine
A75000/B76000/C73000/D73000 last, no optimizer/model/EMA reset or new lost progress.1000-step
recovery retained; no new GPU tests. Defaults unchanged outside explicit opt-in. Same100k
budget/16 dev search nodes; actual failure gets diagnosis, not an infinite blind retry loop.

## CHAMPION7 complete — no improvement, keep51.624336 parent (2026-11-07)

All4 cells completed exactly100000 additional local steps,4 actual25k validations each,
16 declared fixed200 score-search weights and16 node+4 main COMPLETE experiment records.
Selected A100k51.52590320119037 (-0.09843293744895), B100k51.53128750969333
(-0.09304862894599), C75k50.24617303487055 (-1.37816310376877),
D100k50.00145192175998 (-1.62288421687934), all versus unchanged parent51.62433613863932.
All16 score/component rows and regressions appear in CHAMPION7_RESULTS.md/.audit.
SI emphasis gained B SI-SNR+0.31057453dB but lost PESQ/ESTOI/UTMOS; GAN.10 cells worse.
No successful score gain, no automatic continuation/promotion; retain parent and close batch.

Read-only final evidence audit independently recomputed CSV score aggregation, checked all16
checkpoint SHA/config/step, real200-file audio+byte roundtrips (16197971samples/101286frames/
303858bytes each), finite decoded audio/original lengths,4 selected full-path RVQ diagnostics,
20 complete records and frozen v2/parent hashes.1868064params,666.3072total/257.632decoder
MFLOP/s,2400bps,30ms,unclassified0. No new GPU tests/evaluation or sealed access.
Initial scratch-free trained-parent lineage and all discarded attempts/recovery04 saved steps,
non-bitwise worker/crop/RNG replay and latest no-runtime-resource-poll policy05 are disclosed.
All checkpoints/archives retained; no pruning. Full results and self-contained Chinese review
pushed main; this batch monitor deleted after archival. Next experiment requires user approval.

## CHAMPION8 complete — four zero-training decoder interpolations (2026-11-08)

最高新候选c_from_b10，51.6670665400，比父模型增加0.0427304014。
User approved exactly4 posthoc decoder-only parameter interpolations: C7A100k donor.10/.25 and C7B100k donor.10/.25, with trained C6B500k parent51.62433613863932. Zero new optimizer updates;98 decoder parameters mixed/113 tensors frozen, entire encoder/RVQ projections/codebook/EMA/all buffers parent-exact. Inference-only exports never overwrite parents.
All4 fixed200 actual encode/decode/quality/complexity complete and all4 experiment records verified. Each200 bitstreams byte-identical to parent,16197971samples/101286frames/303858bytes,16kmono original lengths/finite audio; independent CSV reaggregation and checkpoint/config/source hashes pass.1868064params,666.3072/257.632MFLOP/s,2400bps/30ms/unclassified0 unchanged. All scores/components/regressions reported in CHAMPION8_RESULTS.md/.audit and self-contained Chinese review. No sealed evaluation, registry promotion, new alpha nodes or automatic training. Next training requires separate approval.
