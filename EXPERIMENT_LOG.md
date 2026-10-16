# Experiment Log

This file is updated by `scripts/record_experiment.py`. Each named experiment records its status, exact configuration, dataset size, training validation, objective evaluation, complexity, and checkpoint hash.

Experiment entries are appended below.

<!-- experiment:fast_b64_2s_v1:start -->
## fast_b64_2s_v1

- Status: `complete`
- Updated (UTC): `2026-10-15T10:26:14.406838+00:00`
- Git commit: `df55ac7ba2e93b8e014d655376984ee66e73983c`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/fast_b64_2s_v1`
- Note: Full training, format validation, objective evaluation and complexity analysis completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/fast_b64_2s_v1/checkpoints/best.pt`
- Checkpoint SHA-256: `45977a6844bb24e08875b2fc2e5e55aa42b7b7030b71be83da12e7b8652ed78c`

### Dataset

| Item | Value |
|---|---:|
| Training files | 394988 |
| Validation files | 14596 |
| VCTK training files | 40208 |
| VCTK validation files | 4247 |
| LibriTTS training files | 354780 |
| LibriTTS validation files | 10349 |

### Last training validation

| Item | Value |
|---|---:|
| Epoch | 30 |
| Global step | 46260 |
| Train loss | 0.510229 |
| Reconstruction loss | 0.088413 |
| Waveform L1 | 0.020551 |
| Spectral loss | 0.067862 |
| Commitment loss | 0.036965 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.2950 |
| ESTOI | 0.5290 |
| SI-SNR (dB) | 2.4292 |
| UTMOS | 1.2887 |
| Course objective score | 24.9042 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 608.768 |
| Decoder MFLOP/s | 244.480 |
| Parameters | 384189 |

### Effective configuration

```yaml
seed: 2026
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: rvq
  encoder_channels:
  - 8
  - 16
  - 32
  - 64
  - 160
  encoder_strides:
  - 2
  - 4
  - 4
  - 5
  decoder_channels:
  - 160
  - 48
  - 24
  - 12
  - 8
  decoder_strides:
  - 5
  - 4
  - 4
  - 2
  residual_blocks: 3
  residual_kernel_size: 3
  rvq_num_codebooks: 3
  rvq_codebook_size: 256
  rvq_codebook_dim: 160
  commitment_weight: 0.1
  rvq_ema_decay: 0.99
  rvq_dead_code_threshold: 0.5
  rvq_dead_code_after_updates: 100
  rvq_kmeans_iterations: 10
  encoder_temporal_layers: 0
  decoder_temporal_layers: 0
  temporal_kernel_size: 3
  temporal_expansion: 2
  fsq_levels:
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.0
  linear_magnitude_weight: 0.0
  adversarial_weight: 0.1
  feature_matching_weight: 1.0
adversarial:
  resolutions:
  - - 256
    - 64
    - 256
  - - 512
    - 128
    - 512
  - - 1024
    - 256
    - 1024
  start_step: 2000
  warmup_steps: 2000
  learning_rate: 0.0002
  gradient_clip_norm: 10.0
training:
  batch_size: 64
  num_workers: 8
  epochs: 30
  learning_rate: 0.0002
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 128
  validation_checkpoint_interval_steps: 2500
  sample_inference_count: 4
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/fast_b64_2s_v1
```

<!-- experiment:fast_b64_2s_v1:end -->

<!-- experiment:ablation_a_trainfix:start -->
## ablation_a_trainfix

- Status: `complete`
- Updated (UTC): `2026-10-16T07:10:44.364019+00:00`
- Git commit: `2030d2ae26afd3a51c2b2c7338a25b95d047910d`
- Run directory: `runs/ablation_a_trainfix`
- Note: Historical ablation record regenerated after removing the separate four-architecture sweep
- Best checkpoint: `runs/ablation_a_trainfix/checkpoints/best.pt`
- Checkpoint SHA-256: `cee7dbd31f753ad6f4114ef77c60ee8911564255c23f9946e62c80d3d8bf124b`

