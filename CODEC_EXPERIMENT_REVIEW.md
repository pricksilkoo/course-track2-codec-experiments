# 低码率语音 Codec 全部实验复盘与方法审计

更新日期：2026-10-27

本文是从官方基线到当前模型的完整实验审计。重点不只是罗列最高分，而是解释每一步为什么做、控制了什么变量、哪些结论可信、哪些只是单随机种子的现象，以及为什么保留或关闭某条路线。数值已与 `EXPERIMENT_LOG.md`、各阶段 `*_RESULTS.md`、确认集记录和检查点哈希交叉核对。

## 1. 先给结论

当前应继续冻结 `strong_baseline_v2`：

- 模型：`runs/struct4_b_residual_later/checkpoints/best.pt`
- 结构：projected residual VQ，三级投影维度 `[48, 64, 80]`
- fixed-200 开发集总分：**46.7463**
- sealed 400 条确认集总分：**44.9637**
- 约束：2400 bps、30 ms lookahead、650.2272 total MFLOP/s、277.44 decoder MFLOP/s
- SHA-256：`f9c71919519dbda7d02bdfc56d6eb309cf9a45976d733e29b3fd808b7b77cc1a`

从官方权重到当前确认模型，sealed 分数从 36.9167 提高到 44.9637，绝对提升 8.0470。最有价值的改进依次来自：正确的训练日程、因果时域建模、较长训练与弱对抗、合理的损失组合、RVQ 后级利用、projected residual VQ，以及结构化三随机种子筛选。

后续 decoder 蒸馏在开发集上证明了“有因果增益”，但三随机种子方差较大；晚期 decoder 平均虽然提高标量总分，却以 PESQ、ESTOI、SI-SNR 全部下降换取 UTMOS 上升，因此不应晋升。也就是说，当前主要瓶颈已经从“码本没用好”转为“感知自然度与信号保真度之间的 decoder 合成权衡”。

## 2. 不可变约束与评测纪律

### 2.1 部署约束

所有有效候选必须同时满足：

| 约束 | 上限或固定值 |
|---|---:|
| 码率 | 恰好 2400 bps |
| 算法 lookahead | 不超过 30 ms |
| 总复杂度 | 不超过 700 MFLOP/s |
| decoder 复杂度 | 不超过 300 MFLOP/s |

主线模型使用 16 kHz 音频、10 ms 一帧（100 Hz latent rate）、每帧三级 256-entry RVQ，每级 8 bit，共 24 bit/frame，即 2400 bit/s。

### 2.2 数据与评测集

- 训练使用 VCTK 与 LibriTTS 训练数据，训练片段通常为 2 秒，batch size 32。
- 调参与候选比较统一使用固定 200 条 development set；固定列表与随机种子保证各实验可配对比较。
- sealed 确认集由 LibriTTS test-clean 与 test-other 各 200 条组成，共 400 条；它不属于训练或开发集。
- sealed 集只在预先选定单一候选后做一次确认，不用于损失、结构或 checkpoint 调参。

总分同时综合 PESQ、ESTOI、SI-SNR 与 UTMOS。后期实验表明，只看总分会隐藏指标间交换，因此从稳定性研究开始增加了组件指标 guardrail。

## 3. 检查点谱系

```text
official baseline
  -> training fix
  -> causal temporal TCN (C)
  -> long-TCN continuation (next4 B)
  -> weak adversarial refinement (refine4 D)
  -> FM1.5 + SI-SNR0.003, three-seed winner
  -> codebook balance + later-stage commitment (strong_baseline_v1)
  -> projected residual VQ, later-heavy dimensions
     -> three-seed tie resolved by lower variance
     -> one-shot sealed confirmation (strong_baseline_v2)
        -> decoder continuation / refiner / Haar / training-only distillation
        -> matched seeds and causal controls
        -> early SWA, late decoder-only averaging, delayed distillation
```

每个箭头都是从已记录 checkpoint warm start，不是把不同实验结果随意拼接。结构变化时记录 missing/new tensors；例如 multiscale refiner 和 Haar 分支只新增 decoder tensors，其余 codec 与 discriminator 权重均完整加载。

## 4. 按阶段复盘

### 阶段 0：官方基线与评测复现

官方 causal convolutional waveform autoencoder 使用三级 256-entry RVQ。官方权重在 fixed-200 上约 37.44，在 sealed 集上 36.9167；复杂度 608.768 total / 244.480 decoder MFLOP/s。组件指标为 PESQ 1.6664、ESTOI 0.7104、SI-SNR 1.1217、UTMOS 2.1817（sealed）。

早期快速训练只有 24.9042，说明首先是训练 recipe 未复现，而不是架构本身不行。这个阶段建立了固定开发列表、复杂度检查、checkpoint 哈希和结果日志，避免后续把数据漂移当作模型改进。

### 阶段 1：训练 recipe 与第一轮可解释消融

第一轮分别测试训练修正、感知损失、时域上下文与 factorized TCN：

| 方案 | fixed-200 分数 | 解释 |
|---|---:|---|
| A 训练修正 | 37.9104 | batch 32、2 秒片段、EMA/日程修正本身有效 |
| B 感知项 | 37.9566 | 小幅有效，但不是主瓶颈 |
| C causal temporal TCN | **40.3124** | 2 个 encoder + 1 个 decoder 因果 TCN，30 ms lookahead，显著有效 |
| D factorized TCN | 37.7866 | 参数化方式没有带来收益 |

结论：主要缺口是时间上下文，不是单纯增加 loss。保留 C，关闭 D。

### 阶段 2：MiniMimi 风格大结构探索

训练 200k steps 比较 plain RVQ、semantic/acoustic split、decoder-heavy Transformer 和 hybrid：32.8036、32.9588、33.8339、34.7105，均明显低于 C。

这是一组重要负结果。它说明在 2400 bps、30 ms、严格算力限制下，大幅改造表征与 Transformer decoder 会破坏已学好的 waveform path，而且训练成本高、warm start 利用差。于是没有继续在 MiniMimi 分支上堆算力。

### 阶段 3：沿正确方向延长训练

以 C 为起点追加约 170k steps：

| 方案 | 分数 |
|---|---:|
| continuation control | 42.9513 |
| long TCN | **43.7272** |
| WavLM stage-0 辅助 | 42.5750 |
| local Transformer | 42.5003 |

长 TCN 相比 control 有真实结构增益；WavLM 与 local Transformer 在当前约束下没有带来收益。这个阶段也提醒我们：继续训练本身贡献很大，因此后续必须包含 continuation control。

### 阶段 4：弱对抗与重建损失细化

在 long-TCN 上测试低学习率、feature matching、SI-SNR 和弱对抗：

| 方案 | 分数 |
|---|---:|
| low LR | 43.8558 |
| feature matching 2.0 | 44.6625 |
| SI-SNR 0.01 | 44.1082 |
| adversarial 0.05 | **45.2681** |

sealed 路径也一致改善：官方 36.9167 → long-TCN 42.0528 → FM2 42.9356 → weak-GAN 43.5903。弱对抗改善了感知合成，但没有突破部署约束。

### 阶段 5：2×2 损失组合与随机种子确认

固定 adversarial weight 0.05，做 feature matching 1.0/1.5 × SI-SNR 0/0.003 的 2×2：

| 方案 | 分数 |
|---|---:|
| control | 45.1760 |
| FM1.5 | 45.4786 |
| SI-SNR0.003 | 45.2666 |
| FM1.5 + SI-SNR0.003 | **45.5554** |

随后对 FM-only 与组合做三随机种子：FM-only 45.4586±0.0360；组合 45.5392±0.0294，并且组合 3/3 配对获胜。选取组合家族中开发分最高的 seed8128 checkpoint（45.5569）做一次 sealed，得到 43.9842。

这里的方法是合理的：先用小型 factorial 找交互，再用 seed replication 决定家族，而不是拿单个最高 checkpoint 直接晋升。

### 阶段 6：码本诊断与利用率实验

诊断不只看 active codes，还看 perplexity、marginal entropy、逐级 residual-MSE reduction 和 partial-stage reconstruction。起点三级 perplexity 约 140.4/132.6/137.7，总边际熵 21.29 bit；后两级 residual reduction 约 41.9% 与 31.9%。这说明不是“死码本”，而是后级仍有优化空间。

四组结果：control 45.6565、balance 45.6244、later-stage commitment 45.8099、两者组合 45.8473。组合成为 `strong_baseline_v1`。这个结论很窄：温和 usage/balance 与后级 commitment 有益；它不支持扩大 codebook 或声称容量不足。

### 阶段 7：结构化量化器 2×2

比较 projected residual VQ 与 product VQ，再比较统一 `[64,64,64]` 和 later-heavy `[48,64,80]` 投影维度。前 5k steps 只适配 quantizer，再做 end-to-end GAN 训练，以降低结构切换风险。

| 结构 | 分数 |
|---|---:|
| residual + uniform | 46.6837 |
| residual + later-heavy | **46.7463** |
| product + uniform | 46.3615 |
| product + later-heavy | 46.3595 |

Residual 明显优于 product；later-heavy 单种子只领先 0.0627，不能直接断言结构更好。

### 阶段 8：结构随机种子确认与 v2 晋升

三随机种子结果：

- residual-uniform：46.7332±0.1097，worst 46.6570，配对胜 1/3。
- residual-later：46.6869±0.0532，worst 46.6438，配对胜 2/3。

均值差小、配对符号冲突，按预注册规则判为 tie，并选择方差更小的 later-heavy 家族。seed20261024 checkpoint 做一次 sealed，得到 44.9637，相比上一确认模型 43.9842 提高 0.9795，而且四个组件指标全升，于是晋升为 `strong_baseline_v2`。

这一步非常关键：开发均值并不是最高，却因稳定性规则被选中，sealed 结果反而证明选择合理。

### 阶段 9：decoder 合成结构与训练时蒸馏

从 v2 出发做 100k continuation：control 47.1943、causal multiscale refiner 47.2741、Haar subband 47.0528、training-only distillation 47.3227。

- control 本身 +0.4480，说明继续训练贡献很大。
- multiscale 相对 control +0.0797，增益较小。
- Haar 相对 control -0.1416，关闭。
- distillation 相对 control +0.1283，且部署模型不包含 teacher，没有推理成本。

Teacher 是 residual-uniform seed8128；waveform 与 spectral distillation weight 各 0.1。四组最佳点都在新训练 10k step，而不是 100k 末尾，说明后期有明显漂移。

### 阶段 10：蒸馏 seed 与组合效应

纯蒸馏三个 seed 为 47.3227、46.8630、46.8433，均值 47.0097±0.2713。最高的 47.3227 是分布高端，不能当作稳定改进。multiscale+distillation 在两个匹配 seed 分别落后纯蒸馏 0.1666 和 0.0577，配对均值 -0.1121，因此关闭组合分支，不再浪费第三个 seed。

这一阶段发生过 GPU0–2 与无关 38–39 GiB 任务共享导致 OOM。所有进程都从 step5000 checkpoint 安全恢复，随后只在 GPU3 串行运行；没有停止或修改他人的任务，也没有重复已完成实验。这说明 runner 的幂等恢复设计有效，但也说明“剩余显存看起来够”不能代替峰值显存测量。

### 阶段 11：因果 control 与 early SWA

匹配 continuation controls 为 46.3005、46.3444；原始蒸馏为 46.8630、46.8433。蒸馏在两个 seed 分别 +0.5625、+0.4988，配对均值 +0.5307，证明 teacher signal 的增益不是简单 continuation 造成的。

early full-model SWA（2.5k/5k/7.5k/10k）只有 44.5262、45.0291，分别比 raw distillation 低 2.3368、1.8142。active codes 仍接近满，但 stage-1 perplexity、总熵和 full-rate reconstruction 下降，说明早期 GAN/quantizer 轨迹之间参数不对齐，平均权重破坏了功能。

