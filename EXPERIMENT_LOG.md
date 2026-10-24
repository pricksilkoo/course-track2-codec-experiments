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

<!-- experiment:refine4_b_feature_matching_2x:start -->
## refine4_b_feature_matching_2x

- Status: `complete`
- Updated (UTC): `2026-10-22T04:06:49.689543+00:00`
- Git commit: `1a2d2fd1daaef5009bd49be77f178a4d4601a3c3`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_b_feature_matching_2x`
- Note: 50000 fine-tuning steps from next4 B best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_b_feature_matching_2x/checkpoints/best.pt`
- Checkpoint SHA-256: `d18f7339387b81ebb57d3f362898437fc4fa19efa957520dd6a7c7948f7314db`

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
| Epoch | 5 |
| Global step | 50000 |
| Train loss | 0.625886 |
| Reconstruction loss | 0.137764 |
| Waveform L1 | 0.015390 |
| Spectral loss | 0.122374 |
| Commitment loss | 0.051832 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9200 |
| ESTOI | 0.7136 |
| SI-SNR (dB) | 4.4371 |
| UTMOS | 2.7966 |
| Course objective score | 44.6625 |

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
  feature_matching_weight: 2.0
  si_snr_weight: 0.0
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
  warmup_steps: 0
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
  learning_rate: 5.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_b_feature_matching_2x
  minimum_learning_rate: 1.0e-05
  warmup_steps: 0
  checkpoint_keep_last: 5
```

<!-- experiment:refine4_b_feature_matching_2x:end -->

<!-- experiment:refine4_c_sisnr_001:start -->
## refine4_c_sisnr_001

- Status: `complete`
- Updated (UTC): `2026-10-22T04:07:03.671669+00:00`
- Git commit: `1a2d2fd1daaef5009bd49be77f178a4d4601a3c3`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_c_sisnr_001`
- Note: 50000 fine-tuning steps from next4 B best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_c_sisnr_001/checkpoints/best.pt`
- Checkpoint SHA-256: `42050803b4397a175c3f78e41ec83e0ee783dec3a2eb6d1bf5af47d88015cd52`

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
| Epoch | 5 |
| Global step | 50000 |
| Train loss | 0.417610 |
| Reconstruction loss | 0.138233 |
| Waveform L1 | 0.014799 |
| Spectral loss | 0.123434 |
| Commitment loss | 0.053405 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.8645 |
| ESTOI | 0.7016 |
| SI-SNR (dB) | 5.0740 |
| UTMOS | 2.7557 |
| Course objective score | 44.1082 |

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
  si_snr_weight: 0.01
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
  warmup_steps: 0
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
  learning_rate: 5.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_c_sisnr_001
  minimum_learning_rate: 1.0e-05
  warmup_steps: 0
  checkpoint_keep_last: 5
```

<!-- experiment:refine4_c_sisnr_001:end -->
<!-- experiment:refine4_a_lr5e5_control:start -->
## refine4_a_lr5e5_control

- Status: `complete`
- Updated (UTC): `2026-10-22T04:06:48.672141+00:00`
- Git commit: `1a2d2fd1daaef5009bd49be77f178a4d4601a3c3`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_a_lr5e5_control`
- Note: 50000 fine-tuning steps from next4 B best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_a_lr5e5_control/checkpoints/best.pt`
- Checkpoint SHA-256: `65dbd87d640cda291a58ac03aa71c9f3573bbba34fdc4c8a2aa71d530115ca5b`

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
| Epoch | 5 |
| Global step | 50000 |
| Train loss | 0.439842 |
| Reconstruction loss | 0.140235 |
| Waveform L1 | 0.015770 |
| Spectral loss | 0.124465 |
| Commitment loss | 0.037990 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.8727 |
| ESTOI | 0.7062 |
| SI-SNR (dB) | 4.2583 |
| UTMOS | 2.7689 |
| Course objective score | 43.8558 |

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
  si_snr_weight: 0.0
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
  warmup_steps: 0
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
  learning_rate: 5.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_a_lr5e5_control
  minimum_learning_rate: 1.0e-05
  warmup_steps: 0
  checkpoint_keep_last: 5
