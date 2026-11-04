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
