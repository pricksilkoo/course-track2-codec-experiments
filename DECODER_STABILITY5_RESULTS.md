# Decoder stabilization follow-up results

Date: 2026-10-27

## Outcome

All four pre-registered candidates completed on the fixed 200-file development
set. No candidate was evaluated on the sealed LibriTTS confirmation set, and
`strong_baseline_v2` remains unchanged.

The late decoder-only averages increased the scalar objective at both seeds,
but did so almost entirely by increasing UTMOS while materially reducing PESQ,
ESTOI, and SI-SNR. They therefore pass the scalar-score retention rule but fail
the registered component-metric guardrail and are not retained as deployment
candidates. Delayed distillation lost at both seeds; both runs selected step
5000, before distillation was enabled, which is direct evidence that the
post-activation trajectory was not useful.

## Fixed-200 results

| Run | Intervention | Score | PESQ | ESTOI | SI-SNR | UTMOS | Selected step |
|---|---|---:|---:|---:|---:|---:|---:|
| A, seed 3407 | decoder-only average, steps 20k/25k/30k | **46.9762** | 2.0004 | 0.7316 | 5.2448 | 2.9219 | 30000 ancestry |
| B, seed 8128 | decoder-only average, steps 20k/25k/30k | **46.9475** | 1.9991 | 0.7301 | 5.2361 | 2.9256 | 30000 ancestry |
| C, seed 3407 | distillation off to 10k, ramp to 15k | 46.2324 | 2.0586 | 0.7425 | 5.5556 | 2.6619 | 5000 |
| D, seed 8128 | distillation off to 10k, ramp to 15k | 46.1260 | 2.0494 | 0.7416 | 5.5511 | 2.6593 | 5000 |

All four are valid at exactly 2400 bps, 30 ms algorithmic lookahead,
650.2272 total MFLOP/s, and 277.44 decoder MFLOP/s.

## Decoder-only late averaging

The matched raw-distillation references were 46.8630 at seed 3407 and 46.8433
at seed 8128. A and B improve them by +0.1132 and +0.1042, respectively, for a
paired mean gain of **+0.1087**. The scalar objective therefore satisfies rule
1 of `DECODER_STABILITY5_PLAN.md`.

The component comparison changes the decision:

| Seed | Delta PESQ | Delta ESTOI | Delta SI-SNR | Delta UTMOS | Delta score |
|---:|---:|---:|---:|---:|---:|
| 3407 | -0.0734 | -0.0103 | -0.2998 | +0.1730 | +0.1132 |
| 8128 | -0.0549 | -0.0118 | -0.3635 | +0.1628 | +0.1042 |

The average is therefore not a general reconstruction improvement. It moves
both seeds to a different point on the perceptual/fidelity trade-off, with a
large UTMOS gain masking consistent losses in all three signal-faithfulness
metrics. Rule 3 explicitly rejects this pattern. The result is still useful:
late decoder weights are functionally compatible, unlike early full-model SWA,
but uniform averaging is not an acceptable promotion rule for this objective.

RVQ utilization remained healthy. A/B used 256/256/256 and 256/256/255 active
codes. Their summed marginal entropies were 21.4619 and 21.3822 bits. Stagewise
residual-MSE reductions were [0.6461, 0.4129, 0.5363] and
[0.6416, 0.4023, 0.5428]. The trade is consequently in decoder synthesis, not
codebook collapse.

## Delayed distillation

C/D average 46.1792. This is 0.6739 below the matched raw-distillation mean and
0.1433 below the matched continuation-control mean. Each run's best checkpoint
is step 5000, while the teacher loss is disabled through step 9999. Validation
therefore rejected every checkpoint after the delayed teacher became active.

The branch fails both the scalar and causal criteria. The evidence supports a
narrow conclusion: the useful teacher signal must shape the early continuation
trajectory; postponing it does not protect the quantizer and instead removes
the period in which it was effective. C/D still have full 256-code activity and
healthy diagnostics, so the loss is not caused by dead codes.

## Checkpoints and reproducibility

| Run | Checkpoint SHA-256 |
|---|---|
| A | `75ace729d6bb12ee962dc1372f4163aea854bf3af1028b3efa1f3c3161de7d54` |
| B | `ad6267eb59ea884eeffdc914eb3c90fd7453668beea50427463e5173ada9cc95` |
| C | `bc9553092640b86dde4c8e39b93bff2b17252c7e05428b762c82c0d3a8094fee` |
| D | `22b0945e26a2849b5434eba32c8458c8e4c8a991a7ea1b66c501d47357a40a30` |

Dataset counts, effective configurations, training summaries, objective
metrics, complexity, constraints, and full RVQ diagnostics are recorded in
`EXPERIMENT_LOG.md` and the corresponding run directories.

## Decision and next step

- Close delayed distillation.
- Do not promote uniform late decoder averaging because it violates the
  component guardrail, even though the scalar score rises.
- Keep raw training-only distillation as a causally supported technique, but
  not as a new frozen baseline because its three-seed variance remains high.
- Keep `strong_baseline_v2` as the confirmed deployment reference.
- If further development is justified, use existing checkpoints first: search
  for a Pareto-safe decoder interpolation or checkpoint choice constrained not
  to regress PESQ, ESTOI, or SI-SNR materially. Pre-register those component
  bounds before any new training and reserve the sealed set for a single final
  promotion decision.
