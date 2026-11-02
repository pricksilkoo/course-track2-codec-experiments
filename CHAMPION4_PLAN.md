# 冠军思路实验：第一轮四组预注册方案

日期：2026-11-02。状态：实现与预检阶段；结果尚未产生。

## 问题与来源

借鉴 LRAC 2025 Track 1 冠军 teamwzqaq，验证其部分建模/训练思路能否改善本项目
16kHz、10ms/帧、每帧3字节的2.4kbps codec。
来源：[冠军原始报告](https://crowdsourcing.cisco.com/lrac-challenge/2025/assets/files/2025_lrac_challenge_technical_report_track1_and_track2_teamwzqaq.pdf)。

冠军用了卷积调制式 Conv2Former 解码器、ISTFT 合成、半数迭代绕过量化、后期减小
mel 损失权重等方法。其配置为24kHz、20ms/帧、1/6kbps，因此本轮是有控制的适配，
不能称为冠军模型的完整复现，也不能将其71.91主观分与我们的开发集分数直接比较。

## 第一轮：2×2设计

| 组 | 配置 | 训练改动 | 解码建模改动 |
|---|---|---|---|
| A | `configs/champion4/a_control.yaml` | 原训练目标续训 | 原解码器 |
| B | `configs/champion4/b_training.yaml` | 50%量化旁路 + 分阶段mel | 原解码器 |
| C | `configs/champion4/c_conv2former.yaml` | 与A相同 | 新增4个因果卷积调制块 |
| D | `configs/champion4/d_combined.yaml` | 与B相同 | 与C相同 |

本轮明确采用**同一个已训练权重续训**，不是此前 lookahead 研究的从零实验。
每组从冻结 strong_baseline_v2 的同一份 codec 和 discriminator 状态出发，重置优化器，
新增模块零初始化而保持初始函数一致。理由是先低成本检验可迁移收益；如进入全新
ISTFT合成架构，再安排有正对照的从零长训，不让随机解码器与成熟模型直接短训比较。

父权重：`runs/struct4_b_residual_later/checkpoints/best.pt`，SHA-256
`f9c71919519dbda7d02bdfc56d6eb309cf9a45976d733e29b3fd808b7b77cc1a`。
所有组保留原encoder、RVQ、原decoder及判别器的兼容张量。无teacher/distillation。

## 建模细节

C/D在 `RVQ → 原synthesis TCN → 新增Conv2Former块 → 原波形decoder` 中加入新模块。
每块输入160维，每帧LayerNorm后分两路：

1. 调制路：1×1卷积160→48，GELU，再做kernel=7、仅左填充的48通道depthwise卷积；
2. value路：1×1卷积160→48；
3. 两路逐元素相乘，1×1卷积48→160后加回输入。

最后的投影权重和bias全零，初始时是精确恒等映射。4块增加240ms历史覆盖，不增加
未来信息。这里是因果、低维的Conv2Former启发式适配，未宣称与冠军8块、372维、
ISTFT头完全一致。保留原波形decoder是为了隔离新增调制建模的效果。

## 训练细节与适配差异

- 每组100000步；seed/data-order seed均为20261102；batch32、2秒裁剪、8个workers；
  codec和RVQ投影LR均2e-5，cosine到5e-6，无quantizer-only冻结。
- 使用同一394988条训练、14596条验证manifest；不把文件数当作音频小时数。
  每5000步验证，固定32个验证batch，保存best/last与最近2个快照。
- 原目标保持：wave L1权重1，STFT权重1，spectral convergence0.25，linear magnitude0.1，
  SI-SNR0.003，adversarial0.05，FM1.5；RVQ阶段commitment相对权重[1,1.5,2]、
  usage权重0.001；判别器配置保持一致。
- 所有组GAN从5000步开始，在10000步内线性升至完整权重。
- B/D按step寻址的独立随机源，以0.5概率完全跳过RVQ；旁路batch不更新codebook EMA，
  不加VQ loss，decoder直接处理连续encoder latent。量化batch仍用完整三个码本。
  推理、验证、码流评测始终经过RVQ；不使用码本dropout，因为部署固定24bit/帧。
- B/D新增三尺度log1p magnitude-mel L1：FFT256/512/1024，对应32/64/80个mel bins，
  HTK三角滤波器按频带求和归一。初始权重1，在80000至85000步线性减到1/15。
  这是借鉴冠军15→1的**相对比例**，并非照搬其绝对权重；现有STFT目标始终保留。
  冠军报告未明确可微PESQ实现，本轮不伪称实现PESQ loss。
- B是一个训练策略包，无法单独区分量化旁路与mel调度；若有效，下一轮必须拆开。
- 所有组加载后重置训练RNG；DataLoader独立generator并按epoch确定seed。
  旁路选择不消耗数据/模型随机流。恢复能继续最新checkpoint，但多worker随机裁剪
  的中断恢复不保证逐bit重放；如发生恢复须在结果中披露。

`best.pt`以共同、全量化的原验证reconstruction最小值选择，不把旁路或附加mel损失
计入选模标准。`training_components.jsonl`每500步记录mel、权重、旁路、GAN和显存峰值。

## 约束与评测

| 组 | 帧长 | 码率 | lookahead | 总MFLOP/s | decoder MFLOP/s | 参数量 |
|---|---:|---:|---:|---:|---:|---:|
| A/B | 10ms | 2400bps | 30ms | 650.2272 | 277.44 | 662109 |
| C/D | 10ms | 2400bps | 30ms | 668.9472 | 296.16 | 758109 |

执行原固定200条开发集的真实encode→3-byte/frame码流→decode，再算PESQ、ESTOI、
SI-SNR、UTMOS和项目分数。计算量必须零未分类MAC；新模块归入decoder预算。
RVQ诊断包含完整新增decoder通路，报告活跃code、perplexity、entropy、各级残差、
部分重建。禁止使用sealed LibriTTS确认集或自动替换strong_baseline_v2。
计算量额外计入卷积调制的逐元素乘法0.0192MFLOP/s；其余计算口径与原分析器一致。

## 预先约定的判定

主要比较B−A、C−A、D−A与D−B/D−C，并计算训练主效应、建模主效应和交互项。
同时对比冻结v2=46.746343068256394，不能把正常续训收益归给新方法。

暂定候选需同时高于A和冻结v2至少0.15分，且相对两个参照均无实质分量退化：
PESQ不低超过0.02，ESTOI不低超过0.003，SI-SNR不低超过0.15dB，UTMOS不低超过0.03。
若A低于46.25或分量严重异常，先诊断正对照，不能仅凭较弱A认定突破。
若差距小于0.15、分量互换或只有单seed收益，写明不确定，先做匹配seed确认。

后续按每轮四组自适应推进：若B有效，拆开旁路与mel再做2×2；若C/D有效，先做
匹配seed确认并检查新增计算是否值得；若全无收益，关闭这两个适配方案，下一轮
研究冠军式ISTFT合成前先完成因果性、计算量和scratch正对照预检。每轮先写计划再训练，
不得把有限适配无效等同于冠军整体思路无效。

## 资源、恢复与清理

用户本轮明确授权共享现有GPU任务。先profile最重D配置，两条量化/旁路路径均用
batch32、2秒、完整GAN反向，再四卡并行。每组独立tmux窗口与run锁，启动需至少
20GiB空闲；运行每2秒采样，总空闲低于8GiB或/storage1低于10GiB时停止**本组私有
进程组**，保留最新checkpoint，由monitor诊断恢复。不会给nvidia-smi发现的进程发信号。
共享仍有对方突发分配显存的风险；出现OOM后仅恢复受影响codec，不无限盲重启。
实测D完整GAN反向：量化路径allocated6461.79MiB/reserved7204MiB，旁路路径
allocated6405.47MiB/reserved7126MiB。当前各卡空闲35–39GiB，足够容纳该训练峰值。

历史清理仅针对已完成训练的last/中间快照和_smoke权重；保留每个正式实验best作为
关键对照、raw_best、SWA/decoder-average必要源快照、初始化step0和所有未完成任务。
外部模型、symlink、tracked checkpoint、日志/config/指标/音频不删除。清单记录每个
文件大小与SHA256，执行后复核保留文件；无备份的已删除中间权重不能直接恢复，
只能按保留配置重新训练。

## 运行产物

- `runs/champion4_{a_control,b_training,c_conv2former,d_combined}`
- `runs/champion4_setup/backward_peak_profile.json`
- `checkpoint_audits/20261102_applied.audit`
- 完成后：`CHAMPION4_RESULTS.md`，追加`EXPERIMENT_HISTORY.md`及`CODEC_EXPERIMENT_REVIEW.md`。

所有正式改动和最终结果提交main；不修改冻结基线marker。