### 阶段 12：late decoder averaging 与 delayed distillation

late decoder-only average 只平均 raw-distill 的 20k/25k/30k decoder 参数，encoder/quantizer 保留 30k 状态：

| seed | raw distill | late avg | 分数变化 |
|---:|---:|---:|---:|
| 3407 | 46.8630 | 46.9762 | +0.1132 |
| 8128 | 46.8433 | 46.9475 | +0.1042 |

但组件变化为：PESQ -0.0734/-0.0549，ESTOI -0.0103/-0.0118，SI-SNR -0.2998/-0.3635，UTMOS +0.1730/+0.1628。它是稳定的指标交换，不是全面提升。按预注册 guardrail 拒绝晋升。

delayed distillation（0–9999 关闭，10k–14999 ramp）为 46.2324、46.1260，平均比 raw distill 低 0.6739，比 controls 低 0.1433。两组都选择 step5000——teacher 尚未开启——说明延后 teacher 没有证据有效，关闭该路线。

### 阶段 13：从零训练的未来上下文上限实验

这一阶段专门回答“30 ms 延迟规则是不是主要瓶颈”。四组不从已有权重
warm-start，而是从同一个从未训练的 codec+discriminator step-0 状态开始；
共享参数和初始前向输出完全一致，并固定 data order 与初始化后的 RNG。
唯一变化是 encoder 能看到未来 30/40/60/80 ms，decoder 仍然严格因果。

| encoder lookahead | objective | PESQ | ESTOI | SI-SNR | UTMOS |
|---:|---:|---:|---:|---:|---:|
| 30 ms control | 21.4078 | 1.1707 | 0.4293 | **2.6145** | 1.2516 |
| 40 ms | **22.8386** | **1.1781** | **0.4859** | 2.5707 | 1.2499 |
| 60 ms | 21.7014 | 1.1718 | 0.4461 | 2.3167 | 1.2488 |
| 80 ms | 22.5166 | 1.1726 | 0.4791 | 2.3641 | **1.2524** |

表面结果不是“未来看得越多越好”：40 ms 最好，60 ms 接近 control，80 ms
回升但仍低于 40 ms。但 30 ms control 只有 21.4078，远低于完全相同架构的
成熟模型 46.7463，因此正对照没有成立。根因是错误沿用了 warm-start 日程：
随机 codec 先被冻结 5k step，只训练 quantizer，随后 codec 刚解冻就引入
GAN，并在 100k 内把微调学习率退火到底。该排序只能描述欠训练状态，不能
用于判断成熟模型的延迟上限。

四组码率均为 2400 bps，total/decoder compute 均满足 700/300 MFLOP/s，
但只有 30 ms control 合规，另外三组仅作科研诊断，不能提交或晋升。四组
scratch 分数远低于成熟 `strong_baseline_v2` 的 46.7463，因此本轮正式标记为
failed positive control / inconclusive。纠正版改为从 step 0 联合训练 codec 与
RVQ、100k 后才启用 GAN、总预算 500k，并规定 control 至少达到 46.25 才允许
解释 lookahead。方案见 `LOOKAHEAD_SCRATCH2_PLAN.md`，sealed 集未使用。

### 阶段 14：纠正后的从零 lookahead 实验

纠正版严格保留同一个未训练 codec+discriminator 初始化、seed、data order 和
初始化后 RNG，只修正训练日程：0--99999 联合训练 codec 与 projected RVQ，
100k--149999 逐步引入 GAN/FM，之后完整 GAN 训练到 500k；学习率峰值为
2e-4。30 ms control 最终为 46.5503，超过预注册最低门槛 46.25，且选中
checkpoint 的 validation reconstruction 为 0.13121，接近成熟参考 0.13151。
因此这次正对照成立，可以解释延迟效应。

| encoder lookahead | objective | 相对 30 ms | PESQ | ESTOI | SI-SNR | UTMOS |
|---:|---:|---:|---:|---:|---:|---:|
| 30 ms control | 46.5503 | -- | 1.9845 | 0.7319 | 5.5852 | 2.8368 |
| 40 ms | 47.2073 | +0.6570 | 2.0250 | 0.7333 | 5.8261 | 2.8659 |
| 60 ms | **47.8593** | **+1.3091** | **2.0512** | **0.7379** | **5.9574** | **2.9086** |
| 80 ms | 46.2402 | -0.3100 | 1.9786 | 0.7275 | 5.8238 | 2.7877 |

60 ms 相比有效 control 的 +1.3091 不是某个指标交换：PESQ、ESTOI、SI-SNR
和 UTMOS 全部改善。因此 30 ms 规则确实造成了可测的质量损失。但 80 ms
反而低于 control，说明关系不是“未来看得越多越好”，也不能把延迟写成唯一
或单调的主导瓶颈。更准确的结论是：当前架构在约 60 ms 有上下文甜点，但
超过甜点后优化/归纳偏置会抵消收益。

四组 active codes 均为 254--256，单级 perplexity 约 131--151，总边际熵
21.12--21.55 bit，没有码本坍塌。所有模型满足 2400 bps 和 700/300 MFLOP/s，
但 40/60/80 ms 违反比赛延迟，只能用于诊断，不能晋升或提交。sealed 集未
使用。完整结果、复杂度、RVQ 诊断与 checkpoint hash 见
`LOOKAHEAD_SCRATCH2_RESULTS.md`。

## 5. 码本是否被有效利用

“active codes 接近 256”只能排除最严重的 dead-code collapse，不能证明利用充分。本项目采用五层证据：

1. active-code count：是否有完全不用的 entry；
2. perplexity：使用分布是否集中在少数 code；
3. marginal entropy：每级实际携带多少离散信息；
4. residual-MSE reduction：后一级加入后还消除多少误差；
5. partial-stage reconstruction：只用前 N 级时 PESQ/ESTOI/SI-SNR 如何变化。

后期主线通常有 255–256 active codes、单级 perplexity 约 120–147、总熵约 20.9–21.5 bit，并且第二、三级仍有显著 residual reduction。因此不存在“码本完全没用”的瓶颈。早期 SWA 的失败也证明 active count 不够敏感：code 还活着，但概率分布与解码器功能已经错位。

## 6. 哪些实验设计是合理的

- 每次结构性结论都有 continuation control，避免把训练时长误判为结构增益。
- 先做 2×2 factorial，再做 seed confirmation，控制算力同时识别交互。
- 家族按三 seed 均值、方差、worst seed 与配对差选择，而不是只挑最高点。
- sealed 集只用于已预选单一候选，且晋升需要组件指标一致改善。
- 记录有效配置、数据计数、训练指标、objective、复杂度、RVQ 诊断和 SHA-256。
- OOM 后只恢复失败 run，不重跑健康 run；不干扰无关 GPU 任务。

## 7. 方法上的局限与需要警惕的地方

1. fixed-200 被反复使用，长期看会形成隐性开发集过拟合；后续应减少尝试次数或建立第二内部验证集。
2. 多数早期阶段只有单 seed，适合筛方向，不适合给小于约 0.1 的差异下强结论。
3. 标量 objective 可被 UTMOS 主导；late averaging 已展示总分上涨但三项保真指标下降。今后必须预注册组件下限。
4. decoder 100k 实验最佳点都在 10k，说明计划训练长度超过有效区间；应采用早停/更密验证，而不是默认长训。
5. sealed 集虽未用于逐候选调参，但已经经历数次阶段性确认；当前应把它视为接近耗尽的最终资源，不再做小步确认。
6. `strong_baseline_v2` 的家族均值不是结构实验最高，但方差更低且 sealed 表现好。不能把某个开发集峰值误写成已确认的新基线。

## 8. 当前最可信的科学结论

- 因果时域上下文是第一大结构收益来源。
- 弱对抗、feature matching 与小权重 SI-SNR 在该架构上互补。
- projected residual VQ 优于 tested product VQ；后级适度增加表达维度/commitment 有益。
- 码本没有严重 collapse；当前瓶颈主要在 decoder 合成与感知/保真权衡。
- training-only waveform/spectral distillation 具有配对 seed 的因果增益，但原始三 seed 方差仍大。
- multiscale 与 distillation 不可直接相加；Haar subband、early SWA、delayed distillation 均应关闭。
- late decoder averaging 是可行的 function-preserving 操作，但当前均匀平均只换取 UTMOS，不能晋升。
- 有效 500k scratch 对照表明，60 ms 相比 30 ms 可带来 +1.3091 且四项组件均改善；但 80 ms 反而退化，因此 30 ms 有可测成本，却不是简单单调或唯一的主导瓶颈。

## 9. 推荐下一步

建议停止大范围结构搜索，先做低成本、预注册的 Pareto 安全选择：

1. 不训练新模型，使用已有 raw-distillation 与 20k/25k/30k checkpoint，做少量 decoder interpolation/权重选择。
2. 在运行前规定组件 guardrail，例如 PESQ、ESTOI、SI-SNR 相对 raw checkpoint 的下降不得超过明确阈值；总分只在 guardrail 内比较。
3. 用 matched seeds 3407/8128 同时通过才保留；若增益小于 0.05 或符号冲突，停止该方向。
4. 若找不到 Pareto 改进，接受 v2 已接近当前架构/预算下的实用瓶颈，转向更丰富训练数据、objective 校准或主观听测，而不是继续在 fixed-200 上微调。
5. 只有出现多 seed、组件一致、幅度足够的候选，才考虑一次最终 sealed 确认；否则保持 v2。
6. 不应继续用超限 lookahead 追分；60 ms 的诊断收益虽真实且全面，但 80 ms 退化、所有超限模型均无部署资格。后续应把精力放回 30 ms 内的因果建模与合成优化。

## 10. 复现实验时应查看的文件

- 总账：`EXPERIMENT_LOG.md`
- 时间线：`EXPERIMENT_HISTORY.md`
- 当前基线：`STRONG_BASELINE.md` 与 `model_registry/strong_baseline_v2.yaml`
- sealed 记录：`CONFIRMATION_RESULTS.md`
- RVQ 方法：`RVQ_DIAGNOSTICS.md`
- 结构研究：`STRUCTURAL_RESULTS.md`、`STRUCTURAL_SEED_RESULTS.md`
- decoder 研究：`DECODER4_RESULTS.md`、`DECODER_SEED4_RESULTS.md`
- 稳定性研究：`DECODER_STABILITY4_RESULTS.md`、`DECODER_STABILITY5_RESULTS.md`
- 延迟上限研究：`LOOKAHEAD4_PLAN.md`、`LOOKAHEAD4_RESULTS.md`、`LOOKAHEAD_SCRATCH2_PLAN.md`、`LOOKAHEAD_SCRATCH2_RESULTS.md`

综合判断：整个过程总体合理，尤其是后半程的预注册、配对 seed、复杂度审计和 sealed 隔离。最需要修正的不是继续堆实验，而是将组件指标 guardrail 提升为与总分同等重要的选择标准，并承认开发集峰值与可部署、可复现改进不是一回事。

## 11. 2026-11-02：按冠军思路进行新一轮有控制的探索

用户要求参考LRAC2025冠军重新尝试建模和训练。第一轮采用四组2×2：原方法续训A、
量化旁路与分阶段mel训练B、因果Conv2Former解码模块C、组合D。每组从同一v2权重
续训100k步，seed与数据顺序一致；新模块初始恒等，避免把随机起点劣势当作架构无效。
完整思路、参数和判定见`CHAMPION4_PLAN.md`。当前尚无新质量结果，不能提前宣布提升。

