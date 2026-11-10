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

<!-- experiment:decoder4_b_multiscale_refiner:start -->
## decoder4_b_multiscale_refiner

- Status: `complete`
- Updated (UTC): `2026-10-25T12:07:50.944673+00:00`
- Git commit: `25d4133825514e48b9f7939b984c600fbe82d309`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_b_multiscale_refiner`
- Note: 100000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_b_multiscale_refiner/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_b_multiscale_refiner/checkpoints/best.pt`
- Checkpoint SHA-256: `d552cf7378ac7e61d8ca92edd5f91d061112ce799263a69c34fb6aa96a93a544`

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
| Train loss | 0.611897 |
| Reconstruction loss | 0.131038 |
| Waveform L1 | 0.014372 |
| Spectral loss | 0.116665 |
| Commitment loss | 0.106551 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0242 |
| ESTOI | 0.7353 |
| SI-SNR (dB) | 5.3746 |
| UTMOS | 2.9146 |
| Course objective score | 47.2741 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 657.139 |
| Decoder MFLOP/s | 284.352 |
| Parameters | 662346 |

### Effective configuration

```yaml
seed: 20261025
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
  decoder_refinement: multiscale
  decoder_refinement_channels: 4
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
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_b_multiscale_refiner
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
```

<!-- experiment:decoder4_b_multiscale_refiner:end -->

<!-- experiment:decoder4_d_teacher_distill:start -->
## decoder4_d_teacher_distill

- Status: `complete`
- Updated (UTC): `2026-10-25T12:34:30.199874+00:00`
- Git commit: `25d4133825514e48b9f7939b984c600fbe82d309`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_d_teacher_distill`
- Note: 100000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_d_teacher_distill/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_d_teacher_distill/checkpoints/best.pt`
- Checkpoint SHA-256: `85f233f386e3c346c46099080c69f853650c86dc58f33f87a70781e8ff53efb2`

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
| Train loss | 0.624954 |
| Reconstruction loss | 0.130805 |
| Waveform L1 | 0.014348 |
| Spectral loss | 0.116457 |
| Commitment loss | 0.109440 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0216 |
| ESTOI | 0.7319 |
| SI-SNR (dB) | 5.3972 |
| UTMOS | 2.9368 |
| Course objective score | 47.3227 |

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
seed: 20261025
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
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_d_teacher_distill
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
waveform_distillation:
  enabled: true
  checkpoint: runs/struct4_seed_a_uniform_8128/checkpoints/best.pt
  waveform_l1_weight: 0.1
  spectral_weight: 0.1
```

<!-- experiment:decoder4_d_teacher_distill:end -->
<!-- experiment:decoder4_c_haar_subband:start -->
## decoder4_c_haar_subband

- Status: `complete`
- Updated (UTC): `2026-10-25T11:53:44.553081+00:00`
- Git commit: `25d4133825514e48b9f7939b984c600fbe82d309`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_c_haar_subband`
- Note: 100000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_c_haar_subband/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_c_haar_subband/checkpoints/best.pt`
- Checkpoint SHA-256: `d19c7ea65e035dc1f46f4bdf58c10f7f7b08e616d5e846707fa36530f969b807`

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
| Train loss | 0.608592 |
| Reconstruction loss | 0.130426 |
| Waveform L1 | 0.014298 |
| Spectral loss | 0.116128 |
| Commitment loss | 0.108201 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0166 |
| ESTOI | 0.7340 |
| SI-SNR (dB) | 5.3136 |
| UTMOS | 2.8992 |
| Course objective score | 47.0528 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 657.075 |
| Decoder MFLOP/s | 284.288 |
| Parameters | 662559 |

### Effective configuration

```yaml
seed: 20261025
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
  decoder_refinement: haar_subband
  decoder_refinement_channels: 8
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
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_c_haar_subband
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
```

<!-- experiment:decoder4_c_haar_subband:end -->
<!-- experiment:decoder4_a_control:start -->
## decoder4_a_control

- Status: `complete`
- Updated (UTC): `2026-10-25T11:42:00.222648+00:00`
- Git commit: `25d4133825514e48b9f7939b984c600fbe82d309`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_a_control`
- Note: 100000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_a_control/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_a_control/checkpoints/best.pt`
- Checkpoint SHA-256: `1c2b8fc3dd57e12d5090a7452eb48835afc72eb31b5b866d953e0c14b8a2e4cd`

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
| Train loss | 0.611198 |
| Reconstruction loss | 0.131135 |
| Waveform L1 | 0.014391 |
| Spectral loss | 0.116744 |
| Commitment loss | 0.105868 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0098 |
| ESTOI | 0.7350 |
| SI-SNR (dB) | 5.3355 |
| UTMOS | 2.9233 |
| Course objective score | 47.1943 |

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
seed: 20261025
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
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder4_a_control
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
```

<!-- experiment:decoder4_a_control:end -->

<!-- experiment:decoder_seed4_d_multiscale_distill_8128:start -->
## decoder_seed4_d_multiscale_distill_8128

- Status: `complete`
- Updated (UTC): `2026-10-25T15:23:22.640758+00:00`
- Git commit: `f0bdf73e1a618f651a78ec600194ca959c48cda6`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_d_multiscale_distill_8128`
- Note: 30000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_d_multiscale_distill_8128/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_d_multiscale_distill_8128/checkpoints/best.pt`
- Checkpoint SHA-256: `ab501141729a19b3373831d2af814a4c3ca78c44812b8837682d04d4831944ab`

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
| Train loss | 0.608914 |
| Reconstruction loss | 0.130919 |
| Waveform L1 | 0.014338 |
| Spectral loss | 0.116581 |
| Commitment loss | 0.104395 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0575 |
| ESTOI | 0.7417 |
| SI-SNR (dB) | 5.5463 |
| UTMOS | 2.7557 |
| Course objective score | 46.7856 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 657.139 |
| Decoder MFLOP/s | 284.352 |
| Parameters | 662346 |

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
  decoder_refinement: multiscale
  decoder_refinement_channels: 4
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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_d_multiscale_distill_8128
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
waveform_distillation:
  enabled: true
  checkpoint: runs/struct4_seed_a_uniform_8128/checkpoints/best.pt
  waveform_l1_weight: 0.1
  spectral_weight: 0.1
```

<!-- experiment:decoder_seed4_d_multiscale_distill_8128:end -->

<!-- experiment:decoder_seed4_a_distill_3407:start -->
## decoder_seed4_a_distill_3407

- Status: `complete`
- Updated (UTC): `2026-10-25T17:33:37.326052+00:00`
- Git commit: `f0bdf73e1a618f651a78ec600194ca959c48cda6`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_a_distill_3407`
- Note: 30000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_a_distill_3407/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_a_distill_3407/checkpoints/best.pt`
- Checkpoint SHA-256: `27803665ba9a5e6415c77c8b06dc38b55adda737120ca7f9e79d715c20062007`

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
| Train loss | 0.607160 |
| Reconstruction loss | 0.131211 |
| Waveform L1 | 0.014375 |
| Spectral loss | 0.116836 |
| Commitment loss | 0.102483 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0738 |
| ESTOI | 0.7419 |
| SI-SNR (dB) | 5.5447 |
| UTMOS | 2.7488 |
| Course objective score | 46.8630 |

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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_a_distill_3407
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
waveform_distillation:
  enabled: true
  checkpoint: runs/struct4_seed_a_uniform_8128/checkpoints/best.pt
  waveform_l1_weight: 0.1
  spectral_weight: 0.1
```

<!-- experiment:decoder_seed4_a_distill_3407:end -->

<!-- experiment:decoder_seed4_b_distill_8128:start -->
## decoder_seed4_b_distill_8128

- Status: `complete`
- Updated (UTC): `2026-10-25T19:44:00.492865+00:00`
- Git commit: `f0bdf73e1a618f651a78ec600194ca959c48cda6`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_b_distill_8128`
- Note: 30000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_b_distill_8128/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_b_distill_8128/checkpoints/best.pt`
- Checkpoint SHA-256: `127491647b1636cac27672e59a749806d9ef10b0f0e7f105f937e3d5a53fadbe`

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
| Train loss | 0.607587 |
| Reconstruction loss | 0.130951 |
| Waveform L1 | 0.014329 |
| Spectral loss | 0.116622 |
| Commitment loss | 0.103712 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0540 |
| ESTOI | 0.7419 |
| SI-SNR (dB) | 5.5996 |
| UTMOS | 2.7627 |
| Course objective score | 46.8433 |

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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_b_distill_8128
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
waveform_distillation:
  enabled: true
  checkpoint: runs/struct4_seed_a_uniform_8128/checkpoints/best.pt
  waveform_l1_weight: 0.1
  spectral_weight: 0.1
```

<!-- experiment:decoder_seed4_b_distill_8128:end -->

<!-- experiment:decoder_seed4_c_multiscale_distill_3407:start -->
## decoder_seed4_c_multiscale_distill_3407

- Status: `complete`
- Updated (UTC): `2026-10-25T23:31:39.487116+00:00`
- Git commit: `f0bdf73e1a618f651a78ec600194ca959c48cda6`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_c_multiscale_distill_3407`
- Note: 30000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_c_multiscale_distill_3407/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_c_multiscale_distill_3407/checkpoints/best.pt`
- Checkpoint SHA-256: `38d85c5d7ef467a2952d486cdcc27c6034bd29b791405eabd657e45d17e7e67d`

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
| Train loss | 0.609681 |
| Reconstruction loss | 0.131088 |
| Waveform L1 | 0.014346 |
| Spectral loss | 0.116743 |
| Commitment loss | 0.103233 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0587 |
| ESTOI | 0.7404 |
| SI-SNR (dB) | 5.5607 |
| UTMOS | 2.7438 |
| Course objective score | 46.6964 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 657.139 |
| Decoder MFLOP/s | 284.352 |
| Parameters | 662346 |

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
  decoder_refinement: multiscale
  decoder_refinement_channels: 4
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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_seed4_c_multiscale_distill_3407
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
waveform_distillation:
  enabled: true
  checkpoint: runs/struct4_seed_a_uniform_8128/checkpoints/best.pt
  waveform_l1_weight: 0.1
  spectral_weight: 0.1
```

<!-- experiment:decoder_seed4_c_multiscale_distill_3407:end -->

<!-- experiment:decoder_stability4_a_control_3407:start -->
## decoder_stability4_a_control_3407

- Status: `complete`
- Updated (UTC): `2026-10-26T02:26:49.713810+00:00`
- Git commit: `9c82fc642373e5ee4b0afefb4db3c1d9b18438be`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_a_control_3407`
- Note: 30000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_a_control_3407/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_a_control_3407/checkpoints/best.pt`
- Checkpoint SHA-256: `f425fdc28ea735cad302c17acc353f43278bef17efdc5cc3411e936a6e10cf20`

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
| Train loss | 0.594358 |
| Reconstruction loss | 0.131221 |
| Waveform L1 | 0.014362 |
| Spectral loss | 0.116858 |
| Commitment loss | 0.101905 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0628 |
| ESTOI | 0.7411 |
| SI-SNR (dB) | 5.5573 |
| UTMOS | 2.6732 |
| Course objective score | 46.3005 |

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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_a_control_3407
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
```

<!-- experiment:decoder_stability4_a_control_3407:end -->

<!-- experiment:decoder_stability4_b_control_8128:start -->
## decoder_stability4_b_control_8128

- Status: `complete`
- Updated (UTC): `2026-10-26T04:11:37.515540+00:00`
- Git commit: `9c82fc642373e5ee4b0afefb4db3c1d9b18438be`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_b_control_8128`
- Note: 30000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_b_control_8128/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_b_control_8128/checkpoints/best.pt`
- Checkpoint SHA-256: `4c249f0392bc4b1780aee2ac501b4884596e4c6d53c3b55f233590b602a94bca`

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
| Train loss | 0.593357 |
| Reconstruction loss | 0.131077 |
| Waveform L1 | 0.014369 |
| Spectral loss | 0.116708 |
| Commitment loss | 0.100711 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0708 |
| ESTOI | 0.7432 |
| SI-SNR (dB) | 5.5871 |
| UTMOS | 2.6599 |
| Course objective score | 46.3444 |

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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_b_control_8128
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
```

<!-- experiment:decoder_stability4_b_control_8128:end -->

<!-- experiment:decoder_stability4_c_distill_swa_3407:start -->
## decoder_stability4_c_distill_swa_3407

- Status: `complete`
- Updated (UTC): `2026-10-26T06:17:10.833312+00:00`
- Git commit: `9c82fc642373e5ee4b0afefb4db3c1d9b18438be`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_c_distill_swa_3407`
- Note: 30000-step distillation plus early-window SWA completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_c_distill_swa_3407/checkpoints/best.pt`
- Checkpoint SHA-256: `18c7b06c3245c2b46e84217ed476678bb1fab01494f89276fc52d3afac7e5935`

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
| Train loss | 0.607645 |
| Reconstruction loss | 0.130988 |
| Waveform L1 | 0.014378 |
| Spectral loss | 0.116610 |
| Commitment loss | 0.103006 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9013 |
| ESTOI | 0.7188 |
| SI-SNR (dB) | 4.5612 |
| UTMOS | 2.7628 |
| Course objective score | 44.5262 |

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
  validation_checkpoint_interval_steps: 2500
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_c_distill_swa_3407
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 12
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
waveform_distillation:
  enabled: true
  checkpoint: runs/struct4_seed_a_uniform_8128/checkpoints/best.pt
  waveform_l1_weight: 0.1
  spectral_weight: 0.1