### Dataset

| Item | Value |
|---|---:|
| Training files | 394988 |
| Validation files | 14596 |
| VCTK training files | 40208 |
| VCTK validation files | 4247 |
| LibriTTS training files | 354780 |
| LibriTTS validation files | 10349 |

### Last training validation

| Item | Value |
|---|---:|
| Epoch | 3 |
| Global step | 30000 |
| Train loss | 0.495580 |
| Reconstruction loss | 0.072140 |
| Waveform L1 | 0.019972 |
| Spectral loss | 0.052169 |
| Commitment loss | 0.026679 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.7738 |
| ESTOI | 0.6864 |
| SI-SNR (dB) | 0.9396 |
| UTMOS | 2.3417 |
| Course objective score | 37.9104 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 608.768 |
| Decoder MFLOP/s | 244.480 |
| Parameters | 384189 |

### Effective configuration

```yaml
seed: 2026
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: rvq
  encoder_channels:
  - 8
  - 16
  - 32
  - 64
  - 160
  encoder_strides:
  - 2
  - 4
  - 4
  - 5
  decoder_channels:
  - 160
  - 48
  - 24
  - 12
  - 8
  decoder_strides:
  - 5
  - 4
  - 4
  - 2
  residual_blocks: 3
  residual_kernel_size: 3
  rvq_num_codebooks: 3
  rvq_codebook_size: 256
  rvq_codebook_dim: 160
  commitment_weight: 0.1
  rvq_ema_decay: 0.95
  rvq_dead_code_threshold: 0.5
  rvq_dead_code_after_updates: 100
  rvq_kmeans_iterations: 10
  encoder_temporal_layers: 0
  decoder_temporal_layers: 0
  temporal_kernel_size: 3
  temporal_expansion: 2
  fsq_levels:
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.0
  linear_magnitude_weight: 0.0
  adversarial_weight: 0.1
  feature_matching_weight: 1.0
adversarial:
  resolutions:
  - - 256
    - 64
    - 256
  - - 512
    - 128
    - 512
  - - 1024
    - 256
    - 1024
  start_step: 0
  warmup_steps: 5000
  learning_rate: 0.0002
  gradient_clip_norm: 10.0
training:
  batch_size: 32
  num_workers: 8
  epochs: 1000
  learning_rate: 0.0004
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 16
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/ablation_a_trainfix
  minimum_learning_rate: 5.0e-05
  warmup_steps: 2000
```

<!-- experiment:ablation_a_trainfix:end -->

<!-- experiment:ablation_b_perceptual:start -->
## ablation_b_perceptual

- Status: `complete`
- Updated (UTC): `2026-10-16T07:10:44.510192+00:00`
- Git commit: `2030d2ae26afd3a51c2b2c7338a25b95d047910d`
- Run directory: `runs/ablation_b_perceptual`
- Note: Historical ablation record regenerated after removing the separate four-architecture sweep
- Best checkpoint: `runs/ablation_b_perceptual/checkpoints/best.pt`
- Checkpoint SHA-256: `dceb82a9fcee26d723859c5dd46c54ef9ed4280efdf35c775dc9748cfdfeb957`

### Dataset

| Item | Value |
|---|---:|
| Training files | 394988 |
| Validation files | 14596 |
| VCTK training files | 40208 |
| VCTK validation files | 4247 |
| LibriTTS training files | 354780 |
| LibriTTS validation files | 10349 |

### Last training validation

| Item | Value |
|---|---:|
| Epoch | 3 |
| Global step | 30000 |
| Train loss | 0.397763 |
| Reconstruction loss | 0.150395 |
| Waveform L1 | 0.019323 |
| Spectral loss | 0.131072 |
| Commitment loss | 0.025072 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.7413 |
| ESTOI | 0.6882 |
| SI-SNR (dB) | 1.4476 |
| UTMOS | 2.3285 |
| Course objective score | 37.9566 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 608.768 |
| Decoder MFLOP/s | 244.480 |
| Parameters | 384189 |

### Effective configuration