本轮从冠军借鉴的是两个可迁移的方向：用连续latent训练帮助合成器，以及用卷积调制
建模较长历史并在后期降低mel约束。冠军24kHz/20ms/1或6kbps与课程16kHz/10ms/2.4kbps
接口不同，因此保留本项目3字节帧格式，并缩小新增模块确保decoder296.16MFLOP/s。
没有直接采用冠军的ISTFT头、GRU、完整判别器组合或宣称完全复现。若训练策略包有效，
后续还需拆解旁路和mel，若建模有效需多seed确认；单seed小幅上涨不能替换v2。

用户同时授权清理冗余权重。已删除301个已完成运行的中间/last及smoke权重，释放3.8444GiB。
每个正式实验best、v1/v2、teacher、关键祖先、平均所需源快照、共享step0、未完成任务与
外部模型均保留。已删除中间权重没有备份，无法直接恢复；清单与哈希见`CHECKPOINT_RETENTION.md`。
这意味着最终模型复测仍可做，任意历史中间步续训能力不再全部保留。

### 11.1 完成后的结果与选模反思（2026-11-03）

四组均完成100k步。原规则选择的best全部在5000步：A46.0115、B46.7819、C45.9936、
D46.8959。A未过46.25门槛，且B/D相对冻结v2的UTMOS明显更低，不能宣布新方法成功。
尤其5000步时GAN刚启动，80k后的mel调度没有进入被评测权重；这是本轮设计中必须
承认的选模缺陷，不能用“训练已经跑到100k”掩盖“评测权重其实只有5k”。

在看到原结果后、未知终点得分前，单独登记了四组统一100000步的补充诊断。最终为
A47.2383、B47.2584、C47.1374、D47.1692。完整GAN终点的control已经恢复旧水平，
并比冻结v2高0.4920；B比A仅高0.0201，C/D都低于A，没有额外方法达到+0.15门槛。
因此初期对弱control的巨大优势不能代表最终持续收益。补充诊断保留独立标记，不能
事后倒改原始门槛或只展示分数更高的一行。

更低wave/STFT验证误差主要偏向保真重建，GAN后期的自然度可能更好但重建误差略高；
两者的最佳点不必相同。这轮真实提供了选模方法学证据，而不是一个新冠军模型。
码本诊断没有坍塌，新增解码计算也没有换来稳定收益。关闭当前小模块/训练包适配，
保持v2冻结；下一轮预注册因果逆傅里叶合成与encoder GRU的四组结构对照，用共同
未训练初始化和已验证500k scratch课程，并在开跑前固定终点评测规则。

详细可复查报告：[CHAMPION4_RESULTS.md](CHAMPION4_RESULTS.md)。

## 12. 第二轮：真正替换合成路径，而非继续追加小模块

在首轮终点对照显示没有额外收益后，登记GRU×Fourier合成的四组：A原模型，B仅加
encoder单向GRU，C仅换因果逆傅里叶/overlap-add decoder，D组合。由于C/D是全新
合成器，四组都从同一个未训练encoder/RVQ/判别器状态开始，训练500k步；没有从v2或
任何成熟权重短训。A复现此前通过正对照的scratch课程，作为同轮控制。

Fourier头每10ms预测320样本，当前输出只融合当前及上一latent产生的窗口，不等待
下一latent；因果性通过输出前缀不变测试。C/D把较多参数放在100Hz latent域，避免
波形高采样率卷积，decoder计算降至257.632MFLOP/s。GRU作为独立因素增加过去状态
建模，保持30ms未来信息上限。四组共同保留10ms帧、24bit、2.4kbps接口。

本轮在新得分产生前固定500000步终点为主要评测，重建最小best只做诊断，吸取首轮
选模教训。35项测试与完整GAN峰值预检已过，暂无本轮质量结果。预注册详情：
[CHAMPION5_PLAN.md](CHAMPION5_PLAN.md)。

四组已于2026-11-03北京时间08:53启动，初期优化迭代正常；巡检已转到这批从零实验。

## 13. 第二轮完成：合成家族明显改善，先确认再推广

2026-11-04四组全部完成50万步，从未训练初始化、同一数据和课程，并严格使用开跑前
固定的500000步last.pt。没有再次按重建best挑开发集分数。A原波形47.0006、B仅GRU
47.3305、C因果Fourier50.3710、D组合51.4126；旧v2为46.7463。A通过46.25正对照门槛，
这一次不再是对偏弱control的假象。C比A高3.3704、D高4.4120，而且相对A及v2的
PESQ/ESTOI/SI-SNR/UTMOS均通过护栏。B虽涨分，但对v2的UTMOS下降0.0435超过0.03，
不能只看总分宣布GRU单独成功。

主要信号来自整个Fourier合成家族。它把更多参数放在100Hz latent层，decoder由
277.440降至257.632MFLOP/s；C总630.4192、D总666.3072，仍满足700总/300解码限制。
真实码流仍是每10ms三字节、2.4kbps，16kHz单声道、30ms未来信息；逐文件音频长度
和字节均检查。Fourier窗只融合当前和上一latent，不等待下一帧。不能把容量、卷积
调制和合成方式共同变化的收益全部说成“IRFFT本身的功劳”。

D对C额外+1.0416分主要提升自然度和可懂度，SI-SNR反而低0.1705dB，不是全指标支配。
GRU主效应+.6858、合成主效应+3.7262、交互+.7117仍只是一个训练种子上的观察。
文件bootstrap只覆盖固定种子下的文件误差，不涵盖训练随机性。末段重建已平台，
没有追分延长。RVQ码本无坍塌，但删掉码本的部分重建很差；latent残差非单调也不等于
音频质量非单调。不要把诊断熵当作未用24bit容量，或假称已有800/1600bps可伸缩产品。

四条完整记录、初始化/最终SHA、20次验证曲线、四分量、复杂度及RVQ证据保留在
[CHAMPION5_RESULTS.md](CHAMPION5_RESULTS.md)和.audit。没有单独逐batch训练分量日志，
这一记录限制如实披露，不伪造补齐。所有旧best/last与v2权重保留，未使用sealed集。

按既有授权下一批只做两个新种子的A对D共四组匹配确认，不层叠新因素、不自动推广。
种子3407和8128同时改变未训练初态与训练数据随机顺序，pair内共享encoder/TCN/RVQ/
判别器。固定500k与原护栏事先登记于[CHAMPION6_PLAN.md](CHAMPION6_PLAN.md)。
C保留低计算备选，B单独部署升级分支关闭；即使确认成功，冻结v2仍须另行明确决策才能替换。

确认批次在35项测试、两套架构完整GAN峰值和全新未训练谱系检查通过、方案提交推送后，
于2026-11-04北京时间17:35启动。四组均已开始优化，原监控已转向CHAMPION6；这只是
运行状态，不是跨seed确认已成功，不能提前宣称新基线。

## 14. 第三轮结束：高分重复出现，但预注册确认没有完整通过

本节可独立阅读：目标是16kHz单声道语音神经编解码，每10ms输入160点，用三层RVQ
各发送一个8bit索引，恰好3字节/帧、2.4kbps；允许最多30ms未来信息，总计算<=700、
解码<=300MFLOP/s。冻结参照strong_baseline_v2为46.746343，仍然不替换、不新评sealed。
上一轮CHAMPION5的51.412604是从未训练codec/判别器完整训练50万步得到，并不是从
46分模型继续微调。本轮也不加载那个51分权重，而用两个全新随机初态检查结构稳定性。

比较对象有两个：control用原波形卷积decoder；candidate保留encoder、TCN和三层
投影RVQ，在量化前加160维单向残差GRU，解码改为latent域8层因果卷积调制模块后预测
320点实信号的复频谱、IRFFT、sin²窗和160点hop的加权重叠合成。当前hop由当前帧
前半段和上一帧后半段融合，不读下一个latent。前后半段都是时域波形，不是频率分组。
这是借鉴冠军思路后的本任务适配，不是完整冠军复现，也不是单独更换一个数学变换。

本轮四组是两对，而非2×2消融：A/B分别是seed3407的control/candidate，C/D是seed8128
的control/candidate。每个seed重新构造codec，判别器seed+100000，新模块seed+200000
（GRU内部+1）；pair内encoder、TCN、latent norm、RVQ和判别器张量共享。两个source和
四个step0均trained=false/global_step0，与预检SHA一致；没有v2/CHAMPION5成熟权重、
smoke训练状态或旧共同初态的偷偷继承。各pair也匹配data-order和加载后RNG重置。

394988训练文件、14596验证文件；batch32、2秒、8 workers；生成器AdamW lr2e-4、5k
warmup后cosine至1e-5、weight_decay1e-6、clip1，判别器lr2e-4/clip10。RVQ从0联合训练，
码本EMA更新。0–99999无GAN，100k–149999渐入，150k起完整；waveform+multi-STFT+
VQ+.003负SI-SNR，GAN/feature matching权重.05/1.5。没有新增teacher、旁路、mel策略。
每25k验证64batch，共20次；所有四组在开跑前固定50万步last.pt为唯一主要终点，
不按开发集分数挑checkpoint。训练从Nov4北京时间17:35到Nov5全部完成，候选pipeline
约26小时02分、control约29小时15分；共享机器周转不能当作严格速度benchmark。

| 组 | 总分 | PESQ | ESTOI | SI-SNR dB | UTMOS |
|---|---:|---:|---:|---:|---:|
| 冻结v2 | 46.746343 | 1.998153 | .728782 | 5.178891 | 2.905652 |
| A 3407 control | 45.974350 | 1.976021 | .728136 | 5.632182 | 2.764680 |
| B 3407 candidate | 51.624336 | 2.223697 | .768387 | 6.600310 | 3.127804 |
| C 8128 control | 46.376849 | 1.968645 | .728125 | 5.793864 | 2.821387 |
| D 8128 candidate | 50.968929 | 2.198076 | .762977 | 6.644038 | 3.069489 |

两候选分别比匹配control高5.649986、4.592080，比v2高4.877993、4.222586；不是只有
UTMOS一项提高，四项都提高。B−A分量为PESQ+.247676、ESTOI+.040251、SI-SNR+.968128dB、
UTMOS+.363124；D−C为+.229431、+.034852、+.850174dB、+.248102。B−v2为+.225544、
+.039605、+1.421420dB、+.222153；D−v2为+.199923、+.034195、+1.465147dB、+.163837。
因此“比匹配control及v2分别>=.15且分量下降不超过.02/.003/.15dB/.03”数值条件全通过。

但预注册同时要求每个control>=46.25。A只有45.974350，低0.275650，C的46.376849通过。
**完整确认没有通过**；不能说候选都高分就自动通过，也不能只保留8128或换掉3407。
这并不等于候选毫无效果：真实、重复的正向信号保留；只是对照稳定性未达预先标准，
不能把该批当作无保留的架构确认和新基线。两个新seed的候选平均51.296632、范围
50.968929–51.624336；control平均46.175599、范围45.974350–46.376849；配对增益平均
5.121033、范围4.592080–5.649986。n=2有限，范围不是置信区间，文件bootstrap也不能
替代训练seed误差。CHAMPION5先前发现单独报告，不混入本轮平均，不伪造因子效应。

先诊断再下结论：四组没有OOM、恢复或非有限损失，监督器均running→complete；原始
日志、20次验证、100k/150k GAN阶段均符合计划。配置和开跑前预检仅有相对输出路径
解析为等价绝对路径的差异，其他超参和数据哈希不变。最终checkpoint确为500k，SHA
与评测证据/实验记录一致；按逐文件分量重算课程总分一致，UTMOS未跳过。固定200条
共16197971样本、101286帧，每组真实303858字节，逐文件音频采样率/声道/长度正确。
RVQ诊断经过analysis_gru和完整合成路径，三层SI-SNR与真实码流解码误差<1e-4dB。
最终35项pytest回归再次通过（7.05秒）。没有发现可安全修复并据此重跑的实现故障。

