# 第三轮预注册：D组合结构的两个新种子匹配确认

登记日期：2026-11-04；在本批任何训练和质量结果之前。
依据：[CHAMPION5_RESULTS.md](CHAMPION5_RESULTS.md)：同轮A47.0006通过正对照门槛，
C50.3710/D51.4126均通过相对A和v2的分数及分量门槛。D最强，但只有一个训练种子。
按用户已授权的连续四组批次，先确认D整套结构，不加入新损失或模型因素。

## 唯一问题及四组

| cell/run（runs/下） | GPU | seed/data-order | 架构 | configs/champion6/下配置 |
|---|---:|---:|---|---|
| champion6_a_s3407_control | 0 | 3407 | CHAMPION5 A原波形control | a_s3407_control.yaml |
| champion6_b_s3407_fourier_gru | 1 | 3407 | CHAMPION5 D Fourier+encoder GRU | b_s3407_fourier_gru.yaml |
| champion6_c_s8128_control | 2 | 8128 | A | c_s8128_control.yaml |
| champion6_d_s8128_fourier_gru | 3 | 8128 | D | d_s8128_fourier_gru.yaml |

这不是新的2×2因素拆解，而是两个control/candidate配对。种子在看到本批结果前固定，
不得因分数不佳换种子或只补跑候选。确认整个D方案，不能据此单独声称GRU或IRFFT机制
在多种子成立。C的低计算方案保留但本批不额外运行它；不重复CHAMPION4/5。

## 真正新的未训练初态

每个种子重新用原模型构造器初始化codec，seed=3407/8128，不加载任何已有学习权重，
也不简单复制CHAMPION5已用的原始初态。判别器独立seed=seed+100000。每对control
与candidate共享新encoder、analysis/synthesis TCN、latent norm、RVQ及判别器张量。
D的GRU和Fourier模块独立seed=seed+200000（GRU内部+1），残差GRU输出零初始化。
不同合成家族初始音频不同，这是预期，不声称整个模型输出相同。

保存每对共同未训练source及各cell的step0，明确trained=false/global_step0，
记录SHA、兼容/新增张量、有效配置、原数据manifest与固定200文件哈希至
`runs/champion6_setup/preflight_report.json`。setup禁止在正式run_metadata出现后重建。
不得从v2、CHAMPION5 last/best或任何成熟codec/discriminator启动。

## 完全固定课程、终点及接口

沿用CHAMPION5全部训练和模型超参数。batch32、2秒、394988/14596训练/验证文件；
joint RVQ从0优化，LR2e-4、5k warmup、cosine至1e-5；GAN100k启动，150k完整；
共500000步，每25k验证64batch。加载未训练权重后重置RNG，pair内数据顺序匹配。
保留best/last和最近2个快照；主要结果仅用预固定500000步last.pt。best只保留诊断。
不设置teacher、旁路、mel、dropout，不根据中途分数修改课程或单组延长。
意外恢复仅从受影响组最新last，披露worker随机裁剪非逐bit重放。

同一固定200条开发集：编码真实码流、解码、PESQ/ESTOI/SI-SNR/UTMOS、复杂度、RVQ。
不增加开发集搜索、不访问sealed集、不自动推广v2。验证模型有限梯度、因果前缀、
真实3字节往返与旧权重兼容；既有35项测试全部重跑。完整batch32/2秒/fullGAN的A和D
各2步反向profile（非正式训练）通过后才启动。profile只验证架构和资源，不用于质量。

| 家族 | 总MFLOP/s | decoder MFLOP/s | 参数 | lookahead |
|---|---:|---:|---:|---:|
| control A | 650.2272 | 277.440 | 662109 | 30ms |
| candidate D | 666.3072 | 257.632 | 1868064 | 30ms |

都必须16kHz单声道、160样本/10ms、24bits/3bytes每帧=2400bps，未分类MAC0。
成本口径不变，含GRU矩阵/gate乘法、卷积调制乘法及保守IRFFT/OLA估计。
Fourier当前hop只合成当前和上一个latent的预测，不等待下一个latent。

## 预固定成功、失败与停止规则

每个seed的control必须>=46.25且无灾难性分量失配；失败先查实现/数据/收敛，不用弱
control宣布成功。确认要求**两个新seed分别**满足：candidate高于各自control及冻结
v2=46.746343068256394均>=0.15，且相对两个参照PESQ下降<=.02、ESTOI<=.003、
SI-SNR<=.15dB、UTMOS<=.03。只有一个seed通过不能称为确认；严禁只报告跨seed平均
掩盖单seed失败。报告每对四项分量、原始差值、两个新seed均值/范围；将CHAMPION5
作为先前发现而不是不加说明并入确认均值。n=2确认seed仍不足以精确估计总体分布。

四组不做新的因素主效应或交互估计；配对增益为B−A和D−C。成对文件bootstrap只能
描述条件文件不确定性，不能代替训练seed随机性。即使确认也不自动改变冻结v2；
后续容量匹配/合成机制拆解另需预注册，不能无限加新分支。若结果冲突或不支持增益，
收敛检查后关闭未证实分支，保留全部证据并停止没有证据支撑的新训练。

## 资源、恢复与交付

tmux `codec_champion6_v1`，setup `codec_champion6_setup`。沿用受保护supervisor：
`scripts/supervise_champion6.py RUN GPU CONFIG --allow-shared --steps 500000`。
共享授权不变：启动GPU>=20GiB free；每2秒检查，GPU<8GiB或/storage1<10GiB只停
本组私有进程组；不触碰无关任务。重复共享OOM就排队空闲GPU，不盲目反复重试。
不新增大范围下载、不自动清理，保护所有已评测last及历史teacher/parents/averaging权重。

完成后审计固定终点、初始化谱系、配置/种子/数据哈希数量、20次训练验证/损失分量、
码流与音频长度、SHA、RVQ完整路径、四分量与约束；四条完整EXPERIMENT_LOG记录。
现有训练脚本只对champion_training开启逐500步分量日志，本批不改训练因素，继续保留
原验证分量与pipeline，不假称存在training_components.jsonl。
输出CHAMPION6_RESULTS.md/.audit，追加历史和自包含中文复盘，限定scope提交推送main。
更新同一个monitor，不新建重复自动化；最终没有后续证据时删除该monitor。

## 正式启动前验收

2026-11-04北京时间17:34：35项pytest测试通过（8.28秒），四个全新未训练snapshot与
两个pair的共享状态/数据哈希通过；完整batch32/2秒/fullGAN反向profile完成。
control allocated6282.09/reserved7030MiB，D allocated5595.49/reserved6364MiB，
均无非有限损失。首次误用unittest发现0项，未执行任何训练，已保留空发现日志并改用
正确pytest入口；不能把0项发现称为测试通过。正式四组仍将从未训练step0而非smoke权重启动。
初始化与profile快照：CHAMPION6_SETUP.audit、CHAMPION6_PROFILE.audit。
