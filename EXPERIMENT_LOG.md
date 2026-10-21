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

<!-- experiment:minimimi_a_plain_rvq:start -->
## minimimi_a_plain_rvq

- Status: `complete`
- Updated (UTC): `2026-10-20T06:55:04.992686+00:00`
- Git commit: `7b1f1754e40e26e5538eb1f1fa4acf8b7c601f44`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_a_plain_rvq`
- Note: 200000-step MiniMimi training and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_a_plain_rvq/checkpoints/best.pt`
- Checkpoint SHA-256: `467b1d031e79d08087664bcd4260ddafbc023ab285fbe0190cfb58df0de0b156`

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
| Epoch | 7 |
| Global step | 200000 |
| Train loss | 0.437557 |
| Reconstruction loss | 0.150955 |
| Waveform L1 | 0.017062 |
| Spectral loss | 0.133893 |
| Commitment loss | 0.047922 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.5592 |
| ESTOI | 0.6405 |
| SI-SNR (dB) | 3.6482 |
| UTMOS | 1.6828 |
| Course objective score | 32.8036 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 602.189 |
| Decoder MFLOP/s | 261.069 |
| Parameters | 1384123 |

### Effective configuration

```yaml
seed: 2026
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  architecture: minimimi
  sample_rate: 16000
  frame_samples: 160
  encoder_strides:
  - 2
  - 4
  - 4
  - 5
  decoder_strides:
  - 5
  - 4
  - 4
  - 2
  encoder_lookahead_frames: 3
  decoder_lookahead_frames: 0
  quantizer_type: rvq
  rvq_num_codebooks: 3
  rvq_codebook_size: 256
  rvq_codebook_dim: 64
  commitment_weight: 0.1
  rvq_ema_decay: 0.95
  rvq_dead_code_threshold: 0.5
  rvq_dead_code_after_updates: 100
  rvq_kmeans_iterations: 10
  minimimi_encoder_channels:
  - 12
  - 24
  - 48
  - 96
  - 192
  minimimi_decoder_channels:
  - 128
  - 64
  - 32
  - 16
  - 8
  minimimi_latent_dim: 128
  minimimi_residual_compression: 2
  minimimi_downsample_overlap: 2
  minimimi_upsample_overlap: 1
  minimimi_encoder_transformer_layers: 3
  minimimi_decoder_transformer_layers: 3
  minimimi_transformer_heads: 4
  minimimi_transformer_ffn_dim: 256
  minimimi_encoder_history_frames: 128
  minimimi_decoder_history_frames: 128
  minimimi_hybrid_kernel_size: 0
  minimimi_semantic_dim: 32
  minimimi_acoustic_dim: 64
semantic_distillation:
  enabled: false
  bundle: WAVLM_BASE_PLUS
  feature_dim: 768
  layer: 9
  weight: 0.1
  warmup_steps: 10000
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
  periods:
  - 2
  - 3
  - 5
  - 7
  - 11
  start_step: 10000
  warmup_steps: 10000
  learning_rate: 0.0002
  gradient_clip_norm: 10.0
training:
  batch_size: 12
  num_workers: 8
  epochs: 1000
  learning_rate: 0.0002
  minimum_learning_rate: 2.0e-05
  warmup_steps: 2000
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  checkpoint_keep_last: 3
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_a_plain_rvq
```

<!-- experiment:minimimi_a_plain_rvq:end -->

<!-- experiment:minimimi_b_split_semantic:start -->
## minimimi_b_split_semantic

- Status: `complete`
- Updated (UTC): `2026-10-20T09:47:27.102875+00:00`
- Git commit: `7b1f1754e40e26e5538eb1f1fa4acf8b7c601f44`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_b_split_semantic`
- Note: 200000-step MiniMimi training and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_b_split_semantic/checkpoints/best.pt`
- Checkpoint SHA-256: `ceb1c6fcdbbf3af24fcdc803cb8b71d99393fce06ddc7ea75f7a5c3047c179de`

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
| Epoch | 7 |
| Global step | 200000 |
| Train loss | 0.487914 |
| Reconstruction loss | 0.150744 |
| Waveform L1 | 0.017450 |
| Spectral loss | 0.133294 |
| Commitment loss | 0.042664 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.5470 |
| ESTOI | 0.6328 |
| SI-SNR (dB) | 3.3405 |
| UTMOS | 1.7830 |
| Course objective score | 32.9588 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 605.466 |
| Decoder MFLOP/s | 261.069 |
| Parameters | 1416891 |

