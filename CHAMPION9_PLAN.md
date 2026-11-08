# CHAMPION9：全新分组卷积编码器，比较解码端TCN（2026-11-08）

用户最终批准：编码器全部不要独立TCN；解码器比较有/无，卷积分组4/8。
本批恰好4组，全部从新构造的未训练codec/RVQ/判别器开始，global_step0；不是C6/C7/C8微调，
不使用任何已训练权重或smoke权重初始化。旧CHAMPION4–8归档，不重复运行。

|cell|GPU|encoder groups|encoder独立TCN|decoder TCN|
|---|---:|---:|---:|---:|
|a_g4_d0|0|4|0|0|
|b_g8_d0|1|8|0|0|
|c_g4_d2|2|4|0|2|
|d_g8_d2|3|8|0|2|

主比较：C-A、D-B为同group的decoder TCN差；B-A、D-C为同decoder条件的groups差。
这里只有一个训练seed20261108，不是多seed确认，也不套旧控制门槛/分量否决。只按实际开发总分比较，
完整披露PESQ/ESTOI/SI-SNR/UTMOS退步。历史51.6670665400仍作不变回退项；不自动晋升v2。

## 明确的模型适配，而非原冠军逐层复刻

参考原报告：https://crowdsourcing.cisco.com/lrac-challenge/2025/assets/files/2025_lrac_challenge_technical_report_track1_and_track2_teamwzqaq.pdf
其编码器残差膨胀卷积/分组/GRU思路与我们的历史latent-TCN必须区分。本批不放编码latent-TCN。
16k输入→左因果kernel7入口卷积→4级残差/下采样→逐帧LayerNorm→一次有限前瞻→单向残差GRU160
→原3级projected RVQ（每级256码字、stage_dims48/64/80）→可选原2层decoder TCN
→当前Fourier解码器（Linear160→256、8层因果调制、hidden160、320点IRFFT、hop160、因果OLA）。

编码通道8/16/32/64/160，下采样2/4/4/5。每级3个残差单元，膨胀1/3/9：
SnakeBeta→分组k3因果卷积→SnakeBeta→dense1x1跨组融合→残差相加。
下采样前另有SnakeBeta，kernel2*stride、左padding=stride；输出j只读到该packet末尾，
不读取下一个packet。入口/下采样及1x1保持dense。激活alpha/beta用log参数保证正数，初始均1。
这是依据公开描述做的可复现适配，报告未公开细节不伪称完全复刻。删除TCN节省的计算不用于加宽。

所有组共同lookahead=2个10ms帧，而不是历史代码的3帧：保守计入10ms成帧+20ms未来=30ms总算法延迟。
这是上一轮讨论中“完整核算延迟”后固定下来的公共预算，不是额外实验因子；历史分数不能当严格
仅结构消融。前瞻在GRU前，编码端只保留前瞻模块（analysis_temporal.blocks为空），不叠加独立TCN。
decoder当前hop仅依赖当前及历史码流，Fourier输出不等未来hop；CPU扰动与前缀测试明确验证边界。

16k单声道、160samples/10ms，每帧24bit/3bytes=2400bps，原长度解码，总<=700/decoder<=300MFLOP/s。
解析计数包括分组Conv/Linear/GRU矩阵与门、调制、IRFFT/OLA；SnakeBeta单独预算每元素36操作
（sin按32加4标量运算）及每通道每次65操作（2exp按32加负号），是透明保守约定而非测得延迟。
其他历史激活/归一化仍沿用原统计约定，不将新增周期激活免费处理；unclassifiedMAC必须0。

## 新初始化、训练预算和评分节点

同一seed/data-order20261108；codec主seed20261108，GRU/Fourier新模块seed20461108（GRU内部+1），
判别器seed20361108。相同形状encoder张量及全体非encoder共享新构造的A未训练张量，
分组spatial卷积形状不同者独立构造并记录。C/D新增decoder TCN来自单独固定seed20561108的新构造，
输出投影初始为0，不继承旧训练。A/C和B/D编码器/RVQ/GRU/Fourier/判别器逐tensor相同，
唯一结构差为decoder TCN；配对step0码流与解码输出需一致。所有EMA计数必须0/尚未kmeans初始化。
每组独立step0快照、source SHA/config/data哈希、共享键证据写CHAMPION9_SETUP.audit，正式启动后不再生成。

各组恰好500000步，从0联合训练codec/RVQ，batch32×2s、8workers，394988train/14596valid。
沿用C6 loss（L1=1、spectral=1、SC=.25、linear=.1、SI=.003、GAN=.05、FM1.5、commit=.1）、
G/VQ lr2e-4、5k warmup后cosine到1e-5、wd1e-6、clipG1/D10；GAN前100k关闭，100k–150k渐增，之后full。
不增加teacher/bypass/mel/PESQ代理等新因素，不训练dev。每25k实际验证64batches，共20次；
保留全部20个step快照、best/last，另每1000步原子恢复last（无伪造验证/无新增评分节点）。
最初无optimizer历史；一旦真实last存在，恢复继承模型/EMA/两个optimizer，不重置预算。
不启用独立逐batch分量日志；保留实际pipeline和25k验证分量，不能补造。

精确8个开发搜索权重：每组step250000、500000。先完成500k训练，再评测两个预定快照，避免修改LR终点。
每组实际分数最高者选中，平分取更早；不使用reconstruction-best，不新增节点/seed/选择性延长。
同一固定200dev文件：200files/16197971samples/101286frames/303858实际码流字节；
逐文件3*ceil(samples/160)、16kmono、原长度、完整四项质量评分、复杂度、checkpoint SHA和CSV。
选中模型运行完整encoder/lookahead/GRU/RVQ/synthesis诊断；保存8节点+4主实验complete记录。
不得新增sealed LibriTTS评测、自动更改strong_baseline_v2（仍46.746343）或开下一批。

## 执行与恢复

本地baseline只读；所有训练/完整评测在远端repo。tmux codec_champion9_v1四窗口，各run/GPU锁防重复。
正式启动前只做必要CPU结构/因果/字节/梯度/旧checkpoint兼容测试和解析计数；遵守用户不再做额外GPU烟测的要求。
训练新架构尚无fullGAN显存实测，不将C7测量误称本批profile；当前四卡空闲约45GiB，正式batch32直接启动。
沿用用户最新资源许可：共享、启动前GPUfree>=8192MiB且disk>=10GiB，容量不足每30s等待；
启动后不实时检测GPU/磁盘，不因外部PID或空闲量下降主动停训。只管理自己私有进程组。
真实退出/OOM后诊断再只恢复受影响cell，不盲目无限重试；重复真实共享OOM则排队空闲GPU，不降低batch或预算。
恢复可能重放worker/crop/RNG，非bitwise，需披露丢弃的未保存更新。原始记录/各次attempt档案不覆盖。
无下载/历史清理；保护C4–8所有来源、best/final、评测快照及本批所有评分快照。

完成后写CHAMPION9_RESULTS.md/.audit，追加EXPERIMENT_HISTORY和自包含中文CODEC_EXPERIMENT_REVIEW，
审计8节点+4主记录、初始化/配置/数据/20验证/4分量/字节/音频/计算/总延迟/RVQ/恢复证据；
限定范围commit/push main，不amend或丢弃无关改动。通知全部组分数、对照差、最好模型与原音/重建路径、GitHub文档。
只保持一个本批监控，健康进展/容量等待不重复打扰；实际失败、恢复、结果、完成或需决定才通知。
归档后删除本批监控；下一批必须另获批准。