A相对v2的SI-SNR反而高.453291dB，但UTMOS低.140971；C也SI-SNR高.614973dB而UTMOS
低.084265。与CHAMPION5 control相比，两组主要感知质量偏弱。这与不同随机初态/顺序
下的训练波动相容，但没有证据把原因确定归于GAN、某层参数或某个随机源。末75k
重建变化较小：A .132374→.131595、C .131946→.131643；总train loss上升还包含VQ/FM
变化，不能据此说重建发散或多训一定改善自然度。best都在500k也不证明必须延长。
没有明确欠收敛证据，因此不改终点、不事后续训或挑中途权重救门槛。

计算折中仍存在：control662109参数、总650.2272/decoder277.440MFLOP/s；candidate
1868064参数、666.3072/257.632。多1205955参数、总+16.080，解码少19.808；容量、
低帧率计算位置、卷积调制和Fourier/WOLA共同变化，不能把收益只归功IRFFT。成本含
GRU矩阵/gate、调制乘法和保守FFT/OLA估计，不含激活/normalization/padding/I/O，
不等同完整流式实现或功耗、时延benchmark。所有接口和30ms信息上限仍通过。

四组码本active全为256/256/256，无坍塌；边际熵总和A21.322/B21.160/C21.152/D21.002bit。
候选熵略低不代表音频差，稀疏联合熵更不是“24bit减去它”的可用容量。投影RVQ的
latent残差可能逐层上升，不能直接等同音频失败；部分层解码很差，例如D只用一层
SI-SNR−36.624dB、两层−4.083dB，完整三层6.644dB。没有800/1600bps可伸缩产品声明。

最终决定是结束本轮，保留候选及全部原始证据，保持v2冻结、不新评sealed。没有明确
故障可修复，也没有正当理由只重跑弱control、换seed或加新因素，因此不自动登记
CHAMPION7，不启动容量匹配训练来绕开失败的确认门槛。以后若继续，先制定新的对照
稳定性/训练随机性诊断方案并在结果前预注册，再讨论机制归因或promotion。按停止
规则移除既有监控，不创建重复任务。全部历史与本轮best/last、teacher、共同source
和已评测终点均保留，没有重复旧301文件清理。

完整逐seed结果、四分量、门槛判断、曲线/损失、RVQ与最终SHA见
[CHAMPION6_RESULTS.md](CHAMPION6_RESULTS.md)；机器可读证据在同名.audit，审计脚本
`scripts/audit_champion6_results.py`可重复检查但不训练。四条complete记录在
[EXPERIMENT_LOG.md](EXPERIMENT_LOG.md)。本轮没有单独逐minibatch分量文件，实际20次
验证分量和原pipeline完整保留，不事后虚构日志。

## 15. 用户改为分数导向：从最高分父模型做四组微调

2026-11-06用户明确表示比赛以分高为主，批准下一轮四组并要求尝试共享GPU。这改变
后续探索目标，不回改上一轮“确认门槛未完整通过”的历史。本轮不再重复波形对照或
种子确认，也不以46.25控制门槛否决涨分探索；合规、真实评测与如实披露仍保留。

四组都从CHAMPION6 B的51.624336权重出发，即已经从零训练过50万步的Fourier+GRU
codec与判别器；源SHA为c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23。
保留全部模型和RVQ码本/EMA状态，只重建优化器。因此这次是明确的有监督继续微调，
不是重新初始化。A保持原损失，B把SI-SNR损失.003提高至.010，C把GAN对抗权重.05提高
至.10，D同时提高；FM固定1.5。目标是低LR继续精修、加强保真、加强自然度以及找平衡。
不能保证权重提高就一定改善对应PESQ/UTMOS，最终直接比较真实课程总分与四项分量。

统一新增10万步、batch32/2秒、seed/data-order20261106；G/量化投影lr5e-5、1k warmup
后cosine至1e-5，D lr5e-5；完整GAN从第1步开启，不重复原始课程的10万步无GAN预热。
原394988训练/14596验证文件不变，不把固定200开发音频混入训练。参数和推理结构不变，
仍1868064参数、666.3072总/257.632解码MFLOP/s、16kHz/10ms/24bit/2400bps/30ms信息上限。

提前固定新增2.5万、5万、7.5万、10万步四节点，四组共16个权重，全部真实编码/解码
后按开发集总分择优，不再按重建best选择；累计父模型训练量分别52.5万至60万步。
保留所有节点并披露全部分数/折中，不能把这种开发集调参说成盲测确认。原51.624336
父模型也保留为回退：如果16个都没超过它，就说本批没有涨分。无新sealed评测、
自动替换v2或无止境追加批次授权。训练完成后再比较各组和父模型，展示最高分重建目录。

最初四卡只有约7.2/11.2/11.2/11.2GiB空闲。按用户要求在GPU1做一次完整batch短测，
父codec211/判别器80个张量全部加载成功，但进入计算后free8039MiB低于8GiB保护线，
只停止自己的测试组并释放显存，没有OOM，也没有操作别人的训练。没有靠静默缩小
batch或降低保护线硬挤。随后外部占用自行下降，四卡各约22GiB空闲，满足正式启动。

方案与CPU证据提交推送35e7e05后，四组于北京时间13:21在codec_champion7_v1启动。
原35项CPU回归7.98秒、新7项流程测试1.80秒均过；正式启动前每组完整batch/fullGAN
两步反向均通过，allocated5611.93/reserved6382MiB，见CHAMPION7_PROFILE.audit。
正式训练仍从原父权重而非两步smoke状态启动，无resume。目前每卡约15GiB空闲，
共享下初期约2.5–2.7步/秒，10万步粗估10–12小时再加评测；外部负载变化会改变时间。
保留20GiB启动、8GiB运行及磁盘10GiB保护，只停本组私有进程组。没有清理旧权重或
新下数据；原监控早已结束，本批只建一个新监控跟踪启动/完成/异常。

新批次尚无质量结果。可复查计划为[CHAMPION7_PLAN.md](CHAMPION7_PLAN.md)，学习权重
谱系、配置和数据哈希见CHAMPION7_SETUP.audit；四条原生记录在EXPERIMENT_LOG.md。

### 15.1 共享显存突增后，改为真正空闲GPU排队

本轮刚运行约35分钟，外部多卡任务显存上涨，13:56–13:57四组依次触发安全停机；
当时GPUfree最低为0卡257MiB、其余1309MiB。监督器只停止我们自己的进程组，未操作
外部训练。没有OOM、Traceback或非有限loss，但也没有正式权重快照：最后可见进度
约A5802/B5991/C6049/D6111步，尚未到首次25k验证保存点。因此这些更新无法恢复，
不能把接下来重新加载父模型说成“接上6000步”。本次约35分钟计算单独计为遗失的
未保存尝试，后续保留模型的累计步数仍按原父500k+新阶段局部步数报告。

已复制归档首轮原始日志、元数据、有效配置及lineage并记录SHA，见
CHAMPION7_RECOVERY01.audit和各run/attempts/attempt01_safety_stop；没有删除任何历史
或当前权重。由于先有短测容量保护、后有正式共享显存突增，四组现在改为idle-only
等待：不再传--allow-shared，等该卡真正没有其他GPU进程且free>=20GiB才自动开始，
8GiB运行/10GiB磁盘保护不变。此时排队不占GPU计算；不趁对方训练某阶段暂时释放
显存再反复启动。没有暗改batch、seed、损失或100k预算，也没有质量结果驱动重试。

仍使用原codec_champion7_v1和同一条监控。只为这四个已停且未保存的受影响任务
重新加载原51.624336父模型；后续一旦有last就必须从last恢复。GPU profile已完整
通过的证据保留，但不会加载smoke作为正式起点。原启动脚本只给首窗口设置保留，
本次也修正为每个窗口单独remain-on-exit，避免退出窗口消失造成状态误判。

### 15.2 空卡只是任务交接间隙，增加连续空闲10分钟判断

15:09前后原外部任务结束，四个等待器按无PID条件开始加载，但15:11另一项多卡
任务2016678接入，独占保护再次停止我们自己的进程。当时还有约44GiB free，所以
此次不是显存耗尽或OOM；触发原因是其他GPU进程出现。没有观察到新的epoch优化
迭代、验证或正式checkpoint，首次约6000步未保存进度也没有凭空恢复。

第二次加载日志/metadata已单独归档并记录SHA至CHAMPION7_RECOVERY02.audit，第一轮
证据不覆盖。教训是“两次查询时没有PID”可能只是别人任务切换，并不能保证长期
可用。现改为连续观测600秒无其他GPU进程且空闲>=20GiB才启动，任何不满足的采样
重置计时；每30秒等待检查，不占GPU。运行时仍每2秒查8GiB保护及磁盘10GiB底线。
新增5个纯时间/状态测试和原7个流程测试通过后，重新放入同一空闲队列；不降低batch、
阈值或修改课程/评分节点，不试图影响外部训练，也不重新启动健康或完成的组。

### 15.3 连续空闲仍不代表有预约：暂不自动重开，询问资源策略

16:40四组通过连续空闲窗口正式优化，约16:47到1575 batch时又有外部GPU进程接入。
当时仍约38GiB空闲，所以这次依然是独占规则触发，而非显存不足或OOM；日志无
Traceback/non-finite loss。尚未到首次25k保存点，这约6分40秒更新也无法恢复，
不能和原父500k合成已保留训练量。第三轮日志/metadata/SHA单独保存在
CHAMPION7_RECOVERY03.audit和各run/attempts/attempt03_exclusive_guard；前两轮不覆盖。

现在四组均已停，**没有正在运行的训练或容量等待器**，不再反复自动重开。向用户
提出两个选择：显存充足时允许共享，保留8GiB底线并增加恢复快照，或继续等待真正
独占空卡。用户回复前不改资源策略、保存频率或训练设置，原51.624336权重保持原样。
这只是计算资源协调问题，本轮还没有新评测分数，不能据此判断损失微调有没有效果。

### 用户确认改为有容量就共享，并加强断点保护

用户随后明确选择显存充足时共享、保留8GiB底线并增加恢复快照，又补充“有空闲就训”。
因此不再因外部PID出现而中断，也不等待600秒独占；20GiB启动和8GiB运行/10GiB磁盘
保护不变。只为本批启用每1000步原子保存last（模型、码本EMA、两个优化器和进度），
不增加评分节点、不虚构验证历史。写入中断仍有上一份完整last；未来恢复不保证worker
随机裁剪逐bit一致。现无last，本次仍从51.624336父权重重新开始；旧未保存尝试不计入
成品训练量。四组模型/损失/种子/100k预算不变，仍只做已批准的16节点开发集搜索。

代码变更前后共56项CPU回归/保存恢复检查通过11.33秒。用户随后要求停止额外测试，
故已取消独立完整batch恢复短测，只停止自己的短测进程组；保留证据，不冒充通过。
正式四组直接恢复共享排队/训练，仍使用原四组完整fullGAN profile和51.624336父权重，
不会加载短测更新。监控同步取消独占条件；尚无本轮新评分，完成后再汇总全部16节点。

### 第四次显存保护已有真实断点，不再丢失整段训练

北京时间11月7日01:07外部显存占用上涨，实际空闲降至4600/2561MiB，四组按8GiB
底线停止自己的进程组；这不是独占PID策略。最近完整权重分别保留到A7.5万、B7.6万、
C/D7.3万步，模型、码本EMA与两个优化器完整；A/B已验证三次，C/D两次，尚无新评分。
本次只从各自last恢复，不从51.624336父权重重来，也不额外增加10万步预算。原日志、
metadata、配置、恢复/验证记录及last副本按SHA归档至attempt04，汇总RECOVERY04.audit。
当前空闲约8–12GiB，重新排队等待20GiB启动条件，仍允许共享、保留8GiB保护，不做新
GPU测试或操作他人任务。恢复的worker裁剪/RNG并非逐bit一致，少于1000步的末段更新
未保存就丢弃，最终报告须披露；全部16个开发集选模节点和父模型回退项仍不变。

