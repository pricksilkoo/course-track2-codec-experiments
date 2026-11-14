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

## CHAMPION9新建模实验已启动（2026-11-08，结果尚待训练）

用户最终批准编码器全部取消独立latent TCN，仅比较分组卷积4/8与解码端TCN0/2层。
四组于北京时间2026-11-08约10:36在tmux codec_champion9_v1正式启动，实际epoch1优化进展、有限loss、
step0来源/config/metadata和启动前容量证据在CHAMPION9_LAUNCH.audit；不是只排队或只加载。

|cell|GPU|encoder groups|decoder TCN层数|total MFLOP/s|decoder MFLOP/s|
|---|---:|---:|---:|---:|---:|
|a_g4_d0|0|4|0|540.9538|236.960|
|b_g8_d0|1|8|0|524.8258|236.960|
|c_g4_d2|2|4|2|561.6258|257.632|
|d_g8_d2|3|8|2|545.4978|257.632|

新编码器：16kmono→k7因果入口→通道8/16/32/64/160、步幅2/4/4/5的4级残差下采样。
每级3个残差单元，膨胀1/3/9，SnakeBeta→分组k3卷积→SnakeBeta→dense1x1混组→残差；
下采样前另有SnakeBeta、kernel2stride和左padding=stride。随后逐帧LayerNorm→一次前瞻→单向残差GRU160→
原projected RVQ（3级256码字、48/64/80维）。编码analysis_temporal只含前瞻，blocks为空，不含独立TCN。
解码端可选原2层因果TCN，再接同一Fourier结构（256宽、160hidden、8因果调制块、320点IRFFT/hop160/OLA）。
所有权重随各组一起从头训练，“解码器不变”指结构不改，不是冻结旧权重。

这是对比赛冠军公开分组残差卷积/GRU思路的课程适配，并非其24k/20ms/不同码本的逐层复现。
前瞻预算统一改为2帧20ms，加10ms packet成帧=30ms总算法延迟，不把原报告30ms总延迟错当额外前瞻30ms。
历史51.667分数仅作回退参照，不能将新旧差异归因于单一因素；四组内部前瞻/损失等完全一致。
每10ms恰好3bytes/24bit=2400bps，解码不读下一帧；CPU前缀/扰动与实际码流测试验证边界和原长度。
计算量除Conv/Linear/GRU/RVQ外，计入GRU门、调制、保守IRFFT/OLA，以及SnakeBeta每元素36和每通道每调用65
操作的透明预算（sin/exp各按32），不是实测超越函数延迟；unclassifiedMAC0，各组均满足总700/decoder300限制。

seed/data-order20261108，所有codec/RVQ和D均新构造，global_step0；GRU/Fourier种子20461108（GRU内部+1），
D种子20361108，新decoderTCN种子20561108。相同形状初态配对共享，分组卷积形状不同时单独构造；
A/C、B/D共有模型张量相同，新增TCN为零输出残差，step0码流/音频一致。所有码本尚未kmeans、EMA更新计数0。
正式init只来自runs/champion9_setup/step0_CELL.pt，绝非C6/C7/C8已训练权重或烟测权重；源快照和历史模型哈希保留。

各组500000总步、batch32×2s/8workers、同394988train/14596valid，G/VQ lr2e-4、5k warmup/cosine到1e-5，
沿用原重建/SI=.003/GAN=.05/FM1.5等损失，GAN100k开始、150k full，不添加teacher/bypass/mel或其它训练因素。
每25k验证64batches，共20次，保留全部20个step/best/last；每1000步原子恢复last不伪造验证。
恰好8个开发评分权重：每组250k/500k，先训满再评测两个预定快照，按真实总分择优、平分取早，非reconstruction-best。
相同固定200dev真实编码/解码和4项评分、303858bytes/101286frames/16197971samples、选中完整RVQ诊断及8节点+4主记录。
本批n=1训练种子，是开发分数搜索，不是多seed确认；无新增sealed评测或自动v2晋升，不自动开下一批。

