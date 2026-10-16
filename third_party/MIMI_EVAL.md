# Kyutai Mimi local evaluation

Date: 2026-10-16

## Provenance

- Official source: `https://github.com/kyutai-labs/moshi`
- Source commit: `e6a55d2722a65870ef52a6c9f6ecfc0e90f38362`
- Hugging Face repository: `kyutai/moshiko-pytorch-bf16`
- Checkpoint: `tokenizer-e351c8d8-checkpoint125.safetensors`
- Checkpoint size: 384,644,900 bytes
- Checkpoint SHA-256: `09b782f0629851a271227fb9d36db65c041790365f11bbe5d3d59369cf863f50`
- Trainable/model values: 79,308,609 parameters

## Evaluation setup

Twenty files were selected at even intervals from
`data/manifests/vctk_libritts/valid.scp`, for a total of 84.684 seconds. The
course evaluator requires mono 16-kHz WAV, so each source was normalized to
that format, resampled to Mimi's native 24 kHz for encoding, decoded at 24 kHz,
then resampled back to exactly the reference length at 16 kHz.

Mimi has a 12.5-Hz token rate and 2,048 entries per codebook, so an uncompressed
index needs 11 bits. Two prefix lengths were evaluated:

- 8 codebooks: `8 * 11 * 12.5 = 1,100 bit/s`.
- 17 codebooks: `17 * 11 * 12.5 = 2,337.5 bit/s`, the largest whole-codebook
  prefix below the course's 2,400-bit/s cap.

## Objective results

| Setting | Nominal bitrate | PESQ | ESTOI | SI-SNR | UTMOS | Course objective score |
|---|---:|---:|---:|---:|---:|---:|
| Mimi 8q | 1,100 bit/s | 2.1269 | 0.7775 | 1.8647 dB | 3.4849 | 50.4318 |
| Mimi 17q | 2,337.5 bit/s | 2.8974 | 0.8438 | 5.9340 dB | 3.7376 | 61.7158 |

The 17-codebook setting gains 11.28 points on the course objective score over
the standard 8-codebook setting. It also improves every component metric.

## Runtime

On one NVIDIA A40 with cuDNN disabled because of the host's known torch
2.11/cuDNN 9.19 handle failure, the warmed 17-codebook run measured:

- Encode real-time factor: 0.00506.
- Decode real-time factor: 0.00784.

The recorded 8-codebook aggregate includes one-time CUDA kernel initialization
in its first two files. Excluding those two warm-up files, its encode real-time
factor is approximately 0.0056, similar to the 17-codebook run.

## Artifacts

- Full run metadata: `outputs/mimi_eval/run_summary.json`
- Fixed file list: `outputs/mimi_eval/selected_files.txt`
- References: `outputs/mimi_eval/reference`
- 8-codebook WAV: `outputs/mimi_eval/reconstructed_8q`
- 17-codebook WAV: `outputs/mimi_eval/reconstructed_17q`
- Serialized token indices: `outputs/mimi_eval/codes_8q` and `codes_17q`
- Per-file metrics: `outputs/mimi_eval/metrics_8q` and `metrics_17q`
- Five convenient listening triplets: `outputs/mimi_eval/listening`

## Constraint warning

This is a quality reference, not a valid course submission. Mimi uses an
80-ms frame (`1,920 / 24,000` seconds), already exceeding the course's 30-ms
delay limit, and its 79.3-million-parameter architecture has not been shown to
fit the course compute limits. The 17-codebook prefix respects the raw bitrate
cap, but the architecture and latency do not.