### 用户选择：不再实时监测资源，实际中断后再处理

用户随后明确要求“只要有空间就去训练，不用实时检测，断了再说”。因此把本批启动
门槛改为GPU空闲8GiB（已有完整GAN实测峰值约6.4GiB，另留约1.8GiB）和磁盘10GiB，
启动后不再GPU/磁盘实时轮询，不会因剩余不足8GiB主动停训。占卡者查询为服务器账号
wangzixuan的船舶类型分类任务；仅回答账号与命令，不对其任务作任何操作。共享可能
遇到外部后续涨显存或真实OOM，届时按实际错误诊断，不盲目无限重试。
只替换4个确认没有训练子进程的旧等待器，仍从A7.5万/B7.6万/C、D7.3万步的完整权重
和两个优化器续训，没有额外优化丢失；每1000步原子恢复保存不变。policy05审计和旧
等待器日志另行归档；模型、码本EMA、loss/seed/data、100k总预算和16评分节点不变。
同一监控只做低频进度/退出检查，不再主动套回旧20GiB启动或运行8GiB保护规则。

## CHAMPION7最终复盘：四组微调完成，原51.6243模型仍最高（2026-11-07）

### 这轮究竟训练了什么

四组不是从零训练，也不是从46.7463的v2直接微调。共同父模型是CHAMPION6 B、
500000步、固定200开发集51.62433613863932，权重在
`runs/champion6_b_s3407_fourier_gru/checkpoints/last.pt`，SHA256
`c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23`。
完整继承codec、RVQ/EMA和判别器；最初新阶段重新建立优化器，后续真正断点恢复则
连同两个优化器一并继承，不重置、不再从父模型重开。资源恢复不增加阶段总预算。

模型始终是Fourier+encoder GRU架构，包含原波形encoder、latent TCN、analysis GRU、
3×256码字的投影RVQ（48/64/80维）与Fourier合成；320采样点块、160点hop、IRFFT/OLA。
接口仍16kHz单声道、160samples/10ms、每帧24bit/3byte=2400bps；参数1868064，
总666.3072、decoder257.632MFLOP/s，lookahead30ms，unclassifiedMAC0。计入GRU门、
调制和保守IRFFT/OLA，不因改loss而改变推理模型或外部码流。

同一394988训练/14596验证文件，seed/data-order20261106；每组追加恰好100000步，
batch32×2秒、8workers，G及VQ投影lr5e-5，1000步warmup后cosine到1e-5，D固定5e-5，
fullGAN从局部0开始、clip G1/D10、weight_decay1e-6、feature matching1.5。四组仅
SI-SNR/GAN loss权重不同：A .003/.05，B .010/.05，C .003/.10，D .010/.10。

### 全部16个开发集节点，而非只报最好的一行

每组25k/50k/75k/100k四个预登记节点（累计父525k/550k/575k/600k），先训满再评测。
同一固定200文件真实编码/解码/四项指标，取实际总分最高、平分取更早，非重建best。
这是分数导向探索，不是盲测或固定终点确认，不再套旧控制门槛/+.15分量否决规则。

|组|25k分数|50k分数|75k分数|100k分数|选中步|最高分对父变化|
|---|---:|---:|---:|---:|---:|---:|
|A继续微调|51.0800800093|51.2138388551|51.0853351137|51.5259032012|100k|-0.0984329374|
|B加强SI|50.7468691381|50.8997952307|51.1328496496|51.5312875097|100k|-0.0930486289|
|C加强GAN|49.6449242717|49.5407160274|50.2461730349|50.2141828845|75k|-1.3781631038|
|D同时加强|49.3555956028|49.6771234055|49.9238243409|50.0014519218|100k|-1.6228842169|

**这轮没涨分，最高的新模型B仍比原51.624336低0.093049。** 因此保留原父模型，
不拿较低的新结果替换。A/B接近父模型不能算成功；GAN加倍分支本轮不受支持。

|各组选中结果对父模型|ΔPESQ|ΔESTOI|ΔSI-SNR dB|ΔUTMOS|
|---|---:|---:|---:|---:|
|A|-0.02319401|+0.00197083|-0.02185516|+0.00506035|
|B|-0.00857160|-0.00380922|+0.31057453|-0.02091224|
|C|-0.09717699|-0.01032609|-0.18401914|-0.04974041|
|D|-0.10690708|-0.01551310|+0.12238926|-0.08766849|

B确实更保真一些（SI-SNR），但PESQ/清晰度/自然度折中后总分没升；不是所有分量都
提升。仅能描述这个父模型、种子和预算下的结果，不推成普遍loss规律。多节点反复
开发集择优有乐观偏差；资源恢复worker裁剪/RNG非逐bit重放，也不宜把小差异当严格
因果消融。未新增sealed评测，CHAMPION6原确认结论不回写。

### 审计、恢复和试听

4组各4次真实25k验证（GAN factor1）、16节点+4主记录均complete；逐文件CSV重算总分
与汇总差<1e-10。每节点200文件、16197971采样点、101286帧、303858实际字节，
逐文件3×ceil(samples/160)，16k单声道、原始解码长度且音频有限；全部权重SHA对应。
4个选中模型均完整走analysis_gru及synthesis诊断，3层各256码字全活跃；只有完整3级
解码正常，前缀1/2级显著变差。保留负残差代理变化和熵估计偏差，不捏造额外bit容量。

初始attempt01约6000步/35分钟和attempt03约1575批/6分40秒未保存，更新丢弃；
attempt02只加载阶段未观察到新优化。后启用1000步原子last，attempt04实际显存保护后
从A75000/B76000/C73000/D73000恢复，末段约376/228/451/677可见更新丢弃；模型和两
优化器保留。用户后来明确取消运行中资源检测，policy05只替换等待器，无额外训练
中断；最终顺利训满100k。原始日志、metrics、恢复事件、全部历史档案/权重都保留。
未启用的独立逐batch分量日志不补造；被用户取消的恢复短测不称通过，不作正式起点。

原音目录：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/fast_b64_2s_v1/validation_200`。
仍最高的父模型重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion6_b_s3407_fourier_gru/evaluation/reconstructed`。
本轮最佳B重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion7_b_si/evaluation/step_00100000/reconstructed`。

完整16行四分量、20记录、SHA/数据/码流/复杂度/RVQ/恢复证据见CHAMPION7_RESULTS.md/.audit
和EXPERIMENT_LOG.md。冻结v2仍46.746343、其登记及权重未动；不自动晋升、不清理历史
快照、不自动开下一批。完成归档并删除本批监控，需要下一轮先由用户批准方案。

## CHAMPION8完整复盘（2026-11-08，零训练解码器插值）

# CHAMPION8结果：四个零训练解码器插值候选

最高新候选c_from_b10，51.6670665400，比父模型增加0.0427304014。

## 设计和来源

父模型CHAMPION6 B500k固定200开发分数51.62433613863932；donor为CHAMPION7 A/B的预登记100k快照（累计600k），分数51.52590320119037/51.53128750969333。
本批无训练、无优化器更新、新增梯度步数0，不是未训练初始化。参数=(1-alpha)父+alpha donor。
只混合98个decoder/synthesis可学习参数，其余113个张量，包括encoder/analysis GRU/latent norm、整个RVQ输入输出投影/码本/EMA及所有buffers逐位保持父模型。
导出inference_only权重，global_step0仅表示后处理新增训练步0，不含误导性的旧优化器/判别器。三份源文件SHA前后不变，完整来源及候选SHA见CHAMPION8_RESULTS.audit/SETUP.audit。

## 全部四个固定开发集搜索点

|候选|donor占比|总分|Δ对父|PESQ|ESTOI|SI-SNR dB|UTMOS|
|---|---:|---:|---:|---:|---:|---:|---:|
|a_from_a10|0.10|51.6668349080|+0.0424987694|2.22779456|0.76857699|6.62242095|3.12694974|
|b_from_a25|0.25|51.5912817421|-0.0330543966|2.22484219|0.76800446|6.63356212|3.11941139|
|c_from_b10|0.10|51.6670665400|+0.0427304014|2.22774523|0.76839200|6.62010526|3.12801473|
|d_from_b25|0.25|51.5418788401|-0.0824572985|2.21925043|0.76739512|6.62248489|3.12144259|

|对父变化|ΔPESQ|ΔESTOI|ΔSI-SNR dB|ΔUTMOS|
|---|---:|---:|---:|---:|
|a_from_a10|+0.00409746|+0.00019011|+0.02211079|-0.00085451|
|b_from_a25|+0.00114508|-0.00038243|+0.03325196|-0.00839286|
|c_from_b10|+0.00404812|+0.00000511|+0.01979510|+0.00021048|
|d_from_b25|-0.00444667|-0.00099177|+0.02217473|-0.00636166|

只按总分择优，四分量退步如实列出，不声称全分量支配。只有四个登记系数，没有追加alpha、搜索seed、微调或选择性扩展。
这是同一开发集四点搜索，不是独立测试提升证明；小增益可能有开发集择优偏差。不更改CHAMPION6确认结论。

## 实际码流、接口和审计

每候选实际重新编码/解码200文件，逐文件码流均与父模型字节完全相同（不仅张量冻结），每文件3×ceil(samples/160)字节。
每候选16197971samples、101286frames、303858实际字节；16k单声道、原长度、音频有限。CSV独立重算四分量及总分与summary差<1e-10；4条实验记录complete且对应权重SHA。
所有候选1868064参数、666.3072total/257.632decoder MFLOP/s、2400bps、lookahead30ms、unclassifiedMAC0；包含GRU门/调制/保守IRFFT/OLA。
RVQ及编码逐tensor和全部实际码流不变，未重复跑RVQ GPU消融，父模型完整analysis_gru/synthesis/RVQ诊断仍保留；不能据此声称新decoder的残差代理诊断已重测。
仅运行必要CPU参数检查（8项1.79秒通过）和解析复杂度/真实评测，没有GPU smoke、反向训练或新的25k训练验证记录；未启用的训练日志不补造。
共享资源只启动前检查8GiB显存/10GiB磁盘，运行中无GPU/磁盘轮询、无外部PID触发停止。无训练恢复或RNG重放；本批实际失败/恢复情况见4个pipeline/state记录。
未新增sealed LibriTTS评测，冻结strong_baseline_v2登记/权重保持46.746343不变，未自动晋升；保留所有来源和候选，不清理历史。

## 试听与下一步

原音：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/fast_b64_2s_v1/validation_200`。
本次总分选用模型：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_c_from_b10/checkpoints/interpolated.pt`。
选用重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_c_from_b10/evaluation/reconstructed`。
四候选分别在`runs/champion8_CELL/evaluation/reconstructed/`，文件名与原音相同。
完整证据CHAMPION8_RESULTS.audit、CHAMPION8_SETUP.audit、EXPERIMENT_LOG.md；预注册CHAMPION8_PLAN.md。
本批仅完成这四个零训练候选，不自动增加系数或开始低LR短程微调；下一批训练需用户另行批准。

## CHAMPION9新建模实验已启动（2026-11-08，结果尚待训练）

用户最终批准编码器全部取消独立latent TCN，仅比较分组卷积4/8与解码端TCN0/2层。
四组于北京时间2026-11-08约10:36在tmux codec_champion9_v1正式启动，实际epoch1优化进展、有限loss、
step0来源/config/metadata和启动前容量证据在CHAMPION9_LAUNCH.audit；不是只排队或只加载。