```

<!-- experiment:decoder_stability4_c_distill_swa_3407:end -->

<!-- experiment:decoder_stability4_d_distill_swa_8128:start -->
## decoder_stability4_d_distill_swa_8128

- Status: `complete`
- Updated (UTC): `2026-10-26T08:17:55.982429+00:00`
- Git commit: `9c82fc642373e5ee4b0afefb4db3c1d9b18438be`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_d_distill_swa_8128`
- Note: 30000-step distillation plus early-window SWA completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_d_distill_swa_8128/checkpoints/best.pt`
- Checkpoint SHA-256: `33a751885cdb61ecc11f97b4873691d95e942db6ee19b77df312a2ba9c136e94`

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
| Train loss | 0.607378 |
| Reconstruction loss | 0.131111 |
| Waveform L1 | 0.014345 |
| Spectral loss | 0.116766 |
| Commitment loss | 0.103446 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9481 |
| ESTOI | 0.7211 |
| SI-SNR (dB) | 4.6429 |
| UTMOS | 2.7726 |
| Course objective score | 45.0291 |

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
  validation_checkpoint_interval_steps: 2500
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/decoder_stability4_d_distill_swa_8128
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 12
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
waveform_distillation:
  enabled: true
  checkpoint: runs/struct4_seed_a_uniform_8128/checkpoints/best.pt
  waveform_l1_weight: 0.1
  spectral_weight: 0.1
```

<!-- experiment:decoder_stability4_d_distill_swa_8128:end -->

<!-- experiment:stability5_a_late_decoder_avg_3407:start -->
## stability5_a_late_decoder_avg_3407

- Status: `complete`
- Updated (UTC): `2026-10-26T11:48:47.555834+00:00`
- Git commit: `abec142e8810bf1f915822ad27015ea5c6b67c7d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_a_late_decoder_avg_3407`
- Note: post-hoc decoder-only stable-window average completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_a_late_decoder_avg_3407/checkpoints/best.pt`
- Checkpoint SHA-256: `75ace729d6bb12ee962dc1372f4163aea854bf3af1028b3efa1f3c3161de7d54`

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
| Train loss | 0.607160 |
| Reconstruction loss | 0.131211 |
| Waveform L1 | 0.014375 |
| Spectral loss | 0.116836 |
| Commitment loss | 0.102483 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0004 |
| ESTOI | 0.7316 |
| SI-SNR (dB) | 5.2448 |
| UTMOS | 2.9219 |
| Course objective score | 46.9762 |

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
_base_: ../decoder_seed4/a_distill_seed3407.yaml

posthoc_average:
  method: decoder_only_uniform
  source_run: runs/decoder_seed4_a_distill_3407
  checkpoint_steps: [20000, 25000, 30000]
  base_step: 30000
  include_prefixes: [decoder.]

training:
  output_dir: runs/stability5_a_late_decoder_avg_3407
```

<!-- experiment:stability5_a_late_decoder_avg_3407:end -->

<!-- experiment:stability5_b_late_decoder_avg_8128:start -->
## stability5_b_late_decoder_avg_8128

- Status: `complete`
- Updated (UTC): `2026-10-26T11:50:44.942311+00:00`
- Git commit: `abec142e8810bf1f915822ad27015ea5c6b67c7d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_b_late_decoder_avg_8128`
- Note: post-hoc decoder-only stable-window average completed
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_b_late_decoder_avg_8128/checkpoints/best.pt`
- Checkpoint SHA-256: `ad6267eb59ea884eeffdc914eb3c90fd7453668beea50427463e5173ada9cc95`

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
| Train loss | 0.607587 |
| Reconstruction loss | 0.130951 |
| Waveform L1 | 0.014329 |
| Spectral loss | 0.116622 |
| Commitment loss | 0.103712 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9991 |
| ESTOI | 0.7301 |
| SI-SNR (dB) | 5.2361 |
| UTMOS | 2.9256 |
| Course objective score | 46.9475 |

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
_base_: ../decoder_seed4/b_distill_seed8128.yaml

posthoc_average:
  method: decoder_only_uniform
  source_run: runs/decoder_seed4_b_distill_8128
  checkpoint_steps: [20000, 25000, 30000]
  base_step: 30000
  include_prefixes: [decoder.]

training:
  output_dir: runs/stability5_b_late_decoder_avg_8128
```

<!-- experiment:stability5_b_late_decoder_avg_8128:end -->

<!-- experiment:stability5_c_delayed_distill_3407:start -->
## stability5_c_delayed_distill_3407

- Status: `complete`
- Updated (UTC): `2026-10-26T13:49:59.288883+00:00`
- Git commit: `abec142e8810bf1f915822ad27015ea5c6b67c7d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_c_delayed_distill_3407`
- Note: 30000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_c_delayed_distill_3407/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_c_delayed_distill_3407/checkpoints/best.pt`
- Checkpoint SHA-256: `bc9553092640b86dde4c8e39b93bff2b17252c7e05428b762c82c0d3a8094fee`

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
| Train loss | 0.608314 |
| Reconstruction loss | 0.131190 |
| Waveform L1 | 0.014328 |
| Spectral loss | 0.116862 |
| Commitment loss | 0.104190 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0586 |
| ESTOI | 0.7425 |
| SI-SNR (dB) | 5.5556 |
| UTMOS | 2.6619 |
| Course objective score | 46.2324 |

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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_c_delayed_distill_3407
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
waveform_distillation:
  enabled: true
  checkpoint: runs/struct4_seed_a_uniform_8128/checkpoints/best.pt
  waveform_l1_weight: 0.1
  spectral_weight: 0.1
  start_step: 10000
  warmup_steps: 5000
```

<!-- experiment:stability5_c_delayed_distill_3407:end -->

<!-- experiment:stability5_d_delayed_distill_8128:start -->
## stability5_d_delayed_distill_8128

- Status: `complete`
- Updated (UTC): `2026-10-26T15:46:43.360864+00:00`
- Git commit: `abec142e8810bf1f915822ad27015ea5c6b67c7d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_d_delayed_distill_8128`
- Note: 30000-step decoder synthesis study completed; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_d_delayed_distill_8128/rvq_diagnostics.json
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_d_delayed_distill_8128/checkpoints/best.pt`
- Checkpoint SHA-256: `22b0945e26a2849b5434eba32c8458c8e4c8a991a7ea1b66c501d47357a40a30`

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
| Train loss | 0.610010 |
| Reconstruction loss | 0.131087 |
| Waveform L1 | 0.014349 |
| Spectral loss | 0.116738 |
| Commitment loss | 0.104680 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0494 |
| ESTOI | 0.7416 |
| SI-SNR (dB) | 5.5511 |
| UTMOS | 2.6593 |
| Course objective score | 46.1260 |

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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/stability5_d_delayed_distill_8128
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
waveform_distillation:
  enabled: true
  checkpoint: runs/struct4_seed_a_uniform_8128/checkpoints/best.pt
  waveform_l1_weight: 0.1
  spectral_weight: 0.1
  start_step: 10000
  warmup_steps: 5000
```

<!-- experiment:stability5_d_delayed_distill_8128:end -->

<!-- experiment:lookahead4_a_control_30ms:start -->
## lookahead4_a_control_30ms

- Status: `complete`
- Updated (UTC): `2026-10-30T19:56:29.518345+00:00`
- Git commit: `476d948cffcad39625c88512180ed4a4e352d4d3`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_a_control_30ms`
- Note: 100000-step from-scratch lookahead study complete; 30 ms; competition-compliant
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_a_control_30ms/checkpoints/best.pt`
- Checkpoint SHA-256: `9fab76aac277d5dc1c1df56bb9b59b77bb90b9b1995c87be7def29e745055bef`

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
| Train loss | 0.827964 |
| Reconstruction loss | 0.267000 |
| Waveform L1 | 0.062669 |
| Spectral loss | 0.204331 |
| Commitment loss | 0.065044 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.1707 |
| ESTOI | 0.4293 |
| SI-SNR (dB) | 2.6145 |
| UTMOS | 1.2516 |
| Course objective score | 21.4078 |

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
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_a_control_30ms
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
  data_order_seed: 20261024
```

<!-- experiment:lookahead4_a_control_30ms:end -->

<!-- experiment:lookahead4_b_future_40ms:start -->
## lookahead4_b_future_40ms

- Status: `complete`
- Updated (UTC): `2026-10-30T20:13:30.283534+00:00`
- Git commit: `476d948cffcad39625c88512180ed4a4e352d4d3`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_b_future_40ms`
- Note: 100000-step from-scratch lookahead study complete; 40 ms; research-only latency violation
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_b_future_40ms/checkpoints/best.pt`
- Checkpoint SHA-256: `88183ea9181ef2e076bb75f6e15bffc3dc6bff29cc9068c68087ffc957208c98`

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
| Train loss | 0.813011 |
| Reconstruction loss | 0.261322 |
| Waveform L1 | 0.062909 |
| Spectral loss | 0.198414 |
| Commitment loss | 0.067653 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.1781 |
| ESTOI | 0.4859 |
| SI-SNR (dB) | 2.5707 |
| UTMOS | 1.2499 |
| Course objective score | 22.8386 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 40 |
| Total MFLOP/s | 650.259 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662269 |

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
  encoder_lookahead_frames: 4
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
  allow_excess_lookahead: true
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
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_b_future_40ms
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
  data_order_seed: 20261024
```

<!-- experiment:lookahead4_b_future_40ms:end -->
<!-- experiment:lookahead4_d_future_80ms:start -->
## lookahead4_d_future_80ms

- Status: `complete`
- Updated (UTC): `2026-10-30T19:51:23.396369+00:00`
- Git commit: `476d948cffcad39625c88512180ed4a4e352d4d3`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_d_future_80ms`
- Note: 100000-step from-scratch lookahead study complete; 80 ms; research-only latency violation
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_d_future_80ms/checkpoints/best.pt`
- Checkpoint SHA-256: `064d67d6ac1b25260d649ebf38f6a967914443e373321c691cb7342725258f14`

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
| Train loss | 0.822244 |
| Reconstruction loss | 0.262286 |
| Waveform L1 | 0.063227 |
| Spectral loss | 0.199059 |
| Commitment loss | 0.063790 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.1726 |
| ESTOI | 0.4791 |
| SI-SNR (dB) | 2.3641 |
| UTMOS | 1.2524 |
| Course objective score | 22.5166 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 80 |
| Total MFLOP/s | 650.387 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662909 |

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
  encoder_lookahead_frames: 8
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
  allow_excess_lookahead: true
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
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_d_future_80ms
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
  data_order_seed: 20261024
```

<!-- experiment:lookahead4_d_future_80ms:end -->

<!-- experiment:lookahead4_c_future_60ms:start -->
## lookahead4_c_future_60ms

- Status: `complete`
- Updated (UTC): `2026-10-30T19:54:11.704526+00:00`
- Git commit: `476d948cffcad39625c88512180ed4a4e352d4d3`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_c_future_60ms`
- Note: 100000-step from-scratch lookahead study complete; 60 ms; research-only latency violation
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_c_future_60ms/checkpoints/best.pt`
- Checkpoint SHA-256: `d1a9ff9062dcdfb90df122760f94b4f4df95e54feac5c3a414fb53c3415fad8f`

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
| Train loss | 0.799239 |
| Reconstruction loss | 0.264704 |
| Waveform L1 | 0.063270 |
| Spectral loss | 0.201434 |
| Commitment loss | 0.065428 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.1718 |
| ESTOI | 0.4461 |
| SI-SNR (dB) | 2.3167 |
| UTMOS | 1.2488 |
| Course objective score | 21.7014 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 60 |
| Total MFLOP/s | 650.323 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662589 |

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
  encoder_lookahead_frames: 6
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
  allow_excess_lookahead: true
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
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead4_c_future_60ms
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 3
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 5000
  data_order_seed: 20261024
```

<!-- experiment:lookahead4_c_future_60ms:end -->

<!-- experiment:lookahead_scratch2_c_future_60ms:start -->
## lookahead_scratch2_c_future_60ms

