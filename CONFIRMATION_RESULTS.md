# Sealed confirmation results

## Protocol

- Date: 2026-10-22
- Data: LibriTTS `test-clean` and `test-other`, which are absent from the training and development manifests.
- Selection: 200 deterministic examples per split (400 total), seed `20261022`.
- Purpose: one-shot confirmation only. These results must not be used for checkpoint selection or repeated hyperparameter tuning.
- Audio: mono 16 kHz, prepared by `scripts/prepare_confirmation_set.py`.
- Selection manifest: `runs/confirmation_libritts_test_400/reference/selection.json` on the experiment server.

## Results

| Checkpoint | Score | PESQ-WB | ESTOI | SI-SNR (dB) | UTMOS |
|---|---:|---:|---:|---:|---:|
| Official baseline | 36.9167 | 1.6664 | 0.7104 | 1.1217 | 2.1817 |
| next4 B long TCN | 42.0528 | 1.7815 | 0.7329 | 3.1375 | 2.5789 |
| refine4 B, feature matching 2.0 | 42.9356 | 1.8232 | 0.7402 | 3.3356 | 2.6259 |
| refine4 D, adversarial 0.05 | **43.5903** | **1.8534** | **0.7449** | **3.4735** | **2.6645** |

The independent ordering matches the repeatedly used fixed-200 development set. Refine4 D leads all four component metrics and is therefore the confirmed initialization for the next factorial experiment.

## Constraints and provenance

| Checkpoint | SHA-256 | Bitrate | Total MFLOP/s | Decoder MFLOP/s | Delay |
|---|---|---:|---:|---:|---:|
| Official baseline | `4f19d236377b8f5d5c10e4f283d6cc80a35a80f081d5b6f135b605bdc7a6d96a` | 2400 | 608.768 | 244.480 | 0 ms |
| next4 B long TCN | `cd9ada0660d9f12f8c9271320f1e2e0128adf8a1ea6f61167e831de63fa5bffe` | 2400 | 676.032 | 265.152 | 30 ms |
| refine4 B, feature matching 2.0 | `d18f7339387b81ebb57d3f362898437fc4fa19efa957520dd6a7c7948f7314db` | 2400 | 676.032 | 265.152 | 30 ms |
| refine4 D, adversarial 0.05 | `9a5b24e3d573471d54a315b45cc3fde24bfec916e26b12d220fafa77baa55fd9` | 2400 | 676.032 | 265.152 | 30 ms |

All four encode/decode outputs passed exact 3-byte-per-10-ms-frame submission validation.

## Three-seed B/D confirmation

The B and D loss profiles were repeated with seeds `3407` and `8128`. Together
with the original seed `2026`, this gives three paired runs per profile. All
runs start from the same refine4-D checkpoint, train for 30,000 steps, and use
the fixed 200-file development set for checkpoint selection and comparison.

| Seed | B: FM 1.5 | D: FM 1.5 + SI-SNR 0.003 | D - B |
|---:|---:|---:|---:|
| 2026 | 45.4786 | 45.5554 | +0.0768 |
| 3407 | 45.4802 | 45.5053 | +0.0251 |
| 8128 | 45.4171 | 45.5569 | +0.1398 |
| Mean | 45.4586 | **45.5392** | **+0.0805** |
| Sample standard deviation | 0.0360 | 0.0294 | — |

D wins all three paired seeds. The selected final checkpoint is D seed `8128`,
which has the highest development score (`45.5569`) within the winning family.
Its checkpoint SHA-256 is
`8ff1abf2d5fb465ab7d8e3823eb8985db643130da03b20b881081667dd8fdb69`.

## Final one-shot confirmation

After the family and checkpoint were selected, only the chosen D seed-8128
checkpoint was evaluated on the 400-file LibriTTS test confirmation set.

| Score | PESQ-WB | ESTOI | SI-SNR (dB) | UTMOS |
|---:|---:|---:|---:|---:|
| **43.9842** | 1.8668 | 0.7476 | 3.7052 | 2.6787 |

This is `+0.3939` over the previously confirmed refine4-D score of `43.5903`
on the same set. The final checkpoint passes the exact bitstream validation and
retains 2400 bps, 30 ms delay, 676.032 total MFLOP/s, and 265.152 decoder
MFLOP/s.

## Projected residual-VQ structural confirmation

After the projected residual family completed its pre-registered three-seed
study, the lower-variance `48/64/80` family was selected. Exactly one of its
checkpoints, the original seed-20261024 `struct4_b_residual_later` candidate,
was evaluated on the sealed 400-file set.

| Checkpoint | Score | PESQ-WB | ESTOI | SI-SNR (dB) | UTMOS |
|---|---:|---:|---:|---:|---:|
| Previous confirmed D seed-8128 | 43.9842 | 1.8668 | 0.7476 | 3.7052 | 2.6787 |
| Projected residual later-heavy | **44.9637** | **1.9015** | **0.7561** | **4.0573** | **2.7267** |

The structural codec improves the sealed objective by `+0.9795` and improves
all four component metrics. Its checkpoint SHA-256 is
`f9c71919519dbda7d02bdfc56d6eb309cf9a45976d733e29b3fd808b7b77cc1a`.
The bitstream validator passed exactly three bytes per 10-ms frame. Measured
constraints are 2400 bit/s, 30 ms lookahead, 650.2272 total MFLOP/s, 277.440
decoder MFLOP/s, and 662109 parameters.

This one-shot confirmation promotes the projected residual codec to
`strong_baseline_v2`. The sealed result is a final confirmation result, not an
additional tuning target; the subsequent decoder study continues to use only
the fixed 200-file development set for model comparison.