|cell|GPU|encoder groups|decoder TCN层数|total MFLOP/s|decoder MFLOP/s|
|---|---:|---:|---:|---:|---:|
|a_g4_d0|0|4|0|540.9538|236.960|
|b_g8_d0|1|8|0|524.8258|236.960|
|c_g4_d2|2|4|2|561.6258|257.632|
|d_g8_d2|3|8|2|545.4978|257.632|

新编码器：16kmono→k7因果入口→通道8/16/32/64/160、步幅2/4/4/5的4级残差下采样。
每级3个残差单元，膨胀1/3/9，SnakeBeta→分组k3卷积→SnakeBeta→dense1x1混组→残差；
下采样前另有SnakeBeta、kernel2stride和左padding=stride。随后逐帧LayerNorm→一次前瞻→单向残差GRU160→
原projected RVQ（3级256码字、48/64/80维）。编码analysis_temporal只含前瞻，blocks为空，不含独立TCN。
解码端可选原2层因果TCN，再接同一Fourier结构（256宽、160hidden、8因果调制块、320点IRFFT/hop160/OLA）。
所有权重随各组一起从头训练，“解码器不变”指结构不改，不是冻结旧权重。

这是对比赛冠军公开分组残差卷积/GRU思路的课程适配，并非其24k/20ms/不同码本的逐层复现。
前瞻预算统一改为2帧20ms，加10ms packet成帧=30ms总算法延迟，不把原报告30ms总延迟错当额外前瞻30ms。
历史51.667分数仅作回退参照，不能将新旧差异归因于单一因素；四组内部前瞻/损失等完全一致。
每10ms恰好3bytes/24bit=2400bps，解码不读下一帧；CPU前缀/扰动与实际码流测试验证边界和原长度。
计算量除Conv/Linear/GRU/RVQ外，计入GRU门、调制、保守IRFFT/OLA，以及SnakeBeta每元素36和每通道每调用65
操作的透明预算（sin/exp各按32），不是实测超越函数延迟；unclassifiedMAC0，各组均满足总700/decoder300限制。

seed/data-order20261108，所有codec/RVQ和D均新构造，global_step0；GRU/Fourier种子20461108（GRU内部+1），
D种子20361108，新decoderTCN种子20561108。相同形状初态配对共享，分组卷积形状不同时单独构造；
A/C、B/D共有模型张量相同，新增TCN为零输出残差，step0码流/音频一致。所有码本尚未kmeans、EMA更新计数0。
正式init只来自runs/champion9_setup/step0_CELL.pt，绝非C6/C7/C8已训练权重或烟测权重；源快照和历史模型哈希保留。

各组500000总步、batch32×2s/8workers、同394988train/14596valid，G/VQ lr2e-4、5k warmup/cosine到1e-5，
沿用原重建/SI=.003/GAN=.05/FM1.5等损失，GAN100k开始、150k full，不添加teacher/bypass/mel或其它训练因素。
每25k验证64batches，共20次，保留全部20个step/best/last；每1000步原子恢复last不伪造验证。
恰好8个开发评分权重：每组250k/500k，先训满再评测两个预定快照，按真实总分择优、平分取早，非reconstruction-best。
相同固定200dev真实编码/解码和4项评分、303858bytes/101286frames/16197971samples、选中完整RVQ诊断及8节点+4主记录。
本批n=1训练种子，是开发分数搜索，不是多seed确认；无新增sealed评测或自动v2晋升，不自动开下一批。

必要CPU回归64项13.75秒通过，静态语法检查通过；遵守用户要求未做GPU烟测/fullGAN反向profile，不能冒称新架构显存峰值已测。
启动时四张A40都空闲约45GiB。延续用户资源政策：允许共享、启动前显存>=8192MiB/磁盘>=10GiB，之后不轮询GPU/磁盘，
不因他人PID或显存下降主动停训；每1000步恢复保存，真实退出后诊断，不盲目无限重试、不改batch/预算或干预外部进程。
恢复只用本组最新last并继承两个optimizer/EMA；worker/crop/RNG重放可能非bitwise，需记录丢弃进度和attempt证据。
本地baseline只读，所有训练在远端；计划CHAMPION9_PLAN.md，初态审计CHAMPION9_SETUP.audit，4条主记录当前running。
目前没有训练完成或质量提升结论。后续完成写CHAMPION9_RESULTS.md/.audit、更新历史/本复盘并推送；原51.667和所有历史权重均保留。

<!-- CHAMPION9_FINAL_ARCHIVE -->

# CHAMPION9结果：分组卷积编码器从头训练、解码器TCN消融

## 结论与实验边界

四组全部从未训练step0完成500000总步，无失败、无恢复、无丢弃更新；每组20次真实训练验证，20份step快照与best/last均保留。
所有组按预登记250k/500k两点开发总分择优，均选500k。A/B/C/D选中分数依次47.9394438295/48.6240098787/49.3182054970/49.7109807091。
本批最好D（groups8、decoderTCN2）49.7109807091，相对历史最好51.6670665400下降1.9560858310分，四项均退步；保留CHAMPION8 c_from_b10作为整体回退。
在相同步数下，解码器TCN两个分组条件都增加总分；4→8组也均增加总分，但SI-SNR均下降，不能称全分量更好。
新编码器/激活/前瞻与历史均不同，新旧对比不是单因素。单seed20261108、固定200开发集搜索，非多seed或独立测试确认，不能宣称统计显著。
没有额外节点、延长、teacher、dev训练、sealed LibriTTS或自动晋升；strong_baseline_v2登记仍46.746343，不开始下一批。

## 模型、初始化与训练（自包含）

16k单声道→k7左因果入口→4级分组残差/下采样，通道8/16/32/64/160、步幅2/4/4/5。
每级3个残差单元、膨胀1/3/9：SnakeBeta→grouped k3→SnakeBeta→dense1x1混组→skip；下采样kernel2s、leftpad=s。
逐帧LN→一次2帧20ms有限前瞻→单向残差GRU160→原projected RVQ3×256、投影48/64/80。
编码独立TCN全为0（analysis_temporal.blocks为空）；decoderTCN0/2后接原Fourier256/hidden160/8因果调制块、320IRFFT/hop160/当前hop OLA。
这是公开冠军思想的可复现适配，不冒称逐层复刻。所有解码权重也从头训练，结构保持不等于冻结旧模型。
10ms成帧+20ms前瞻=30ms总算法延迟；解码不等下一个latent，160samples/帧、24bit/3bytes、2400bps，无隐藏旁路。

codec/RVQ/D真正全新构造global_step0；正式初态仅runs/champion9_setup/step0_CELL.pt，NOT C6/7/8或smoke。
seed/data-order20261108；D20361108；GRU/Fourier20461108（GRU内部+1）；新增decoderTCN20561108。
初态码本initialized全FALSE、EMAupdate_count0；A/C、B/D相同键逐tensor一致，零输出新TCN令配对step0码流/音频一致；不同group空间卷积形状独立构造。
初始优化器新建；本批实际未发生resume。setup/source/config/data/core-code原证据冻结未再生成，最终逐hash复核通过。

每组500000 TOTAL scratch steps、batch32×2s、8workers、394988训练/14596验证（VCTK40208/4247，LibriTTS354780/10349），非训练dev。
G/VQ lr2e-4，5000 warmup/cosine到1e-5，D固定2e-4、wd1e-6、clipG1/D10。
L1=1/spectral1/SC.25/linear.1/SI.003/commit.1/GAN.05/FM1.5；jointcodecRVQ从0，GAN<100k关闭，100k–150k渐增，之后full。
真实验证100k factor.00002、125k .50002、150k及以后1.0（实现按完成更新计入+1）。每25k验证64batches共20次，完整分量在audit。
每1000次完整G/D更新原子last、temp+fsync+replace；每组480个recovery_only事件、20次验证，未伪造metrics或新增搜索权重。
逐minibatch training_components日志未启用，不能从验证补造；保留原始pipeline与80条真实验证分量。
资源按用户最终政策共享，仅启动前>=8192MiB显存/10GiB磁盘检查，运行中无GPU/磁盘轮询或主动停训。未干预其它任务。
四个原tmux监督任务均exit0/complete；无重复启动、无actual OOM/Traceback/恢复，未保存更新丢失0；若未来恢复worker/crop/RNG仍可能非bitwise。

## 全部8个预登记开发搜索节点

|cell|step|总分|Δ历史最好|PESQ|ESTOI|SI-SNR dB|UTMOS|
|---|---:|---:|---:|---:|---:|---:|---:|
|a_g4_d0|250000|45.7075033539|-5.9595631861|1.97324715|0.73356779|6.35797189|2.63084974|
|a_g4_d0|500000|47.9394438295|-3.7276227105|2.08104682|0.74207971|6.47442160|2.81906794|
|b_g8_d0|250000|46.5026825269|-5.1643840131|2.00987372|0.73799604|6.19129239|2.71517441|
|b_g8_d0|500000|48.6240098787|-3.0430566613|2.10491566|0.75046587|6.35140197|2.88007717|
|c_g4_d2|250000|46.8049233144|-4.8621432256|2.00289926|0.74011889|6.37033248|2.74510834|
|c_g4_d2|500000|49.3182054970|-2.3488610430|2.14275988|0.75142720|6.49461644|2.92973114|
|d_g8_d2|250000|47.3925859441|-4.2744805959|2.03656015|0.74433846|6.18965539|2.80185420|
|d_g8_d2|500000|49.7109807091|-1.9560858310|2.15195896|0.75506487|6.33324945|2.98364798|

总分逐文件分别clip归一化再均值，不是先平均分量再裁剪：25×[clip((PESQ−1)/3.5)+clip(ESTOI)+clip((SI-SNR+10)/40)+clip((UTMOS−1)/4)]。
全部CSV四均值与总分独立重算误差<1e-10；每个节点完整四分量，不只呈现最好行。

## 同一步数的因素对照

|step|对照|Δ总分|ΔPESQ|ΔESTOI|ΔSI-SNR|ΔUTMOS|
|---:|---|---:|---:|---:|---:|---:|
|250000|c_g4_d2-a_g4_d0|+1.09741996|+0.02965211|+0.00655110|+0.01236059|+0.11425860|
|250000|d_g8_d2-b_g8_d0|+0.88990342|+0.02668643|+0.00634242|-0.00163700|+0.08667980|
|250000|b_g8_d0-a_g4_d0|+0.79517917|+0.03662657|+0.00442825|-0.16667950|+0.08432466|
|250000|d_g8_d2-c_g4_d2|+0.58766263|+0.03366089|+0.00421957|-0.18067709|+0.05674586|
|500000|c_g4_d2-a_g4_d0|+1.37876167|+0.06171305|+0.00934750|+0.02019484|+0.11066320|
|500000|d_g8_d2-b_g8_d0|+1.08697083|+0.04704330|+0.00459900|-0.01815252|+0.10357082|
|500000|b_g8_d0-a_g4_d0|+0.68456605|+0.02386884|+0.00838616|-0.12301963|+0.06100923|
|500000|d_g8_d2-c_g4_d2|+0.39277521|+0.00919908|+0.00363766|-0.16136699|+0.05391684|

500k时decoderTCN：C−A +1.37876167，四分量均升；D−B +1.08697083，PESQ/ESTOI/UTMOS升、SI-SNR−.01815252dB。
500k时groups8−4：B−A +.68456605、D−C +.39277521，均以PESQ/ESTOI/UTMOS改善换取SI-SNR下降。
250k亦同向总分，不能据单seed宣称可普遍复现。500k相对250k四组均提高，但预定预算已经耗尽，不据趋势自动延长。