- Status: `complete`
- Updated (UTC): `2026-11-01T11:20:15.188692+00:00`
- Git commit: `20dab48ae78adf9185829c8fcc5d6c262f0540c5`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_c_future_60ms`
- Note: 500000-step from-scratch lookahead study complete; 60 ms; research-only latency violation
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_c_future_60ms/checkpoints/best.pt`
- Checkpoint SHA-256: `44ae8018494476bb66a1c211952ee063c3172678e7d7051fe39acd068f3800d7`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.501040 |
| Reconstruction loss | 0.129802 |
| Waveform L1 | 0.013652 |
| Spectral loss | 0.116150 |
| Commitment loss | 0.104487 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0512 |
| ESTOI | 0.7379 |
| SI-SNR (dB) | 5.9574 |
| UTMOS | 2.9086 |
| Course objective score | 47.8593 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 60 |
| Total MFLOP/s | 650.323 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662589 |

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
  encoder_lookahead_frames: 6
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
  allow_excess_lookahead: true
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_c_future_60ms
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 5
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261024
```

<!-- experiment:lookahead_scratch2_c_future_60ms:end -->

<!-- experiment:lookahead_scratch2_b_future_40ms:start -->
## lookahead_scratch2_b_future_40ms

- Status: `complete`
- Updated (UTC): `2026-11-01T11:20:18.302637+00:00`
- Git commit: `20dab48ae78adf9185829c8fcc5d6c262f0540c5`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_b_future_40ms`
- Note: 500000-step from-scratch lookahead study complete; 40 ms; research-only latency violation
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_b_future_40ms/checkpoints/best.pt`
- Checkpoint SHA-256: `e97c5a93791518f5d63f73559e94b74da70b4bd97572a926d0b721daabc9765f`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.503747 |
| Reconstruction loss | 0.130055 |
| Waveform L1 | 0.013702 |
| Spectral loss | 0.116353 |
| Commitment loss | 0.096992 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0250 |
| ESTOI | 0.7333 |
| SI-SNR (dB) | 5.8261 |
| UTMOS | 2.8659 |
| Course objective score | 47.2073 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 40 |
| Total MFLOP/s | 650.259 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662269 |

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
  encoder_lookahead_frames: 4
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
  allow_excess_lookahead: true
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_b_future_40ms
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 5
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261024
```

<!-- experiment:lookahead_scratch2_b_future_40ms:end -->
<!-- experiment:lookahead_scratch2_d_future_80ms:start -->
## lookahead_scratch2_d_future_80ms

- Status: `complete`
- Updated (UTC): `2026-11-01T11:20:18.149437+00:00`
- Git commit: `20dab48ae78adf9185829c8fcc5d6c262f0540c5`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_d_future_80ms`
- Note: 500000-step from-scratch lookahead study complete; 80 ms; research-only latency violation
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_d_future_80ms/checkpoints/best.pt`
- Checkpoint SHA-256: `d7041b0391fd4506ac67ac2b8059073094bd22231b5eaf4c9f1935fdc6a4a20e`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.533839 |
| Reconstruction loss | 0.131617 |
| Waveform L1 | 0.013905 |
| Spectral loss | 0.117713 |
| Commitment loss | 0.117791 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9786 |
| ESTOI | 0.7275 |
| SI-SNR (dB) | 5.8238 |
| UTMOS | 2.7877 |
| Course objective score | 46.2402 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 80 |
| Total MFLOP/s | 650.387 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 662909 |

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
  encoder_lookahead_frames: 8
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
  allow_excess_lookahead: true
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_d_future_80ms
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 5
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261024
```

<!-- experiment:lookahead_scratch2_d_future_80ms:end -->

<!-- experiment:lookahead_scratch2_a_control_30ms:start -->
## lookahead_scratch2_a_control_30ms

- Status: `complete`
- Updated (UTC): `2026-11-01T11:41:43.518478+00:00`
- Git commit: `20dab48ae78adf9185829c8fcc5d6c262f0540c5`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_a_control_30ms`
- Note: 500000-step from-scratch lookahead study complete; 30 ms; competition-compliant
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_a_control_30ms/checkpoints/best.pt`
- Checkpoint SHA-256: `0a06fd2df88df26b175528291612ca19c4e86d43e756624c02bb256b337b2ed7`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.507069 |
| Reconstruction loss | 0.131282 |
| Waveform L1 | 0.013866 |
| Spectral loss | 0.117416 |
| Commitment loss | 0.103443 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9845 |
| ESTOI | 0.7319 |
| SI-SNR (dB) | 5.5852 |
| UTMOS | 2.8368 |
| Course objective score | 46.5503 |

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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/lookahead_scratch2_a_control_30ms
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 5
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261024
```

<!-- experiment:lookahead_scratch2_a_control_30ms:end -->

<!-- experiment:champion4_a_control:start -->
## champion4_a_control

- Status: `complete`
- Updated (UTC): `2026-11-03T00:38:57.660108+00:00`
- Git commit: `3d8553d21f76bfe3b785ca48be5460c67f209fd4`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_a_control`
- Note: 100000 training steps completed. Pre-registered reconstruction-selected checkpoint; primary control gate failed; see CHAMPION4_RESULTS.md.
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_a_control/checkpoints/best.pt`
- Checkpoint SHA-256: `40e71c3f125a6e4da4fb0fe011577b83745d56ce3c7d5eee98be2253257d0303`
- Selected checkpoint global step: `5000`

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
| Train loss | 0.609097 |
| Reconstruction loss | 0.130946 |
| Waveform L1 | 0.014297 |
| Spectral loss | 0.116649 |
| Commitment loss | 0.105398 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0382 |
| ESTOI | 0.7424 |
| SI-SNR (dB) | 5.5017 |
| UTMOS | 2.6557 |
| Course objective score | 46.0115 |

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
seed: 20261102
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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_a_control
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 2
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261102
  epoch_addressed_data_order: true
  reset_rng_after_init: true
champion_training:
  quantizer_bypass_probability: 0.0
  mel_weight: 0.0
  mel_fft_sizes:
  - 256
  - 512
  - 1024
  mel_bins:
  - 32
  - 64
  - 80
  mel_reduction_start: 80000
  mel_reduction_ramp: 5000
  mel_final_ratio: 0.06666666666666667
```

<!-- experiment:champion4_a_control:end -->

<!-- experiment:champion4_b_training:start -->
## champion4_b_training

- Status: `complete`
- Updated (UTC): `2026-11-03T00:39:02.235348+00:00`
- Git commit: `3d8553d21f76bfe3b785ca48be5460c67f209fd4`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_b_training`
- Note: 100000 training steps completed. Pre-registered reconstruction-selected checkpoint; primary control gate failed; see CHAMPION4_RESULTS.md.
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_b_training/checkpoints/best.pt`
- Checkpoint SHA-256: `7a82b4efca8f299fcf51593f6f1a8a83540219336c175f359e17de7623fa0c84`
- Selected checkpoint global step: `5000`

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
| Train loss | 0.498625 |
| Reconstruction loss | 0.130704 |
| Waveform L1 | 0.014399 |
| Spectral loss | 0.116305 |
| Commitment loss | 0.109524 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0799 |
| ESTOI | 0.7521 |
| SI-SNR (dB) | 5.3005 |
| UTMOS | 2.7126 |
| Course objective score | 46.7819 |

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
seed: 20261102
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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_b_training
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 2
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261102
  epoch_addressed_data_order: true
  reset_rng_after_init: true
champion_training:
  quantizer_bypass_probability: 0.5
  mel_weight: 1.0
  mel_fft_sizes:
  - 256
  - 512
  - 1024
  mel_bins:
  - 32
  - 64
  - 80
  mel_reduction_start: 80000
  mel_reduction_ramp: 5000
  mel_final_ratio: 0.06666666666666667
```

<!-- experiment:champion4_b_training:end -->

<!-- experiment:champion4_c_conv2former:start -->
## champion4_c_conv2former

- Status: `complete`
- Updated (UTC): `2026-11-03T00:39:06.892208+00:00`
- Git commit: `3d8553d21f76bfe3b785ca48be5460c67f209fd4`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_c_conv2former`
- Note: 100000 training steps completed. Pre-registered reconstruction-selected checkpoint; primary control gate failed; see CHAMPION4_RESULTS.md.
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_c_conv2former/checkpoints/best.pt`
- Checkpoint SHA-256: `ae971f8ab253d3fab72d970e7bc2964087d44429a89fe8de6d5522fdb614becc`
- Selected checkpoint global step: `5000`

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
| Train loss | 0.603241 |
| Reconstruction loss | 0.130676 |
| Waveform L1 | 0.014350 |
| Spectral loss | 0.116326 |
| Commitment loss | 0.103534 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0449 |
| ESTOI | 0.7436 |
| SI-SNR (dB) | 5.5590 |
| UTMOS | 2.6347 |
| Course objective score | 45.9936 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 668.947 |
| Decoder MFLOP/s | 296.160 |
| Parameters | 758109 |

### Effective configuration

```yaml
seed: 20261102
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
  decoder_conv2former_layers: 4
  decoder_conv2former_hidden: 48
  decoder_conv2former_kernel: 7
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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_c_conv2former
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 2
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261102
  epoch_addressed_data_order: true
  reset_rng_after_init: true
champion_training:
  quantizer_bypass_probability: 0.0
  mel_weight: 0.0
  mel_fft_sizes:
  - 256
  - 512
  - 1024
  mel_bins:
  - 32
  - 64
  - 80
  mel_reduction_start: 80000
  mel_reduction_ramp: 5000
  mel_final_ratio: 0.06666666666666667
```

<!-- experiment:champion4_c_conv2former:end -->

<!-- experiment:champion4_d_combined:start -->
## champion4_d_combined

- Status: `complete`
- Updated (UTC): `2026-11-03T00:39:12.048398+00:00`
- Git commit: `3d8553d21f76bfe3b785ca48be5460c67f209fd4`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_d_combined`
- Note: 100000 training steps completed. Pre-registered reconstruction-selected checkpoint; primary control gate failed; see CHAMPION4_RESULTS.md.
- Best checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_d_combined/checkpoints/best.pt`
- Checkpoint SHA-256: `0e5cfea2f6aebc00a76723843e5f313709644241b0d6ee4ff3604b9d2ec2d0a9`
- Selected checkpoint global step: `5000`

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
| Train loss | 0.496961 |
| Reconstruction loss | 0.130527 |
| Waveform L1 | 0.014407 |
| Spectral loss | 0.116121 |
| Commitment loss | 0.109320 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0803 |
| ESTOI | 0.7528 |
| SI-SNR (dB) | 5.3306 |
| UTMOS | 2.7245 |
| Course objective score | 46.8959 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 668.947 |
| Decoder MFLOP/s | 296.160 |
| Parameters | 758109 |

### Effective configuration

```yaml
seed: 20261102
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
  decoder_conv2former_layers: 4
  decoder_conv2former_hidden: 48
  decoder_conv2former_kernel: 7
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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_d_combined
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 2
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261102
  epoch_addressed_data_order: true
  reset_rng_after_init: true
champion_training:
  quantizer_bypass_probability: 0.5
  mel_weight: 1.0
  mel_fft_sizes:
  - 256
  - 512
  - 1024
  mel_bins:
  - 32
  - 64
  - 80
  mel_reduction_start: 80000
  mel_reduction_ramp: 5000
  mel_final_ratio: 0.06666666666666667
```

<!-- experiment:champion4_d_combined:end -->
<!-- experiment:champion4_a_control_final100k_diagnostic:start -->
## champion4_a_control_final100k_diagnostic

- Status: `complete`
- Updated (UTC): `2026-11-03T00:38:59.887639+00:00`
- Git commit: `3d8553d21f76bfe3b785ca48be5460c67f209fd4`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_a_control`
- Note: 100000 training steps completed. Post-primary fixed100000 endpoint diagnostic; no additional training or checkpoint reselection; see CHAMPION4_FINAL_DIAGNOSTIC_PLAN.md.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_a_control/checkpoints/last.pt`
- Checkpoint SHA-256: `cb25f19bb4f9504cbfbcb12097f83750a4c3937972438442470f95a9d7b00a1c`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.609097 |
| Reconstruction loss | 0.130946 |
| Waveform L1 | 0.014297 |
| Spectral loss | 0.116649 |
| Commitment loss | 0.105398 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0220 |
| ESTOI | 0.7321 |
| SI-SNR (dB) | 5.2707 |
| UTMOS | 2.9346 |
| Course objective score | 47.2383 |

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
seed: 20261102
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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_a_control
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 2
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261102
  epoch_addressed_data_order: true
  reset_rng_after_init: true
champion_training:
  quantizer_bypass_probability: 0.0
  mel_weight: 0.0
  mel_fft_sizes:
  - 256
  - 512
  - 1024
  mel_bins:
  - 32
  - 64
  - 80
  mel_reduction_start: 80000
  mel_reduction_ramp: 5000
  mel_final_ratio: 0.06666666666666667