```

<!-- experiment:refine4_a_lr5e5_control:end -->
<!-- experiment:refine4_d_adversarial_005:start -->
## refine4_d_adversarial_005

- Status: `complete`
- Updated (UTC): `2026-10-22T04:06:48.487353+00:00`
- Git commit: `1a2d2fd1daaef5009bd49be77f178a4d4601a3c3`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_d_adversarial_005`
- Note: 50000 fine-tuning steps from next4 B best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_d_adversarial_005/checkpoints/best.pt`
- Checkpoint SHA-256: `9a5b24e3d573471d54a315b45cc3fde24bfec916e26b12d220fafa77baa55fd9`

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
| Epoch | 5 |
| Global step | 50000 |
| Train loss | 0.406449 |
| Reconstruction loss | 0.136107 |
| Waveform L1 | 0.015238 |
| Spectral loss | 0.120869 |
| Commitment loss | 0.036500 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9397 |
| ESTOI | 0.7187 |
| SI-SNR (dB) | 4.5150 |
| UTMOS | 2.8424 |
| Course objective score | 45.2681 |

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
  adversarial_weight: 0.05
  feature_matching_weight: 1.0
  si_snr_weight: 0.0
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
  warmup_steps: 0
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
  learning_rate: 5.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/refine4_d_adversarial_005
  minimum_learning_rate: 1.0e-05
  warmup_steps: 0
  checkpoint_keep_last: 5
```

<!-- experiment:refine4_d_adversarial_005:end -->

<!-- experiment:factorial4_a_d_control:start -->
## factorial4_a_d_control

- Status: `complete`
- Updated (UTC): `2026-10-22T07:01:05.066498+00:00`
- Git commit: `834fa6100b53fe00be81427784766a08e2fdbf9a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_a_d_control`
- Note: 30000 factorial fine-tuning steps from refine4 D best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_a_d_control/checkpoints/best.pt`
- Checkpoint SHA-256: `bbe5e42f4c277745e67ba21af5ded052b3399e4291424d92db78edf84857958c`

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
| Train loss | 0.409837 |
| Reconstruction loss | 0.136058 |
| Waveform L1 | 0.015248 |
| Spectral loss | 0.120810 |
| Commitment loss | 0.036766 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9468 |
| ESTOI | 0.7168 |
| SI-SNR (dB) | 4.5230 |
| UTMOS | 2.8266 |
| Course objective score | 45.1760 |

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
  adversarial_weight: 0.05
  feature_matching_weight: 1.0
  si_snr_weight: 0.0
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_a_d_control
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:factorial4_a_d_control:end -->

<!-- experiment:factorial4_c_sisnr003:start -->
## factorial4_c_sisnr003

- Status: `complete`
- Updated (UTC): `2026-10-22T07:01:05.304150+00:00`
- Git commit: `834fa6100b53fe00be81427784766a08e2fdbf9a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_c_sisnr003`
- Note: 30000 factorial fine-tuning steps from refine4 D best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_c_sisnr003/checkpoints/best.pt`
- Checkpoint SHA-256: `342f94c123fefbcb3b69fbe586c08f69e1dedef59d5aac3be6c88a001fce7cdd`

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
| Train loss | 0.403454 |
| Reconstruction loss | 0.135277 |
| Waveform L1 | 0.014922 |
| Spectral loss | 0.120355 |
| Commitment loss | 0.041079 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9324 |
| ESTOI | 0.7170 |
| SI-SNR (dB) | 4.7635 |
| UTMOS | 2.8327 |
| Course objective score | 45.2666 |

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
  adversarial_weight: 0.05
  feature_matching_weight: 1.0
  si_snr_weight: 0.003
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_c_sisnr003
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:factorial4_c_sisnr003:end -->
<!-- experiment:factorial4_d_fm15_sisnr003:start -->
## factorial4_d_fm15_sisnr003