## 约束、独立证据与真实损失

|cell|参数|总MFLOP/s|decoder MFLOP/s|总算法延迟|
|---|---:|---:|---:|---:|
|a_g4_d0|1548960|540.9538|236.960|30ms|
|b_g8_d0|1542840|524.8258|236.960|30ms|
|c_g4_d2|1653280|561.6258|257.632|30ms|
|d_g8_d2|1647160|545.4978|257.632|30ms|

总/decoder均满足700/300限制，unclassifiedMAC0。包括GRU矩阵及门、调制、保守IRFFT/OLA；新增SnakeBeta按36op/元素+65/通道/次（sin/exp预算32）。
解析运算口径不是实测超越函数延迟，其他历史激活/归一化约定未改。CPU因果/字节/兼容64项13.75s和语法检查启动前通过，遵守用户要求无额外GPU smoke/反向profile；新架构fullGAN峰值未测，不能引用C7旧profile替代。
最终审计为只读CPU证据复核，不重复训练或重跑质量评分。8节点×200文件实际码流每节点303858bytes/101286frames/16197971samples；逐文件3×ceil(samples/160)、16kmono原长度、有限音频。
每个节点checkpoint、CSV/summary/复杂度/roundtrip及1600组bitstream/metadata/重建音频SHA、所有80step/best/last、step0/source/数据/核心代码和12条complete记录均验证；细节在CHAMPION9_RESULTS.audit。

以下为500k真实训练验证及末段训练loss，不是200开发集四项评分，也非逐batch分量：

|cell|最后train loss|wave L1|spectral|commit|G adv|FM|D|reconstruction|总validation|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|a_g4_d0|0.46313370|0.01321233|0.12004301|0.07864516|0.70435774|0.12300132|1.56119311|0.13325534|0.43162037|
|b_g8_d0|0.47727005|0.01337217|0.11953437|0.09626066|0.64028704|0.12014861|1.56548381|0.13290654|0.44140448|
|c_g4_d2|0.47124181|0.01328886|0.11870530|0.09382330|0.75511783|0.11874101|1.61138785|0.13199417|0.44168487|
|d_g8_d2|0.47191344|0.01324466|0.11687496|0.08372565|0.64434260|0.12636243|1.60879028|0.13011961|0.43560604|

## 完整路径RVQ诊断

四个选中节点均沿encoder→LN→lookahead→analysis_gru→projectedRVQ→可选decoderTCN→完整Fourier/synthesis运行，非跳过GRU代理；三层均256个活跃码字。

|cell|3级perplexity|3级潜在MSE相对降幅|1/2/3级SI-SNR dB|
|---|---|---|---|
|a_g4_d0|115.601/111.031/104.606|+40.059%/-5.508%/-16.327%|-9.92384/-0.84898/6.47442|
|b_g8_d0|117.615/123.617/107.436|+0.562%/+16.621%/+9.412%|-19.08483/-5.23933/6.35141|
|c_g4_d2|111.738/122.475/109.940|+19.632%/+0.680%/+4.395%|-13.26416/-1.13593/6.49462|
|d_g8_d2|126.266/108.443/113.865|+39.997%/+26.619%/-2.992%|-17.26442/-0.34378/6.33325|

潜在MSE降幅并不保证波形目标单调：如D第3级潜在MSE反升约2.99%，但三层波形SI-SNR由−.344升至6.333dB；不能据此删除码本。
所有组三层partial结果与实码流SI-SNR差<1e-4dB。稀疏plug-in联合熵受log2(frames)上限/向下偏差影响，不把24减该值解读为可用空闲容量。

## 权重、试听与归档