```

<!-- experiment:champion4_a_control_final100k_diagnostic:end -->

<!-- experiment:champion4_b_training_final100k_diagnostic:start -->
## champion4_b_training_final100k_diagnostic

- Status: `complete`
- Updated (UTC): `2026-11-03T00:39:04.425934+00:00`
- Git commit: `3d8553d21f76bfe3b785ca48be5460c67f209fd4`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_b_training`
- Note: 100000 training steps completed. Post-primary fixed100000 endpoint diagnostic; no additional training or checkpoint reselection; see CHAMPION4_FINAL_DIAGNOSTIC_PLAN.md.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_b_training/checkpoints/last.pt`
- Checkpoint SHA-256: `3639f2762a58315cdd3903883098417f567db0708e55381236d445f478667d06`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.498625 |
| Reconstruction loss | 0.130704 |
| Waveform L1 | 0.014399 |
| Spectral loss | 0.116305 |
| Commitment loss | 0.109524 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0195 |
| ESTOI | 0.7372 |
| SI-SNR (dB) | 5.2573 |
| UTMOS | 2.9216 |
| Course objective score | 47.2584 |

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
seed: 20261102
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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_b_training
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 2
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261102
  epoch_addressed_data_order: true
  reset_rng_after_init: true
champion_training:
  quantizer_bypass_probability: 0.5
  mel_weight: 1.0
  mel_fft_sizes:
  - 256
  - 512
  - 1024
  mel_bins:
  - 32
  - 64
  - 80
  mel_reduction_start: 80000
  mel_reduction_ramp: 5000
  mel_final_ratio: 0.06666666666666667
```

<!-- experiment:champion4_b_training_final100k_diagnostic:end -->

<!-- experiment:champion4_c_conv2former_final100k_diagnostic:start -->
## champion4_c_conv2former_final100k_diagnostic

- Status: `complete`
- Updated (UTC): `2026-11-03T00:39:09.067688+00:00`
- Git commit: `3d8553d21f76bfe3b785ca48be5460c67f209fd4`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_c_conv2former`
- Note: 100000 training steps completed. Post-primary fixed100000 endpoint diagnostic; no additional training or checkpoint reselection; see CHAMPION4_FINAL_DIAGNOSTIC_PLAN.md.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_c_conv2former/checkpoints/last.pt`
- Checkpoint SHA-256: `41b4fc071a0f092b21e0ef6c6c4f00cfc64250486f668a7a7305ca73fa8a14b4`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.603241 |
| Reconstruction loss | 0.130676 |
| Waveform L1 | 0.014350 |
| Spectral loss | 0.116326 |
| Commitment loss | 0.103534 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0182 |
| ESTOI | 0.7324 |
| SI-SNR (dB) | 5.2554 |
| UTMOS | 2.9231 |
| Course objective score | 47.1374 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 668.947 |
| Decoder MFLOP/s | 296.160 |
| Parameters | 758109 |

### Effective configuration

```yaml
seed: 20261102
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
  decoder_conv2former_layers: 4
  decoder_conv2former_hidden: 48
  decoder_conv2former_kernel: 7
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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_c_conv2former
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 2
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261102
  epoch_addressed_data_order: true
  reset_rng_after_init: true
champion_training:
  quantizer_bypass_probability: 0.0
  mel_weight: 0.0
  mel_fft_sizes:
  - 256
  - 512
  - 1024
  mel_bins:
  - 32
  - 64
  - 80
  mel_reduction_start: 80000
  mel_reduction_ramp: 5000
  mel_final_ratio: 0.06666666666666667
```

<!-- experiment:champion4_c_conv2former_final100k_diagnostic:end -->

<!-- experiment:champion4_d_combined_final100k_diagnostic:start -->
## champion4_d_combined_final100k_diagnostic

- Status: `complete`
- Updated (UTC): `2026-11-03T00:39:14.417253+00:00`
- Git commit: `3d8553d21f76bfe3b785ca48be5460c67f209fd4`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_d_combined`
- Note: 100000 training steps completed. Post-primary fixed100000 endpoint diagnostic; no additional training or checkpoint reselection; see CHAMPION4_FINAL_DIAGNOSTIC_PLAN.md.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_d_combined/checkpoints/last.pt`
- Checkpoint SHA-256: `567d70b5ad74e0db91bc1b218db5e907c433500ea57aea965ea8540c6e92c301`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.496961 |
| Reconstruction loss | 0.130527 |
| Waveform L1 | 0.014407 |
| Spectral loss | 0.116121 |
| Commitment loss | 0.109320 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0316 |
| ESTOI | 0.7371 |
| SI-SNR (dB) | 5.2395 |
| UTMOS | 2.8956 |
| Course objective score | 47.1692 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 668.947 |
| Decoder MFLOP/s | 296.160 |
| Parameters | 758109 |

### Effective configuration

```yaml
seed: 20261102
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
  decoder_conv2former_layers: 4
  decoder_conv2former_hidden: 48
  decoder_conv2former_kernel: 7
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
  validation_checkpoint_interval_steps: 5000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion4_d_combined
  minimum_learning_rate: 5.0e-06
  warmup_steps: 0
  checkpoint_keep_last: 2
  quantizer_learning_rate: 2.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261102
  epoch_addressed_data_order: true
  reset_rng_after_init: true
champion_training:
  quantizer_bypass_probability: 0.5
  mel_weight: 1.0
  mel_fft_sizes:
  - 256
  - 512
  - 1024
  mel_bins:
  - 32
  - 64
  - 80
  mel_reduction_start: 80000
  mel_reduction_ramp: 5000
  mel_final_ratio: 0.06666666666666667
```

<!-- experiment:champion4_d_combined_final100k_diagnostic:end -->

<!-- experiment:champion5_a_control:start -->
## champion5_a_control

- Status: `complete`
- Updated (UTC): `2026-11-04T09:09:01.145661+00:00`
- Git commit: `ddaf7237ba6b5390a96ec8db7b2369ff8367a105`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_a_control`
- Note: 500000-step GRU/Fourier scratch study complete; fixed endpoint checkpoint evaluated; 2400bps, 10ms frames, <=30ms lookahead; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_a_control/rvq_diagnostics.json
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_a_control/checkpoints/last.pt`
- Checkpoint SHA-256: `23d3f5d085ca68ef01235da2c2fbe549e4de315a73461704f8fe5ad64cdb5dc7`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.509444 |
| Reconstruction loss | 0.131066 |
| Waveform L1 | 0.013860 |
| Spectral loss | 0.117206 |
| Commitment loss | 0.103355 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0102 |
| ESTOI | 0.7353 |
| SI-SNR (dB) | 5.6636 |
| UTMOS | 2.8580 |
| Course objective score | 47.0006 |

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
  encoder_gru: false
  synthesis_type: waveform
  synthesis_initialization_seed: 20261103
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_a_control
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 2
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261024
  reset_rng_after_init: true
  fail_on_nonfinite: true
```

<!-- experiment:champion5_a_control:end -->

<!-- experiment:champion5_b_encoder_gru:start -->
## champion5_b_encoder_gru

- Status: `complete`
- Updated (UTC): `2026-11-04T09:23:15.602804+00:00`
- Git commit: `ddaf7237ba6b5390a96ec8db7b2369ff8367a105`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_b_encoder_gru`
- Note: 500000-step GRU/Fourier scratch study complete; fixed endpoint checkpoint evaluated; 2400bps, 10ms frames, <=30ms lookahead; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_b_encoder_gru/rvq_diagnostics.json
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_b_encoder_gru/checkpoints/last.pt`
- Checkpoint SHA-256: `2105f62858aaf1bb3b55495f9a06464013d01f5c8184e1f6d0e5db18bdd2f6f6`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.505743 |
| Reconstruction loss | 0.130242 |
| Waveform L1 | 0.013665 |
| Spectral loss | 0.116578 |
| Commitment loss | 0.102863 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0280 |
| ESTOI | 0.7365 |
| SI-SNR (dB) | 5.8975 |
| UTMOS | 2.8621 |
| Course objective score | 47.3305 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 686.115 |
| Decoder MFLOP/s | 277.440 |
| Parameters | 842749 |

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
  encoder_gru: true
  synthesis_type: waveform
  synthesis_initialization_seed: 20261103
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_b_encoder_gru
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 2
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261024
  reset_rng_after_init: true
  fail_on_nonfinite: true
```

<!-- experiment:champion5_b_encoder_gru:end -->
<!-- experiment:champion5_c_fourier:start -->
## champion5_c_fourier

- Status: `complete`
- Updated (UTC): `2026-11-04T08:17:48.831778+00:00`
- Git commit: `ddaf7237ba6b5390a96ec8db7b2369ff8367a105`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_c_fourier`
- Note: 500000-step GRU/Fourier scratch study complete; fixed endpoint checkpoint evaluated; 2400bps, 10ms frames, <=30ms lookahead; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_c_fourier/rvq_diagnostics.json
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_c_fourier/checkpoints/last.pt`
- Checkpoint SHA-256: `bf2bfa8cf9e156f825e70a06324101956dce44a2355a0adea0e4c07ebcc3832c`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.474647 |
| Reconstruction loss | 0.129344 |
| Waveform L1 | 0.013016 |
| Spectral loss | 0.116328 |
| Commitment loss | 0.100767 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.2000 |
| ESTOI | 0.7582 |
| SI-SNR (dB) | 6.6875 |
| UTMOS | 2.9865 |
| Course objective score | 50.3710 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 630.419 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1687424 |

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
  encoder_gru: false
  synthesis_type: fourier
  synthesis_initialization_seed: 20261103
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_c_fourier
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 2
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261024
  reset_rng_after_init: true
  fail_on_nonfinite: true
```

<!-- experiment:champion5_c_fourier:end -->

<!-- experiment:champion5_d_fourier_gru:start -->
## champion5_d_fourier_gru

- Status: `complete`
- Updated (UTC): `2026-11-04T08:27:13.631621+00:00`
- Git commit: `ddaf7237ba6b5390a96ec8db7b2369ff8367a105`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_d_fourier_gru`
- Note: 500000-step GRU/Fourier scratch study complete; fixed endpoint checkpoint evaluated; 2400bps, 10ms frames, <=30ms lookahead; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_d_fourier_gru/rvq_diagnostics.json
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_d_fourier_gru/checkpoints/last.pt`
- Checkpoint SHA-256: `70fbc46a1c0649ea5f80eb079b59a7c0f4f30765150dbe8f522b16e5490e16bf`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.448024 |
| Reconstruction loss | 0.127334 |
| Waveform L1 | 0.013083 |
| Spectral loss | 0.114251 |
| Commitment loss | 0.078831 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.2074 |
| ESTOI | 0.7700 |
| SI-SNR (dB) | 6.5169 |
| UTMOS | 3.1145 |
| Course objective score | 51.4126 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20261103
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion5_d_fourier_gru
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 2
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261024
  reset_rng_after_init: true
  fail_on_nonfinite: true
```

<!-- experiment:champion5_d_fourier_gru:end -->

<!-- experiment:champion6_a_s3407_control:start -->
## champion6_a_s3407_control

- Status: `complete`
- Updated (UTC): `2026-11-05T14:50:24.296757+00:00`
- Git commit: `81f2d16acb86037c45a1342b79ec6e8b41e2ff28`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_a_s3407_control`
- Note: 500000-step GRU/Fourier scratch study complete; fixed endpoint checkpoint evaluated; 2400bps, 10ms frames, <=30ms lookahead; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_a_s3407_control/rvq_diagnostics.json
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_a_s3407_control/checkpoints/last.pt`
- Checkpoint SHA-256: `b28285ab1a66b14677000a559103ea4d6564895fcaa870611c95eda35867f3ae`
- Selected checkpoint global step: `500000`
- Initialization: genuinely untrained (`trained=false`, `global_step=0`), seed/data-order3407; `runs/champion6_setup/step0_a_s3407_control.pt` SHA256 `d34c9966e42e7935e614e46b11af56ffbf9cd356018dc751ad127551d721afdd`; no resume or learned parent.
- Pair source: `runs/champion6_setup/source_step0_seed3407.pt`, SHA256 `0537e2b716e6f2d649c3b69b875d805372ecb2f8eebba0411319911299353e95`.
- Data/config/training/bitstream evidence: [CHAMPION6_RESULTS.audit](CHAMPION6_RESULTS.audit), cell `a_s3407_control`; manifest counts/hashes and fixed200 audio hashes in the same audit, matching [CHAMPION6_SETUP.audit](CHAMPION6_SETUP.audit).
- Registered interpretation: score45.974350 fails46.25 control gate; not rescued by best/mean/another seed. See [CHAMPION6_RESULTS.md](CHAMPION6_RESULTS.md).

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.582089 |
| Reconstruction loss | 0.131595 |
| Waveform L1 | 0.013884 |
| Spectral loss | 0.117711 |
| Commitment loss | 0.127620 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9760 |
| ESTOI | 0.7281 |
| SI-SNR (dB) | 5.6322 |
| UTMOS | 2.7647 |
| Course objective score | 45.9744 |

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
  encoder_gru: false
  synthesis_type: waveform
  synthesis_initialization_seed: 203407
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_a_s3407_control
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 2
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 3407
  reset_rng_after_init: true
  fail_on_nonfinite: true
