# CHAMPION12：GRU→RVQ 衔接与投影顺序 2×2 从头实验

用户于 2026-11-21 授权四张卡继续实验。本轮只执行以下四组；没有自动下一批、晋升或 sealed 测试。所有写入位于独立 checkout，原 storage1 及历史 runs 只读。

## 问题与预登记
CHAMPION10/11 D 的 500k 得分为 50.213593/50.245769；单独加宽解码器 C−A 的方向不一致。三级码本均全部活跃，不能认定码本塌缩。部分共同潜在空间残差 MSE 不逐级下降，也不能直接判定量化失效（各级投影/合成联合学习）。
本轮探索逐帧归一化能否改善 GRU 到 RVQ 的尺度衔接，以及把投影维度更多分配到前级是否有益。没有预先假定任一项必胜。

| cell | GPU | GRU 后 / RVQ 前 | 三级投影维度 |
|---|---:|---|---|
| a_control | 0 | Identity | 48/64/80 |
| b_norm | 1 | LayerNorm(160, elementwise_affine=False, eps=1e-5) | 48/64/80 |
| c_front | 2 | Identity | 80/64/48 |
| d_both | 3 | 同 B | 80/64/48 |

每级仍 256 码字和 8bit，三级 24bit。改变内部维度和级次，不是改变每级比特数。
固定 D 主干：group8 encoder channels8/24/40/80/160；四级 stride2/4/4/5，SnakeBeta/dilation1/3/9；encoder 独立 TCN0，LN→一次 2 帧前瞻→单向残差 GRU160→本轮可选逐帧 LN→projected RVQ→decoder TCN2→Fourier width256/hidden184/8blocks/320IRFFT/hop160/当前 hop 因果 OLA。
新增 LN 沿最后一维逐帧计算，无未来帧、无旁路、无解码附加信息。16k 单声道、160samples/10ms、3bytes/frame、2400bps、10ms成帧+20ms前瞻=30ms，总<=700/decoder<=300 MFLOP/s。
新增 LN 以每帧 10D+32 标量运算保守计入总复杂度，包含统计量/稳定化/归一化及 reciprocal-sqrt 预算；历史 LN 排除口径保持并注明。这是解析口径，不是 GPU 运行时测量。

## 公平初始化和训练
共同 seed/data-order20261121，D20361121，GRU/Fourier20461121（GRU内部+1）。全新 codec/RVQ/discriminator；没有历史/teacher/smoke 初态。A 是新构造；B 与 A 全部张量逐一相等；C 将 A 未训练投影及码本各级按 2/1/0 排列，非量化张量相同；D 与 C 全部张量相同。这样保留相同初始投影行集合/整体 tight frame，仅改变其前后级分配。所有 initializedFALSE、EMAupdate_count0、global_step0、初始优化器全新。归一化启用时不要求 step0 音频相同。
禁止修改已冻结 step0/preflight 证据，禁止重复启动或替换健康等待者。

每组500000 TOTAL从头训练，batch32×2s/8workers；394988train/14596valid，固定训练/验证清单，无dev训练。G/VQ lr2e-4，5kwarmup/cosine到1e-5；D lr2e-4、wd1e-6、clipG1/D10。
原 loss 不变：waveL1=1、spectral1、SC.25、linear.1、SI.003、commit.1、GAN.05、FM1.5。codec/RVQ联合从0，GAN<100k关闭、100k–150k渐增、>=150k全权重。
每25k验证64batches，20条真实分量记录，20份step快照及best/last全保留；每1000完整更新atomic last保存模型/RVQEMA/G+D优化器及进度。恢复不增总预算。

## 端点、评价与解释
每组先训练到500k，再仅评250k/500k，共8个节点；500k固定主端点，250k仅诊断，不按分数择优。固定200dev，真实编码/3字节码流/解码后 PESQ-WB、ESTOI、SI-SNR、UTMOS，按既有逐文件归一化裁剪四项等权求总分再均值。
主对照同500k：归一化 B−A、D−C；投影顺序 C−A、D−B；报告交互(D−C)−(B−A)、全部四分量/退步和算力。单共同seed探索，不称多seed确认；与C11比较同时改变seed/初始化，不能当纯因素效应。
完整路径 RVQ 诊断必须包含新增 LN，报告活跃/困惑度/逐级潜在残差/1、2、3级波形结果；部分级波形仅诊断，不新增模型搜索节点。
独立复核8节点+4主complete、80快照、80验证、GAN计划、config/data/source/code/checkpoint SHA、恢复史、逐CSV重算、200音频原长度/有限值/16k单声道、每节点16197971samples/101286frames/303858bytes及逐树哈希。
历史 C8 fallback 51.66706654001837/SHA a5cffa2dfcf39fc69b36b84e8ca238e7cbd9408ee008a1042bb7bbb253e4eb19 保留；v2登记不变、不碰sealed、不自动晋升。

## 资源与监控
独立 tmux codec_champion12_v1，4个只启动一次的监督者。启动前 freeGPU>=8192MiB、新工作区freeDisk>=10GiB；允许与外部任务共享；不足保留等待者30s检查。管线启动后不查询 GPU/磁盘、不因外部任务或资源下降主动停止；child.wait，不自动重试、不改batch、不额外GPU smoke/backward profile，fullGAN峰值未测。
实际退出后先保存/哈希受影响日志、config、metadata、lineage、latest last、metrics/recovery状态再诊断。仅恢复受影响未完成组最新自身完整 last，仍同500k预算，披露回滚及worker/crop/RNG非bitwise重放；无last只能诊断后从自身未训练step0重启并披露丢失步数。重复共享OOM需诊断后排队真正空闲GPU。禁止触碰外部进程及历史权重。
每3小时监控，仅失败/恢复/有效结果/完成/需要选择时通知，健康推进与未变等待保持静默。完成后写 RESULTS.md/.audit、历史与中文复盘，推main相关记录，通知分数四分量/对照/链接/确切音频路径，删除本监控；下一批另获授权。
