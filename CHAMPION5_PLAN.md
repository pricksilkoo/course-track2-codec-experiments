# 第二轮冠军思路：encoder GRU × 因果傅里叶合成，从零四组

日期：2026-11-03。正式长训前登记，35项测试和完整GAN预检通过后于北京时间08:53启动。
承接CHAMPION4_RESULTS.md：上一轮小型追加模块
和训练包在完整终点没有可靠增益，本轮转向尚未测试的核心合成结构。

## 问题与四组

| 组 | 配置 | encoder GRU | 合成器 |
|---|---|---|---|
| A | configs/champion5/a_control.yaml | 无 | 原波形上采样decoder，正对照 |
| B | configs/champion5/b_encoder_gru.yaml | 有 | 与A相同 |
| C | configs/champion5/c_fourier.yaml | 无 | 新的因果Fourier/overlap-add decoder |
| D | configs/champion5/d_fourier_gru.yaml | 有 | 与C相同 |

这是2×2结构对照。GRU是在encoder末端、原analysis TCN之后、RVQ之前的单向循环层；
Fourier路径替换波形上采样decoder，而不是继续叠加上一轮的4个小块。
保持原三阶段later-heavy projected RVQ、10ms帧和24bit码流。

## 起点：全部未训练

不加载任何已训练codec或discriminator。共享原始未训练来源：
`runs/lookahead4_scratch_init/step0.pt`，SHA256
`3488d8448d523d5db57aa4afe99c65f6bd9089092db661ab8ed4dcc97fd9196e`，trained=false/global_step=0。

分别构造并保存`runs/champion5_setup/step0_{a_control,b_encoder_gru,c_fourier,d_fourier_gru}.pt`。
四组共享encoder、原TCN、RVQ及判别器的未训练张量；A/B的原波形decoder相同，C/D
的Fourier decoder相同，B/D的GRU相同。新模块采用独立、固定的初始化随机流20261103，
避免GRU构造改变另一因素的初始参数。GRU残差输出初始为0，A/B初始重建逐位一致，
C/D初始重建逐位一致。不同合成家族输出无须相同，也不能假称整个模型完全一致。
具体初始化SHA与兼容/新增张量清单见preflight_report.json。

## GRU结构

输入每10ms一帧、每帧160维。按帧LayerNorm → 单层单向GRU(160→160) → Linear160→160
→ 加回输入。线性输出权重与bias零初始化。状态只向过去传播，无双向层、无未来帧。
训练在每个2秒裁剪起点清零状态；推理在每条文件起点清零，与现有按文件接口一致。
相对A增加180640参数和35.888MFLOP/s（矩阵运算及三组gate乘法）。

## Fourier合成结构与为什么不额外等未来帧

`RVQ → 原synthesis TCN → Linear160→256 → 8个因果卷积调制块 → LayerNorm → Fourier头`。
每块在256维残差空间，用160维调制/value分支，depthwise kernel7，只左填充。
与冠军报告一样采用卷积调制和逆傅里叶合成的方向，但本轮不是其24kHz/20ms架构的
逐项复现。保持16kHz/10ms接口，既未引入额外lookahead，也未改变发送字节数。

Fourier头每帧输出320个实数：161个实部系数和159个非DC/non-Nyquist虚部系数；
构成161个复数单边频谱，IRFFT得到320样本波形。帧t的窗口从样本160t开始，预测
当前10ms和接下来10ms。当前输出hop仅融合帧t的前半段与帧t−1的后半段，
**不使用帧t+1**。追加未来latent不改变已经输出的hop，已通过前缀不变测试。

使用半样本偏移的sin²正窗，以及sum-of-window归一化的weighted overlap-add，最后tanh。
头预测的是未加窗的局部波形Fourier系数，因此采用窗和而非窗平方和归一化。
这里避免了centered torch.istft带来的额外未来缓存；它是学习式因果Fourier合成，
不是声称对某个输入STFT实现精确可逆。最终裁剪到原始长度。

## 训练课程与选模：提前固定终点

每组500000步、batch32、2秒裁剪，seed/data-order20261024；共享394988训练文件和14596
验证文件，与已完成并通过正对照的LOOKAHEAD_SCRATCH2课程一致。A重复该30ms控制模型，
作为同轮正对照；既往同架构500k best分46.5503是参考，不代替本轮实际A结果。

- 全模型和投影RVQ从step0共同训练，无quantizer-only冻结。
- LR从5000步warmup升到2e-4，cosine衰减至1e-5，总schedule500000。
- GAN在100000步启动，在100000–149999线性增加，随后完整GAN。
- 判别器、原损失及其权重与scratch2控制一致；没有teacher、量化旁路、mel新损失或dropout。
- 每25000步验证，固定64个验证batch，保存best/last与最近2个快照。

