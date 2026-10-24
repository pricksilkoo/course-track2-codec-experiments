# Structured quantizer study

Date: 2026-10-24

## Question

The pre-study strong baseline (`strong_baseline_v1`) already used a well-trained long-TCN causal codec and a three-stage EMA RVQ. The remaining question was whether the plateau came from:

1. the residual coupling between codebooks;
2. an unsuitable equal-capacity allocation across stages; or
3. the surrounding encoder, temporal model, decoder, and loss recipe.

To isolate the quantizer structure, this study kept the waveform model, long TCN, loss weights, 2-second segments, data, seed, bitrate, delay, and evaluation set fixed. Only quantizer composition and stage dimensions changed.

## Controlled 2 x 2 design

| Run | Quantizer composition | Projected dimensions | Fixed-200 score |
|---|---|---:|---:|
| A `struct4_a_residual_uniform` | projected residual VQ | 64 / 64 / 64 | 46.683654 |
| B `struct4_b_residual_later` | projected residual VQ | 48 / 64 / 80 | **46.746343** |
| C `struct4_c_product_uniform` | product VQ | 64 / 64 / 64 | 46.361507 |
| D `struct4_d_product_later` | product VQ | 48 / 64 / 80 | 46.359523 |
| Previous strong baseline | full-latent EMA RVQ | 160 / 160 / 160 | 45.847260 |

All four models emit three uint8 indices per 10 ms frame and therefore preserve exactly 2400 bit/s. Their measured complexity is identical: 650.2272 MFLOP/s total, 277.44 MFLOP/s on the decoder side, 30 ms algorithmic lookahead, and 662,109 parameters.

The sealed LibriTTS confirmation set was not used.

## Objective metrics

| Run | PESQ | ESTOI | SI-SNR | UTMOS | Score | Delta vs baseline |
|---|---:|---:|---:|---:|---:|---:|
| A | 1.98547 | **0.72928** | 5.16467 | **2.90956** | 46.68365 | +0.83639 |
| B | **1.99815** | 0.72878 | **5.17889** | 2.90565 | **46.74634** | **+0.89908** |
| C | 1.97667 | 0.72564 | 5.01183 | 2.89791 | 46.36151 | +0.51425 |
| D | 1.98267 | 0.72615 | 4.98001 | 2.89186 | 46.35952 | +0.51226 |

The average residual-VQ score is 46.714998, while the average product-VQ score is 46.360515. Holding dimensional allocation constant, residual composition is worth about +0.3545 score.

Later-heavy allocation changes residual VQ by +0.06269 but changes product VQ by -0.00198. The interaction is therefore material: moving capacity to later stages helps only when later stages refine a shared residual.

## Codebook diagnostics

All variants activate essentially every code and have marginal entropy around 7.0-7.24 bits per stage. Occupancy alone therefore does not distinguish a useful codebook from a poorly organized one.

| Run | Active codes | Perplexities | Per-stage error reduction | Partial SI-SNR at 0.8 / 1.6 / 2.4 kbit/s |
|---|---|---|---|---|
| A | 256 / 256 / 256 | 143.2 / 138.3 / 139.5 | 67.6% / 40.8% / 57.7% | -8.33 / -3.01 / 5.16 dB |
| B | 256 / 256 / 256 | 141.9 / 140.6 / 143.1 | 72.2% / 49.0% / 44.6% | -8.61 / -1.74 / 5.18 dB |
| C | 256 / 256 / 255 | 140.0 / 128.3 / 151.3 | -0.7% / 24.6% / 60.8% | -37.00 / -13.74 / 5.01 dB |
| D | 256 / 256 / 256 | 129.3 / 129.6 / 149.4 | 3.1% / 37.9% / 52.8% | -45.01 / -10.51 / 4.98 dB |

The key difference is not whether indices are diverse. It is whether early stages carry a coherent coarse representation. Residual VQ makes stage 1 immediately useful and lets later stages refine the same signal. Product VQ partitions the latent into independently projected subspaces; its first partition carries almost no standalone reconstruction value, and even two partitions remain much worse. The decoder can combine all three partitions into a reasonable waveform, but the organization is less efficient for this low-rate, progressive three-index budget.

## Interpretation

1. The previous model had not reached the overall architecture ceiling. A quantizer-only structural change improves the fixed-200 score by up to 0.899 without increasing bitrate, delay, or compute.
2. Residual refinement is the correct inductive bias for this task. Product VQ should not be the main branch for the next round.
3. Equal stage dimensions are already strong. Later-heavy residual allocation gives a small additional gain, mostly through PESQ and SI-SNR, but the +0.0627 margin is small enough to require seed confirmation.
4. Full codebook occupancy is not proof of optimal utilization. Partial reconstruction and per-stage error reduction reveal utility that active-code counts and marginal entropy miss.
5. The training validation ranking predicted the final fixed-200 ranking, but checkpoint selection still matters: A, B, and C selected their 100k checkpoints, while D selected its 80k checkpoint.

## Decision

`struct4_b_residual_later` is the leading structural candidate, not yet the promoted strong baseline. The frozen `strong_baseline_v1` marker remains on `codebook4_d_combined` until the new structure survives repeated seeds and one final sealed-set confirmation.

Recommended next step:

1. repeat A and B with two additional seeds;
2. choose residual-uniform versus residual-later by three-seed mean rather than the single best run;
3. promote the winning residual family only after stability is established;
4. then run exactly one sealed confirmation evaluation;
5. only after that explore residual-only refinements such as 32/64/96 allocation, learned analysis/synthesis regularization, or stage-dropout training.

## Checkpoints

| Run | Selected step | SHA-256 |
|---|---:|---|
| A | 100000 | `64d230d565e0eb3c9f137ae44ac9b88a4bbcf68fc4ff6b0dd3edf552d06ecc4a` |
| B | 100000 | `f9c71919519dbda7d02bdfc56d6eb309cf9a45976d733e29b3fd808b7b77cc1a` |
| C | 100000 | `9bc86aab038bba0f27907d42d9e93213bd1767acd509af5b6a284089a2e316c5` |
| D | 80000 | `01451a47dd2f893a8e50ac0569fc05e707bd1f1f48cb0596553aaa26e9681033` |