### Effective configuration

```yaml
seed: 2026
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  architecture: minimimi
  sample_rate: 16000
  frame_samples: 160
  encoder_strides:
  - 2
  - 4
  - 4
  - 5
  decoder_strides:
  - 5
  - 4
  - 4
  - 2
  encoder_lookahead_frames: 3
  decoder_lookahead_frames: 0
  quantizer_type: split_rvq
  rvq_num_codebooks: 3
  rvq_codebook_size: 256
  rvq_codebook_dim: 64
  commitment_weight: 0.1
  rvq_ema_decay: 0.95
  rvq_dead_code_threshold: 0.5
  rvq_dead_code_after_updates: 100
  rvq_kmeans_iterations: 10
  minimimi_encoder_channels:
  - 12
  - 24
  - 48
  - 96
  - 192
  minimimi_decoder_channels:
  - 128
  - 64
  - 32
  - 16
  - 8
  minimimi_latent_dim: 128
  minimimi_residual_compression: 2
  minimimi_downsample_overlap: 2
  minimimi_upsample_overlap: 1
  minimimi_encoder_transformer_layers: 3
  minimimi_decoder_transformer_layers: 3
  minimimi_transformer_heads: 4
  minimimi_transformer_ffn_dim: 256
  minimimi_encoder_history_frames: 128
  minimimi_decoder_history_frames: 128
  minimimi_hybrid_kernel_size: 0
  minimimi_semantic_dim: 32
  minimimi_acoustic_dim: 64
semantic_distillation:
  enabled: true
  bundle: WAVLM_BASE_PLUS
  feature_dim: 768
  layer: 9
  weight: 0.1
  warmup_steps: 10000
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
  periods:
  - 2
  - 3
  - 5
  - 7
  - 11
  start_step: 10000
  warmup_steps: 10000
  learning_rate: 0.0002
  gradient_clip_norm: 10.0
training:
  batch_size: 12
  num_workers: 8
  epochs: 1000
  learning_rate: 0.0002
  minimum_learning_rate: 2.0e-05
  warmup_steps: 2000
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  checkpoint_keep_last: 3
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_b_split_semantic
```

<!-- experiment:minimimi_b_split_semantic:end -->

<!-- experiment:minimimi_c_decoder_heavy:start -->
## minimimi_c_decoder_heavy

- Status: `complete`
- Updated (UTC): `2026-10-20T17:12:51.987051+00:00`
- Git commit: `7b1f1754e40e26e5538eb1f1fa4acf8b7c601f44`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_c_decoder_heavy`
- Note: 200000-step MiniMimi training and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_c_decoder_heavy/checkpoints/best.pt`
- Checkpoint SHA-256: `9e5452579e5db6ad352b25c129f4323e9a3326fdb00a95d68a73206f1baae0a8`

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
| Epoch | 7 |
| Global step | 200000 |
| Train loss | 0.459073 |
| Reconstruction loss | 0.149083 |
| Waveform L1 | 0.017360 |
| Spectral loss | 0.131724 |
| Commitment loss | 0.045938 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.5824 |
| ESTOI | 0.6418 |
| SI-SNR (dB) | 3.5039 |
| UTMOS | 1.8303 |
| Course objective score | 33.8339 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 585.805 |
| Decoder MFLOP/s | 279.296 |
| Parameters | 1318203 |

### Effective configuration

