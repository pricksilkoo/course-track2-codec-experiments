# Decoder synthesis and distillation study

Date: 2026-10-25

## Question

The projected residual-VQ study established `struct4_b_residual_later` as
`strong_baseline_v2`. This study asks whether the next limitation is simply
unfinished optimization or the causal waveform synthesis path. All candidates
start from the same v2 checkpoint, use seed 20261025, train for 100000 steps,
and are selected by the same validation rule before evaluation on the same
fixed 200-file development set. The sealed LibriTTS confirmation set was not
used.

## Controlled variants

| Run | Deployment change | Training-only change |
|---|---|---|
| A control | None | 100000-step continuation |
| B multiscale | Zero-initialized causal full-band refiner, dilations 1/4/16 | None |
| C Haar subband | Fixed two-band Haar split/synthesis with a small causal band network | None |
| D teacher distill | None | Waveform and spectral distillation from the best residual-uniform teacher |

All four use projected residual VQ with three 8-bit stages and preserve exactly
2400 bps and 30 ms algorithmic lookahead.

## Fixed-200 results

| Run | Score | Delta vs v2 | Delta vs A | PESQ | ESTOI | SI-SNR | UTMOS | Total / decoder MFLOP/s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| v2 starting checkpoint | 46.7463 | - | -0.4480 | 1.9982 | 0.7288 | 5.1789 | 2.9057 | 650.227 / 277.440 |
| A control | 47.1943 | +0.4480 | - | 2.0098 | 0.7350 | 5.3355 | 2.9233 | 650.227 / 277.440 |
| B multiscale | 47.2741 | +0.5277 | +0.0797 | **2.0242** | **0.7353** | 5.3746 | 2.9146 | 657.139 / 284.352 |
| C Haar subband | 47.0528 | +0.3064 | -0.1416 | 2.0166 | 0.7340 | 5.3136 | 2.8992 | 657.075 / 284.288 |
| D teacher distill | **47.3227** | **+0.5763** | **+0.1283** | 2.0216 | 0.7319 | **5.3972** | **2.9368** | 650.227 / 277.440 |

The best checkpoint for every run was selected at 10000 new steps, even
though training was deliberately allowed to continue to 100000. Later GAN
training did not improve the validation selection metric.

## Complexity and validity

| Run | Bitrate | Lookahead | Total MFLOP/s | Decoder MFLOP/s | Parameters | Valid |
|---|---:|---:|---:|---:|---:|---|
| A control | 2400 | 30 ms | 650.2272 | 277.440 | 662109 | yes |
| B multiscale | 2400 | 30 ms | 657.1392 | 284.352 | 662346 | yes |
| C Haar subband | 2400 | 30 ms | 657.0752 | 284.288 | 662559 | yes |
| D teacher distill | 2400 | 30 ms | 650.2272 | 277.440 | 662109 | yes |

Checkpoint SHA-256:

- A: `1c2b8fc3dd57e12d5090a7452eb48835afc72eb31b5b866d953e0c14b8a2e4cd`
- B: `d552cf7378ac7e61d8ca92edd5f91d061112ce799263a69c34fb6aa96a93a544`
- C: `d19c7ea65e035dc1f46f4bdf58c10f7f7b08e616d5e846707fa36530f969b807`
- D: `85f233f386e3c346c46099080c69f853650c86dc58f33f87a70781e8ff53efb2`

## RVQ diagnostics

There is no codebook-collapse explanation for the score differences. Each
stage uses 255 or 256 of 256 entries. Marginal entropy remains approximately
7.06--7.28 bits and perplexity approximately 134--155 across candidates. The
three-stage partial reconstructions track the objective comparison: A, B, C,
and D reach 5.3355, 5.3746, 5.3135, and 5.3972 dB SI-SNR respectively. D also
has the strongest one-stage partial reconstruction (-10.4341 dB versus
-10.7037 dB for A), suggesting that distillation improves the information
organization seen by the synthesis path rather than merely changing code
occupancy.

## Interpretation

1. **The previous checkpoint was not fully exhausted.** A plain continuation
   contributes +0.4480, which is most of the observed gain.
2. **Full-band causal refinement is useful but modest.** B adds +0.0797 over A,
   improving PESQ, ESTOI, and SI-SNR at a cost of 6.912 decoder MFLOP/s and 237
   parameters.
3. **The tested Haar branch is not worthwhile.** C underperforms A by 0.1416
   despite almost the same extra compute as B. The fixed split likely
   constrains phase/full-band interaction too strongly for this small head.
4. **Training-only distillation is the best direction.** D leads A by +0.1283
   and B by +0.0486 while adding no deployment parameters, bitrate, delay, or
   compute. Its ESTOI is lower than A/B, so the gain is not uniformly dominant
   across every metric and needs seed confirmation.
5. **The useful training window is short.** Every selected checkpoint occurs
   at 10000 steps. Future studies should keep the long upper bound for safety
   but use denser early validation and checkpoint-based stopping; blindly
   spending 100000 steps is inefficient.

## Next decision

Treat D as the leading development candidate, not yet as a new frozen strong
baseline. The next four-GPU experiment should use the existing seed-20261025
results as references and run two additional seeds for each of:

- D distillation with the unchanged deployment model; and
- B multiscale refinement plus the same training-only distillation.

This simultaneously tests whether the zero-cost distillation gain is stable
and whether it composes with the smaller independent multiscale gain. Select by
three-seed mean and variance before any new sealed-set confirmation.