- Status: `complete`
- Updated (UTC): `2026-10-22T07:01:01.955154+00:00`
- Git commit: `834fa6100b53fe00be81427784766a08e2fdbf9a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_d_fm15_sisnr003`
- Note: 30000 factorial fine-tuning steps from refine4 D best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_d_fm15_sisnr003/checkpoints/best.pt`
- Checkpoint SHA-256: `d1f4c0eced39f10082cc2e5f7f6650a178938ee1ab65182c54acaf4e70f10469`

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
| Train loss | 0.498550 |
| Reconstruction loss | 0.134958 |
| Waveform L1 | 0.014892 |
| Spectral loss | 0.120066 |
| Commitment loss | 0.047868 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9531 |
| ESTOI | 0.7165 |
| SI-SNR (dB) | 4.7998 |
| UTMOS | 2.8538 |
| Course objective score | 45.5554 |

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
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_d_fm15_sisnr003
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:factorial4_d_fm15_sisnr003:end -->

<!-- experiment:factorial4_b_fm15:start -->
## factorial4_b_fm15

- Status: `complete`
- Updated (UTC): `2026-10-22T07:01:05.188625+00:00`
- Git commit: `834fa6100b53fe00be81427784766a08e2fdbf9a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_b_fm15`
- Note: 30000 factorial fine-tuning steps from refine4 D best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_b_fm15/checkpoints/best.pt`
- Checkpoint SHA-256: `dfad8424e75faabdfe72b8a30a6c615b949186e6e2a325c133df3bdd49bd2a71`

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
| Train loss | 0.504215 |
| Reconstruction loss | 0.135034 |
| Waveform L1 | 0.015110 |
| Spectral loss | 0.119923 |
| Commitment loss | 0.043065 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9514 |
| ESTOI | 0.7205 |
| SI-SNR (dB) | 4.5366 |
| UTMOS | 2.8534 |
| Course objective score | 45.4786 |

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
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.0
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/factorial4_b_fm15
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:factorial4_b_fm15:end -->

<!-- experiment:seed_confirm_d_combo_seed3407:start -->
## seed_confirm_d_combo_seed3407

- Status: `complete`
- Updated (UTC): `2026-10-22T14:19:18.097117+00:00`
- Git commit: `8ea5ccf93f0b3dcfcab31e8aba0ac0745054d98c`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_d_combo_seed3407`
- Note: 30000 factorial fine-tuning steps from refine4 D best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_d_combo_seed3407/checkpoints/best.pt`
- Checkpoint SHA-256: `74770753b07195a6ee88170d547a43128b99db89aeb24d2f882eb305c46ced0b`

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
| Train loss | 0.498862 |
| Reconstruction loss | 0.134671 |
| Waveform L1 | 0.014871 |
| Spectral loss | 0.119800 |
| Commitment loss | 0.047091 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9522 |
| ESTOI | 0.7197 |
| SI-SNR (dB) | 4.7922 |
| UTMOS | 2.8345 |
| Course objective score | 45.5053 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 676.032 |
| Decoder MFLOP/s | 265.152 |
| Parameters | 723549 |

### Effective configuration

```yaml
seed: 3407
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
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_d_combo_seed3407
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:seed_confirm_d_combo_seed3407:end -->

<!-- experiment:seed_confirm_d_combo_seed8128:start -->
## seed_confirm_d_combo_seed8128

- Status: `complete`
- Updated (UTC): `2026-10-22T14:19:18.387868+00:00`
- Git commit: `8ea5ccf93f0b3dcfcab31e8aba0ac0745054d98c`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_d_combo_seed8128`
- Note: 30000 factorial fine-tuning steps from refine4 D best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_d_combo_seed8128/checkpoints/best.pt`
- Checkpoint SHA-256: `8ff1abf2d5fb465ab7d8e3823eb8985db643130da03b20b881081667dd8fdb69`

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
| Train loss | 0.498608 |
| Reconstruction loss | 0.134840 |
| Waveform L1 | 0.014848 |
| Spectral loss | 0.119992 |
| Commitment loss | 0.047363 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9586 |
| ESTOI | 0.7192 |
| SI-SNR (dB) | 4.7771 |
| UTMOS | 2.8391 |
| Course objective score | 45.5569 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 676.032 |
| Decoder MFLOP/s | 265.152 |
| Parameters | 723549 |

### Effective configuration

```yaml
seed: 8128
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
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_d_combo_seed8128
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:seed_confirm_d_combo_seed8128:end -->

