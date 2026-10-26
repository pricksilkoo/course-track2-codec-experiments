# Decoder stabilization follow-up plan

Date: 2026-10-26

## Motivation

The matched control study established a causal +0.5307 mean benefit from
waveform/spectral distillation, while early full-model SWA lost 2.0755 points
on average. The failure coincided with lower stage-one perplexity and marginal
entropy despite nearly complete code occupancy. This follow-up separates two
possible repairs: average only the decoder after the GAN regime has stabilized,
or delay the teacher signal so it cannot perturb the early quantizer trajectory.

## Registered experiments

| Run | Seed | Intervention | Training cost |
|---|---:|---|---:|
| A | 3407 | Decoder-only uniform average of raw-distill steps 20000/25000/30000; all encoder and quantizer state from step 30000 | evaluation only |
| B | 8128 | Same decoder-only stable-window average | evaluation only |
| C | 3407 | Distillation off through step 9999, ramped from 0 to full weight over steps 10000--14999 | 30000 steps |
| D | 8128 | Same delayed/ramped distillation | 30000 steps |

All candidates use `strong_baseline_v2` ancestry, the same fixed 200-file
development set, and no sealed data. A/B reuse already-completed raw-distill
training trajectories; C/D are fresh matched runs. The original raw-distill
scores are 46.8630436 (seed 3407) and 46.8432698 (seed 8128). Matched
continuation controls are 46.3005183 and 46.3444345.

## Decision rules

1. Retain decoder-only averaging only if it improves both raw-distillation
   seeds, or its paired mean gain is at least 0.05 with no seed dropping more
   than 0.05.
2. Prefer delayed distillation over raw distillation only if it wins both seeds,
   or its paired mean gain is positive without a drop larger than 0.05 or a
   material component-metric regression.
3. A method that improves only UTMOS while materially reducing PESQ, ESTOI, or
   SI-SNR is rejected as an unstable metric trade.
4. Do not change `strong_baseline_v2` or use the sealed LibriTTS set
   automatically.
5. Valid candidates must remain exactly 2400 bps, at most 30 ms lookahead,
   at most 700 total MFLOP/s, and at most 300 decoder MFLOP/s.

## Final documentation requirement

After all four runs, write `CODEC_EXPERIMENT_REVIEW.md`: a self-contained audit
of the full project history covering the official baseline, each hypothesis,
all experiment families and configurations, dataset/evaluation protocol,
positive and negative results, decision rules, checkpoint lineage, constraint
checks, failure/recovery events, interpretation, remaining uncertainty, and a
reasoned next-step recommendation. Cross-check numeric claims against
`EXPERIMENT_LOG.md` and the per-study result documents.