必要CPU回归64项13.75秒通过，静态语法检查通过；遵守用户要求未做GPU烟测/fullGAN反向profile，不能冒称新架构显存峰值已测。
启动时四张A40都空闲约45GiB。延续用户资源政策：允许共享、启动前显存>=8192MiB/磁盘>=10GiB，之后不轮询GPU/磁盘，
不因他人PID或显存下降主动停训；每1000步恢复保存，真实退出后诊断，不盲目无限重试、不改batch/预算或干预外部进程。
恢复只用本组最新last并继承两个optimizer/EMA；worker/crop/RNG重放可能非bitwise，需记录丢弃进度和attempt证据。
本地baseline只读，所有训练在远端；计划CHAMPION9_PLAN.md，初态审计CHAMPION9_SETUP.audit，4条主记录当前running。
目前没有训练完成或质量提升结论。后续完成写CHAMPION9_RESULTS.md/.audit、更新历史/本复盘并推送；原51.667和所有历史权重均保留。

<!-- CHAMPION9_FINAL_ARCHIVE -->

# CHAMPION9结果：分组卷积编码器从头训练、解码器TCN消融

## 结论与实验边界

四组全部从未训练step0完成500000总步，无失败、无恢复、无丢弃更新；每组20次真实训练验证，20份step快照与best/last均保留。
所有组按预登记250k/500k两点开发总分择优，均选500k。A/B/C/D选中分数依次47.9394438295/48.6240098787/49.3182054970/49.7109807091。
本批最好D（groups8、decoderTCN2）49.7109807091，相对历史最好51.6670665400下降1.9560858310分，四项均退步；保留CHAMPION8 c_from_b10作为整体回退。
在相同步数下，解码器TCN两个分组条件都增加总分；4→8组也均增加总分，但SI-SNR均下降，不能称全分量更好。
新编码器/激活/前瞻与历史均不同，新旧对比不是单因素。单seed20261108、固定200开发集搜索，非多seed或独立测试确认，不能宣称统计显著。
没有额外节点、延长、teacher、dev训练、sealed LibriTTS或自动晋升；strong_baseline_v2登记仍46.746343，不开始下一批。

## 模型、初始化与训练（自包含）

16k单声道→k7左因果入口→4级分组残差/下采样，通道8/16/32/64/160、步幅2/4/4/5。
每级3个残差单元、膨胀1/3/9：SnakeBeta→grouped k3→SnakeBeta→dense1x1混组→skip；下采样kernel2s、leftpad=s。
逐帧LN→一次2帧20ms有限前瞻→单向残差GRU160→原projected RVQ3×256、投影48/64/80。
编码独立TCN全为0（analysis_temporal.blocks为空）；decoderTCN0/2后接原Fourier256/hidden160/8因果调制块、320IRFFT/hop160/当前hop OLA。
这是公开冠军思想的可复现适配，不冒称逐层复刻。所有解码权重也从头训练，结构保持不等于冻结旧模型。
10ms成帧+20ms前瞻=30ms总算法延迟；解码不等下一个latent，160samples/帧、24bit/3bytes、2400bps，无隐藏旁路。

codec/RVQ/D真正全新构造global_step0；正式初态仅runs/champion9_setup/step0_CELL.pt，NOT C6/7/8或smoke。
seed/data-order20261108；D20361108；GRU/Fourier20461108（GRU内部+1）；新增decoderTCN20561108。
初态码本initialized全FALSE、EMAupdate_count0；A/C、B/D相同键逐tensor一致，零输出新TCN令配对step0码流/音频一致；不同group空间卷积形状独立构造。
初始优化器新建；本批实际未发生resume。setup/source/config/data/core-code原证据冻结未再生成，最终逐hash复核通过。

