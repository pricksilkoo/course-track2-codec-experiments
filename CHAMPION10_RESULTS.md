# CHAMPION10：四格 scratch 容量消融结果

## 结论

四组均从真正未训练的 codec/RVQ/判别器 step 0 完成 500000 个总更新，并严格只在预登记的 250k/500k 两个开发节点评分。四组都由 500k 节点胜出；本批最好是 `d_both`，总分 50.2135927469，比同 seed 新对照 A 高 1.0780350799，比 CHAMPION9D 高 0.5026120379（但同时改变 seed，不能解释为纯容量因果），仍比历史最好 C8 低 1.4534737931。

因此：容量增加在本次单 seed 开发探索中有明显交互。只加宽编码器 B 在 500k 反而低于 A；只加宽解码器 C 小幅提高；两端加宽 D 最好，且 D−B 的解码器增益最大。历史 C8 `c_from_b10` 继续作为回退，不晋升 strong_baseline_v2，不进行 sealed LibriTTS 评测，也不自动开始下一批。

## 固定设计与约束

| cell | encoder channels | Fourier hidden | 参数 | total MFLOP/s | decoder MFLOP/s | 总延迟 |
|---|---|---:|---:|---:|---:|---:|
| a_base | 8/16/32/64/160 | 160 | 1647160 | 545.49780 | 257.6320 | 30 ms |
| b_enc | 8/24/40/80/160 | 160 | 1699688 | 640.58436 | 257.6320 | 30 ms |
| c_dec | 8/16/32/64/160 | 184 | 1796536 | 575.27700 | 287.4112 | 30 ms |
| d_both | 8/24/40/80/160 | 184 | 1849064 | 670.36356 | 287.4112 | 30 ms |

四组均为 groups8、encoder 独立 TCN0、decoder 因果 TCN2、GRU160、projected RVQ 3×256（投影 48/64/80）、20 ms 单次前瞻；10 ms 成帧加 20 ms 前瞻合计 30 ms。接口固定 16 kHz 单声道、160 samples/帧、24 bit/3 bytes、2400 bps。解析复杂度含 GRU 矩阵/门、调制、保守 IRFFT/OLA 与 SnakeBeta 口径；unclassified MAC 为 0，四组均满足 700/300 MFLOP/s 上限。

## 全部 8 个预登记开发节点

| cell | step | 总分 | PESQ | ESTOI | SI-SNR dB | UTMOS | checkpoint SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---|
| a_base | 250000 | 46.5071734977 | 1.99423579 | 0.73459606 | 6.31577909 | 2.73491615 | `85f882fa92fd1b0bbb1cc59dacbb8c984af743e61c1175aa1b2074bc123f8453` |
| a_base | 500000 | 49.1355576670 | 2.11300890 | 0.75075382 | 6.43062383 | 2.94360138 | `85b4018efb5f575a51ac855fc72ee76fcfe886c5dd46a3185b947cfe89fe7418` |
| b_enc | 250000 | 46.7512776416 | 2.02345705 | 0.73655944 | 5.95715627 | 2.76858585 | `b7f5d29fc9f577cf8dc5125800323f23fa81aab7ae7f5d85018461554d643d09` |
| b_enc | 500000 | 48.8660338454 | 2.12470738 | 0.74568221 | 6.29769476 | 2.92068724 | `62ebf16124489a6edb8724ae190a849628844f86ab80b487dfca9b7a492657e8` |
| c_dec | 250000 | 47.2872609349 | 2.02208600 | 0.74425969 | 6.41666035 | 2.77915866 | `83fcc29f7fb9b33f6518a5b3cbdb714e88bf08fe5650aa09c88b6fef6c63e613` |
| c_dec | 500000 | 49.5401376557 | 2.15154193 | 0.75485216 | 6.60806503 | 2.93015894 | `8deef797654510969b0cfa294ffc3b05ecca9c0051a21ac05045122ee25f7ad9` |
| d_both | 250000 | 47.6870944939 | 2.02663534 | 0.74104367 | 6.41210485 | 2.85125241 | `dd117179d8082e07f0da82bf1183f4756609f821b8e21ec09bfa726cd1a100e7` |
| d_both | 500000 | 50.2135927469 | 2.16125861 | 0.75579438 | 6.58091334 | 3.02575330 | `6ef9c3081595db45d0ce90bdc7d9381bad718fdfdb7c8df7c27fff8c91bd07bd` |

总分按逐文件四项 clip 归一化后再求均值。8 份 `per_file.csv` 均独立重算至误差小于 1e-10；每节点均为 200 files、16197971 samples、101286 frames、303858 实际 bytes。

## 同端点因素对照

