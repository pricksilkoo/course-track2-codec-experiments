# Decoder synthesis study plan

Date: 2026-10-25

## Motivation

The structured-quantizer study established projected residual VQ as a robust
improvement, while three-seed confirmation found no reliable winner between
uniform `64/64/64` and later-heavy `48/64/80` stage dimensions. Fine-grained
codebook allocation is therefore closed as the immediate search axis.

This study holds the selected lower-variance residual-later codec, bitrate,
lookahead, encoder, latent TCN, quantizer, training data, losses, seed, and
100000-step budget fixed. It changes only the decoder-side synthesis treatment
or a training-only teacher signal.

## Runs

| GPU | Run | Change |
|---:|---|---|
| 0 | `decoder4_a_control` | Low-LR continuation control; no deployed architecture change. |
| 1 | `decoder4_b_multiscale_refiner` | Zero-initialized causal full-band residual head with dilation 1/4/16 branches. |
| 2 | `decoder4_c_haar_subband` | Zero-initialized two-band Haar residual correction with a small causal band network. |
| 3 | `decoder4_d_teacher_distill` | Baseline deployment graph plus training-only waveform and spectral distillation from the best uniform-family seed. |

All runs warm-start codec and discriminator state from
`runs/struct4_b_residual_later/checkpoints/best.pt`. New refinement heads start
as exact identities. The teacher in D is frozen, is not serialized into the
student, and adds no deployed parameters or computation.

## Evaluation and decision rule

Each run trains for 100000 steps and is evaluated on the same fixed 200-file
development set. The sealed LibriTTS set is not used for these four candidates.
All candidates must preserve exactly 2400 bit/s, no more than 30 ms algorithmic
lookahead, no more than 700 total MFLOP/s, and no more than 300 decoder
MFLOP/s.

The primary comparison is course objective score against the continuation
control, supported by PESQ, ESTOI, SI-SNR, UTMOS, validation reconstruction,
and RVQ diagnostics. A structural head is retained only if it improves the
objective without a material component regression. Because this is one seed,
small margins below normal seed variation are treated as inconclusive.