```yaml
seed: 2026
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  architecture: minimimi
  sample_rate: 16000
  frame_samples: 160
  encoder_strides:
  - 2
  - 4
  - 4
  - 5
  decoder_strides:
  - 5
  - 4
  - 4
  - 2
  encoder_lookahead_frames: 3
  decoder_lookahead_frames: 0
  quantizer_type: split_rvq
  rvq_num_codebooks: 3
  rvq_codebook_size: 256
  rvq_codebook_dim: 64
  commitment_weight: 0.1
  rvq_ema_decay: 0.95
  rvq_dead_code_threshold: 0.5
  rvq_dead_code_after_updates: 100
  rvq_kmeans_iterations: 10
  minimimi_encoder_channels:
  - 12
  - 24
  - 48
  - 96
  - 192
  minimimi_decoder_channels:
  - 128
  - 64
  - 32
  - 16
  - 8
  minimimi_latent_dim: 128
  minimimi_residual_compression: 2
  minimimi_downsample_overlap: 2
  minimimi_upsample_overlap: 1
  minimimi_encoder_transformer_layers: 2
  minimimi_decoder_transformer_layers: 4
  minimimi_transformer_heads: 4
  minimimi_transformer_ffn_dim: 192
  minimimi_encoder_history_frames: 128
  minimimi_decoder_history_frames: 128
  minimimi_hybrid_kernel_size: 0
  minimimi_semantic_dim: 32
  minimimi_acoustic_dim: 64
semantic_distillation:
  enabled: true
  bundle: WAVLM_BASE_PLUS
  feature_dim: 768
  layer: 9
  weight: 0.1
  warmup_steps: 10000
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
  periods:
  - 2
  - 3
  - 5
  - 7
  - 11
  start_step: 10000
  warmup_steps: 10000
  learning_rate: 0.0002
  gradient_clip_norm: 10.0
training:
  batch_size: 12
  num_workers: 8
  epochs: 1000
  learning_rate: 0.0002
  minimum_learning_rate: 2.0e-05
  warmup_steps: 2000
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  checkpoint_keep_last: 3
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_c_decoder_heavy
```

<!-- experiment:minimimi_c_decoder_heavy:end -->
<!-- experiment:minimimi_d_hybrid_temporal:start -->
## minimimi_d_hybrid_temporal

- Status: `complete`
- Updated (UTC): `2026-10-20T00:22:12.981042+00:00`
- Git commit: `7b1f1754e40e26e5538eb1f1fa4acf8b7c601f44`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_d_hybrid_temporal`
- Note: 200000-step MiniMimi training and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_d_hybrid_temporal/checkpoints/best.pt`
- Checkpoint SHA-256: `609a7f3512614f34b4110358eedc30b01d17a1384779539c3d75dcc55251fad9`

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
| Epoch | 7 |
| Global step | 200000 |
| Train loss | 0.488880 |
| Reconstruction loss | 0.149441 |
| Waveform L1 | 0.017505 |
| Spectral loss | 0.131936 |
| Commitment loss | 0.051132 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.5879 |
| ESTOI | 0.6470 |
| SI-SNR (dB) | 3.4964 |
| UTMOS | 1.9441 |
| Course objective score | 34.7105 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 626.202 |
| Decoder MFLOP/s | 271.437 |
| Parameters | 1524411 |

### Effective configuration

```yaml
seed: 2026
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  architecture: minimimi
  sample_rate: 16000
  frame_samples: 160
  encoder_strides:
  - 2
  - 4
  - 4
  - 5
  decoder_strides:
  - 5
  - 4
  - 4
  - 2
  encoder_lookahead_frames: 3
  decoder_lookahead_frames: 0
  quantizer_type: split_rvq
  rvq_num_codebooks: 3
  rvq_codebook_size: 256
  rvq_codebook_dim: 64
  commitment_weight: 0.1
  rvq_ema_decay: 0.95
  rvq_dead_code_threshold: 0.5
  rvq_dead_code_after_updates: 100
  rvq_kmeans_iterations: 10
  minimimi_encoder_channels:
  - 12
  - 24
  - 48
  - 96
  - 192
  minimimi_decoder_channels:
  - 128
  - 64
  - 32
  - 16
  - 8
  minimimi_latent_dim: 128
  minimimi_residual_compression: 2
  minimimi_downsample_overlap: 2
  minimimi_upsample_overlap: 1
  minimimi_encoder_transformer_layers: 3
  minimimi_decoder_transformer_layers: 3
  minimimi_transformer_heads: 4
  minimimi_transformer_ffn_dim: 256
  minimimi_encoder_history_frames: 128
  minimimi_decoder_history_frames: 128
  minimimi_hybrid_kernel_size: 7
  minimimi_semantic_dim: 32
  minimimi_acoustic_dim: 64
semantic_distillation:
  enabled: true
  bundle: WAVLM_BASE_PLUS
  feature_dim: 768
  layer: 9
  weight: 0.1
  warmup_steps: 10000
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
  periods:
  - 2
  - 3
  - 5
  - 7
  - 11
  start_step: 10000
  warmup_steps: 10000
  learning_rate: 0.0002
  gradient_clip_norm: 10.0
training:
  batch_size: 12
  num_workers: 8
  epochs: 1000
  learning_rate: 0.0002
  minimum_learning_rate: 2.0e-05
  warmup_steps: 2000
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  checkpoint_keep_last: 3
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/minimimi_d_hybrid_temporal
```

