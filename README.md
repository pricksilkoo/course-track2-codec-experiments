# Track 2：2.4 kbps 神经语音编解码实验平台

本仓库从课程 baseline 派生，保留原始 16 kHz / 10 ms / 24 bit 接口，同时把常见研究变量做成可组合配置，方便进行严格的单变量消融实验。赛题要求见 [大作业 track 2.md](大作业%20track%202.md)，数据准备和完整评测闭环见 [COURSE_GUIDE.md](COURSE_GUIDE.md)。

## 保持不变的比赛接口

- 输入、输出均为 16 kHz 单声道音频；
- 每 160 个采样点产生一个 24-bit 传输帧；
- `.bin` 大小严格为 `3 * ceil(num_samples / 160)` 字节；
- 解码器只访问 `.bin`、`.json`、模型和代码；
- 总计算量不超过 700 MFLOP/s，解码端不超过 300 MFLOP/s；
- 总理论时延不超过 30 ms。

## 可切换的实验组件

| 变量 | 配置键 | 说明 |
|---|---|---|
| 原始 EMA-RVQ | `model.quantizer_type: rvq` | 三个 256 项码本，保持 3×8 bit |
| 低维因子化 RVQ | `model.rvq_codebook_dim` | 在低维空间检索码字，再投影回 latent |
| 24-bit FSQ | `model.quantizer_type: fsq` | 默认 8 维×每维 8 levels，打包成 3 bytes |
| 编码端 latent TCN | `model.encoder_temporal_layers` | 100 Hz 上的因果空洞深度可分离卷积 |
| 解码端 latent TCN | `model.decoder_temporal_layers` | 只使用当前和历史码流帧 |
| 频谱收敛损失 | `loss.spectral_convergence_weight` | 在原始 log-magnitude STFT loss 上叠加 |
| 线性幅度损失 | `loss.linear_magnitude_weight` | 加强绝对频谱能量约束 |

`configs/baseline_16k_2p4k.yaml` 与原始 baseline 结构兼容。预置实验位于 `configs/experiments/`：

```text
factorized_rvq_32.yaml       32 维 RVQ 查找空间
latent_tcn.yaml              编码端 3 层、解码端 1 层 causal TCN
factorized_rvq_tcn.yaml      低维 RVQ + TCN + 增强频谱损失
fsq_24bit.yaml               无码本搜索的 24-bit FSQ
improved_spectral_loss.yaml  只改变训练损失
```

以一秒输入做静态 MAC 估算时，这些预设都留在赛题上限内：

| 预设 | 总计算量 (MFLOP/s) | 解码端 (MFLOP/s) |
|---|---:|---:|
| baseline | 608.768 | 244.480 |
| factorized RVQ 32 | 551.834 | 244.480 |
| latent TCN (3 + 1 层) | 691.072 | 265.056 |
| factorized RVQ + TCN (4 + 2 层) | 675.290 | 285.632 |
| FSQ 24-bit | 535.552 | 244.480 |

这些数字只表示模型结构的解析估算，不代表训练后音质；提交前仍应在远程环境用最终 checkpoint 重新运行 `scripts/complexity.py`。

## 推荐实验流程

先安装与平台 CUDA 对应的 PyTorch，再安装项目：

```bash
python -m pip install -e '.[test]'
python -m pip install -r requirements-evaluation.txt
```

准备 VCTK 和 LibriTTS 清单：

```bash
python scripts/prepare_vctk_libritts.py \
  --vctk-root "$VCTK_ROOT" \
  --libritts-root "$LIBRITTS_ROOT" \
  --output-dir "$WORK_ROOT/manifests"
```

先跑原始基线：

```bash
python scripts/train.py \
  --config configs/baseline_16k_2p4k.yaml \
  --train-manifest "$WORK_ROOT/manifests/train.scp" \
  --valid-manifest "$WORK_ROOT/manifests/valid.scp" \
  --output-dir "$WORK_ROOT/runs/baseline" \
  --device cuda
```

然后只改变一个变量，例如 32 维因子化 RVQ：

```bash
python scripts/train.py \
  --config configs/experiments/factorized_rvq_32.yaml \
  --train-manifest "$WORK_ROOT/manifests/train.scp" \
  --valid-manifest "$WORK_ROOT/manifests/valid.scp" \
  --output-dir "$WORK_ROOT/runs/factorized_rvq_32" \
  --device cuda
```

也可以不新增 YAML，直接覆盖已有字段：

```bash
python scripts/train.py \
  --config configs/baseline_16k_2p4k.yaml \
  --set model.rvq_codebook_dim=64 \
  --set loss.spectral_convergence_weight=0.25 \
  --run-name rvq64_sc025 \
  --train-manifest "$WORK_ROOT/manifests/train.scp" \
  --valid-manifest "$WORK_ROOT/manifests/valid.scp" \
  --device cuda
```

每个 run 自动保存：

```text
effective_config.yaml    最终生效配置
run_metadata.json        命令、时间、PyTorch 版本和设备
metrics.jsonl            每次验证的训练损失、验证损失和码字利用率
checkpoints/last.pt
checkpoints/best.pt
samples/                 固定样本的参考与重建音频
```

## 编码、解码与评分

```bash
python scripts/encode.py \
  --checkpoint "$CKPT" --input-dir "$VALID_DIR" \
  --output-dir "$WORK_ROOT/bitstreams" --device cuda

python scripts/decode.py \
  --checkpoint "$CKPT" --bitstream-dir "$WORK_ROOT/bitstreams" \
  --output-dir "$WORK_ROOT/reconstructed" --device cuda

python scripts/validate_submission.py \
  --input-dir "$VALID_DIR" \
  --bitstream-dir "$WORK_ROOT/bitstreams" \
  --output-dir "$WORK_ROOT/reconstructed"

python scripts/evaluate.py \
  --reference-dir "$VALID_DIR" \
  --reconstructed-dir "$WORK_ROOT/reconstructed" \
  --output-dir "$WORK_ROOT/metrics" --device cuda

python scripts/complexity.py --checkpoint "$CKPT" \
  --output "$WORK_ROOT/complexity.json"
```

## 做消融时的约定

1. 固定训练/验证清单、随机种子、训练步数和 checkpoint 选择规则。
2. 每次只修改一个主要变量；组合实验放在单变量结论之后。
3. 同时报告 PESQ-WB、ESTOI、SI-SNR、UTMOS、复杂度和理论时延。
4. GAN 判别器只影响训练，不计入推理复杂度；编码器、量化器、解码器和推理期前后处理都必须统计。
5. FSQ 和 RVQ 都输出三个字节，因而外部码率完全相同。

## 代码入口

- `src/ssp_codec/model.py`：编码器、因果 latent-TCN、RVQ、FSQ、解码器；
- `src/ssp_codec/config.py`：YAML 继承、深度合并和命令行覆盖；
- `src/ssp_codec/losses.py`：可组合多尺度频谱损失；
- `scripts/train.py`：训练、验证、实验元数据和 checkpoint；
- `scripts/complexity.py`：按模型配置统计推理复杂度；
- `tests/test_codec.py`：码率接口、量化器 round-trip 和因果性检查。