每组500000 TOTAL scratch steps、batch32×2s、8workers、394988训练/14596验证（VCTK40208/4247，LibriTTS354780/10349），非训练dev。
G/VQ lr2e-4，5000 warmup/cosine到1e-5，D固定2e-4、wd1e-6、clipG1/D10。
L1=1/spectral1/SC.25/linear.1/SI.003/commit.1/GAN.05/FM1.5；jointcodecRVQ从0，GAN<100k关闭，100k–150k渐增，之后full。
真实验证100k factor.00002、125k .50002、150k及以后1.0（实现按完成更新计入+1）。每25k验证64batches共20次，完整分量在audit。
每1000次完整G/D更新原子last、temp+fsync+replace；每组480个recovery_only事件、20次验证，未伪造metrics或新增搜索权重。
逐minibatch training_components日志未启用，不能从验证补造；保留原始pipeline与80条真实验证分量。
资源按用户最终政策共享，仅启动前>=8192MiB显存/10GiB磁盘检查，运行中无GPU/磁盘轮询或主动停训。未干预其它任务。
四个原tmux监督任务均exit0/complete；无重复启动、无actual OOM/Traceback/恢复，未保存更新丢失0；若未来恢复worker/crop/RNG仍可能非bitwise。

## 全部8个预登记开发搜索节点

|cell|step|总分|Δ历史最好|PESQ|ESTOI|SI-SNR dB|UTMOS|
|---|---:|---:|---:|---:|---:|---:|---:|
|a_g4_d0|250000|45.7075033539|-5.9595631861|1.97324715|0.73356779|6.35797189|2.63084974|
|a_g4_d0|500000|47.9394438295|-3.7276227105|2.08104682|0.74207971|6.47442160|2.81906794|
|b_g8_d0|250000|46.5026825269|-5.1643840131|2.00987372|0.73799604|6.19129239|2.71517441|
|b_g8_d0|500000|48.6240098787|-3.0430566613|2.10491566|0.75046587|6.35140197|2.88007717|
|c_g4_d2|250000|46.8049233144|-4.8621432256|2.00289926|0.74011889|6.37033248|2.74510834|
|c_g4_d2|500000|49.3182054970|-2.3488610430|2.14275988|0.75142720|6.49461644|2.92973114|
|d_g8_d2|250000|47.3925859441|-4.2744805959|2.03656015|0.74433846|6.18965539|2.80185420|
|d_g8_d2|500000|49.7109807091|-1.9560858310|2.15195896|0.75506487|6.33324945|2.98364798|

总分逐文件分别clip归一化再均值，不是先平均分量再裁剪：25×[clip((PESQ−1)/3.5)+clip(ESTOI)+clip((SI-SNR+10)/40)+clip((UTMOS−1)/4)]。
全部CSV四均值与总分独立重算误差<1e-10；每个节点完整四分量，不只呈现最好行。

## 同一步数的因素对照

|step|对照|Δ总分|ΔPESQ|ΔESTOI|ΔSI-SNR|ΔUTMOS|
|---:|---|---:|---:|---:|---:|---:|
|250000|c_g4_d2-a_g4_d0|+1.09741996|+0.02965211|+0.00655110|+0.01236059|+0.11425860|
|250000|d_g8_d2-b_g8_d0|+0.88990342|+0.02668643|+0.00634242|-0.00163700|+0.08667980|
|250000|b_g8_d0-a_g4_d0|+0.79517917|+0.03662657|+0.00442825|-0.16667950|+0.08432466|
|250000|d_g8_d2-c_g4_d2|+0.58766263|+0.03366089|+0.00421957|-0.18067709|+0.05674586|
|500000|c_g4_d2-a_g4_d0|+1.37876167|+0.06171305|+0.00934750|+0.02019484|+0.11066320|
|500000|d_g8_d2-b_g8_d0|+1.08697083|+0.04704330|+0.00459900|-0.01815252|+0.10357082|
|500000|b_g8_d0-a_g4_d0|+0.68456605|+0.02386884|+0.00838616|-0.12301963|+0.06100923|
|500000|d_g8_d2-c_g4_d2|+0.39277521|+0.00919908|+0.00363766|-0.16136699|+0.05391684|