<!-- experiment:minimimi_d_hybrid_temporal:end -->

<!-- experiment:official_baseline_reference_eval:start -->
## official_baseline_reference_eval

- Status: `complete`
- Updated (UTC): `2026-10-21T00:39:28.043586+00:00`
- Git commit: `6168477f62d8d86a6a2fca04b8dc6a4635e7382c`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/official_baseline_reference_eval`
- Note: Official bundled reference checkpoint re-evaluated on the shared fixed 200-file set
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/official_baseline_reference_eval/checkpoints/best.pt`
- Checkpoint SHA-256: `4f19d236377b8f5d5c10e4f283d6cc80a35a80f081d5b6f135b605bdc7a6d96a`

### Dataset

| Item | Value |
|---|---:|
| Training files | 394988 |
| Validation files | 14596 |
| VCTK training files | 40208 |
| VCTK validation files | 4247 |
| LibriTTS training files | 354780 |
| LibriTTS validation files | 10349 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.7323 |
| ESTOI | 0.6798 |
| SI-SNR (dB) | 0.8275 |
| UTMOS | 2.3517 |
| Course objective score | 37.4414 |

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
  segment_samples: 16000

model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: rvq
  encoder_channels: [8, 16, 32, 64, 160]
  encoder_strides: [2, 4, 4, 5]
  decoder_channels: [160, 48, 24, 12, 8]
  decoder_strides: [5, 4, 4, 2]
  residual_blocks: 3
  residual_kernel_size: 3
  rvq_num_codebooks: 3
  rvq_codebook_size: 256
  rvq_codebook_dim: 160
  commitment_weight: 0.10
  rvq_ema_decay: 0.99
  rvq_dead_code_threshold: 0.5
  rvq_dead_code_after_updates: 100
  rvq_kmeans_iterations: 10
  # Optional causal modeling at the 100-Hz latent rate. Zero preserves the
  # original baseline and existing checkpoint compatibility.
  encoder_temporal_layers: 0
  decoder_temporal_layers: 0
  temporal_kernel_size: 3
  temporal_expansion: 2
  # Used only when quantizer_type is fsq. 8^8 = 2^24 combinations.
  fsq_levels: [8, 8, 8, 8, 8, 8, 8, 8]

loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes: [256, 512, 1024]
  spectral_convergence_weight: 0.0
  linear_magnitude_weight: 0.0
  adversarial_weight: 0.1
  feature_matching_weight: 1.0

adversarial:
  resolutions:
    - [256, 64, 256]
    - [512, 128, 512]
    - [1024, 256, 1024]
  start_step: 10000
  warmup_steps: 10000
  learning_rate: 0.0002
  gradient_clip_norm: 10.0

training:
  batch_size: 8
  num_workers: 2
  epochs: 100
  learning_rate: 0.0002
  weight_decay: 0.000001
  gradient_clip_norm: 1.0
  validation_limit: 128
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 4
  output_dir: runs/baseline_16k_2p4k_ema_rvq_gan
```

<!-- experiment:official_baseline_reference_eval:end -->

<!-- experiment:next4_b_long_tcn:start -->
## next4_b_long_tcn

- Status: `complete`
- Updated (UTC): `2026-10-21T12:20:34.648856+00:00`
- Git commit: `826428da048eaadc6bdb564ae3aaaceba154a39b`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_b_long_tcn`
- Note: 170000 additional steps from common C checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_b_long_tcn/checkpoints/best.pt`
- Checkpoint SHA-256: `cd9ada0660d9f12f8c9271320f1e2e0128adf8a1ea6f61167e831de63fa5bffe`

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
| Epoch | 14 |
| Global step | 170000 |
| Train loss | 0.426664 |
| Reconstruction loss | 0.139788 |
| Waveform L1 | 0.015627 |
| Spectral loss | 0.124161 |
| Commitment loss | 0.035296 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.8730 |
| ESTOI | 0.7054 |
| SI-SNR (dB) | 4.2767 |
| UTMOS | 2.7494 |
| Course objective score | 43.7272 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 676.032 |
| Decoder MFLOP/s | 265.152 |
| Parameters | 723549 |

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
  encoder_temporal_layers: 4
  decoder_temporal_layers: 2
  temporal_kernel_size: 3
  temporal_expansion: 1
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
  learning_rate: 0.0002
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_b_long_tcn
  minimum_learning_rate: 2.0e-05
  warmup_steps: 2000
  checkpoint_keep_last: 3
```

