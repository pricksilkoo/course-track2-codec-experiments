# CHAMPION8：四个解码器参数插值候选（不训练）

2026-11-08。用户同意先尝试四个无需训练的候选，再依据结果决定是否需要低LR短程微调。
本批只做以下4个固定开发集搜索点，不自动启动后续训练或新增alpha。

父模型为CHAMPION6 B500k、分数51.62433613863932，SHA256
`c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23`。
donor A=CHAMPION7 A的预定100k快照（累计600k，51.52590320119037），
SHA `8dcebc6cdf298ef29c420c3d09be66e9f2b995e27eb76176b62caf8ba924313a`；
donor B=CHAMPION7 B100k（累计600k，51.53128750969333），
SHA `8741b75536892152d09adb176ec1a0db6c345496b499443c092051ca24d9b3f4`。

|新cell|donor|donor占比alpha|父占比|
|---|---|---:|---:|
|a_from_a10|C7 A100k|.10|.90|
|b_from_a25|C7 A100k|.25|.75|
|c_from_b10|C7 B100k|.10|.90|
|d_from_b25|C7 B100k|.25|.75|

新参数=(1-alpha)×父参数+alpha×donor参数。仅对named_parameters中以decoder.、
decoder_refinement.、synthesis_temporal.、synthesis_transformer.、synthesis_conv2former.
开头的可学习参数插值。全部encoder、latent_norm、analysis TCN/GRU、整个RVQ（含
输入/输出投影、码本、EMA、计数等）及全部非参数buffers逐位保留父模型。
特别说明：RVQ输出投影虽计入decoder复杂度，但本批仍冻结，绝不与码本一起平均。

这是已训练权重的后处理，不是从零训练或新一轮微调；新梯度更新0、无优化器/判别器
更新。导出的inference_only checkpoint局部global_step=0仅表示新增优化步数0，来源
父500k与donor600k分别记录，不能误称随机初始化。原3个源checkpoint永不覆盖。
CPU检查插值系数/键形状、逐tensor冻结范围和有限值，必要的解析复杂度核对；不做
GPU反向、smoke训练或任何新增训练。准备完成后固定权重SHA，不再重建setup。

沿用完全相同的固定200开发文件（16197971samples/101286frames），逐候选实际编码、
解码、格式校验、PESQ/ESTOI/SI-SNR/UTMOS和课程总分。全部200码流必须与父模型相同，
逐文件3×ceil(samples/160)字节、共303858字节，16k单声道解码保持原长度，不能用
额外encoder信息。完整运行所有4个点；保留未改动的父模型作为回退项，只有真实总分
更高才报告涨分；平分保留父，候选间平分按上述登记顺序。四分量退步全部披露。

架构相同：1868064参数，666.3072total/257.632decoder MFLOP/s、2400bps、lookahead30ms、
unclassifiedMAC0，计入GRU门、调制和保守IRFFT/OLA。4个候选均运行解析复杂度报告。
本批是4点开发集择优，不是盲测或严格种子确认；不新增sealed LibriTTS评测、不自动
修改strong_baseline_v2登记（仍46.746343）、不自动开始四组低LR训练。

每cell输出runs/champion8_CELL/，权重checkpoints/interpolated.pt、lineage.json、
effective_config.yaml、evaluation/metrics/summary.json/per_file.csv、bitstreams/reconstructed、
checkpoint.sha256和roundtrip_audit.json，EXPERIMENT_LOG记录全部4个cell。编码/RVQ
逐tensor和实际码流相同，故不增加重复的RVQ GPU诊断；保留父模型完整诊断作参照。

资源沿用用户最新许可：显存能容纳即可共享，只有启动前检查>=8GiB和磁盘>=10GiB；
启动后不实时查询GPU/磁盘、不因外部PID或显存下降主动停止。无容量每30秒等待。
使用tmux codec_champion8_v1，4窗口/锁防重复；真实失败后诊断，只恢复受影响cell，
不盲目无限重试、不操作外部任务。CHAMPION4/5/6/7归档，绝不重跑。

最终写CHAMPION8_RESULTS.md/.audit，追加历史与自包含中文复盘，核对4条complete记录，
限定范围提交推送main并通知所有4分数、分量变化、试听目录和GitHub文档。保留全部
源权重、历史档案和4候选，不做清理。结果后再与用户决定是否开展短程微调。