```

<!-- experiment:champion6_a_s3407_control:end -->
<!-- experiment:champion6_b_s3407_fourier_gru:start -->
## champion6_b_s3407_fourier_gru

- Status: `complete`
- Updated (UTC): `2026-11-05T11:37:02.677393+00:00`
- Git commit: `81f2d16acb86037c45a1342b79ec6e8b41e2ff28`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_b_s3407_fourier_gru`
- Note: 500000-step GRU/Fourier scratch study complete; fixed endpoint checkpoint evaluated; 2400bps, 10ms frames, <=30ms lookahead; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_b_s3407_fourier_gru/rvq_diagnostics.json
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_b_s3407_fourier_gru/checkpoints/last.pt`
- Checkpoint SHA-256: `c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23`
- Selected checkpoint global step: `500000`
- Initialization: genuinely untrained (`trained=false`, `global_step=0`), seed/data-order3407; `runs/champion6_setup/step0_b_s3407_fourier_gru.pt` SHA256 `7c7c5356252a747892bd153f8a17c609506f6998d31947d0ad706f59b85d4aa7`; no resume or learned parent.
- Pair source: `runs/champion6_setup/source_step0_seed3407.pt`, SHA256 `0537e2b716e6f2d649c3b69b875d805372ecb2f8eebba0411319911299353e95`; shared encoder/TCN/RVQ/discriminator verified; new synthesis/GRU seed203407 (GRU internally+1).
- Data/config/training/bitstream evidence: [CHAMPION6_RESULTS.audit](CHAMPION6_RESULTS.audit), cell `b_s3407_fourier_gru`; manifest counts/hashes and fixed200 audio hashes in the same audit, matching [CHAMPION6_SETUP.audit](CHAMPION6_SETUP.audit).
- Registered interpretation: score51.624336 passes numeric candidate/component gates versus own control/v2, but own control gate failed; not a clean confirmation or promotion. See [CHAMPION6_RESULTS.md](CHAMPION6_RESULTS.md).

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.440534 |
| Reconstruction loss | 0.125832 |
| Waveform L1 | 0.012957 |
| Spectral loss | 0.112875 |
| Commitment loss | 0.072601 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.2237 |
| ESTOI | 0.7684 |
| SI-SNR (dB) | 6.6003 |
| UTMOS | 3.1278 |
| Course objective score | 51.6243 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_b_s3407_fourier_gru
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 2
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 3407
  reset_rng_after_init: true
  fail_on_nonfinite: true
```

<!-- experiment:champion6_b_s3407_fourier_gru:end -->

<!-- experiment:champion6_c_s8128_control:start -->
## champion6_c_s8128_control

- Status: `complete`
- Updated (UTC): `2026-11-05T14:50:27.163049+00:00`
- Git commit: `81f2d16acb86037c45a1342b79ec6e8b41e2ff28`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_c_s8128_control`
- Note: 500000-step GRU/Fourier scratch study complete; fixed endpoint checkpoint evaluated; 2400bps, 10ms frames, <=30ms lookahead; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_c_s8128_control/rvq_diagnostics.json
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_c_s8128_control/checkpoints/last.pt`
- Checkpoint SHA-256: `d1af4d0fd2e8cb91e1800c4afee364839d2069db93e2632b555d637c377bbf81`
- Selected checkpoint global step: `500000`
- Initialization: genuinely untrained (`trained=false`, `global_step=0`), seed/data-order8128; `runs/champion6_setup/step0_c_s8128_control.pt` SHA256 `9a9a26782b70011cb4b88da3102a557596dce0daf46b6235777f334afa7992ee`; no resume or learned parent.
- Pair source: `runs/champion6_setup/source_step0_seed8128.pt`, SHA256 `c90622c4a6096a1afc72f815c01c271dc62be1b9cfe6c25d217db904b8f392ed`.
- Data/config/training/bitstream evidence: [CHAMPION6_RESULTS.audit](CHAMPION6_RESULTS.audit), cell `c_s8128_control`; manifest counts/hashes and fixed200 audio hashes in the same audit, matching [CHAMPION6_SETUP.audit](CHAMPION6_SETUP.audit).
- Registered interpretation: score46.376849 passes46.25 control gate, but cannot replace failed3407 control. See [CHAMPION6_RESULTS.md](CHAMPION6_RESULTS.md).

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.571473 |
| Reconstruction loss | 0.131643 |
| Waveform L1 | 0.013860 |
| Spectral loss | 0.117783 |
| Commitment loss | 0.122655 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9686 |
| ESTOI | 0.7281 |
| SI-SNR (dB) | 5.7939 |
| UTMOS | 2.8214 |
| Course objective score | 46.3768 |

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
  encoder_gru: false
  synthesis_type: waveform
  synthesis_initialization_seed: 208128
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_c_s8128_control
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 2
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 8128
  reset_rng_after_init: true
  fail_on_nonfinite: true
```

<!-- experiment:champion6_c_s8128_control:end -->
<!-- experiment:champion6_d_s8128_fourier_gru:start -->
## champion6_d_s8128_fourier_gru

- Status: `complete`
- Updated (UTC): `2026-11-05T11:36:59.625580+00:00`
- Git commit: `81f2d16acb86037c45a1342b79ec6e8b41e2ff28`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_d_s8128_fourier_gru`
- Note: 500000-step GRU/Fourier scratch study complete; fixed endpoint checkpoint evaluated; 2400bps, 10ms frames, <=30ms lookahead; diagnostics: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_d_s8128_fourier_gru/rvq_diagnostics.json
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_d_s8128_fourier_gru/checkpoints/last.pt`
- Checkpoint SHA-256: `1dc5ab61dde98b8e281d7168418331eb97233c63a90ec5ead14f138dd9296586`
- Selected checkpoint global step: `500000`
- Initialization: genuinely untrained (`trained=false`, `global_step=0`), seed/data-order8128; `runs/champion6_setup/step0_d_s8128_fourier_gru.pt` SHA256 `c8c12013ffa60ffb0811d05ad684ea973d042c0a7d42923c000cae000aae3763`; no resume or learned parent.
- Pair source: `runs/champion6_setup/source_step0_seed8128.pt`, SHA256 `c90622c4a6096a1afc72f815c01c271dc62be1b9cfe6c25d217db904b8f392ed`; shared encoder/TCN/RVQ/discriminator verified; new synthesis/GRU seed208128 (GRU internally+1).
- Data/config/training/bitstream evidence: [CHAMPION6_RESULTS.audit](CHAMPION6_RESULTS.audit), cell `d_s8128_fourier_gru`; manifest counts/hashes and fixed200 audio hashes in the same audit, matching [CHAMPION6_SETUP.audit](CHAMPION6_SETUP.audit).
- Registered interpretation: score50.968929 passes numeric candidate/component gates versus own control/v2 and this pair passes; whole batch still fails the other control gate. See [CHAMPION6_RESULTS.md](CHAMPION6_RESULTS.md).

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.422288 |
| Reconstruction loss | 0.126524 |
| Waveform L1 | 0.012934 |
| Spectral loss | 0.113590 |
| Commitment loss | 0.073616 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1981 |
| ESTOI | 0.7630 |
| SI-SNR (dB) | 6.6440 |
| UTMOS | 3.0695 |
| Course objective score | 50.9689 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 208128
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_d_s8128_fourier_gru
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 2
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 8128
  reset_rng_after_init: true
  fail_on_nonfinite: true
```

<!-- experiment:champion6_d_s8128_fourier_gru:end -->

<!-- experiment:champion7_a_continue:start -->
## champion7_a_continue

- Status: `complete`
- Updated (UTC): `2026-11-07T05:48:16.603155+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_a_continue/lineage.json; CHAMPION7_SETUP.audit. Selected extra step100000 by actual score; gain_vs_parent=-0.09843294.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue/checkpoints/step_00100000.pt`
- Checkpoint SHA-256: `8dcebc6cdf298ef29c420c3d09be66e9f2b995e27eb76176b62caf8ba924313a`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.469501 |
| Reconstruction loss | 0.125660 |
| Waveform L1 | 0.013052 |
| Spectral loss | 0.112608 |
| Commitment loss | 0.079991 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.2005 |
| ESTOI | 0.7704 |
| SI-SNR (dB) | 6.5785 |
| UTMOS | 3.1329 |
| Course objective score | 51.5259 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_a_continue:end -->

<!-- experiment:champion7_b_si:start -->
## champion7_b_si

- Status: `complete`
- Updated (UTC): `2026-11-07T05:48:18.803851+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_b_si/lineage.json; CHAMPION7_SETUP.audit. Selected extra step100000 by actual score; gain_vs_parent=-0.09304863.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si/checkpoints/step_00100000.pt`
- Checkpoint SHA-256: `8741b75536892152d09adb176ec1a0db6c345496b499443c092051ca24d9b3f4`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.455244 |
| Reconstruction loss | 0.125469 |
| Waveform L1 | 0.012688 |
| Spectral loss | 0.112781 |
| Commitment loss | 0.102146 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.2151 |
| ESTOI | 0.7646 |
| SI-SNR (dB) | 6.9109 |
| UTMOS | 3.1069 |
| Course objective score | 51.5313 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_b_si:end -->

<!-- experiment:champion7_c_gan:start -->
## champion7_c_gan

- Status: `complete`
- Updated (UTC): `2026-11-07T06:57:50.359625+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_c_gan/lineage.json; CHAMPION7_SETUP.audit. Selected extra step75000 by actual score; gain_vs_parent=-1.37816310.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan/checkpoints/step_00075000.pt`
- Checkpoint SHA-256: `48c7867aac73c9c8ab57f7ac699b970c039dc29f993f7812c4f8e8be55a256e0`
- Selected checkpoint global step: `75000`

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
| Train loss | 0.485958 |
| Reconstruction loss | 0.129084 |
| Waveform L1 | 0.013357 |
| Spectral loss | 0.115727 |
| Commitment loss | 0.077357 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1265 |
| ESTOI | 0.7581 |
| SI-SNR (dB) | 6.4163 |
| UTMOS | 3.0781 |
| Course objective score | 50.2462 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_c_gan:end -->
<!-- experiment:champion7_d_both:start -->
## champion7_d_both

- Status: `complete`
- Updated (UTC): `2026-11-07T06:56:14.527905+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_d_both/lineage.json; CHAMPION7_SETUP.audit. Selected extra step100000 by actual score; gain_vs_parent=-1.62288422.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both/checkpoints/step_00100000.pt`
- Checkpoint SHA-256: `1a02193091eb6a891302bb6d2851d3b77731e178aaf3cd10108fb31686ffd7fc`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.473779 |
| Reconstruction loss | 0.128279 |
| Waveform L1 | 0.012959 |
| Spectral loss | 0.115320 |
| Commitment loss | 0.101043 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1168 |
| ESTOI | 0.7529 |
| SI-SNR (dB) | 6.7227 |
| UTMOS | 3.0401 |
| Course objective score | 50.0015 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  feature_matching_weight: 1.5
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_d_both:end -->
<!-- experiment:champion7_a_continue_step025000:start -->
## champion7_a_continue_step025000

- Status: `complete`
- Updated (UTC): `2026-11-07T05:43:51.917626+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_a_continue/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step25000, cumulative parent+stage=525000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue/checkpoints/step_00025000.pt`
- Checkpoint SHA-256: `68483342fdc2c4d4a036b36920d49900dcb2832d092610023508b894805203de`
- Selected checkpoint global step: `25000`

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
| Train loss | 0.469501 |
| Reconstruction loss | 0.125660 |
| Waveform L1 | 0.013052 |
| Spectral loss | 0.112608 |
| Commitment loss | 0.079991 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1843 |
| ESTOI | 0.7666 |
| SI-SNR (dB) | 6.5066 |
| UTMOS | 3.1022 |
| Course objective score | 51.0801 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_a_continue_step025000:end -->

<!-- experiment:champion7_b_si_step025000:start -->
## champion7_b_si_step025000

- Status: `complete`
- Updated (UTC): `2026-11-07T05:43:54.405086+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_b_si/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step25000, cumulative parent+stage=525000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si/checkpoints/step_00025000.pt`
- Checkpoint SHA-256: `42e906f38290e62ef3b56a6ca44ed52a11acab2bc3e3ca490a9c5ea2781a5986`
- Selected checkpoint global step: `25000`

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
| Train loss | 0.455244 |
| Reconstruction loss | 0.125469 |
| Waveform L1 | 0.012688 |
| Spectral loss | 0.112781 |
| Commitment loss | 0.102146 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1633 |
| ESTOI | 0.7606 |
| SI-SNR (dB) | 6.8956 |
| UTMOS | 3.0583 |
| Course objective score | 50.7469 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_b_si_step025000:end -->

<!-- experiment:champion7_a_continue_step050000:start -->
## champion7_a_continue_step050000

- Status: `complete`
- Updated (UTC): `2026-11-07T05:45:11.911542+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_a_continue/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step50000, cumulative parent+stage=550000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue/checkpoints/step_00050000.pt`
- Checkpoint SHA-256: `1076e462239a8984438e0b21ba38c9d9cf0ebc2e924a42802bbabb84272acac8`
- Selected checkpoint global step: `50000`

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
| Train loss | 0.469501 |
| Reconstruction loss | 0.125660 |
| Waveform L1 | 0.013052 |
| Spectral loss | 0.112608 |
| Commitment loss | 0.079991 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1828 |
| ESTOI | 0.7666 |
| SI-SNR (dB) | 6.5794 |
| UTMOS | 3.1182 |
| Course objective score | 51.2138 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_a_continue_step050000:end -->

