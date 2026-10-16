# Third-party models

This directory keeps external model source trees, isolated environments,
checkpoints, and evaluation artifacts outside the course codec implementation.

## Kyutai Mimi

- Source: `models/moshi` (official `kyutai-labs/moshi` shallow clone)
- Environment: `envs/mimi` (reuses the server's CUDA PyTorch)
- Checkpoint: `checkpoints/mimi/tokenizer-e351c8d8-checkpoint125.safetensors`
- Evaluation driver: `tools/evaluate_mimi.py`
- Outputs: `outputs/mimi_eval`

The evaluation uses local validation speech and produces 16-kHz reference WAVs,
Mimi reconstructions, serialized codes, runtime statistics, and the project's
standard PESQ/ESTOI/SI-SNR/UTMOS summaries. Mimi itself runs at 24 kHz; inputs
and outputs are resampled explicitly for comparison with the course evaluation.

Two settings are evaluated:

- 8 codebooks: 8 x 11 bits x 12.5 Hz = 1100 bit/s.
- 17 codebooks: 17 x 11 bits x 12.5 Hz = 2337.5 bit/s, the largest whole-codebook
  setting below the course 2400 bit/s cap.

Run the reconstruction again with:

```bash
third_party/envs/mimi/bin/python third_party/tools/evaluate_mimi.py
```