<!-- experiment:seed_confirm_b_fm15_seed3407:start -->
## seed_confirm_b_fm15_seed3407

- Status: `complete`
- Updated (UTC): `2026-10-22T14:19:44.246869+00:00`
- Git commit: `8ea5ccf93f0b3dcfcab31e8aba0ac0745054d98c`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_b_fm15_seed3407`
- Note: 30000 factorial fine-tuning steps from refine4 D best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_b_fm15_seed3407/checkpoints/best.pt`
- Checkpoint SHA-256: `4c82b331566a81893f3931af4fa7ceed99be460d436c2f8e99251d5e7cf4f347`

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
| Train loss | 0.504635 |
| Reconstruction loss | 0.135139 |
| Waveform L1 | 0.015096 |
| Spectral loss | 0.120043 |
| Commitment loss | 0.042825 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9531 |
| ESTOI | 0.7210 |
| SI-SNR (dB) | 4.5304 |
| UTMOS | 2.8506 |
| Course objective score | 45.4802 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 676.032 |
| Decoder MFLOP/s | 265.152 |
| Parameters | 723549 |

### Effective configuration

```yaml
seed: 3407
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
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.0
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_b_fm15_seed3407
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:seed_confirm_b_fm15_seed3407:end -->
<!-- experiment:seed_confirm_b_fm15_seed8128:start -->
## seed_confirm_b_fm15_seed8128

- Status: `complete`
- Updated (UTC): `2026-10-22T14:19:19.511868+00:00`
- Git commit: `8ea5ccf93f0b3dcfcab31e8aba0ac0745054d98c`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_b_fm15_seed8128`
- Note: 30000 factorial fine-tuning steps from refine4 D best checkpoint and fixed evaluation completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_b_fm15_seed8128/checkpoints/best.pt`
- Checkpoint SHA-256: `70e7d1df50659ce93eacb9db0fc6938a88d27b6d47062a53ef2dfdbb73f682a8`

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
| Train loss | 0.504409 |
| Reconstruction loss | 0.135304 |
| Waveform L1 | 0.015107 |
| Spectral loss | 0.120197 |
| Commitment loss | 0.042427 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9506 |
| ESTOI | 0.7202 |
| SI-SNR (dB) | 4.5528 |
| UTMOS | 2.8442 |
| Course objective score | 45.4171 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 676.032 |
| Decoder MFLOP/s | 265.152 |
| Parameters | 723549 |

### Effective configuration

```yaml
seed: 8128
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
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.0
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/seed_confirm_b_fm15_seed8128
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:seed_confirm_b_fm15_seed8128:end -->

<!-- experiment:codebook4_d_combined:start -->
## codebook4_d_combined

- Status: `complete`
- Updated (UTC): `2026-10-23T03:48:25.843917+00:00`
- Git commit: `d6d09513f73dcf67c79a4a9f6d790fb82cd42d07`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_d_combined`
- Note: 30000-step RVQ study completed; stagewise analysis: /storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_d_combined/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_d_combined/checkpoints/best.pt`
- Checkpoint SHA-256: `e0ab196eab8963a3dd178f7fa3b6fc72e233b70824a0a0d04c87163c03be1b89`

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
| Train loss | 0.502141 |
| Reconstruction loss | 0.134388 |
| Waveform L1 | 0.014788 |
| Spectral loss | 0.119600 |
| Commitment loss | 0.048892 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9629 |
| ESTOI | 0.7203 |
| SI-SNR (dB) | 4.8426 |
| UTMOS | 2.8697 |
| Course objective score | 45.8473 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 676.032 |
| Decoder MFLOP/s | 265.152 |
| Parameters | 723549 |

### Effective configuration