<!-- experiment:champion7_b_si_step050000:start -->
## champion7_b_si_step050000

- Status: `complete`
- Updated (UTC): `2026-11-07T05:45:14.232712+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_b_si/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step50000, cumulative parent+stage=550000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si/checkpoints/step_00050000.pt`
- Checkpoint SHA-256: `5ea5347b6a769e427de6c62008d15a0a54be4a0b2de8530c793f43066dc3134d`
- Selected checkpoint global step: `50000`

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
| Train loss | 0.455244 |
| Reconstruction loss | 0.125469 |
| Waveform L1 | 0.012688 |
| Spectral loss | 0.112781 |
| Commitment loss | 0.102146 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1775 |
| ESTOI | 0.7618 |
| SI-SNR (dB) | 6.8597 |
| UTMOS | 3.0652 |
| Course objective score | 50.8998 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_b_si_step050000:end -->

<!-- experiment:champion7_a_continue_step075000:start -->
## champion7_a_continue_step075000

- Status: `complete`
- Updated (UTC): `2026-11-07T05:46:32.533115+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_a_continue/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step75000, cumulative parent+stage=575000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue/checkpoints/step_00075000.pt`
- Checkpoint SHA-256: `d08b19e36f5a9ed7661fad466f577eba64bad28b3eef73a3b5da8c04254337e7`
- Selected checkpoint global step: `75000`

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
| Train loss | 0.469501 |
| Reconstruction loss | 0.125660 |
| Waveform L1 | 0.013052 |
| Spectral loss | 0.112608 |
| Commitment loss | 0.079991 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1864 |
| ESTOI | 0.7678 |
| SI-SNR (dB) | 6.5142 |
| UTMOS | 3.0950 |
| Course objective score | 51.0853 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_a_continue_step075000:end -->

<!-- experiment:champion7_b_si_step075000:start -->
## champion7_b_si_step075000

- Status: `complete`
- Updated (UTC): `2026-11-07T05:46:34.831873+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_b_si/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step75000, cumulative parent+stage=575000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si/checkpoints/step_00075000.pt`
- Checkpoint SHA-256: `8a5e142c4ab94f1a087a9f4863eba9c172c277909a4298976dd2b9485e4649c9`
- Selected checkpoint global step: `75000`

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
| Train loss | 0.455244 |
| Reconstruction loss | 0.125469 |
| Waveform L1 | 0.012688 |
| Spectral loss | 0.112781 |
| Commitment loss | 0.102146 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1985 |
| ESTOI | 0.7636 |
| SI-SNR (dB) | 6.8021 |
| UTMOS | 3.0770 |
| Course objective score | 51.1328 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_b_si_step075000:end -->

<!-- experiment:champion7_a_continue_step100000:start -->
## champion7_a_continue_step100000

- Status: `complete`
- Updated (UTC): `2026-11-07T05:47:53.704690+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_a_continue/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step100000, cumulative parent+stage=600000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue/checkpoints/step_00100000.pt`
- Checkpoint SHA-256: `8dcebc6cdf298ef29c420c3d09be66e9f2b995e27eb76176b62caf8ba924313a`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.469501 |
| Reconstruction loss | 0.125660 |
| Waveform L1 | 0.013052 |
| Spectral loss | 0.112608 |
| Commitment loss | 0.079991 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.2005 |
| ESTOI | 0.7704 |
| SI-SNR (dB) | 6.5785 |
| UTMOS | 3.1329 |
| Course objective score | 51.5259 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_a_continue
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_a_continue_step100000:end -->

<!-- experiment:champion7_b_si_step100000:start -->
## champion7_b_si_step100000

- Status: `complete`
- Updated (UTC): `2026-11-07T05:47:56.186092+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_b_si/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step100000, cumulative parent+stage=600000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si/checkpoints/step_00100000.pt`
- Checkpoint SHA-256: `8741b75536892152d09adb176ec1a0db6c345496b499443c092051ca24d9b3f4`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.455244 |
| Reconstruction loss | 0.125469 |
| Waveform L1 | 0.012688 |
| Spectral loss | 0.112781 |
| Commitment loss | 0.102146 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.2151 |
| ESTOI | 0.7646 |
| SI-SNR (dB) | 6.9109 |
| UTMOS | 3.1069 |
| Course objective score | 51.5313 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_b_si_step100000:end -->

<!-- experiment:champion7_d_both_step025000:start -->
## champion7_d_both_step025000

- Status: `complete`
- Updated (UTC): `2026-11-07T06:51:56.711097+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_d_both/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step25000, cumulative parent+stage=525000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both/checkpoints/step_00025000.pt`
- Checkpoint SHA-256: `b254d293a90971330b60da6b51070a5f9cabcca440a75b4ea85813df1b5eb748`
- Selected checkpoint global step: `25000`

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
| Train loss | 0.473779 |
| Reconstruction loss | 0.128279 |
| Waveform L1 | 0.012959 |
| Spectral loss | 0.115320 |
| Commitment loss | 0.101043 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0992 |
| ESTOI | 0.7478 |
| SI-SNR (dB) | 6.6975 |
| UTMOS | 2.9795 |
| Course objective score | 49.3556 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  feature_matching_weight: 1.5
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_d_both_step025000:end -->

<!-- experiment:champion7_d_both_step050000:start -->
## champion7_d_both_step050000

- Status: `complete`
- Updated (UTC): `2026-11-07T06:53:16.343217+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_d_both/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step50000, cumulative parent+stage=550000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both/checkpoints/step_00050000.pt`
- Checkpoint SHA-256: `996e4e658c515c11b9492e08e8c8b4aac6b29bd2f50df212085ca97bcd31a08f`
- Selected checkpoint global step: `50000`

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
| Train loss | 0.473779 |
| Reconstruction loss | 0.128279 |
| Waveform L1 | 0.012959 |
| Spectral loss | 0.115320 |
| Commitment loss | 0.101043 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1035 |
| ESTOI | 0.7526 |
| SI-SNR (dB) | 6.6680 |
| UTMOS | 3.0099 |
| Course objective score | 49.6771 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  feature_matching_weight: 1.5
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_d_both_step050000:end -->

<!-- experiment:champion7_c_gan_step025000:start -->
## champion7_c_gan_step025000

- Status: `complete`
- Updated (UTC): `2026-11-07T06:53:34.149497+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_c_gan/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step25000, cumulative parent+stage=525000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan/checkpoints/step_00025000.pt`
- Checkpoint SHA-256: `fe1bed31ce31e60549c835f7d749425881482bb72b140e4d46dd26f20556aa2c`
- Selected checkpoint global step: `25000`

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
| Train loss | 0.485958 |
| Reconstruction loss | 0.129084 |
| Waveform L1 | 0.013357 |
| Spectral loss | 0.115727 |
| Commitment loss | 0.077357 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1034 |
| ESTOI | 0.7551 |
| SI-SNR (dB) | 6.3030 |
| UTMOS | 3.0314 |
| Course objective score | 49.6449 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_c_gan_step025000:end -->

<!-- experiment:champion7_d_both_step075000:start -->
## champion7_d_both_step075000

- Status: `complete`
- Updated (UTC): `2026-11-07T06:54:34.739151+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_d_both/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step75000, cumulative parent+stage=575000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both/checkpoints/step_00075000.pt`
- Checkpoint SHA-256: `28e9f458f663d47576cf38b48856d3ff2cfe52b9a84b9c372e1bf57cfc843388`
- Selected checkpoint global step: `75000`

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
| Train loss | 0.473779 |
| Reconstruction loss | 0.128279 |
| Waveform L1 | 0.012959 |
| Spectral loss | 0.115320 |
| Commitment loss | 0.101043 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1234 |
| ESTOI | 0.7542 |
| SI-SNR (dB) | 6.7228 |
| UTMOS | 3.0150 |
| Course objective score | 49.9238 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  feature_matching_weight: 1.5
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_d_both_step075000:end -->

<!-- experiment:champion7_c_gan_step050000:start -->
## champion7_c_gan_step050000

- Status: `complete`
- Updated (UTC): `2026-11-07T06:54:53.689043+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_c_gan/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step50000, cumulative parent+stage=550000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan/checkpoints/step_00050000.pt`
- Checkpoint SHA-256: `2f28d20db0db628d91133038880e3407a497a5a40074ab76a2efebbf27ec5898`
- Selected checkpoint global step: `50000`

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
| Train loss | 0.485958 |
| Reconstruction loss | 0.129084 |
| Waveform L1 | 0.013357 |
| Spectral loss | 0.115727 |
| Commitment loss | 0.077357 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0831 |
| ESTOI | 0.7568 |
| SI-SNR (dB) | 6.2949 |
| UTMOS | 3.0319 |
| Course objective score | 49.5407 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_c_gan_step050000:end -->

<!-- experiment:champion7_d_both_step100000:start -->
## champion7_d_both_step100000

- Status: `complete`
- Updated (UTC): `2026-11-07T06:55:55.529909+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_d_both/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step100000, cumulative parent+stage=600000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both/checkpoints/step_00100000.pt`
- Checkpoint SHA-256: `1a02193091eb6a891302bb6d2851d3b77731e178aaf3cd10108fb31686ffd7fc`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.473779 |
| Reconstruction loss | 0.128279 |
| Waveform L1 | 0.012959 |
| Spectral loss | 0.115320 |
| Commitment loss | 0.101043 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1168 |
| ESTOI | 0.7529 |
| SI-SNR (dB) | 6.7227 |
| UTMOS | 3.0401 |
| Course objective score | 50.0015 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  feature_matching_weight: 1.5
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_d_both
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_d_both_step100000:end -->

<!-- experiment:champion7_c_gan_step075000:start -->
## champion7_c_gan_step075000

- Status: `complete`
- Updated (UTC): `2026-11-07T06:56:11.681302+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_c_gan/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step75000, cumulative parent+stage=575000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan/checkpoints/step_00075000.pt`
- Checkpoint SHA-256: `48c7867aac73c9c8ab57f7ac699b970c039dc29f993f7812c4f8e8be55a256e0`
- Selected checkpoint global step: `75000`

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
| Train loss | 0.485958 |
| Reconstruction loss | 0.129084 |
| Waveform L1 | 0.013357 |
| Spectral loss | 0.115727 |
| Commitment loss | 0.077357 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1265 |
| ESTOI | 0.7581 |
| SI-SNR (dB) | 6.4163 |
| UTMOS | 3.0781 |
| Course objective score | 50.2462 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_c_gan_step075000:end -->

<!-- experiment:champion7_c_gan_step100000:start -->
## champion7_c_gan_step100000

- Status: `complete`
- Updated (UTC): `2026-11-07T06:57:31.887410+00:00`
- Git commit: `4f724acc8447771d8902c54672edcf42adb77f6d`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan`
- Note: Exploratory learned-parent fine-tuning, NOT scratch; parent CHAMPION6 B500k score51.624336 SHA256 c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23; inherit all codec/RVQ EMA/discriminator, reset optimizers; extra100k; select by fixed200 score among declared25k/50k/75k/100k, not reconstruction-best. Lineage runs/champion7_c_gan/lineage.json; CHAMPION7_SETUP.audit. This searched endpoint extra step100000, cumulative parent+stage=600000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan/checkpoints/step_00100000.pt`
- Checkpoint SHA-256: `75ef0c38cbf2e689e17e3cc8c0a6cda7e35036970544e2234b7a6d1505a178ca`
- Selected checkpoint global step: `100000`

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
| Train loss | 0.485958 |
| Reconstruction loss | 0.129084 |
| Waveform L1 | 0.013357 |
| Spectral loss | 0.115727 |
| Commitment loss | 0.077357 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1250 |
| ESTOI | 0.7587 |
| SI-SNR (dB) | 6.3741 |
| UTMOS | 3.0763 |
| Course objective score | 50.2142 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_c_gan
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion7_c_gan_step100000:end -->

<!-- experiment:champion8_c_from_b10:start -->
## champion8_c_from_b10

- Status: `complete`
- Updated (UTC): `2026-11-08T01:26:45.788841+00:00`
- Git commit: `814cac8e62fe252b62dcc6cc020c7a648d1a68fe`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_c_from_b10`
- Note: Posthoc decoder-parameter interpolation, ZERO new training, NOT untrained initialization. alpha=0.1; parent500k51.624336 and donor C7local100k/cumulative600k. All encoder/latent/RVQ input+output projections/codebooks/EMA/buffers bitwise parent; no optimizer or discriminator in inference-only export. Four registered dev-search candidates only. CHAMPION8_PLAN.md/SETUP.audit; source SHAs in lineage.json. No runtime resource guard per user. Gain_vs_parent=+0.0427304014.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_c_from_b10/checkpoints/interpolated.pt`
- Checkpoint SHA-256: `a5cffa2dfcf39fc69b36b84e8ca238e7cbd9408ee008a1042bb7bbb253e4eb19`
- Selected checkpoint global step: `0`

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
| PESQ-WB | 2.2277 |
| ESTOI | 0.7684 |
| SI-SNR (dB) | 6.6201 |
| UTMOS | 3.1280 |
| Course objective score | 51.6671 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_c_from_b10
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
posthoc_interpolation:
  donor_label: b
  alpha: 0.1
  new_gradient_updates: 0
  frozen_encoder_and_entire_rvq: true
  interpolate_parameters_only: true
