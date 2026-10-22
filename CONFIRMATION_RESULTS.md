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
