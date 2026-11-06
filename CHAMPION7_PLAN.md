# CHAMPION7：从51.6243权重出发的四组涨分微调

登记日期：2026-11-06；用户明确批准运行并允许共享GPU，随后要求先试当前显存。
本批是比赛开发集分数导向的探索，不是重复CHAMPION6的严格种子确认。用户已明确不再
以46.25正对照门槛否决下一轮涨分探索；旧CHAMPION6结论不回写、不伪装成确认通过。

## 共同父权重和四组

父模型：`runs/champion6_b_s3407_fourier_gru/checkpoints/last.pt`，原训练seed3407、
global_step500000，固定200开发集总分51.62433613863932。SHA256：
`c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23`。
四组均加载这个**已经训练过的**codec、全部RVQ/EMA buffers及判别器。不是从零训练，
不继承smoke更新，不清空码本；重建生成器和判别器优化器，局部global_step从0开始。
局部25k/50k/75k/100k对应累计父模型525k/550k/575k/600k。源权重绝不覆盖。

| cell/run（runs/下） | 首选GPU | SI-SNR loss weight | GAN adversarial weight |
|---|---:|---:|---:|
| champion7_a_continue | 0 | .003（原值） | .05（原值） |
| champion7_b_si | 1 | .010 | .05 |
| champion7_c_gan | 2 | .003 | .10 |
| champion7_d_both | 3 | .010 | .10 |

配置在configs/champion7/，以a_continue为共同训练课程，另三组只改两项损失及输出目录。
全部保持Fourier+encoder GRU架构、父model_config、新模块原seed203407，参数1868064，
总666.3072/decoder257.632MFLOP/s；不因改变训练loss而增加推理解码计算。
目标分别是继续低LR精修、加强保真、加强自然度，以及尝试二者平衡。loss系数与
PESQ/ESTOI/SI-SNR/UTMOS并非一一对应或保证单调，最终以真实总分决定。

## 固定训练预算

每组新增100000步，batch32、2秒、8 workers；同一394988训练/14596验证文件。新阶段
训练seed/data-order=20261106，加载父权重后reset RNG。生成器与量化器投影层lr5e-5，
1000步warmup、100k阶段内cosine至1e-5；判别器固定lr5e-5。clip沿用G1/D10，
weight_decay1e-6；GAN从新阶段第1步完整开启，不重复100k重建预热；FM权重始终1.5。
waveform/STFT、VQ/EMA等其余项与父方案一致，不加teacher/bypass/mel新策略。
每25k验证64batch，保留4个预定step快照、best和last，不做历史清理。best仍按重建
损失保存但不用于本批选模。原脚本没有单独逐batch分量日志，本批不虚构历史。

## 明确的开发集搜索规则

每组预先固定额外25k、50k、75k、100k四个checkpoint，合计16个网络权重，均在原同一
固定200开发集真实编码/解码评测PESQ、ESTOI、SI-SNR、UTMOS及课程总分。不得新增
节点、换seed、选择性延长或把开发音频混入训练。四节点先完整训练保留，再逐一评测，
所以早期分数不能改动本批课程；同分取较早节点。每组写selection.json和4条节点记录，
主记录明确该模型经过四节点开发集择优，绝不再称“固定终点主要确认”。

总体比较也保留未改变的51.624336父模型为回退项；若16个都不超过它，结论是本批
没涨分，不用较差的新模型覆盖父模型。所有四分量及退步如实展示，不再用旧+.15/
分量护栏自动否决这轮以分数为主的探索；但不能掩盖听感或分量折中。开发集反复搜索
有乐观偏差，不当成盲测泛化结论。无需重新跑原波形seed对照或CHAMPION4/5/6。

绝不使用sealed LibriTTS，不自动修改strong_baseline_v2 registry。任何候选必须仍满足
16kHz mono、160samples/10ms、24bit/3bytes每帧=2400bps、<=30ms lookahead、总<=700/
decoder<=300MFLOP/s、unclassifiedMAC0。逐文件审计真实字节与音频长度，记录每个节点
SHA及四分量；每组所选权重再做包含analysis_gru/完整合成路径的RVQ诊断。

## GPU共享、一次实测和排队

首次资源检查：GPU0 free7374MiB、GPU1/2/3 free11504MiB，四卡均为外部同一进程占用。
已有同架构batch32/2s/fullGAN profile reserved6364MiB，现有空闲不足以在运行后保留
8GiB。用户要求先试：一次受保护的GPU1完整batch短测加载父codec211个张量、判别器
80个张量，均无missing/skipped/new，进入计算后GPUfree降至8039MiB，触发8GiB保护。
只终止测试私有进程组，显存恢复；没有OOM、未改动外部进程。它是**容量保护中止**，
不是完整两步反向profile通过，更不是正式实验失败；不盲目重试、不从此smoke续训。
证据：runs/champion7_setup/shared_capacity_probe.json及两个probe日志，保留不删除。

