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