```yaml
seed: 20261023
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
  rvq_usage_loss_weight: 0.001
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.5
  - 2.0
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_d_combined
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:codebook4_d_combined:end -->
<!-- experiment:codebook4_a_control:start -->
## codebook4_a_control

- Status: `complete`
- Updated (UTC): `2026-10-23T03:48:15.798914+00:00`
- Git commit: `d6d09513f73dcf67c79a4a9f6d790fb82cd42d07`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_a_control`
- Note: 30000-step RVQ study completed; stagewise analysis: /storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_a_control/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_a_control/checkpoints/best.pt`
- Checkpoint SHA-256: `593f2bf7dbdbe332109a607db69e1e114ae9ca7d4fbdcc96a2d0cc1b332601a1`

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
| Train loss | 0.501371 |
| Reconstruction loss | 0.134851 |
| Waveform L1 | 0.014865 |
| Spectral loss | 0.119986 |
| Commitment loss | 0.048268 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9508 |
| ESTOI | 0.7216 |
| SI-SNR (dB) | 4.8127 |
| UTMOS | 2.8507 |
| Course objective score | 45.6565 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 676.032 |
| Decoder MFLOP/s | 265.152 |
| Parameters | 723549 |

### Effective configuration

```yaml
seed: 20261023
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
  rvq_usage_loss_weight: 0.0
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.0
  - 1.0
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_a_control
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:codebook4_a_control:end -->

<!-- experiment:codebook4_b_balance:start -->
## codebook4_b_balance

- Status: `complete`
- Updated (UTC): `2026-10-23T03:48:24.418318+00:00`
- Git commit: `d6d09513f73dcf67c79a4a9f6d790fb82cd42d07`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_b_balance`
- Note: 30000-step RVQ study completed; stagewise analysis: /storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_b_balance/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_b_balance/checkpoints/best.pt`
- Checkpoint SHA-256: `b9096a55e24ce8e44fc474b9e0a24e97e46ad4f1914fb59e021299d793416286`

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
| Train loss | 0.502196 |
| Reconstruction loss | 0.134733 |
| Waveform L1 | 0.014844 |
| Spectral loss | 0.119889 |
| Commitment loss | 0.048189 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9509 |
| ESTOI | 0.7202 |
| SI-SNR (dB) | 4.8235 |
| UTMOS | 2.8502 |
| Course objective score | 45.6244 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 676.032 |
| Decoder MFLOP/s | 265.152 |
| Parameters | 723549 |

### Effective configuration