```

<!-- experiment:champion8_c_from_b10:end -->

<!-- experiment:champion8_d_from_b25:start -->
## champion8_d_from_b25

- Status: `complete`
- Updated (UTC): `2026-11-08T01:26:47.869976+00:00`
- Git commit: `814cac8e62fe252b62dcc6cc020c7a648d1a68fe`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_d_from_b25`
- Note: Posthoc decoder-parameter interpolation, ZERO new training, NOT untrained initialization. alpha=0.25; parent500k51.624336 and donor C7local100k/cumulative600k. All encoder/latent/RVQ input+output projections/codebooks/EMA/buffers bitwise parent; no optimizer or discriminator in inference-only export. Four registered dev-search candidates only. CHAMPION8_PLAN.md/SETUP.audit; source SHAs in lineage.json. No runtime resource guard per user. Gain_vs_parent=-0.0824572985.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_d_from_b25/checkpoints/interpolated.pt`
- Checkpoint SHA-256: `18849eecc133201481629ffed304d33244d8c6dc02c80e04f7c5c680ae571e53`
- Selected checkpoint global step: `0`

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
| PESQ-WB | 2.2193 |
| ESTOI | 0.7674 |
| SI-SNR (dB) | 6.6225 |
| UTMOS | 3.1214 |
| Course objective score | 51.5419 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_d_from_b25
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
posthoc_interpolation:
  donor_label: b
  alpha: 0.25
  new_gradient_updates: 0
  frozen_encoder_and_entire_rvq: true
  interpolate_parameters_only: true
```

<!-- experiment:champion8_d_from_b25:end -->

<!-- experiment:champion8_a_from_a10:start -->
## champion8_a_from_a10

- Status: `complete`
- Updated (UTC): `2026-11-08T01:26:50.009838+00:00`
- Git commit: `814cac8e62fe252b62dcc6cc020c7a648d1a68fe`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_a_from_a10`
- Note: Posthoc decoder-parameter interpolation, ZERO new training, NOT untrained initialization. alpha=0.1; parent500k51.624336 and donor C7local100k/cumulative600k. All encoder/latent/RVQ input+output projections/codebooks/EMA/buffers bitwise parent; no optimizer or discriminator in inference-only export. Four registered dev-search candidates only. CHAMPION8_PLAN.md/SETUP.audit; source SHAs in lineage.json. No runtime resource guard per user. Gain_vs_parent=+0.0424987694.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_a_from_a10/checkpoints/interpolated.pt`
- Checkpoint SHA-256: `72779adf5b86e7df626b47c0eb96e76d16b30cc4bdbddd5e30e3fd753ec68433`
- Selected checkpoint global step: `0`

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
| PESQ-WB | 2.2278 |
| ESTOI | 0.7686 |
| SI-SNR (dB) | 6.6224 |
| UTMOS | 3.1269 |
| Course objective score | 51.6668 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_a_from_a10
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
posthoc_interpolation:
  donor_label: a
  alpha: 0.1
  new_gradient_updates: 0
  frozen_encoder_and_entire_rvq: true
  interpolate_parameters_only: true
```

<!-- experiment:champion8_a_from_a10:end -->

<!-- experiment:champion8_b_from_a25:start -->
## champion8_b_from_a25

- Status: `complete`
- Updated (UTC): `2026-11-08T01:26:52.069190+00:00`
- Git commit: `814cac8e62fe252b62dcc6cc020c7a648d1a68fe`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_b_from_a25`
- Note: Posthoc decoder-parameter interpolation, ZERO new training, NOT untrained initialization. alpha=0.25; parent500k51.624336 and donor C7local100k/cumulative600k. All encoder/latent/RVQ input+output projections/codebooks/EMA/buffers bitwise parent; no optimizer or discriminator in inference-only export. Four registered dev-search candidates only. CHAMPION8_PLAN.md/SETUP.audit; source SHAs in lineage.json. No runtime resource guard per user. Gain_vs_parent=-0.0330543966.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_b_from_a25/checkpoints/interpolated.pt`
- Checkpoint SHA-256: `aed4aaa90d6e3f6cc5d72fca60d99d6008c6803402a8ffab4ab271b462ccb558`
- Selected checkpoint global step: `0`

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
| PESQ-WB | 2.2248 |
| ESTOI | 0.7680 |
| SI-SNR (dB) | 6.6336 |
| UTMOS | 3.1194 |
| Course objective score | 51.5913 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 30 |
| Total MFLOP/s | 666.307 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1868064 |

### Effective configuration

```yaml
seed: 20261106
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 203407
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
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
  learning_rate: 5.0e-05
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_b_from_a25
  minimum_learning_rate: 1.0e-05
  warmup_steps: 1000
  checkpoint_keep_last: 4
  quantizer_learning_rate: 5.0e-05
  quantizer_only_steps: 0
  data_order_seed: 20261106
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
posthoc_interpolation:
  donor_label: a
  alpha: 0.25
  new_gradient_updates: 0
  frozen_encoder_and_entire_rvq: true
  interpolate_parameters_only: true
```

<!-- experiment:champion8_b_from_a25:end -->

<!-- experiment:champion9_a_g4_d0:start -->
## champion9_a_g4_d0

- Status: `complete`
- Updated (UTC): `2026-11-09T15:57:08.628615+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0`
- Note: CHAMPION9 scratch, no learned parent. groups4/decoderTCN0; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA1a97674af58af9b361ada1895dff6d9f04d1e0b7b254e708f2a98255e439f924; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Selectedstep500000;delta_vs51.667066=-3.7276227105.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0/checkpoints/step_00500000.pt`
- Checkpoint SHA-256: `84e2ae9ca427d2c0fe2bfd198ccafce93d0f5783a0113f05eda427264c4107c7`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.463134 |
| Reconstruction loss | 0.133255 |
| Waveform L1 | 0.013212 |
| Spectral loss | 0.120043 |
| Commitment loss | 0.078645 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0810 |
| ESTOI | 0.7421 |
| SI-SNR (dB) | 6.4744 |
| UTMOS | 2.8191 |
| Course objective score | 47.9394 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 540.954 |
| Decoder MFLOP/s | 236.960 |
| Parameters | 1548960 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
  decoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 4
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_a_g4_d0:end -->
<!-- experiment:champion9_b_g8_d0:start -->
## champion9_b_g8_d0

- Status: `complete`
- Updated (UTC): `2026-11-09T14:01:40.727114+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0`
- Note: CHAMPION9 scratch, no learned parent. groups8/decoderTCN0; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA7188179004a7c1035bd68bc22338c425b7cc5ceedea68c44f6bcace204635f4c; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Selectedstep500000;delta_vs51.667066=-3.0430566613.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0/checkpoints/step_00500000.pt`
- Checkpoint SHA-256: `7f42b0583d17dee046c1effe2e3041f468ec4bff2d7084cb6768ae46c7b87e10`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.477270 |
| Reconstruction loss | 0.132907 |
| Waveform L1 | 0.013372 |
| Spectral loss | 0.119534 |
| Commitment loss | 0.096261 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1049 |
| ESTOI | 0.7505 |
| SI-SNR (dB) | 6.3514 |
| UTMOS | 2.8801 |
| Course objective score | 48.6240 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 524.826 |
| Decoder MFLOP/s | 236.960 |
| Parameters | 1542840 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
  decoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 8
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_b_g8_d0:end -->

<!-- experiment:champion9_c_g4_d2:start -->
## champion9_c_g4_d2

- Status: `complete`
- Updated (UTC): `2026-11-09T15:34:35.815525+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2`
- Note: CHAMPION9 scratch, no learned parent. groups4/decoderTCN2; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA71a15c2160c634c4ac44f2f9dfe32984cf4062e69005087c356ddc7e405bf4c6; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Selectedstep500000;delta_vs51.667066=-2.3488610430.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2/checkpoints/step_00500000.pt`
- Checkpoint SHA-256: `4925e325195dc480663cea2717a64dae4de23dfd2f9699768e9c956ba7f05e5f`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.471242 |
| Reconstruction loss | 0.131994 |
| Waveform L1 | 0.013289 |
| Spectral loss | 0.118705 |
| Commitment loss | 0.093823 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1428 |
| ESTOI | 0.7514 |
| SI-SNR (dB) | 6.4946 |
| UTMOS | 2.9297 |
| Course objective score | 49.3182 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 561.626 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1653280 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 4
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_c_g4_d2:end -->
<!-- experiment:champion9_d_g8_d2:start -->
## champion9_d_g8_d2

- Status: `complete`
- Updated (UTC): `2026-11-09T14:01:37.832729+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2`
- Note: CHAMPION9 scratch, no learned parent. groups8/decoderTCN2; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA8359bd16760cec323ae11ab0f5712725abbcbe734a57a0a75e45c695d05ffc61; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Selectedstep500000;delta_vs51.667066=-1.9560858310.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2/checkpoints/step_00500000.pt`
- Checkpoint SHA-256: `82e924efe948c517f4c74d2abeb0e93b4aed8ee6d01aabf01c572ef496aaf4a0`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.471913 |
| Reconstruction loss | 0.130120 |
| Waveform L1 | 0.013245 |
| Spectral loss | 0.116875 |
| Commitment loss | 0.083726 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1520 |
| ESTOI | 0.7551 |
| SI-SNR (dB) | 6.3332 |
| UTMOS | 2.9836 |
| Course objective score | 49.7110 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 545.498 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1647160 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 8
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_d_g8_d2:end -->
<!-- experiment:champion9_d_g8_d2_step250000:start -->
## champion9_d_g8_d2_step250000

- Status: `complete`
- Updated (UTC): `2026-11-09T13:59:57.643785+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2`
- Note: CHAMPION9 scratch, no learned parent. groups8/decoderTCN2; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA8359bd16760cec323ae11ab0f5712725abbcbe734a57a0a75e45c695d05ffc61; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Declared searched scratch endpoint250000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2/checkpoints/step_00250000.pt`
- Checkpoint SHA-256: `b919fcbd3b34d36b0d77a82af031694ef8c628eca5b83936a267861773bbc0b7`
- Selected checkpoint global step: `250000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.471913 |
| Reconstruction loss | 0.130120 |
| Waveform L1 | 0.013245 |
| Spectral loss | 0.116875 |
| Commitment loss | 0.083726 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0366 |
| ESTOI | 0.7443 |
| SI-SNR (dB) | 6.1897 |
| UTMOS | 2.8019 |
| Course objective score | 47.3926 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 545.498 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1647160 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 8
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_d_g8_d2_step250000:end -->

<!-- experiment:champion9_b_g8_d0_step250000:start -->
## champion9_b_g8_d0_step250000

- Status: `complete`
- Updated (UTC): `2026-11-09T14:00:00.074480+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0`
- Note: CHAMPION9 scratch, no learned parent. groups8/decoderTCN0; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA7188179004a7c1035bd68bc22338c425b7cc5ceedea68c44f6bcace204635f4c; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Declared searched scratch endpoint250000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0/checkpoints/step_00250000.pt`
- Checkpoint SHA-256: `44a1ba9fc300f560ba6f4453971b014baca405a3ec281019e2a923dd5984e475`
- Selected checkpoint global step: `250000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.477270 |
| Reconstruction loss | 0.132907 |
| Waveform L1 | 0.013372 |
| Spectral loss | 0.119534 |
| Commitment loss | 0.096261 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0099 |
| ESTOI | 0.7380 |
| SI-SNR (dB) | 6.1913 |
| UTMOS | 2.7152 |
| Course objective score | 46.5027 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 524.826 |
| Decoder MFLOP/s | 236.960 |
| Parameters | 1542840 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
  decoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 8
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_b_g8_d0_step250000:end -->

<!-- experiment:champion9_d_g8_d2_step500000:start -->
## champion9_d_g8_d2_step500000

- Status: `complete`
- Updated (UTC): `2026-11-09T14:01:16.954195+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2`
- Note: CHAMPION9 scratch, no learned parent. groups8/decoderTCN2; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA8359bd16760cec323ae11ab0f5712725abbcbe734a57a0a75e45c695d05ffc61; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Declared searched scratch endpoint500000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2/checkpoints/step_00500000.pt`
- Checkpoint SHA-256: `82e924efe948c517f4c74d2abeb0e93b4aed8ee6d01aabf01c572ef496aaf4a0`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.471913 |
| Reconstruction loss | 0.130120 |
| Waveform L1 | 0.013245 |
| Spectral loss | 0.116875 |
| Commitment loss | 0.083726 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1520 |
| ESTOI | 0.7551 |
| SI-SNR (dB) | 6.3332 |
| UTMOS | 2.9836 |
| Course objective score | 49.7110 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 545.498 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1647160 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 8
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_d_g8_d2_step500000:end -->