| step | 对照 | Δ总分 | ΔPESQ | ΔESTOI | ΔSI-SNR | ΔUTMOS |
|---:|---|---:|---:|---:|---:|---:|
| 250000 | B−A（编码器） | +0.24410414 | +0.02922127 | +0.00196338 | −0.35862282 | +0.03366970 |
| 250000 | D−C（编码器） | +0.39983356 | +0.00454935 | −0.00321602 | −0.00455550 | +0.07209376 |
| 250000 | C−A（解码器） | +0.78008744 | +0.02785021 | +0.00966364 | +0.10088126 | +0.04424251 |
| 250000 | D−B（解码器） | +0.93581685 | +0.00317829 | +0.00448424 | +0.45494859 | +0.08266656 |
| 500000 | B−A（编码器） | −0.26952382 | +0.01169848 | −0.00507161 | −0.13292907 | −0.02291414 |
| 500000 | D−C（编码器） | +0.67345509 | +0.00971668 | +0.00094221 | −0.02715169 | +0.09559436 |
| 500000 | C−A（解码器） | +0.40457999 | +0.03853303 | +0.00409834 | +0.17744120 | −0.01344244 |
| 500000 | D−B（解码器） | +1.34755890 | +0.03655123 | +0.01011217 | +0.28321858 | +0.10506606 |

500k 的编码器加宽效果依赖解码器：在 hidden160 下 B−A 为负，在 hidden184 下 D−C 为正。解码器加宽在两个编码器条件下均提高总分，但 C−A 的 UTMOS 略降，而 D−B 四项全升。这是同 seed、n=1 的开发探索，不是多 seed 确认。

## 训练完整性与真实损失

| cell | 最后 train loss | wave L1 | spectral | commitment | G adv | FM | D | reconstruction | validation total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| a_base | 0.51041552 | 0.01323414 | 0.11786058 | 0.10923795 | 0.74925637 | 0.13081853 | 1.57779658 | 0.13109472 | 0.47402328 |
| b_enc | 0.41875149 | 0.01319593 | 0.11756687 | 0.06096842 | 0.68920714 | 0.11021705 | 1.57965899 | 0.13076279 | 0.39151714 |
| c_dec | 0.48600750 | 0.01304875 | 0.11712235 | 0.10072259 | 0.73084968 | 0.12441399 | 1.60487604 | 0.13017110 | 0.45405716 |
| d_both | 0.45839742 | 0.01297140 | 0.11462388 | 0.07723756 | 0.72671431 | 0.12394340 | 1.59884644 | 0.12759528 | 0.42708366 |

每组 20 条真实 25k 间隔验证，共 80 条；GAN factor 在 100k/125k/150k 分别为 0.00002/0.50002/1.0，之后保持 1.0。每组保留 20 个 step 快照及 best/last，共 80 个 step 快照。每个 last 均为 500k，含模型/RVQ EMA/buffers 与非空 G、D 优化器状态。每组 480 条 `recovery_only` 周期记录不是恢复事件；四组实际 recovery event 均为 0，未发生 resume、OOM、丢弃更新或重启。

step-0 四快照均为 global_step0、trained=false、三层 codebook initialized=false、EMA cluster/embed 全零且不含优化器状态；配对共同形状张量逐 tensor 完全一致。配置、source step0、3 个数据文件、12 个核心代码文件、200 个冻结原音和 101 个历史文件哈希均复核通过。

## 选中节点的完整路径 RVQ

| cell | 3 级 perplexity | 3 级潜在 MSE 相对降幅 | 1/2/3 级 SI-SNR dB |
|---|---|---|---|
| a_base | 118.759 / 116.291 / 112.500 | +22.068% / −4.291% / +17.842% | −12.922 / −0.921 / 6.431 |
| b_enc | 126.210 / 119.225 / 128.956 | +18.559% / +35.743% / +10.036% | −20.803 / −1.556 / 6.298 |
| c_dec | 124.918 / 114.274 / 113.955 | −2.206% / −0.990% / +26.424% | −13.323 / −1.819 / 6.608 |
| d_both | 117.314 / 120.169 / 113.218 | +18.127% / +31.738% / −5.288% | −16.554 / −1.944 / 6.581 |

四个 `rvq_diagnostics.json` 均位于各自选中的 `evaluation/step_00500000` 节点，确认完整 encoder→lookahead→GRU→RVQ→decoder TCN→Fourier/synthesis 路径；三层均有 256 个活跃码字。潜在残差 MSE 不保证每级单调，但三层完整波形 SI-SNR 与实码流评分差小于 1e-4 dB。

## 审计、权重与试听路径

独立终审通过 526 项检查；4 个主 `PIPELINE_COMPLETE`、8 个节点 `ROUNDTRIP_COMPLETE`、8 个 `EXPERIMENT_LOG` complete 记录齐全。逐文件 3×ceil(samples/160)、16 kHz 单声道、原长度、有限音频、checkpoint SHA、复杂度、CSV 重算与码流/重建树哈希证据详见 `CHAMPION10_RESULTS.audit`。

原音目录：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/fast_b64_2s_v1/validation_200`

- A 重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_a_base/evaluation/step_00500000/reconstructed`
- B 重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_b_enc/evaluation/step_00500000/reconstructed`
- C 重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_c_dec/evaluation/step_00500000/reconstructed`
- D 重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_d_both/evaluation/step_00500000/reconstructed`

历史回退保持：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_c_from_b10/checkpoints/interpolated.pt`，SHA `a5cffa2dfcf39fc69b36b84e8ca238e7cbd9408ee008a1042bb7bbb253e4eb19`，分数 51.6670665400。

本批不替换历史冠军，不自动晋升注册表，不清理任何历史权重，不开始下一批；下一实验必须另行获得用户批准。