```yaml
seed: 20261023
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
  rvq_usage_loss_weight: 0.001
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.0
  - 1.0
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_b_balance
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:codebook4_b_balance:end -->
<!-- experiment:codebook4_c_later_stages:start -->
## codebook4_c_later_stages

- Status: `complete`
- Updated (UTC): `2026-10-23T03:48:15.599300+00:00`
- Git commit: `d6d09513f73dcf67c79a4a9f6d790fb82cd42d07`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_c_later_stages`
- Note: 30000-step RVQ study completed; stagewise analysis: /storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_c_later_stages/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_c_later_stages/checkpoints/best.pt`
- Checkpoint SHA-256: `f33810831d161e2f6646b28c3bf1d359d56be2adcd2c8aa4d4b784e3e1197c85`

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
| Train loss | 0.502026 |
| Reconstruction loss | 0.134499 |
| Waveform L1 | 0.014770 |
| Spectral loss | 0.119729 |
| Commitment loss | 0.048835 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9558 |
| ESTOI | 0.7219 |
| SI-SNR (dB) | 4.8799 |
| UTMOS | 2.8616 |
| Course objective score | 45.8099 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Total MFLOP/s | 676.032 |
| Decoder MFLOP/s | 265.152 |
| Parameters | 723549 |

### Effective configuration

```yaml
seed: 20261023
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
  rvq_usage_loss_weight: 0.0
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.5
  - 2.0
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  warmup_steps: 0
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/codebook4_c_later_stages
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
```

<!-- experiment:codebook4_c_later_stages:end -->

<!-- experiment:struct4_b_residual_later:start -->
## struct4_b_residual_later

- Status: `complete`
- Updated (UTC): `2026-10-23T17:31:07.740393+00:00`
- Git commit: `0810f32be4b8da40b36bb60436d4ec0cdd5bfcba`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_b_residual_later`
- Note: 100000-step structural quantizer study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_b_residual_later/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_b_residual_later/checkpoints/best.pt`
- Checkpoint SHA-256: `f9c71919519dbda7d02bdfc56d6eb309cf9a45976d733e29b3fd808b7b77cc1a`

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
| Epoch | 9 |
| Global step | 100000 |
| Train loss | 0.589039 |
| Reconstruction loss | 0.131509 |
| Waveform L1 | 0.014402 |
| Spectral loss | 0.117107 |
| Commitment loss | 0.101074 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9982 |
| ESTOI | 0.7288 |
| SI-SNR (dB) | 5.1789 |
| UTMOS | 2.9057 |
| Course objective score | 46.7463 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 650.227 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662109 |

### Effective configuration

```yaml
seed: 20261024
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: projected_rvq
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
  rvq_usage_loss_weight: 0.001
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.5
  - 2.0
  projected_stage_dims:
  - 48
  - 64
  - 80
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  start_step: 5000
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_b_residual_later
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
```

<!-- experiment:struct4_b_residual_later:end -->
<!-- experiment:struct4_c_product_uniform:start -->
## struct4_c_product_uniform

- Status: `complete`
- Updated (UTC): `2026-10-23T17:31:01.383493+00:00`
- Git commit: `0810f32be4b8da40b36bb60436d4ec0cdd5bfcba`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_c_product_uniform`
- Note: 100000-step structural quantizer study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_c_product_uniform/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_c_product_uniform/checkpoints/best.pt`
- Checkpoint SHA-256: `9bc86aab038bba0f27907d42d9e93213bd1767acd509af5b6a284089a2e316c5`

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
| Epoch | 9 |
| Global step | 100000 |
| Train loss | 0.536397 |
| Reconstruction loss | 0.132806 |
| Waveform L1 | 0.014622 |
| Spectral loss | 0.118183 |
| Commitment loss | 0.054422 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9767 |
| ESTOI | 0.7256 |
| SI-SNR (dB) | 5.0118 |
| UTMOS | 2.8979 |
| Course objective score | 46.3615 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 650.227 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662109 |

### Effective configuration

```yaml
seed: 20261024
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: product_vq
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
  rvq_usage_loss_weight: 0.001
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.5
  - 2.0
  projected_stage_dims:
  - 64
  - 64
  - 64
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  start_step: 5000
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_c_product_uniform
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
```

<!-- experiment:struct4_c_product_uniform:end -->

<!-- experiment:struct4_a_residual_uniform:start -->
## struct4_a_residual_uniform

- Status: `complete`
- Updated (UTC): `2026-10-23T17:32:43.856982+00:00`
- Git commit: `0810f32be4b8da40b36bb60436d4ec0cdd5bfcba`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_a_residual_uniform`
- Note: 100000-step structural quantizer study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_a_residual_uniform/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_a_residual_uniform/checkpoints/best.pt`
- Checkpoint SHA-256: `64d230d565e0eb3c9f137ae44ac9b88a4bbcf68fc4ff6b0dd3edf552d06ecc4a`

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
| Epoch | 9 |
| Global step | 100000 |
| Train loss | 0.587337 |
| Reconstruction loss | 0.131516 |
| Waveform L1 | 0.014426 |
| Spectral loss | 0.117090 |
| Commitment loss | 0.100134 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9855 |
| ESTOI | 0.7293 |
| SI-SNR (dB) | 5.1647 |
| UTMOS | 2.9096 |
| Course objective score | 46.6837 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 650.227 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662109 |

### Effective configuration

```yaml
seed: 20261024
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: projected_rvq
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
  rvq_usage_loss_weight: 0.001
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.5
  - 2.0
  projected_stage_dims:
  - 64
  - 64
  - 64
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  start_step: 5000
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_a_residual_uniform
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
```

<!-- experiment:struct4_a_residual_uniform:end -->
<!-- experiment:struct4_d_product_later:start -->
## struct4_d_product_later

- Status: `complete`
- Updated (UTC): `2026-10-23T17:31:02.001553+00:00`
- Git commit: `0810f32be4b8da40b36bb60436d4ec0cdd5bfcba`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_d_product_later`
- Note: 100000-step structural quantizer study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_d_product_later/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_d_product_later/checkpoints/best.pt`
- Checkpoint SHA-256: `01451a47dd2f893a8e50ac0569fc05e707bd1f1f48cb0596553aaa26e9681033`

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
| Epoch | 9 |
| Global step | 100000 |
| Train loss | 0.535320 |
| Reconstruction loss | 0.133307 |
| Waveform L1 | 0.014667 |
| Spectral loss | 0.118640 |
| Commitment loss | 0.054243 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9827 |
| ESTOI | 0.7262 |
| SI-SNR (dB) | 4.9800 |
| UTMOS | 2.8919 |
| Course objective score | 46.3595 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 650.227 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662109 |

### Effective configuration

```yaml
seed: 20261024
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: product_vq
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
  rvq_usage_loss_weight: 0.001
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.5
  - 2.0
  projected_stage_dims:
  - 48
  - 64
  - 80
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  start_step: 5000
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_d_product_later
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
```

<!-- experiment:struct4_d_product_later:end -->

<!-- experiment:struct4_seed_b_later_8128:start -->
## struct4_seed_b_later_8128

- Status: `complete`
- Updated (UTC): `2026-10-24T13:29:15.043505+00:00`
- Git commit: `9e943c9f658bf50c0f480ac3a0211d8ee186de55`
- Run directory: `runs/struct4_seed_b_later_8128`
- Note: 100000-step structural seed confirmation completed; diagnostics: runs/struct4_seed_b_later_8128/rvq_diagnostics.json
- Best checkpoint: `runs/struct4_seed_b_later_8128/checkpoints/best.pt`
- Checkpoint SHA-256: `6ec0f4955fd008d2155b6d8c30fb89caa6b5f44a085ebe1cfdf59b9f88f1f6a5`

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
| Epoch | 9 |
| Global step | 100000 |
| Train loss | 0.586311 |
| Reconstruction loss | 0.132476 |
| Waveform L1 | 0.014655 |
| Spectral loss | 0.117821 |
| Commitment loss | 0.103153 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9941 |
| ESTOI | 0.7289 |
| SI-SNR (dB) | 5.1158 |
| UTMOS | 2.8998 |
| Course objective score | 46.6438 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 650.227 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662109 |

### Effective configuration

```yaml
seed: 8128
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: projected_rvq
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
  rvq_usage_loss_weight: 0.001
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.5
  - 2.0
  projected_stage_dims:
  - 48
  - 64
  - 80
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  start_step: 5000
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_seed_b_later_8128
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
```

<!-- experiment:struct4_seed_b_later_8128:end -->
<!-- experiment:struct4_seed_a_uniform_3407:start -->
## struct4_seed_a_uniform_3407

- Status: `complete`
- Updated (UTC): `2026-10-24T13:29:14.701617+00:00`
- Git commit: `9e943c9f658bf50c0f480ac3a0211d8ee186de55`
- Run directory: `runs/struct4_seed_a_uniform_3407`
- Note: 100000-step structural seed confirmation completed; diagnostics: runs/struct4_seed_a_uniform_3407/rvq_diagnostics.json
- Best checkpoint: `runs/struct4_seed_a_uniform_3407/checkpoints/best.pt`
- Checkpoint SHA-256: `5ae3236e5d63ba21ae599334529faefeb0ad85f9ba6181b912b404c453c7b218`

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
| Epoch | 9 |
| Global step | 100000 |
| Train loss | 0.588459 |
| Reconstruction loss | 0.131302 |
| Waveform L1 | 0.014414 |
| Spectral loss | 0.116889 |
| Commitment loss | 0.102761 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9889 |
| ESTOI | 0.7296 |
| SI-SNR (dB) | 5.0870 |
| UTMOS | 2.9077 |
| Course objective score | 46.6570 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 650.227 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662109 |

### Effective configuration

```yaml
seed: 3407
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: projected_rvq
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
  rvq_usage_loss_weight: 0.001
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.5
  - 2.0
  projected_stage_dims:
  - 64
  - 64
  - 64
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  start_step: 5000
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_seed_a_uniform_3407
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
```

<!-- experiment:struct4_seed_a_uniform_3407:end -->

<!-- experiment:struct4_seed_a_uniform_8128:start -->
## struct4_seed_a_uniform_8128

- Status: `complete`
- Updated (UTC): `2026-10-24T13:29:14.817262+00:00`
- Git commit: `9e943c9f658bf50c0f480ac3a0211d8ee186de55`
- Run directory: `runs/struct4_seed_a_uniform_8128`
- Note: 100000-step structural seed confirmation completed; diagnostics: runs/struct4_seed_a_uniform_8128/rvq_diagnostics.json
- Best checkpoint: `runs/struct4_seed_a_uniform_8128/checkpoints/best.pt`
- Checkpoint SHA-256: `9bdabf9a897ed25ab69d1e344d40e180eb4e7ae5e29229d667c82526cacf192b`

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
| Epoch | 9 |
| Global step | 100000 |
| Train loss | 0.580683 |
| Reconstruction loss | 0.131651 |
| Waveform L1 | 0.014439 |
| Spectral loss | 0.117212 |
| Commitment loss | 0.100223 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0051 |
| ESTOI | 0.7298 |
| SI-SNR (dB) | 5.1594 |
| UTMOS | 2.9137 |
| Course objective score | 46.8589 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 650.227 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662109 |

### Effective configuration

```yaml
seed: 8128
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: projected_rvq
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
  rvq_usage_loss_weight: 0.001
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.5
  - 2.0
  projected_stage_dims:
  - 64
  - 64
  - 64
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  start_step: 5000
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_seed_a_uniform_8128
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
```

<!-- experiment:struct4_seed_a_uniform_8128:end -->

<!-- experiment:struct4_seed_b_later_3407:start -->
## struct4_seed_b_later_3407

- Status: `complete`
- Updated (UTC): `2026-10-24T13:29:14.931503+00:00`
- Git commit: `9e943c9f658bf50c0f480ac3a0211d8ee186de55`
- Run directory: `runs/struct4_seed_b_later_3407`
- Note: 100000-step structural seed confirmation completed; diagnostics: runs/struct4_seed_b_later_3407/rvq_diagnostics.json
- Best checkpoint: `runs/struct4_seed_b_later_3407/checkpoints/best.pt`
- Checkpoint SHA-256: `8c35191307838d375b704f7dc039cacefecf3bcb47dca10151a219ff07e20f14`

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
| Epoch | 9 |
| Global step | 100000 |
| Train loss | 0.589994 |
| Reconstruction loss | 0.131432 |
| Waveform L1 | 0.014428 |
| Spectral loss | 0.117004 |
| Commitment loss | 0.102994 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9987 |
| ESTOI | 0.7276 |
| SI-SNR (dB) | 5.1392 |
| UTMOS | 2.9017 |
| Course objective score | 46.6707 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 650.227 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662109 |

### Effective configuration

```yaml
seed: 3407
audio:
  sample_rate: 16000
  frame_samples: 160
  segment_samples: 32000
model:
  sample_rate: 16000
  frame_samples: 160
  quantizer_type: projected_rvq
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
  rvq_usage_loss_weight: 0.001
  rvq_usage_temperature: 1.0
  rvq_stage_commitment_weights:
  - 1.0
  - 1.5
  - 2.0
  projected_stage_dims:
  - 48
  - 64
  - 80
loss:
  waveform_l1_weight: 1.0
  spectral_weight: 1.0
  fft_sizes:
  - 256
  - 512
  - 1024
  spectral_convergence_weight: 0.25
  linear_magnitude_weight: 0.1
  adversarial_weight: 0.05
  feature_matching_weight: 1.5
  si_snr_weight: 0.003
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
  start_step: 5000
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
  learning_rate: 2.0e-05
  weight_decay: 1.0e-06
  gradient_clip_norm: 1.0
  validation_limit: 32
  validation_checkpoint_interval_steps: 10000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/struct4_seed_b_later_3407
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
```

<!-- experiment:struct4_seed_b_later_3407:end -->