正式四组用tmux codec_champion7_v1，监督器scripts/supervise_champion7.py。各组首选卡
不足20GiB空闲则排队，每30秒复查；进入pipeline后每2秒检查GPU和磁盘。GPUfree<8GiB
或/storage1<10GiB只停本组私有进程组，不触碰外部DDP/训练。实际profile内同样受保护。
每组在正式优化前从父权重做完整batch/fullGAN两步有限反向预检，smoke单独保留，
绝不作为正式起点。启动后若资源停机，诊断再从受影响组最新last续训，披露worker
随机裁剪非逐bit重放；完成/健康组不重启。重复OOM不循环重试，必要时转移受影响
未完成任务至空闲GPU，并维持同run锁、单组单进程。

不为挤进显存静默缩小batch或改变训练课程，不降低8GiB运行保护，不新下大数据，
不清理历史301文件或任何当前/历史best/last/teacher权重。当前磁盘约145GiB空闲。
等待资源没有固定完成ETA；原候选末10万步约5.93小时是独占程度不同下的参考，不是
从入队开始的承诺，也不是共享满载机器的速度保证。

## 预检与交付

CPU预检逐张量确认四组codec/discriminator/RVQ EMA完整继承父模型，记录parent SHA、
配置、数据counts/hash及固定200音频hash至CHAMPION7_SETUP.audit；原35项pytest重跑。
新脚本py_compile，GPU完整预检推迟到有容量时由受保护pipeline执行，不假称已通过。
排队计划/配置/CPU证据先提交再启动监督器，正式优化不会先于登记。运行元数据与
lineage.json清楚区分训练过的parent和新阶段局部步数。

完成后输出CHAMPION7_RESULTS.md/.audit，列出全部16节点而不只好看的一行；比较对父
模型及各组增益、四分量、码流/复杂度/RVQ、所有选模与权重SHA、训练阶段/恢复记录，
并追加EXPERIMENT_HISTORY和自包含中文复盘。限定范围提交推送main，通知用户最高分
和原音/重建目录。仅执行本批四组，不因看到涨分自动叠加下一批；要继续先提出方案。
恢复一个跟踪本批的heartbeat，不重复创建；等待/健康且无新信息时保持安静，通知
实质启动、完成、故障或需要用户选择时，完成归档后删除该监控。

## 正式启动实况（2026-11-06北京时间13:21）

CPU原35项回归通过7.98秒，新增7项流程安全/选模测试通过1.80秒；四组完整父模型/
RVQ EMA/判别器张量及配置、复杂度和数据哈希通过。计划与CPU证据先提交推送35e7e05。
最初一次显存保护短测中止后，外部任务占用自行下降，四卡free约22GiB，达到正式
启动条件；没有干预外部进程。四组随后均完成完整batch32/2秒/fullGAN两步反向预检，
每组allocated5611.93/reserved6382MiB，有限损失，证据CHAMPION7_PROFILE.audit。
正式四组从原51.6243父权重（不是smoke）启动，均无resume，已进入优化迭代。
当前共享运行每卡free约15GiB；初期约2.5–2.7步/秒，100k训练粗估10–12小时再加评测，
后续外部占用变化可能显著改变耗时。此前约6小时只适用于上一轮较空闲条件，不作本轮承诺。
原监控已结束并删除，本轮只建立一个新heartbeat跟踪，不重复监控CHAMPION4/5/6。

## 首次共享资源中断及空闲卡排队（2026-11-06北京时间13:56起）

外部同一多卡任务1924870在本轮运行约35分钟后显存明显上涨，GPU0 free瞬间降至
257MiB，其余三卡降至1309MiB。四组supervisor均按保护规则只终止自己的进程组；
原日志无OOM、Traceback或non-finite loss，外部任务未被操作。可见末batch分别约
A5802/B5991/C6049/D6111，均未到首次25k验证/保存点，因此四组没有任何正式last或
step快照。不能声称已经断点续上这些进度；它们将丢弃，后续成品轨迹必须重新从原
训练过500k的51.6243父模型开始，本轮四节点/同seed/配置不变。中断所耗约35分钟及
未保存更新单独披露，不算作成品继承的训练量；没有根据质量结果换seed或追分重开。

全部原始supervisor/pipeline日志、首轮metadata/config/lineage在每个run的
attempts/attempt01_safety_stop只复制归档、不删除，并记录SHA至CHAMPION7_RECOVERY01.audit。
这是继初始短测后再次出现共享显存风险，故**覆盖上文共享许可的当前执行策略**：
四组都已改为idle-only排队，调用supervise_champion7时不传--allow-shared，要求该卡
没有其他GPU进程且free>=20GiB后自动启动，运行8GiB/磁盘10GiB保护保持。此时只是
等待，不继续GPU计算；不要趁外部同一任务临时释放部分内存又反复共享启动。
已有完整GPU profile仍保留，正式起点绝不是smoke；CPU/setup也不重建。

tmux仍为codec_champion7_v1，四窗口重新建立为活动等待器；每个窗口单独设置
remain-on-exit，避免原来只在首窗口生效而丢失其余退出窗口的可见性。此次中断/空闲
恢复脚本只适用于已诊断、已停且没有快照的四组，不得用它重开健康/完成任务或有
checkpoint的任务。未来若已有last，只从last恢复并披露worker裁剪非逐bit重放。
现有监控同步更新为上述实际状态，不新增监控、不降低batch或安全阈值、不操作外部进程。
