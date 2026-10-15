# V2 Four-GPU Ablation Plan

These experiments use one independent training job per A40. All four jobs warm-start from the
700k-step reference checkpoint, use two-second crops and stop after 30,000 new optimizer steps.
This avoids the very large DDP global batch that produced only 46,260 updates in `fast_b64_2s_v1`.

| GPU | Run | Change from previous row | Total MFLOP/s | Decoder MFLOP/s |
|---:|---|---|---:|---:|
| 0 | `ablation_a_trainfix` | Corrected LR schedule and faster RVQ EMA adaptation | 608.768 | 244.480 |
| 1 | `ablation_b_perceptual` | Spectral convergence, linear magnitude and period discriminators | 608.768 | 244.480 |
| 2 | `ablation_c_temporal` | Two encoder TCN blocks, one decoder TCN block and 30-ms encoder lookahead | 675.744 | 265.056 |
| 3 | `ablation_d_factorized_tcn` | 32-D factorized RVQ, four encoder and two decoder TCN blocks, 30-ms lookahead | 680.538 | 285.632 |

Common settings:

- one GPU per experiment, batch size 32, crop length 2 seconds;
- fresh AdamW optimizer, 2k-step LR warm-up and cosine decay;
- validation and checkpoint every 5k steps;
- fixed 200-file objective evaluation after training;
- exact 2.4-kbps bitstream and the same held-out validation material;
- persistent tmux execution and checkpoint-based recovery.

The A/B comparison isolates perceptual training. B/C isolates temporal modeling and legal
lookahead. B/D tests whether quantizer factorization can fund a stronger temporal model while
remaining below both course compute limits.