```yaml
seed: 2026
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: rvq
  encoder_channels:
  - 8
  - 16
  - 32
  - 64
  - 160
  encoder_strides:
  - 2
  - 4
  - 4
  - 5
  decoder_channels:
  - 160
  - 48
  - 24
  - 12
  - 8
  decoder_strides:
  - 5
  - 4
  - 4
  - 2
  residual_blocks: 3
  residual_kernel_size: 3
  rvq_num_codebooks: 3
  rvq_codebook_size: 256
  rvq_codebook_dim: 160
  commitment_weight: 0.1
  rvq_ema_decay: 0.95
  rvq_dead_code_threshold: 0.5
  rvq_dead_code_after_updates: 100
  rvq_kmeans_iterations: 10
  encoder_temporal_layers: 0
  decoder_temporal_layers: 0
  temporal_kernel_size: 3
  temporal_expansion: 2
  fsq_levels:
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.1
  feature_matching_weight: 1.0
adversarial:
  resolutions:
  - - 256
    - 64
    - 256
  - - 512
    - 128
    - 512
  - - 1024
    - 256
    - 1024
  start_step: 0
  warmup_steps: 10000
  learning_rate: 0.0002
  gradient_clip_norm: 10.0
  periods:
  - 2
  - 3
  - 5
  - 7
  - 11
training:
  batch_size: 32
  num_workers: 8
  epochs: 1000
  learning_rate: 0.0004
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 16
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/ablation_b_perceptual
  minimum_learning_rate: 5.0e-05
  warmup_steps: 2000
```

<!-- experiment:ablation_b_perceptual:end -->

<!-- experiment:ablation_c_temporal:start -->
## ablation_c_temporal

- Status: `complete`
- Updated (UTC): `2026-10-16T07:10:44.667108+00:00`
- Git commit: `2030d2ae26afd3a51c2b2c7338a25b95d047910d`
- Run directory: `runs/ablation_c_temporal`
- Note: Historical ablation record regenerated after removing the separate four-architecture sweep
- Best checkpoint: `runs/ablation_c_temporal/checkpoints/best.pt`
- Checkpoint SHA-256: `d9aa9fa17f5d4791ac633ed2753b13e1b73f51f992c7e4a0a0ca00c73184cb41`

### Dataset

| Item | Value |
|---|---:|
| Training files | 394988 |
| Validation files | 14596 |
| VCTK training files | 40208 |
| VCTK validation files | 4247 |
| LibriTTS training files | 354780 |
| LibriTTS validation files | 10349 |

### Last training validation

| Item | Value |
|---|---:|
| Epoch | 3 |
| Global step | 30000 |
| Train loss | 0.386642 |
| Reconstruction loss | 0.143154 |
| Waveform L1 | 0.018379 |
| Spectral loss | 0.124775 |
| Commitment loss | 0.035101 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.7899 |
| ESTOI | 0.6917 |
| SI-SNR (dB) | 2.2148 |
| UTMOS | 2.5590 |
| Course objective score | 40.3124 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 675.744 |
| Decoder MFLOP/s | 265.056 |
| Parameters | 721149 |

### Effective configuration

```yaml
seed: 2026
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: rvq
  encoder_channels:
  - 8
  - 16
  - 32
  - 64
  - 160
  encoder_strides:
  - 2
  - 4
  - 4
  - 5
  decoder_channels:
  - 160
  - 48
  - 24
  - 12
  - 8
  decoder_strides:
  - 5
  - 4
  - 4
  - 2
  residual_blocks: 3
  residual_kernel_size: 3
  rvq_num_codebooks: 3
  rvq_codebook_size: 256
  rvq_codebook_dim: 160
  commitment_weight: 0.1
  rvq_ema_decay: 0.95
  rvq_dead_code_threshold: 0.5
  rvq_dead_code_after_updates: 100
  rvq_kmeans_iterations: 10
  encoder_temporal_layers: 2
  decoder_temporal_layers: 1
  temporal_kernel_size: 3
  temporal_expansion: 2
  fsq_levels:
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  encoder_lookahead_frames: 3
  decoder_lookahead_frames: 0
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.1
  feature_matching_weight: 1.0
adversarial:
  resolutions:
  - - 256
    - 64
    - 256
  - - 512
    - 128
    - 512
  - - 1024
    - 256
    - 1024
  start_step: 0
  warmup_steps: 10000
  learning_rate: 0.0002
  gradient_clip_norm: 10.0
  periods:
  - 2
  - 3
  - 5
  - 7
  - 11
training:
  batch_size: 32
  num_workers: 8
  epochs: 1000
  learning_rate: 0.0004
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 16
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/ablation_c_temporal
  minimum_learning_rate: 5.0e-05
  warmup_steps: 2000
```