500k时decoderTCN：C−A +1.37876167，四分量均升；D−B +1.08697083，PESQ/ESTOI/UTMOS升、SI-SNR−.01815252dB。
500k时groups8−4：B−A +.68456605、D−C +.39277521，均以PESQ/ESTOI/UTMOS改善换取SI-SNR下降。
250k亦同向总分，不能据单seed宣称可普遍复现。500k相对250k四组均提高，但预定预算已经耗尽，不据趋势自动延长。

## 约束、独立证据与真实损失

|cell|参数|总MFLOP/s|decoder MFLOP/s|总算法延迟|
|---|---:|---:|---:|---:|
|a_g4_d0|1548960|540.9538|236.960|30ms|
|b_g8_d0|1542840|524.8258|236.960|30ms|
|c_g4_d2|1653280|561.6258|257.632|30ms|
|d_g8_d2|1647160|545.4978|257.632|30ms|

总/decoder均满足700/300限制，unclassifiedMAC0。包括GRU矩阵及门、调制、保守IRFFT/OLA；新增SnakeBeta按36op/元素+65/通道/次（sin/exp预算32）。
解析运算口径不是实测超越函数延迟，其他历史激活/归一化约定未改。CPU因果/字节/兼容64项13.75s和语法检查启动前通过，遵守用户要求无额外GPU smoke/反向profile；新架构fullGAN峰值未测，不能引用C7旧profile替代。
最终审计为只读CPU证据复核，不重复训练或重跑质量评分。8节点×200文件实际码流每节点303858bytes/101286frames/16197971samples；逐文件3×ceil(samples/160)、16kmono原长度、有限音频。
每个节点checkpoint、CSV/summary/复杂度/roundtrip及1600组bitstream/metadata/重建音频SHA、所有80step/best/last、step0/source/数据/核心代码和12条complete记录均验证；细节在CHAMPION9_RESULTS.audit。

以下为500k真实训练验证及末段训练loss，不是200开发集四项评分，也非逐batch分量：

|cell|最后train loss|wave L1|spectral|commit|G adv|FM|D|reconstruction|总validation|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|a_g4_d0|0.46313370|0.01321233|0.12004301|0.07864516|0.70435774|0.12300132|1.56119311|0.13325534|0.43162037|
|b_g8_d0|0.47727005|0.01337217|0.11953437|0.09626066|0.64028704|0.12014861|1.56548381|0.13290654|0.44140448|
|c_g4_d2|0.47124181|0.01328886|0.11870530|0.09382330|0.75511783|0.11874101|1.61138785|0.13199417|0.44168487|
|d_g8_d2|0.47191344|0.01324466|0.11687496|0.08372565|0.64434260|0.12636243|1.60879028|0.13011961|0.43560604|

## 完整路径RVQ诊断

四个选中节点均沿encoder→LN→lookahead→analysis_gru→projectedRVQ→可选decoderTCN→完整Fourier/synthesis运行，非跳过GRU代理；三层均256个活跃码字。

|cell|3级perplexity|3级潜在MSE相对降幅|1/2/3级SI-SNR dB|
|---|---|---|---|
|a_g4_d0|115.601/111.031/104.606|+40.059%/-5.508%/-16.327%|-9.92384/-0.84898/6.47442|
|b_g8_d0|117.615/123.617/107.436|+0.562%/+16.621%/+9.412%|-19.08483/-5.23933/6.35141|
|c_g4_d2|111.738/122.475/109.940|+19.632%/+0.680%/+4.395%|-13.26416/-1.13593/6.49462|
|d_g8_d2|126.266/108.443/113.865|+39.997%/+26.619%/-2.992%|-17.26442/-0.34378/6.33325|

