# Four-architecture 2.4-kbps sweep

These experiments are fixed-interface adaptations, not claims of exact paper
reproduction.  Every model emits three 8-bit RVQ indices per 10-ms frame at
16 kHz, uses at most 30 ms algorithmic delay, and is rejected by a preflight
check if total complexity exceeds 700 MFLOP/s or decoder complexity exceeds
300 MFLOP/s.

| Run | GPU | Architecture adaptation | Training schedule |
|---|---:|---|---|
| `arch4_a_vocodec_tf` | 0 | causal 30-ms STFT, ConvNeXt frame blocks, bounded PosNet-like attention, spectral decoder | MR-STFT GAN after 6k steps |
| `arch4_b_nanocodec_tf` | 1 | magnitude/energy decoupling, large-kernel gated blocks, explicit phase and energy losses | MPD + MR-STFT GAN after 8k steps |
| `arch4_c_winner_hybrid` | 2 | causal SnakeBeta waveform encoder, dilated residual units and GRU, spectral decoder | two-stage loss weighting and MPD + MR-STFT GAN |
| `arch4_d_phoenix_hybrid` | 3 | spectral encoder with GRU, causal SnakeBeta waveform decoder | reconstruction → GAN → reconstruction recovery cycle |

All runs use two-second crops, per-GPU batch 48, 30,000 optimizer steps, the
same VCTK/LibriTTS manifests, and the same fixed 200-file final evaluation set.
The runner writes the effective configuration, training metrics, objective
evaluation, complexity, best-checkpoint hash and status to `EXPERIMENT_LOG.md`.

Launch command:

```bash
scripts/launch_architecture_sweep.sh codec_architecture_sweep_v1 30000
```