**主要评测一律采用预先固定的500000步last.pt**；checkpoint必须global_step=500000。
最低reconstruction的best.pt留作诊断，不能悄悄拿来替换主要结果。此规则在新结果前登记，
吸取上一轮在GAN前选到5k权重的教训；无逐checkpoint开发集追分搜索。
加载未训练初始化后重置RNG。恢复可从last续训，但worker随机裁剪不保证逐bit重放，
若恢复会披露；不得因个别组慢或失败改变其余组训练课程。

## 计算量与接口预检

| 组 | 总MFLOP/s | decoder MFLOP/s | 参数量 | bitrate | lookahead |
|---|---:|---:|---:|---:|---:|
| A | 650.2272 | 277.44 | 662109 | 2400bps | 30ms |
| B | 686.1152 | 277.44 | 842749 | 2400bps | 30ms |
| C | 630.4192 | 257.632 | 1687424 | 2400bps | 30ms |
| D | 666.3072 | 257.632 | 1868064 | 2400bps | 30ms |

Fourier模型拥有更多参数，却把大部分计算放在100Hz latent层，减少波形高采样率计算。
该因素同时改变网络位置、参数容量和合成方式，因此即使成功也只能归因于整个合成
家族，不能单独归功于IRFFT这一操作；GRU因素也包含额外容量。若有效，后续需做
容量匹配/分量拆解与多seed确认。本轮先回答部署预算内整套结构是否更好。
GRU矩阵/gate、卷积调制乘法、IRFFT和overlap-add均计入。IRFFT按保守上界
5*N*ceil(log2N) FLOPs/帧，OLA/window/归一化另计4*N；合计1.568MFLOP/s，
具体实现可能更省。未分类MAC必须为0。激活、LayerNorm和padding沿原课程口径不计。

35项CPU回归/结构测试通过，包括原模型兼容、真实3-byte/frame往返、Fourier与GRU
因果性、输出形状和有限反向梯度。正式启动还需B和D完整batch32/2秒/GAN反向GPU
profile通过；不能用仅重建、batch1的静态显存代表完整GAN峰值。
GPU完整反向实测已通过：B allocated6325.80/reserved7064MiB，D allocated5593.81/
reserved6380MiB；两组均正常完成2步训练和1批验证，所有损失有限。

## 预注册判断

A的固定终点分数必须>=46.25，并且相对冻结v2=46.746343没有灾难性分量失配，
否则先诊断正对照，不能宣布架构方向的成功或失败。报告训练收敛曲线与最后区间。

比较B−A、C−A、D−A、D−B、D−C与GRU/合成主效应、交互项。候选需相对A及冻结v2
均>=0.15分，且相对两个参照的分量下降不超过PESQ0.02、ESTOI0.003、SI-SNR0.15dB、
UTMOS0.03。若单seed达到门槛也只进入多seed确认，不自动推广。小幅、符号冲突或
分量互换不作为突破；参数/复杂度更低时可记录独立的质量-计算折中，但不能冒充涨分。

若500k仍明显未收敛，可在看任何延长后结果前登记四组共同的匹配延长课程，并说明
依据；禁止只延长有希望的组或静默改损失、架构。单个不收敛组先诊断，不能无限加算力。

## 执行、资源与输出

tmux：codec_champion5_v1；A/B/C/D分配GPU0/1/2/3。用户已授权共享，启动要求20GiB
GPU空闲；每2秒检查，空闲低于8GiB或/storage1低于10GiB时只停本组私有进程组。
不改动其他人的任务；重复OOM时改为空闲GPU排队，而非盲重启。

仅评测同一固定200文件开发集；生成真实码流再重建，报告PESQ、ESTOI、SI-SNR、UTMOS、
总分、复杂度、SHA、RVQ activity/perplexity/entropy/residual/partial reconstruction。
不使用sealed LibriTTS，不自动改变strong_baseline_v2。旧研究best与final权重继续保留。

脚本：preflight_champion5.py、profile_champion5.py、launch_champion5.py、
supervise_champion5.py、run_champion5_experiment.sh。完成后写CHAMPION5_RESULTS.md，
追加EXPERIMENT_HISTORY.md和中文CODEC_EXPERIMENT_REVIEW.md，再据证据决定下一批四组。

启动检查：四个supervisor均running，各组已开始优化迭代；原生实验记录已更新为running。
当前没有本轮最终质量结果。巡检已从champion4转到本批，仍遵守10GiB磁盘停止线。