潜在MSE降幅并不保证波形目标单调：如D第3级潜在MSE反升约2.99%，但三层波形SI-SNR由−.344升至6.333dB；不能据此删除码本。
所有组三层partial结果与实码流SI-SNR差<1e-4dB。稀疏plug-in联合熵受log2(frames)上限/向下偏差影响，不把24减该值解读为可用空闲容量。

## 权重、试听与归档

原音：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/fast_b64_2s_v1/validation_200`。

- a_g4_d0选中权重：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0/checkpoints/step_00500000.pt`；SHA `84e2ae9ca427d2c0fe2bfd198ccafce93d0f5783a0113f05eda427264c4107c7`。
  重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0/evaluation/step_00500000/reconstructed`。
- b_g8_d0选中权重：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0/checkpoints/step_00500000.pt`；SHA `7f42b0583d17dee046c1effe2e3041f468ec4bff2d7084cb6768ae46c7b87e10`。
  重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0/evaluation/step_00500000/reconstructed`。
- c_g4_d2选中权重：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2/checkpoints/step_00500000.pt`；SHA `4925e325195dc480663cea2717a64dae4de23dfd2f9699768e9c956ba7f05e5f`。
  重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2/evaluation/step_00500000/reconstructed`。
- d_g8_d2选中权重：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2/checkpoints/step_00500000.pt`；SHA `82e924efe948c517f4c74d2abeb0e93b4aed8ee6d01aabf01c572ef496aaf4a0`。
  重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2/evaluation/step_00500000/reconstructed`。

整体仍选历史模型：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_c_from_b10/checkpoints/interpolated.pt`，SHA `a5cffa2dfcf39fc69b36b84e8ca238e7cbd9408ee008a1042bb7bbb253e4eb19`。
历史重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_c_from_b10/evaluation/reconstructed`，分数51.6670665400，四项PESQ/ESTOI/SI-SNR/UTMOS分别2.22774523/0.76839200/6.62010526/3.12801473.
本批最好D四项相对历史均低，未替换历史结论/权重/注册项。两个节点的原始bitstreams/reconstructed/metrics均留在各run/evaluation/step_00250000或step_00500000，文件名与原音一致。
保留所有历史来源/teacher/comparison/averaging/scratch和C4–9所有best/final/评测快照；本次无下载/清理/删除任何模型文件。
结果CHAMPION9_RESULTS.md/.audit，初始化CHAMPION9_SETUP.audit，启动CHAMPION9_LAUNCH.audit，预登记CHAMPION9_PLAN.md，完整记录EXPERIMENT_LOG.md。
本批归档完成后删除仅codec-champion9-monitor这一个监控，不启动下一批；下一实验需用户另行批准。

## CHAMPION10四格容量实验已入队，尚未实际训练（2026-11-10）

用户批准保持CHAMPION9D结构大致不变、增加容量的四组实验。预注册先提交推送，随后仅一次启动持久tmux codec_champion10_v1。
同新seed/data-order20261110：A原规模，B只扩encoder通道8/24/40/80/160，C只扩Fourier hidden184，D两端扩；A/C原encoder8/16/32/64/160，A/B hidden160。
统一groups8、encoder独立TCN0、decoder因果TCN2、GRU160、原3x256 projectedRVQ dims48/64/80、20ms前瞻+10ms成帧=30msTOTAL；16kmono/160sample/24bit3bytes/2400bps。
总/decoder MFLOP/s：A545.4978/257.632，B640.58436/257.632，C575.277/287.4112，D670.36356/287.4112；参数1647160/1699688/1796536/1849064，均满足700/300。统一解析口径含SnakeBeta/GRU/IRFFT/OLA，unclassifiedMAC0，不冒称实测算子延迟。
68项远端CPU形状、真实字节往返、强制前瞻/前缀因果、梯度和旧兼容回归28.78s通过；未做用户禁止的额外GPU烟测/反向profile，新扩容fullGAN显存峰值未测。
codec/RVQ/D真正未训练step0，码本initializedFALSE/EMAupdate_count0，初始优化器新建；无任何学得C6–9或smoke权重。相同形状配对精确共享，A/C、B/D step0音频/码流完全一致。来源/config/data/code哈希冻结CHAMPION10_SETUP.audit，不再生成。
每组500000TOTAL、batch32x2s/8workers、394988train/14596valid；全部损失、lr/warmup/cosine/clip/weightdecay和GAN100k开始150kfull保持C9。每25k/64batches真验证共20条、保留20step+best/last，每1000完整更新原子last恢复EMA/G+D优化器；不补造逐batch分量。
先训满500k再只评每组250k/500k共8节点，同冻结200dev16197971samples/101286frames/303858bytes，实码流/原长度有限16kmono音频与PESQ/ESTOI/SI-SNR/UTMOS四指标；按实际总分选择、平分取早。
同端点B-A/D-C编码容量、C-A/D-B解码容量单因素对照，n=1不是确认；对历史C9还含seed变化，不能当纯容量提升。C8历史最佳51.66706654001837及其SHA保持回退，v2冻结46.746343，不自动晋升/新sealed评测/下一批。

首次监督检查四张卡可用显存均约7.4GiB，低于原8GiB启动门槛，因此四组目前只有健康容量等待任务，尚无run_metadata、真实优化或质量结果。证据CHAMPION10_QUEUE.audit；真正开始后另生成CHAMPION10_LAUNCH.audit，不能将本次排队当成训练启动。
监督器每30s仅启动前检查free>=8192MiB/disk>=10GiB，允许共享而不排斥其它PID；启动后child.wait，无GPU/磁盘运行期轮询，不停止其它任务、不改batch、不盲目重试。实际退出后先诊断和留证据，仅受影响组从最新自己的last恢复，仍500kTOTAL；无last披露丢失并从新step0重启，worker/crop/RNG重放非bitwise需披露。
保持一个低频监控，健康进展/不变等待静默；结果、失败/恢复/完成或需决定时通知。最终独立审计8节点+4主记录、80step快照、CSV重算/字节音频SHA/配对效应/全路径RVQ，写CHAMPION10_RESULTS.md/.audit，追加历史和中文复盘并限定commit/push main。保护所有历史权重，本地baseline只读，无清理/下载。完成删除仅本批监控，下一批另获批准。

## CHAMPION10部分真实启动：B/D已优化，A/C仍容量等待（2026-11-10）

同一tmux codec_champion10_v1、原四个监督进程未替换。D（两端加宽）随后B（仅编码器加宽）自行满足启动容量后进入正式scratch训练；A（原规模）、C（仅解码器加宽）仍由原健康监督器等待。未停止外部任务、未改batch或门槛、未增加GPU烟测/反向profile、未查询运行期显存/磁盘。
B/D的run_metadata确认从本批各自真正未训练step0启动，resume_checkpoint=null；pipeline有真实优化和有限loss，不是只加载。CPU只读检查原子last文件，证据CHAMPION10_PARTIAL_LAUNCH.audit：

|cell|审计last完整更新step|可见有限loss（日志滚动值，非开发评分）|
|---|---:|---:|
|b_enc|4000|0.5409|
|d_both|6000|0.2359|

检查点的model_config与冻结配置一致，RVQ update_count等于global_step、三层码本已由训练初始化，G优化器状态非空，D优化器对象保留但100k前状态为空符合GAN关闭计划。epoch/batch/model/RVQEMA/buffers/G+D优化器均在last内。没有resume事件、没有到25k，因而没有伪造验证、没有开发质量分数。
本批继续同seed20261110的2x2容量对照：groups8/encoderTCN0/decoderTCN2/GRU160/RVQ3x256/20ms前瞻不变，总延迟30ms、2400bps；B/D只扩encoder，C/D只扩Fourier hidden。每组仍500000TOTAL、batch32x2s/8workers，全部原损失和GAN100k–150k计划不变；先训满500k再只评每组250k/500k，共8节点，实际分数最高选择。历史C8回退不变，不启动新批次。
CHAMPION10_QUEUE.audit仍是最初四组等待的历史事实；本次partial审计不能当成四组全部启动。只有日后A/C也观察到真实有限优化时才运行一次capture_champion10_launch.py生成CHAMPION10_LAUNCH.audit；不得为补齐启动记录重跑launch/preflight或替换健康等待者。最终统一审计8节点、4主记录、80step快照和完整RVQ后另写结果与中文复盘。

## CHAMPION10四格容量实验已实际启动（2026-11-11取证，暂无质量结论）

用户批准结构大致不变、用更多计算容量，四组为新原规模对照/仅编码加宽/仅解码加宽/两端加宽。
同新seed/data-order20261110，从真正未训练codec/RVQ/D step0开始，初始优化器新建；非C9旧seed重跑、非已训练模型微调。
四个tmux codec_champion10_v1监督任务均已看到实际优化和有限loss，证据CHAMPION10_LAUNCH.audit。取证时A/C为epoch3，B/D为epoch10；各组异步开始，非同时启动。A/C已有25k真实验证，B/D已有100k真实验证并进入GAN渐增阶段；这些是训练验证记录，尚无开发集质量评分。

|cell|GPU|encoder channels|Fourier hidden|total MFLOP/s|decoder MFLOP/s|
|---|---:|---|---:|---:|---:|
|a_base|0|8/16/32/64/160|160|545.49780|257.6320|
|b_enc|1|8/24/40/80/160|160|640.58436|257.6320|
|c_dec|2|8/16/32/64/160|184|575.27700|287.4112|
|d_both|3|8/24/40/80/160|184|670.36356|287.4112|

其余结构全固定：groups8、k7入口、4级stride2/4/4/5、每级3个SnakeBeta/groupk3/dense1x1残差dilation1/3/9，无编码独立TCN。
LN→一次20ms前瞻→GRU160→原3级256码字projectedRVQ dims48/64/80→原2层decoderTCN→Fourier width256/8块/320IRFFT/hop160/当前hop OLA。
只扩中间encoder通道和Fourier hidden160/184；末端160、码本、GRU、前瞻与损失不变。10ms成帧+20ms前瞻=30msTOTAL，16kmono/160samples/3bytes/2400bps。
CPU计数包含GRU矩阵/门、调制、保守IRFFT/OLA及SnakeBeta36op/元素+65/通道/调用，unclassifiedMAC0，总700/decoder300均满足；不是实测算子延迟。
全新A共同来源、不同形状fresh，D编码来自新B其它来自新C；各单因素对照其它tensor精确一致，较宽decoder零输出残差使A/C、B/D step0音频和码流一致。
所有保存初态码本initializedFALSE/EMA0，新source/config/data/core-code哈希冻结SETUP.audit，禁止正式启动后再生成；D种子20361110、GRU/Fourier20461110（GRU内部+1）。

每组500kTOTAL scratch，batch32×2s/8workers、394988train/14596valid。G/VQ2e-4、5kwarmup/cosine1e-5、D2e-4、wd1e-6、clipG1/D10。
沿用L1=1/spectral1/SC.25/linear.1/SI.003/commit.1/GAN.05/FM1.5，GAN100k开始150kfull；不加mel/teacher/bypass或其它新因素。
每25k验证64batches共20真分量，保留20step+best/last；每1000完整更新原子last含模型/EMA/G+D优化器，recovery事件不伪造验证，未启用的逐batch日志不补造。
先训满500k再评测每组250k/500k，恰好8开发搜索模型，按实际总分选、平分取早，非reconstruction-best，无选择性延长/额外种子。
固定同200dev，每节点16197971samples/101286frames/303858真实字节、16kmono原长度有限音频、4评分/CSV/复杂度/checkpointSHA/选中完整GRU-RVQ-synthesis诊断。
同端点B−A/D−C编码容量、C−A/D−B解码容量，n=1不是确认实验；历史C9比较含seed差异。旧C8最佳51.6670665400保留回退，v2冻结46.746343不自动晋升。
遵守用户不做额外GPU烟测/反向profile，新扩容fullGAN峰值未实测；只做必要CPU形状/真实字节/因果/梯度/旧兼容与原子恢复回归，结果见setup日志。
资源只启动前>=8192MiB显存/10GiB磁盘，不足30s容量等候；允许共享，不因其它PID排他。启动后child.wait，无GPU/磁盘实时轮询/主动停止，无batch降低。
真实退出才诊断/留attempt证据，仅恢复受影响组自己的最新last继承EMA/G+D优化器，仍500kTOTAL，worker/crop/RNG重放可能非bitwise；无last披露丢失并回新未训练step0，重复真实共享OOM诊断后等待空闲卡。
本地baseline只读，C4–9归档不重跑、不清理任何历史来源/模型；无sealed新评测。仅一个本批监控，健康进展静默。
计划CHAMPION10_PLAN.md、初态CHAMPION10_SETUP.audit、实际启动CHAMPION10_LAUNCH.audit、4主实验running记录已保存；暂未完成训练、没有质量提升结论。
完成写CHAMPION10_RESULTS.md/.audit，追加历史和中文复盘、限定commit/push，通知全组结果及确切试听目录并删除本批监控；下一批另获批准。

## CHAMPION10四格 scratch 容量实验完成（2026-11-14）

四组均从本批真正未训练 step0 完成 500000 TOTAL 更新，严格先训练满再只评预登记的 250k/500k 两节点；四组实际均选择 500k。A/B/C/D 选中总分分别 49.1355576670、48.8660338454、49.5401376557、50.2135927469。最好 D 比同 seed 新对照 A 高 1.0780350799，比 CHAMPION9D 高 0.5026120379（但 seed 同时变化），仍比历史 C8 最好 51.6670665400 低 1.4534737931。

500k 同端点容量对照：编码器 B−A 为 −0.26952382，D−C 为 +0.67345509；解码器 C−A 为 +0.40457999，D−B 为 +1.34755890。编码器扩容存在明显上下文交互，解码器扩容在两个编码器条件下均提高总分。单 seed n=1 仅为开发探索，不作普遍确认。

独立终审 526 项全通过：4 主/8 节点 COMPLETE、80 step 快照、80 条真实验证、1920 条周期 recovery_only 且 0 个实际恢复事件；8 份 CSV 分数重算、每节点 200 files/16197971 samples/101286 frames/303858 bytes、逐文件码流契约、16 kHz 单声道原长度有限重建音频、checkpoint/config/source/data/code/200 原音/101 历史哈希与选中全路径 RVQ 均通过。四个 last 均含 500k 模型/RVQ EMA 与非空 G+D 优化器状态；无 resume、OOM、重启或丢弃更新。

复杂度/decoder MFLOP/s A 545.4978/257.632、B 640.58436/257.632、C 575.277/287.4112、D 670.36356/287.4112，参数 1647160/1699688/1796536/1849064，全部 30 ms 总延迟并满足 700/300 上限。完整结果 `CHAMPION10_RESULTS.md`，机器审计 `CHAMPION10_RESULTS.audit`，节点记录 `EXPERIMENT_LOG.md`。

历史 C8 checkpoint SHA `a5cffa2dfcf39fc69b36b84e8ca238e7cbd9408ee008a1042bb7bbb253e4eb19` 保持不变且继续回退；不更新 strong_baseline_v2、不做 sealed LibriTTS、不清理历史模型、不启动下一批。下一实验需用户另行批准。
