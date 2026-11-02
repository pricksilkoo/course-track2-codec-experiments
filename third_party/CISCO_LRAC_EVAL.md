# Cisco LRAC 2025 Track-1 local evaluation

Date: 2026-11-02

## Provenance

- Official source: `https://github.com/cisco-open/espnet`
- Source commit: `032f90047e8d7783905f59da32330f6970008ba1`
- Checkpoint: `egs2/lrac/track1/baseline_model/LRAC2025_Track1_baseline_model.pth`
- Checkpoint SHA-256: `c6e6429db50bbf72c15e8813c5dd6ef8549bc50d9d4f2456de67d26f7f081f70`
- Native sampling rate: 24 kHz
- Latent frame rate: 100 Hz, or one frame per 10 ms

## Evaluation setup

The released Track-1 checkpoint was evaluated on the same fixed 200-file
development set used by the project experiments. The source files are mono
16-kHz WAV. Each file was resampled to the model's native 24 kHz, encoded and
decoded, then resampled back to 16 kHz and restored to the exact source length.
The existing course implementation computed PESQ, ESTOI, SI-SNR, UTMOS, and
the per-file-normalized aggregate score.

The model has six 1,024-entry RVQ layers. At 100 frames/s, each transmitted
layer costs 1,000 bit/s. The official training recipe samples only the 1- and
6-kbit/s endpoints. The 2- and 3-layer runs below are diagnostic unsupported
intermediate prefixes, not trained operating points.

## Objective results

| Setting | Status | Nominal bitrate | PESQ | ESTOI | SI-SNR | UTMOS | Course score |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 RVQ layer | Official training endpoint | 1,000 bit/s | 1.1358 | 0.5292 | -32.5224 dB | 1.4391 | 16.9470 |
| 2 RVQ layers | Unsupported diagnostic | 2,000 bit/s | 1.1316 | 0.4674 | -14.5104 dB | 1.2809 | 14.4537 |
| 3 RVQ layers | Unsupported diagnostic | 3,000 bit/s | 1.1942 | 0.5633 | -9.5983 dB | 1.3458 | 18.4684 |
| 6 RVQ layers | Official training endpoint | 6,000 bit/s | 2.3686 | 0.8298 | 0.7189 dB | 3.0844 | 50.2515 |

For context, `strong_baseline_v2` scores 46.7463 at exactly 2,400 bit/s on
the same 200 files. Cisco's 6-kbit/s result is 3.5052 points higher, but it
uses 2.5 times the bitrate and is not a valid same-rate comparison. The
highest whole-layer Cisco prefix within the 2.4-kbit/s course limit is the
unsupported 2-kbit/s point, which scores 32.2926 points below
`strong_baseline_v2`.

## Interpretation and limitations

- The 6-kbit/s endpoint demonstrates that the small Cisco 100-Hz architecture
  can reconstruct this development set reasonably well when given six RVQ
  layers.
- The poor, non-monotonic 2- and 3-layer results do not establish that the
  architecture is intrinsically weak at those rates. The released training
  schedule optimizes only one or six layers, so intermediate residual prefixes
  are out of distribution for the decoder.
- The released model cannot represent exactly 2,400 bit/s: every layer adds
  10 bits per 10-ms frame, so the available rates are integer kbit/s.
- Scores include a necessary 16-to-24-to-16-kHz resampling adapter because the
  course evaluator and fixed development set operate at 16 kHz.
- This was an external quality reference. It does not alter the retained
  project baseline or qualify the Cisco checkpoint as a course submission.

## Artifacts on the experiment server

- Official source tree: `/storage1/hehaoran/project/cisco-lrac-espnet`
- 1/3/6-kbit/s outputs: `runs/cisco_lrac_track1_official_eval`
- 2-kbit/s outputs: `runs/cisco_lrac_track1_official_eval_2kbps`
- Evaluation driver: `third_party/tools/evaluate_cisco_lrac.py`
