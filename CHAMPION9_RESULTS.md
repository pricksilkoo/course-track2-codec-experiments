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
