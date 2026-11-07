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

## 第二次资源交接中断：连续空闲窗口（2026-11-06北京时间15:09起）

原外部任务退出后出现空卡，四个idle-only等待器于15:09–15:10开始加载父权重；
15:11新外部多卡任务2016678接入。虽然当时free仍约44GiB，但idle-only禁止与新任务
共用，监督器再次只停止自己的私有进程组。这不是显存耗尽或OOM，而是外部进程
出现触发的独占保护。没有观察到新的epoch优化进度，metadata仍为首轮创建时间，
四组仍没有正式checkpoint或验证记录。首轮约6000步遗失的事实不变，不声称恢复。

新证据保存在CHAMPION7_RECOVERY02.audit及各run/attempts/attempt02_external_job_arrival，
第一轮归档完全保留。短暂无PID不代表真正可用长时段，故将idle-only的启动判据
从两次/5秒观察提高为**连续观测600秒**均无其他GPU PID且free>=20GiB；任何一次
观测不满足即清空计时。等待每30秒复查，不占GPU计算。启动后的2秒资源检查及
8GiB运行/磁盘10GiB保护不变，仍不共享、不操作外部训练。新增5项纯CPU时间/状态
测试覆盖600秒边界、外部进程/显存变化重置以及原显式shared模式兼容；与原7项流程
测试一起12项通过后，才为四个已停任务重新建立等待器。没有重开健康/完成任务。
原source、课程、batch、seed、100k阶段预算、16个评分节点不变；已有完整profile不重做。

## 第三次独占保护中断：等待资源策略选择（2026-11-06北京时间16:47起）

连续空闲窗口于16:40满足，四组开始加载并正式优化；16:47各组约1575 batch时出现
新的外部GPU进程，idle-only监督器按规则退出。检测时free仍38353/38057MiB，触发
原因是其他PID出现，不是显存耗尽；原始日志无OOM、Traceback或non-finite loss。
本次约6分40秒的优化仍未到首次25k保存点，四组没有last或step快照，进度无法恢复。
首轮约6000步和第三轮约1575步的未保存尝试分别保留，不计入任何成品继承步数。

证据及SHA为CHAMPION7_RECOVERY03.audit、各run/attempts/attempt03_exclusive_guard，
前两轮档案未覆盖。本轮没有新增质量结果、选模节点或改seed，不重建setup。
**当前四组全部停止，且没有活动GPU等待器；不继续自动重开。** 已向用户询问资源
策略：允许显存充足时共享并保留8GiB保护、增加恢复快照，或继续等待独占空卡。
在用户选择前不恢复共享、不更改batch/训练课程或恢复保存频率，不操作外部进程。
原51.624336父权重未动；本批仍未完成，不能将资源中断当作方法质量结论。

## 用户选择：有显存容量就共享训练（2026-11-06，覆盖上述独占/等待选择状态）

用户已明确选择“允许显存充足时共享：保留8GiB显存底线，并增加恢复快照”，并补充
“就是有空闲就训”。四个已诊断停止的任务恢复使用--allow-shared，不要求无外部PID，
不再等待600秒独占。保持启动空闲>=20GiB，运行每2秒检查free>=8GiB、磁盘>=10GiB；
只停止自己的私有进程组，绝不操作外部任务，不静默缩小batch。无容量则监督器排队。
非零失败仍先诊断，不盲目反复启动；已有last后只从受影响任务的last续训。

新增唯一配置项training.recovery_checkpoint_interval_steps=1000，其他模型、损失、
seed、数据、学习率及100k预算不变。每1000个完整G/D优化更新后原子保存last.pt，
包含模型/RVQ EMA、两个优化器、epoch/batch/global_step及best_validation；写临时文件、
fsync后原子替换，写入中断仍保留上一份完整last。恢复日志为recovery_checkpoints.jsonl。
它们标记recovery_only，不伪造验证指标，不写metrics.jsonl，不额外保存或评分step快照。
25k验证、四个评分节点、四分量和全部16节点搜索规则完全不变；验证点优先完整保存。
恢复后的worker裁剪/RNG并非逐bit重放，必须披露；此改动只改善可恢复性而非新实验因素。

三次旧档案和原SETUP/PROFILE证据不重建。当前仍无正式last，所以本次必须从原51.624336
父模型开始，不能恢复首轮约6000步和第三轮约1575步的未保存更新。启动前运行回归与
原子写入/恢复测试，使用一次性restart_champion7_shared.py并记录CHAMPION7_SHARED_RESTART.audit；
同一个监控改为此共享策略，不新增监控或下一批实验。

执行记录：56项CPU回归/原子保存恢复测试通过（11.33秒），包含原35项及既有12项流程
和新增9项。独立完整batch恢复短测启动后，用户明确要求“直接跑吧，不要测试了”，
故只终止该短测自己的两个进程组，不再做额外测试；保留runs/_smoke_champion7_recovery_io_v1
和日志，不称短测通过、绝不从此目录初始化正式任务。四组使用原已完成fullGAN profile，
按新授权在原tmux重启，--allow-shared、1000步恢复保存；旧archives不动。新启动没有
正式last可续，所以仍从原训练过500k父模型开始。原监控已替换为一致的共享规则，
不会再因外部PID自动独占停机；非零失败仍须诊断后只恢复受影响组。

## 第四次资源保护：真正断点恢复（2026-11-07北京时间01:07）

共享运行到局部约73k–76k时，外部多卡任务显存上涨，GPU0 free4600MiB，GPU1–3
free2561MiB，实际低于8GiB；四组只停止本组私有进程组。这次不是外部PID出现即
独占停机。末段日志未见OOM/Traceback/nonfinite；已有1000步恢复机制起效。
保留的last分别A75000（真实验证点）、B76000、C73000、D73000；保留模型/RVQ EMA、
两个优化器及epoch/batch/global_step。不能把恢复称为从父模型重开或新增100k预算。
A/B已有25k/50k/75k验证与快照，C/D已有25k/50k；评分仍等训练100k后进行。

CHAMPION7_RECOVERY04.audit记录原停机、checkpoint SHA和实际验证；各run/attempts/
attempt04_shared_memory_guard保留原日志、metadata/config/lineage/恢复事件/metrics及
该次完整last副本（有SHA），旧attempt01–03不动。只核对断点完整性，不新增GPU测试。
当前free约8–12GiB，低于20GiB启动线；同一tmux建立共享容量等待器，--allow-shared，
不是强行计算重试，也不因其他PID而要求独占。达到启动线后runner只--resume各自last，
不加载父模型/smoke；披露worker裁剪/RNG非逐bit重放，未保存末段更新丢弃。
原batch/seed/loss/学习率与总预算、16评分节点、8GiB运行/10GiB磁盘保护全部不变。