<!-- experiment:champion9_b_g8_d0_step500000:start -->
## champion9_b_g8_d0_step500000

- Status: `complete`
- Updated (UTC): `2026-11-09T14:01:20.743306+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0`
- Note: CHAMPION9 scratch, no learned parent. groups8/decoderTCN0; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA7188179004a7c1035bd68bc22338c425b7cc5ceedea68c44f6bcace204635f4c; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Declared searched scratch endpoint500000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0/checkpoints/step_00500000.pt`
- Checkpoint SHA-256: `7f42b0583d17dee046c1effe2e3041f468ec4bff2d7084cb6768ae46c7b87e10`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.477270 |
| Reconstruction loss | 0.132907 |
| Waveform L1 | 0.013372 |
| Spectral loss | 0.119534 |
| Commitment loss | 0.096261 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1049 |
| ESTOI | 0.7505 |
| SI-SNR (dB) | 6.3514 |
| UTMOS | 2.8801 |
| Course objective score | 48.6240 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 524.826 |
| Decoder MFLOP/s | 236.960 |
| Parameters | 1542840 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
  decoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 8
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_b_g8_d0_step500000:end -->

<!-- experiment:champion9_c_g4_d2_step250000:start -->
## champion9_c_g4_d2_step250000

- Status: `complete`
- Updated (UTC): `2026-11-09T15:32:53.911043+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2`
- Note: CHAMPION9 scratch, no learned parent. groups4/decoderTCN2; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA71a15c2160c634c4ac44f2f9dfe32984cf4062e69005087c356ddc7e405bf4c6; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Declared searched scratch endpoint250000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2/checkpoints/step_00250000.pt`
- Checkpoint SHA-256: `864027dd7fa6a2061a177a72036644d2973ba933d1ad17e489a46e9a57164995`
- Selected checkpoint global step: `250000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.471242 |
| Reconstruction loss | 0.131994 |
| Waveform L1 | 0.013289 |
| Spectral loss | 0.118705 |
| Commitment loss | 0.093823 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0029 |
| ESTOI | 0.7401 |
| SI-SNR (dB) | 6.3703 |
| UTMOS | 2.7451 |
| Course objective score | 46.8049 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 561.626 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1653280 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 4
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_c_g4_d2_step250000:end -->

<!-- experiment:champion9_c_g4_d2_step500000:start -->
## champion9_c_g4_d2_step500000

- Status: `complete`
- Updated (UTC): `2026-11-09T15:34:15.879317+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2`
- Note: CHAMPION9 scratch, no learned parent. groups4/decoderTCN2; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA71a15c2160c634c4ac44f2f9dfe32984cf4062e69005087c356ddc7e405bf4c6; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Declared searched scratch endpoint500000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2/checkpoints/step_00500000.pt`
- Checkpoint SHA-256: `4925e325195dc480663cea2717a64dae4de23dfd2f9699768e9c956ba7f05e5f`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.471242 |
| Reconstruction loss | 0.131994 |
| Waveform L1 | 0.013289 |
| Spectral loss | 0.118705 |
| Commitment loss | 0.093823 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.1428 |
| ESTOI | 0.7514 |
| SI-SNR (dB) | 6.4946 |
| UTMOS | 2.9297 |
| Course objective score | 49.3182 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 561.626 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1653280 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 4
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_c_g4_d2_step500000:end -->

<!-- experiment:champion9_a_g4_d0_step250000:start -->
## champion9_a_g4_d0_step250000

- Status: `complete`
- Updated (UTC): `2026-11-09T15:55:23.295325+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0`
- Note: CHAMPION9 scratch, no learned parent. groups4/decoderTCN0; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA1a97674af58af9b361ada1895dff6d9f04d1e0b7b254e708f2a98255e439f924; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Declared searched scratch endpoint250000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0/checkpoints/step_00250000.pt`
- Checkpoint SHA-256: `afcf8ea257c83178e6a113de39e460238b3300e8ec8d750820724397fb3158a2`
- Selected checkpoint global step: `250000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.463134 |
| Reconstruction loss | 0.133255 |
| Waveform L1 | 0.013212 |
| Spectral loss | 0.120043 |
| Commitment loss | 0.078645 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 1.9732 |
| ESTOI | 0.7336 |
| SI-SNR (dB) | 6.3580 |
| UTMOS | 2.6308 |
| Course objective score | 45.7075 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 540.954 |
| Decoder MFLOP/s | 236.960 |
| Parameters | 1548960 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
  decoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 4
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_a_g4_d0_step250000:end -->

<!-- experiment:champion9_a_g4_d0_step500000:start -->
## champion9_a_g4_d0_step500000

- Status: `complete`
- Updated (UTC): `2026-11-09T15:56:49.323996+00:00`
- Git commit: `b2ec4c3a2016aa05804381959c27861b8052727a`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0`
- Note: CHAMPION9 scratch, no learned parent. groups4/decoderTCN0; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA1a97674af58af9b361ada1895dff6d9f04d1e0b7b254e708f2a98255e439f924; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION9_PLAN.md/SETUP.audit. Declared searched scratch endpoint500000.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0/checkpoints/step_00500000.pt`
- Checkpoint SHA-256: `84e2ae9ca427d2c0fe2bfd198ccafce93d0f5783a0113f05eda427264c4107c7`
- Selected checkpoint global step: `500000`

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
| Epoch | 41 |
| Global step | 500000 |
| Train loss | 0.463134 |
| Reconstruction loss | 0.133255 |
| Waveform L1 | 0.013212 |
| Spectral loss | 0.120043 |
| Commitment loss | 0.078645 |

### Objective evaluation

| Item | Value |
|---|---:|
| Files | 200 |
| PESQ-WB | 2.0810 |
| ESTOI | 0.7421 |
| SI-SNR (dB) | 6.4744 |
| UTMOS | 2.8191 |
| Course objective score | 47.9394 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 540.954 |
| Decoder MFLOP/s | 236.960 |
| Parameters | 1548960 |

### Effective configuration

```yaml
seed: 20261108
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
  encoder_temporal_layers: 0
  decoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461108
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 4
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261108
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion9_a_g4_d0_step500000:end -->

<!-- experiment:champion10_a_base:start -->
## champion10_a_base

- Status: `planned`
- Updated (UTC): `2026-11-10T01:59:25.493866+00:00`
- Git commit: `d662a1aedfd8d7754baedd4195b155cdb3aef168`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_a_base`
- Note: CHAMPION10 registered scratch capacity2x2, new seed20261110,500kTOTAL. Persistent supervisor queued on GPU0; startup free<8192MiB, waiting30s, NO actual optimization yet as of this queue audit. No runtime polling, no external-job stops or batch changes. See CHAMPION10_PLAN.md/SETUP.audit/QUEUE.audit. Exactly250k/500k development nodes after500k training.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_setup/step0_a_base.pt`
- Checkpoint SHA-256: `f582f93b44a5d64c1f9a9b651cd4e065782deb7622e692c48cc854f13bf09cb2`
- Selected checkpoint global step: `0`

### Dataset

| Item | Value |
|---|---:|
| Training files | 394988 |
| Validation files | 14596 |
| VCTK training files | 40208 |
| VCTK validation files | 4247 |
| LibriTTS training files | 354780 |
| LibriTTS validation files | 10349 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 545.498 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1647160 |

### Effective configuration

```yaml
seed: 20261110
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
  encoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461110
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 8
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_a_base
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261110
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion10_a_base:end -->

<!-- experiment:champion10_b_enc:start -->
## champion10_b_enc

- Status: `running`
- Updated (UTC): `2026-11-10T13:37:21.439562+00:00`
- Git commit: `8f4d3c745027bfb0fce1a099c6e09cc478f39507`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_b_enc`
- Note: CHAMPION10 scratch capacity2x2, no learned parent. groups8/decoderTCN2; encoder[8, 24, 40, 80, 160]/decoderhidden160; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA85687d4e4825de1d3fec97091d05181ebb6f4dfe9f88a4212cba7ab728ff7848; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION10_PLAN.md/SETUP.audit.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_setup/step0_b_enc.pt`
- Checkpoint SHA-256: `85687d4e4825de1d3fec97091d05181ebb6f4dfe9f88a4212cba7ab728ff7848`
- Selected checkpoint global step: `0`

### Dataset

| Item | Value |
|---|---:|
| Training files | 394988 |
| Validation files | 14596 |
| VCTK training files | 40208 |
| VCTK validation files | 4247 |
| LibriTTS training files | 354780 |
| LibriTTS validation files | 10349 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 640.584 |
| Decoder MFLOP/s | 257.632 |
| Parameters | 1699688 |

### Effective configuration

```yaml
seed: 20261110
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
  - 24
  - 40
  - 80
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461110
  fourier_width: 256
  fourier_hidden: 160
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 8
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_b_enc
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261110
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion10_b_enc:end -->
<!-- experiment:champion10_c_dec:start -->
## champion10_c_dec

- Status: `planned`
- Updated (UTC): `2026-11-10T01:59:29.854130+00:00`
- Git commit: `d662a1aedfd8d7754baedd4195b155cdb3aef168`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_c_dec`
- Note: CHAMPION10 registered scratch capacity2x2, new seed20261110,500kTOTAL. Persistent supervisor queued on GPU2; startup free<8192MiB, waiting30s, NO actual optimization yet as of this queue audit. No runtime polling, no external-job stops or batch changes. See CHAMPION10_PLAN.md/SETUP.audit/QUEUE.audit. Exactly250k/500k development nodes after500k training.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_setup/step0_c_dec.pt`
- Checkpoint SHA-256: `bfe7c8b02ef3e1aa16af52a85f49badf3e7ac7a43920ea926d4ff117ac5f1b04`
- Selected checkpoint global step: `0`

### Dataset

| Item | Value |
|---|---:|
| Training files | 394988 |
| Validation files | 14596 |
| VCTK training files | 40208 |
| VCTK validation files | 4247 |
| LibriTTS training files | 354780 |
| LibriTTS validation files | 10349 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 575.277 |
| Decoder MFLOP/s | 287.411 |
| Parameters | 1796536 |

### Effective configuration

```yaml
seed: 20261110
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
  encoder_temporal_layers: 0
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461110
  fourier_width: 256
  fourier_hidden: 184
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 8
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_c_dec
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261110
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion10_c_dec:end -->

<!-- experiment:champion10_d_both:start -->
## champion10_d_both

- Status: `running`
- Updated (UTC): `2026-11-10T13:10:58.993675+00:00`
- Git commit: `8f4d3c745027bfb0fce1a099c6e09cc478f39507`
- Run directory: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_d_both`
- Note: CHAMPION10 scratch capacity2x2, no learned parent. groups8/decoderTCN2; encoder[8, 24, 40, 80, 160]/decoderhidden184; encoder TCN0;lookahead20ms+packet10ms=total30ms. Newly untrained codec/RVQ/D step0; initSHA33fe56190e1e60a17ebf40208281982d547a771f1933f846227a3255aeec83d6; fresh initial optimizers.500000 total steps; score search ONLY250k/500k. Full states resume latest own last, no budget reset; worker/crop/RNG replay may be non-bitwise. CHAMPION10_PLAN.md/SETUP.audit.
- Evaluated checkpoint: `/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_setup/step0_d_both.pt`
- Checkpoint SHA-256: `33fe56190e1e60a17ebf40208281982d547a771f1933f846227a3255aeec83d6`
- Selected checkpoint global step: `0`

### Dataset

| Item | Value |
|---|---:|
| Training files | 394988 |
| Validation files | 14596 |
| VCTK training files | 40208 |
| VCTK validation files | 4247 |
| LibriTTS training files | 354780 |
| LibriTTS validation files | 10349 |

### Submission constraints

| Item | Value |
|---|---:|
| Bitrate (bps) | 2400 |
| Algorithmic lookahead (ms) | 20 |
| Total MFLOP/s | 670.364 |
| Decoder MFLOP/s | 287.411 |
| Parameters | 1849064 |

### Effective configuration

```yaml
seed: 20261110
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
  - 24
  - 40
  - 80
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
  encoder_lookahead_frames: 2
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
  encoder_gru: true
  synthesis_type: fourier
  synthesis_initialization_seed: 20461110
  fourier_width: 256
  fourier_hidden: 184
  fourier_layers: 8
  fourier_n_fft: 320
  encoder_type: champion_grouped
  encoder_groups: 8
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
  start_step: 100000
  warmup_steps: 50000
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
  validation_limit: 64
  validation_checkpoint_interval_steps: 25000
  sample_inference_count: 2
  output_dir: /storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_d_both
  minimum_learning_rate: 1.0e-05
  warmup_steps: 5000
  checkpoint_keep_last: 20
  quantizer_learning_rate: 0.0002
  quantizer_only_steps: 0
  data_order_seed: 20261110
  reset_rng_after_init: true
  fail_on_nonfinite: true
  recovery_checkpoint_interval_steps: 1000
```

<!-- experiment:champion10_d_both:end -->