<!-- experiment:next4_b_long_tcn:end -->

<!-- experiment:next4_a_c_long:start -->
## next4_a_c_long

- Status: `complete`
- Updated (UTC): `2026-10-21T12:50:15.929263+00:00`
- Git commit: `826428da048eaadc6bdb564ae3aaaceba154a39b`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_a_c_long`
- Note: 170000 additional steps from common C checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_a_c_long/checkpoints/best.pt`
- Checkpoint SHA-256: `61ea0263492816d88acb414c2591774db55da812488df4da5c06047d9fe3b384`

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
| Epoch | 14 |
| Global step | 170000 |
| Train loss | 0.441007 |
| Reconstruction loss | 0.141157 |
| Waveform L1 | 0.015895 |
| Spectral loss | 0.125262 |
| Commitment loss | 0.040536 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.8425 |
| ESTOI | 0.7029 |
| SI-SNR (dB) | 4.1547 |
| UTMOS | 2.6824 |
| Course objective score | 42.9513 |

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
  learning_rate: 0.0002
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_a_c_long
  minimum_learning_rate: 2.0e-05
  warmup_steps: 2000
  checkpoint_keep_last: 3
```

<!-- experiment:next4_a_c_long:end -->

<!-- experiment:next4_c_semantic_rvq:start -->
## next4_c_semantic_rvq

- Status: `complete`
- Updated (UTC): `2026-10-21T14:48:27.888396+00:00`
- Git commit: `826428da048eaadc6bdb564ae3aaaceba154a39b`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_c_semantic_rvq`
- Note: 170000 additional steps from common C checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_c_semantic_rvq/checkpoints/best.pt`
- Checkpoint SHA-256: `999b60520a6833893d4909041daab54bb5e87eaac77dfebdfdf9b033f33a418b`

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
| Epoch | 14 |
| Global step | 170000 |
| Train loss | 0.479895 |
| Reconstruction loss | 0.144590 |
| Waveform L1 | 0.016286 |
| Spectral loss | 0.128305 |
| Commitment loss | 0.042585 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.8363 |
| ESTOI | 0.6978 |
| SI-SNR (dB) | 4.0177 |
| UTMOS | 2.6632 |
| Course objective score | 42.5750 |

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
  learning_rate: 0.0002
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_c_semantic_rvq
  minimum_learning_rate: 2.0e-05
  warmup_steps: 2000
  checkpoint_keep_last: 3
semantic_distillation:
  enabled: true
  bundle: WAVLM_BASE_PLUS
  feature_dim: 768
  layer: 9
  weight: 0.05
  warmup_steps: 10000
```

<!-- experiment:next4_c_semantic_rvq:end -->
<!-- experiment:next4_d_local_transformer:start -->
## next4_d_local_transformer

- Status: `complete`
- Updated (UTC): `2026-10-21T13:18:51.616414+00:00`
- Git commit: `826428da048eaadc6bdb564ae3aaaceba154a39b`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_d_local_transformer`
- Note: 170000 additional steps from common C checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_d_local_transformer/checkpoints/best.pt`
- Checkpoint SHA-256: `dbb2ec10c915d912097e5bd7dec8445151ebc1fdeccd62b99621a1ccdca161a2`

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
| Epoch | 14 |
| Global step | 170000 |
| Train loss | 0.440753 |
| Reconstruction loss | 0.143707 |
| Waveform L1 | 0.016150 |
| Spectral loss | 0.127557 |
| Commitment loss | 0.035578 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.8256 |
| ESTOI | 0.6963 |
| SI-SNR (dB) | 3.8408 |
| UTMOS | 2.6873 |
| Course objective score | 42.5003 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 689.280 |
| Decoder MFLOP/s | 269.568 |
| Parameters | 775237 |

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
  temporal_model: transformer
  temporal_transformer_heads: 4
  temporal_transformer_ffn_dim: 56
  encoder_history_frames: 16
  decoder_history_frames: 16
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
  learning_rate: 0.0002
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/next4_d_local_transformer
  minimum_learning_rate: 2.0e-05
  warmup_steps: 2000
  checkpoint_keep_last: 3
```

<!-- experiment:next4_d_local_transformer:end -->