原音：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/fast_b64_2s_v1/validation_200`。

- a_g4_d0选中权重：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0/checkpoints/step_00500000.pt`；SHA `84e2ae9ca427d2c0fe2bfd198ccafce93d0f5783a0113f05eda427264c4107c7`。
  重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_a_g4_d0/evaluation/step_00500000/reconstructed`。
- b_g8_d0选中权重：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0/checkpoints/step_00500000.pt`；SHA `7f42b0583d17dee046c1effe2e3041f468ec4bff2d7084cb6768ae46c7b87e10`。
  重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_b_g8_d0/evaluation/step_00500000/reconstructed`。
- c_g4_d2选中权重：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2/checkpoints/step_00500000.pt`；SHA `4925e325195dc480663cea2717a64dae4de23dfd2f9699768e9c956ba7f05e5f`。
  重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_c_g4_d2/evaluation/step_00500000/reconstructed`。
- d_g8_d2选中权重：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2/checkpoints/step_00500000.pt`；SHA `82e924efe948c517f4c74d2abeb0e93b4aed8ee6d01aabf01c572ef496aaf4a0`。
  重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion9_d_g8_d2/evaluation/step_00500000/reconstructed`。

整体仍选历史模型：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_c_from_b10/checkpoints/interpolated.pt`，SHA `a5cffa2dfcf39fc69b36b84e8ca238e7cbd9408ee008a1042bb7bbb253e4eb19`。
历史重建：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion8_c_from_b10/evaluation/reconstructed`，分数51.6670665400，四项PESQ/ESTOI/SI-SNR/UTMOS分别2.22774523/0.76839200/6.62010526/3.12801473.
本批最好D四项相对历史均低，未替换历史结论/权重/注册项。两个节点的原始bitstreams/reconstructed/metrics均留在各run/evaluation/step_00250000或step_00500000，文件名与原音一致。
保留所有历史来源/teacher/comparison/averaging/scratch和C4–9所有best/final/评测快照；本次无下载/清理/删除任何模型文件。
结果CHAMPION9_RESULTS.md/.audit，初始化CHAMPION9_SETUP.audit，启动CHAMPION9_LAUNCH.audit，预登记CHAMPION9_PLAN.md，完整记录EXPERIMENT_LOG.md。
本批归档完成后删除仅codec-champion9-monitor这一个监控，不启动下一批；下一实验需用户另行批准。

## CHAMPION10四格容量实验已入队，尚未实际训练（2026-11-10）

用户批准保持CHAMPION9D结构大致不变、增加容量的四组实验。预注册先提交推送，随后仅一次启动持久tmux codec_champion10_v1。
同新seed/data-order20261110：A原规模，B只扩encoder通道8/24/40/80/160，C只扩Fourier hidden184，D两端扩；A/C原encoder8/16/32/64/160，A/B hidden160。
统一groups8、encoder独立TCN0、decoder因果TCN2、GRU160、原3x256 projectedRVQ dims48/64/80、20ms前瞻+10ms成帧=30msTOTAL；16kmono/160sample/24bit3bytes/2400bps。
总/decoder MFLOP/s：A545.4978/257.632，B640.58436/257.632，C575.277/287.4112，D670.36356/287.4112；参数1647160/1699688/1796536/1849064，均满足700/300。统一解析口径含SnakeBeta/GRU/IRFFT/OLA，unclassifiedMAC0，不冒称实测算子延迟。
68项远端CPU形状、真实字节往返、强制前瞻/前缀因果、梯度和旧兼容回归28.78s通过；未做用户禁止的额外GPU烟测/反向profile，新扩容fullGAN显存峰值未测。
codec/RVQ/D真正未训练step0，码本initializedFALSE/EMAupdate_count0，初始优化器新建；无任何学得C6–9或smoke权重。相同形状配对精确共享，A/C、B/D step0音频/码流完全一致。来源/config/data/code哈希冻结CHAMPION10_SETUP.audit，不再生成。
每组500000TOTAL、batch32x2s/8workers、394988train/14596valid；全部损失、lr/warmup/cosine/clip/weightdecay和GAN100k开始150kfull保持C9。每25k/64batches真验证共20条、保留20step+best/last，每1000完整更新原子last恢复EMA/G+D优化器；不补造逐batch分量。
先训满500k再只评每组250k/500k共8节点，同冻结200dev16197971samples/101286frames/303858bytes，实码流/原长度有限16kmono音频与PESQ/ESTOI/SI-SNR/UTMOS四指标；按实际总分选择、平分取早。
同端点B-A/D-C编码容量、C-A/D-B解码容量单因素对照，n=1不是确认；对历史C9还含seed变化，不能当纯容量提升。C8历史最佳51.66706654001837及其SHA保持回退，v2冻结46.746343，不自动晋升/新sealed评测/下一批。

首次监督检查四张卡可用显存均约7.4GiB，低于原8GiB启动门槛，因此四组目前只有健康容量等待任务，尚无run_metadata、真实优化或质量结果。证据CHAMPION10_QUEUE.audit；真正开始后另生成CHAMPION10_LAUNCH.audit，不能将本次排队当成训练启动。
监督器每30s仅启动前检查free>=8192MiB/disk>=10GiB，允许共享而不排斥其它PID；启动后child.wait，无GPU/磁盘运行期轮询，不停止其它任务、不改batch、不盲目重试。实际退出后先诊断和留证据，仅受影响组从最新自己的last恢复，仍500kTOTAL；无last披露丢失并从新step0重启，worker/crop/RNG重放非bitwise需披露。
保持一个低频监控，健康进展/不变等待静默；结果、失败/恢复/完成或需决定时通知。最终独立审计8节点+4主记录、80step快照、CSV重算/字节音频SHA/配对效应/全路径RVQ，写CHAMPION10_RESULTS.md/.audit，追加历史和中文复盘并限定commit/push main。保护所有历史权重，本地baseline只读，无清理/下载。完成删除仅本批监控，下一批另获批准。

## CHAMPION10部分真实启动：B/D已优化，A/C仍容量等待（2026-11-10）

同一tmux codec_champion10_v1、原四个监督进程未替换。D（两端加宽）随后B（仅编码器加宽）自行满足启动容量后进入正式scratch训练；A（原规模）、C（仅解码器加宽）仍由原健康监督器等待。未停止外部任务、未改batch或门槛、未增加GPU烟测/反向profile、未查询运行期显存/磁盘。
B/D的run_metadata确认从本批各自真正未训练step0启动，resume_checkpoint=null；pipeline有真实优化和有限loss，不是只加载。CPU只读检查原子last文件，证据CHAMPION10_PARTIAL_LAUNCH.audit：

|cell|审计last完整更新step|可见有限loss（日志滚动值，非开发评分）|
|---|---:|---:|
|b_enc|4000|0.5409|
|d_both|6000|0.2359|

检查点的model_config与冻结配置一致，RVQ update_count等于global_step、三层码本已由训练初始化，G优化器状态非空，D优化器对象保留但100k前状态为空符合GAN关闭计划。epoch/batch/model/RVQEMA/buffers/G+D优化器均在last内。没有resume事件、没有到25k，因而没有伪造验证、没有开发质量分数。
本批继续同seed20261110的2x2容量对照：groups8/encoderTCN0/decoderTCN2/GRU160/RVQ3x256/20ms前瞻不变，总延迟30ms、2400bps；B/D只扩encoder，C/D只扩Fourier hidden。每组仍500000TOTAL、batch32x2s/8workers，全部原损失和GAN100k–150k计划不变；先训满500k再只评每组250k/500k，共8节点，实际分数最高选择。历史C8回退不变，不启动新批次。
CHAMPION10_QUEUE.audit仍是最初四组等待的历史事实；本次partial审计不能当成四组全部启动。只有日后A/C也观察到真实有限优化时才运行一次capture_champion10_launch.py生成CHAMPION10_LAUNCH.audit；不得为补齐启动记录重跑launch/preflight或替换健康等待者。最终统一审计8节点、4主记录、80step快照和完整RVQ后另写结果与中文复盘。

## CHAMPION10四格容量实验已实际启动（2026-11-11取证，暂无质量结论）

用户批准结构大致不变、用更多计算容量，四组为新原规模对照/仅编码加宽/仅解码加宽/两端加宽。
同新seed/data-order20261110，从真正未训练codec/RVQ/D step0开始，初始优化器新建；非C9旧seed重跑、非已训练模型微调。
四个tmux codec_champion10_v1监督任务均已看到实际优化和有限loss，证据CHAMPION10_LAUNCH.audit。取证时A/C为epoch3，B/D为epoch10；各组异步开始，非同时启动。A/C已有25k真实验证，B/D已有100k真实验证并进入GAN渐增阶段；这些是训练验证记录，尚无开发集质量评分。

|cell|GPU|encoder channels|Fourier hidden|total MFLOP/s|decoder MFLOP/s|
|---|---:|---|---:|---:|---:|
|a_base|0|8/16/32/64/160|160|545.49780|257.6320|
|b_enc|1|8/24/40/80/160|160|640.58436|257.6320|
|c_dec|2|8/16/32/64/160|184|575.27700|287.4112|
|d_both|3|8/24/40/80/160|184|670.36356|287.4112|

其余结构全固定：groups8、k7入口、4级stride2/4/4/5、每级3个SnakeBeta/groupk3/dense1x1残差dilation1/3/9，无编码独立TCN。
LN→一次20ms前瞻→GRU160→原3级256码字projectedRVQ dims48/64/80→原2层decoderTCN→Fourier width256/8块/320IRFFT/hop160/当前hop OLA。
只扩中间encoder通道和Fourier hidden160/184；末端160、码本、GRU、前瞻与损失不变。10ms成帧+20ms前瞻=30msTOTAL，16kmono/160samples/3bytes/2400bps。
CPU计数包含GRU矩阵/门、调制、保守IRFFT/OLA及SnakeBeta36op/元素+65/通道/调用，unclassifiedMAC0，总700/decoder300均满足；不是实测算子延迟。
全新A共同来源、不同形状fresh，D编码来自新B其它来自新C；各单因素对照其它tensor精确一致，较宽decoder零输出残差使A/C、B/D step0音频和码流一致。
所有保存初态码本initializedFALSE/EMA0，新source/config/data/core-code哈希冻结SETUP.audit，禁止正式启动后再生成；D种子20361110、GRU/Fourier20461110（GRU内部+1）。

每组500kTOTAL scratch，batch32×2s/8workers、394988train/14596valid。G/VQ2e-4、5kwarmup/cosine1e-5、D2e-4、wd1e-6、clipG1/D10。
沿用L1=1/spectral1/SC.25/linear.1/SI.003/commit.1/GAN.05/FM1.5，GAN100k开始150kfull；不加mel/teacher/bypass或其它新因素。
每25k验证64batches共20真分量，保留20step+best/last；每1000完整更新原子last含模型/EMA/G+D优化器，recovery事件不伪造验证，未启用的逐batch日志不补造。
先训满500k再评测每组250k/500k，恰好8开发搜索模型，按实际总分选、平分取早，非reconstruction-best，无选择性延长/额外种子。
固定同200dev，每节点16197971samples/101286frames/303858真实字节、16kmono原长度有限音频、4评分/CSV/复杂度/checkpointSHA/选中完整GRU-RVQ-synthesis诊断。
同端点B−A/D−C编码容量、C−A/D−B解码容量，n=1不是确认实验；历史C9比较含seed差异。旧C8最佳51.6670665400保留回退，v2冻结46.746343不自动晋升。
遵守用户不做额外GPU烟测/反向profile，新扩容fullGAN峰值未实测；只做必要CPU形状/真实字节/因果/梯度/旧兼容与原子恢复回归，结果见setup日志。
资源只启动前>=8192MiB显存/10GiB磁盘，不足30s容量等候；允许共享，不因其它PID排他。启动后child.wait，无GPU/磁盘实时轮询/主动停止，无batch降低。
真实退出才诊断/留attempt证据，仅恢复受影响组自己的最新last继承EMA/G+D优化器，仍500kTOTAL，worker/crop/RNG重放可能非bitwise；无last披露丢失并回新未训练step0，重复真实共享OOM诊断后等待空闲卡。
本地baseline只读，C4–9归档不重跑、不清理任何历史来源/模型；无sealed新评测。仅一个本批监控，健康进展静默。
计划CHAMPION10_PLAN.md、初态CHAMPION10_SETUP.audit、实际启动CHAMPION10_LAUNCH.audit、4主实验running记录已保存；暂未完成训练、没有质量提升结论。
完成写CHAMPION10_RESULTS.md/.audit，追加历史和中文复盘、限定commit/push，通知全组结果及确切试听目录并删除本批监控；下一批另获批准。

## CHAMPION10复盘：结构固定后的容量交互（2026-11-14，完整自包含）

### 问题与设计

本批回答一个很窄的问题：在 CHAMPION9D 的 groups8/encoder TCN0/decoder TCN2/GRU160/RVQ3×256/20 ms 前瞻结构上，只增加编码器中间通道与 Fourier hidden，是否能提高同一开发协议下的质量。2×2 四格为 A 原规模、B 只宽编码器、C 只宽解码器、D 两端都宽；共同 seed/data-order 为 20261110。A/C 编码器 8/16/32/64/160，B/D 为 8/24/40/80/160；A/B hidden160，C/D hidden184。

音频接口始终是 16 kHz 单声道、160 samples/10 ms、每帧 24 bit/3 bytes/2400 bps。编码器 k7 左因果入口、四级 stride 2/4/4/5、每级三个 dilation 1/3/9 的 SnakeBeta→grouped k3→SnakeBeta→dense 1×1 混组残差；逐帧 LN 后仅一次两帧/20 ms 有限前瞻，再经单向残差 GRU160 与 projected RVQ 3×256（48/64/80）。解码器保留两层因果 TCN、Fourier width256、8 调制块、320 IRFFT/hop160/当前 hop OLA。10 ms 成帧加 20 ms 前瞻就是全部 30 ms 延迟，没有额外未来缓存或隐藏信息。

四个 codec/RVQ/D 均真正从头构造 global_step0，无 C6–9 或 smoke 学得权重。step0 三码本 initialized=false、EMA cluster/embed 全零、无优化器状态；训练时创建全新 G/D 优化器。相同形状配对张量逐 tensor 相同，D 编码器来自新 B、其余来自新 C。所有 source/config/data/core-code 哈希在训练前冻结，正式运行后未重建。

训练固定 500000 TOTAL scratch steps、batch32×2 s、8 workers、394988 train/14596 valid。G/VQ lr 2e-4、5000 warmup/cosine 到 1e-5，D lr 2e-4、weight decay 1e-6、clip G1/D10。损失保持 L1=1、spectral=1、SC=.25、linear=.1、SI=.003、commit=.1、GAN=.05、FM=1.5；GAN 在 100k 开始、150k full。每 25k 做 64 batches 真验证，共 20 条/组并保留 20 个 step 快照；每 1000 完整更新保存可恢复 last。没有 teacher、bypass、mel、新损失或 dev 训练。

### 预登记节点与选择

| cell | 250k 总分 | 500k 总分（选中） | PESQ | ESTOI | SI-SNR | UTMOS |
|---|---:|---:|---:|---:|---:|---:|
| A | 46.50717350 | 49.13555767 | 2.11300890 | 0.75075382 | 6.43062383 | 2.94360138 |
| B | 46.75127764 | 48.86603385 | 2.12470738 | 0.74568221 | 6.29769476 | 2.92068724 |
| C | 47.28726093 | 49.54013766 | 2.15154193 | 0.75485216 | 6.60806503 | 2.93015894 |
| D | 47.68709449 | 50.21359275 | 2.16125861 | 0.75579438 | 6.58091334 | 3.02575330 |

所有组都在 500k 得到更高实际总分，因此选择 500k；没有增加节点、种子或选择性延长。D 是本批最好，较 A +1.07803508；较 CHAMPION9D +0.50261204，但该比较还改变 seed，不能视作纯容量提升；较历史 C8 最好仍 −1.45347379。

### 因素解释

500k 时只宽编码器 B−A 为 −0.26952382：PESQ +0.01169848，却伴随 ESTOI −0.00507161、SI-SNR −0.13292907 dB、UTMOS −0.02291414。相同编码器变化放到宽解码器上，D−C 为 +0.67345509，主要来自 UTMOS +0.09559436 和小幅 PESQ/ESTOI 增益，SI-SNR −0.02715169。编码器容量不是独立稳定的正效应。

只宽解码器 C−A 为 +0.40457999，PESQ/ESTOI/SI-SNR 提高但 UTMOS −0.01344244；在宽编码器上 D−B 为 +1.34755890，PESQ +0.03655123、ESTOI +0.01011217、SI-SNR +0.28321858、UTMOS +0.10506606，四项全升。本次最清晰信号是解码器容量与宽编码器的正交互，但只有 common-seed n=1，不能替代复现实验。

### 约束与训练证据

A/B/C/D 总 MFLOP/s 为 545.4978/640.58436/575.277/670.36356，decoder 为 257.632/257.632/287.4112/287.4112，参数为 1647160/1699688/1796536/1849064；全部 30 ms、unclassified MAC0，满足 700/300。该口径包含 GRU、调制、保守 IRFFT/OLA 与 SnakeBeta 解析预算，不冒称实测超越函数延迟；遵守用户要求未做新增 GPU smoke 或 fullGAN backward profile，扩容峰值显存仍未测。

四组 80 条验证均有限，GAN schedule 与预登记一致；最后 reconstruction A/B/C/D 为 0.13109472/0.13076279/0.13017110/0.12759528。每组 480 条 recovery_only 是周期 last 记录，不是恢复；实际 recovery event、resume、OOM、重启和丢弃更新均为 0。四个 last 均含非空 G+D 优化器与完整 RVQ EMA。

### 评测与 RVQ 审计

固定 200dev 仅来自 `runs/fast_b64_2s_v1/validation_200`。每个节点独立验证 200 files、16197971 samples、101286 frames、303858 bytes；逐文件大小严格为 3×ceil(samples/160)，重建均为 16 kHz 单声道、原长度、有限值。8 份 CSV 的四项均值和逐文件裁剪总分重算误差小于 1e-10；checkpoint SHA、复杂度、码流树和音频树均留在 `CHAMPION10_RESULTS.audit`。

四个选中节点的 RVQ 诊断位于各自 `evaluation/step_00500000/rvq_diagnostics.json`，而非 run 根目录。每层 256 个码字都活跃；A/B/C/D 三层 perplexity 分别为 118.759/116.291/112.500、126.210/119.225/128.956、124.918/114.274/113.955、117.314/120.169/113.218。潜在 MSE 有个别阶段反升，但完整三层波形 SI-SNR 与实码流评分误差小于 1e-4 dB，不能据局部潜在量删除码本。

### 决策与路径

本批不替换历史冠军。历史回退仍为 `runs/champion8_c_from_b10/checkpoints/interpolated.pt`，SHA `a5cffa2dfcf39fc69b36b84e8ca238e7cbd9408ee008a1042bb7bbb253e4eb19`，分数 51.6670665400。strong_baseline_v2 继续冻结，不做 sealed LibriTTS，不自动开下一批。

原音：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/fast_b64_2s_v1/validation_200`。

- A：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_a_base/evaluation/step_00500000/reconstructed`
- B：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_b_enc/evaluation/step_00500000/reconstructed`
- C：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_c_dec/evaluation/step_00500000/reconstructed`
- D：`/storage1/hehaoran/project/course-track2-codec-experiments/runs/champion10_d_both/evaluation/step_00500000/reconstructed`

完整数值、SHA 与审计定义见 `CHAMPION10_RESULTS.md`、`CHAMPION10_RESULTS.audit` 和 `EXPERIMENT_LOG.md`。下一实验必须先向用户申请批准。