<!-- experiment:ablation_c_temporal:end -->

<!-- experiment:ablation_d_factorized_tcn:start -->
## ablation_d_factorized_tcn

- Status: `complete`
- Updated (UTC): `2026-10-16T07:10:44.808493+00:00`
- Git commit: `2030d2ae26afd3a51c2b2c7338a25b95d047910d`
- Run directory: `runs/ablation_d_factorized_tcn`
- Note: Historical ablation record regenerated after removing the separate four-architecture sweep
- Best checkpoint: `runs/ablation_d_factorized_tcn/checkpoints/best.pt`
- Checkpoint SHA-256: `2dd826152e5ad0dc7b352c647f79baf01a4101c75fc8982f400f837f87fd535b`

### Dataset

| Item | Value |
|---|---:|
| Training files | 394988 |
| Validation files | 14596 |
| VCTK training files | 40208 |
| VCTK validation files | 4247 |
| LibriTTS training files | 354780 |
| LibriTTS validation files | 10349 |

### Last training validation

| Item | Value |
|---|---:|
| Epoch | 3 |
| Global step | 30000 |
| Train loss | 0.376071 |
| Reconstruction loss | 0.140703 |
| Waveform L1 | 0.018040 |
| Spectral loss | 0.122663 |
| Commitment loss | 0.027808 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9355 |
| ESTOI | 0.7223 |
| SI-SNR (dB) | 1.6720 |
| UTMOS | 1.9203 |
| Course objective score | 37.7866 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 680.538 |
| Decoder MFLOP/s | 285.632 |
| Parameters | 943645 |

### Effective configuration

```yaml
seed: 2026
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: rvq
  encoder_channels:
  - 8
  - 16
  - 32
  - 64
  - 160
  encoder_strides:
  - 2
  - 4
  - 4
  - 5
  decoder_channels:
  - 160
  - 48
  - 24
  - 12
  - 8
  decoder_strides:
  - 5
  - 4
  - 4
  - 2
  residual_blocks: 3
  residual_kernel_size: 3
  rvq_num_codebooks: 3
  rvq_codebook_size: 256
  rvq_codebook_dim: 32
  commitment_weight: 0.1
  rvq_ema_decay: 0.9
  rvq_dead_code_threshold: 0.5
  rvq_dead_code_after_updates: 100
  rvq_kmeans_iterations: 10
  encoder_temporal_layers: 4
  decoder_temporal_layers: 2
  temporal_kernel_size: 3
  temporal_expansion: 2
  fsq_levels:
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  - 8
  encoder_lookahead_frames: 3
  decoder_lookahead_frames: 0
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.1
  feature_matching_weight: 1.0
adversarial:
  resolutions:
  - - 256
    - 64
    - 256
  - - 512
    - 128
    - 512
  - - 1024
    - 256
    - 1024
  start_step: 10000
  warmup_steps: 10000
  learning_rate: 0.0002
  gradient_clip_norm: 10.0
  periods:
  - 2
  - 3
  - 5
  - 7
  - 11
training:
  batch_size: 32
  num_workers: 8
  epochs: 1000
  learning_rate: 0.0004
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 16
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/ablation_d_factorized_tcn
  minimum_learning_rate: 5.0e-05
  warmup_steps: 2000
```

<!-- experiment:ablation_d_factorized_tcn:end -->
