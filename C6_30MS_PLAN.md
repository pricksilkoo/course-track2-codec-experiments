# C6-30ms：仅缩短 C6B 有限前瞻的单组复验

2026-11-22用户明确批准：GPU空闲后训练C6的总30ms版本，只改有限前瞻层。本轮只一个seed3407单组，不是四组或新种子搜索。现有C12健康等待者/训练不替换、不停止，本任务等真正空闲且项目GPU锁可获得时启动。

基准为CHAMPION6 B（seed3407，固定500k分51.62433613863932，历史40ms模型）。唯一建模变化：encoder_lookahead_frames 3→2，有限前瞻depthwise kernel4→3；右前视覆盖由[t,t+3]改为[t,t+2]。10ms成帧+20ms前瞻=30ms，解码当前hop不等未来latent。不得改为C9分组编码器或C10/11宽度，不引入GRU后LN，不变更RVQ/loss/teacher。

保留原卷积编码器8/16/32/64/160、stride2/4/4/5、每级三双k3/ELU残差；逐帧LN→有限前瞻→4层analysis TCN(kernel3,dilation1/2/4/8,expansion1)→单向残差GRU160→projected RVQ3×256 dims48/64/80→2层synthesis TCN→Fourier256/hidden160/8调制块/320IRFFT/hop160因果OLA。16kmono、160samples/10ms、24bit/3bytes、2400bps。

## 真正从头与配对初始化
直接读取并验证C6B已保存的未训练step0（CHAMPION6_SETUP.audit载其SHA），不是加载C6B已训练500k/C7/C8权重。所有模型/判别器张量与原C6B step0精确相同，唯一形状差是analysis_temporal.lookahead.depthwise.weight最后一维4→3，保留原filter对应t/t+1/t+2的前三tap，不重采样其它权重；删去t+3 tap，不额外重缩放。原前瞻输出投影全零，配对step0音频和码流应精确相同。新snapshot global_step0、RVQ initializedFALSE/EMA0，无优化器历史。源快照不改、不重建历史preflight。

原seed/data-order3407、判别器103407、新模块203407(GRU内部+1)与原初态保持；没有新seed。GPU浮点及多worker裁剪可能非bitwise，不声称与历史优化轨迹逐bit重现。历史C6B作为同seed不同前瞻的参考，不重跑40ms组。

## 训练与固定端点
500000 TOTAL从0训练codec/RVQ/D，batch32×2s/8workers；394988train/14596valid，原清单。G/VQ lr2e-4，5kwarmup/cosine至1e-5，D2e-4、wd1e-6、clipG1/D10。
wave1、spectral1（log幅度+.25SC+.1线性幅度，FFT256/512/1024）、负SI-SNR.003、commit.1且stage权重1/1.5/2、usage.001温度1、GAN.05、FM1.5；RVQ EMA.95。GAN<100k关闭、100k起渐增、150k全启用；原3个STFT判别器与periods2/3/5/7/11不变，无teacher/mel/bypass或PESQ/UTMOS训练监督。

保持原25k/64batch真实验证；只增加恢复/留档I/O：1000完整更新atomic last，保留全部20step快照+best/last。这不改训练目标/数据/学习率。恢复自身完整last继承model/RVQEMA/G+Doptimizers，仍500k总预算。禁止从头重试增加预算；真实退出先归档诊断，披露回滚及非bitwise重放，不自动重试。

唯一预登记质量端点是500k，先训满再真实编码/解码固定200dev和PESQ/ESTOI/SI-SNR/UTMOS，按既有逐文件clip四项等权得分。250k等仅保留训练快照，不额外搜索评分、不按重建best换主结果、不做C8插值。本轮不自动生成第二个seed/节点/延长/微调。
每节点200files/16197971samples/101286frames/303858bytes，逐文件3ceil(samples/160)、16kmono原长度有限音频、位流/重建树hash、完整encoder-lookahead-TCN-GRU-RVQ-Fourier诊断。报告与历史C6B40ms参考的差（历史环境/恢复可能非bitwise，不作严格随机性确认），并列C11D30ms参照50.24576933222705（架构/seed亦变），不能把C8的51.667当合规提交门槛。

## 执行与保护
唯一tmux codec_c6_30ms_v1；唯一run runs/c6_30ms_b_s3407。启动前选择项目GPU锁可获得、无任何compute PID、free>=8192MiB且本工作区disk>=10GiB的GPU0–3之一；不足30s等待，不替换C12持有的锁/健康等待者。启动后child.wait，无GPU/磁盘资源轮询、无主动停止、无自动重试，无GPU smoke/backward profile。
所有写入在本独立checkout，原storage1和本地baseline只读。禁止改核心模型/训练代码或C12冻结源/初态/审计；只新增本组config/scripts/测试/记录。预登记先推main，再一次性准备新快照并冻结，再推SETUP后只挂一次监督队列；不重复launch或预检。
完成后独立复核20验证/20快照+完整last/真实GAN时序/全部SHA和实码流/CSV分数/30ms前缀因果边界与<=700/decoder<=300解析复杂度，写C6_30MS_RESULTS.md/.audit、追加历史中文复盘并推main限定文件；不写runs/audio/cache，不晋升旧注册、不碰sealed。当前单一3小时监控同时照看本组和C12，无新重复monitor；只有两项批准工作都终审完成后才删除监控，无下一批。
