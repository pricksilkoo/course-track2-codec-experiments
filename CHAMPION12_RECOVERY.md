# CHAMPION12 两次共享显存 OOM 与恢复排队

四组尚未完成，不存在本轮开发集质量评分或胜出结论。原预登记、冻结初态、模型/损失/数据/批量/500k总预算均不变。

首轮四组已从自身未训练step0实际优化至99999个完整更新。每组已完成25000/50000/75000三次真实64batch验证、保留三份step快照与best/last；最后完整原子last为99000步。所有验证损失有限。第一次尝试第100000步时GAN开始渐增，判别器前向新增显存，错误报告显示外部进程约38GiB/卡，使本进程约6.37GiB时仍无法分配28/42MiB而退出。四个原进程均确认退出后才复制并哈希日志/config/metadata/lineage/最新last/真实验证/周期恢复记录。

按批准政策第一次仅重挂原窗格同一supervisor。监督者先在free1182MiB时等待，2026-11-22约03:48UTC观察启动free45218MiB后派发自身last续跑；这时原外部computePID仍存在，允许共享。其后新外部进程增至43.25GiB/卡，四组在首个续跑批次的编码器SnakeBeta前向再次OOM，每组新增完整更新0，last/验证/周期恢复记录SHA均与第一次归档相同。第二次退出证据已另行归档，不盲目再按共享门槛重试。

|cell|物理GPU|保存/后续恢复步数|首轮最后完整更新|首轮丢弃完整更新|第二次新增完整更新|
|---|---:|---:|---:|---:|---:|
|a_control|0|99000|99999|999|0|
|b_norm|1|99000|99999|999|0|
|c_front|2|99000|99999|999|0|
|d_both|3|99000|99999|999|0|

每组从自身99000恢复完整model/RVQ EMA/缓冲区/G优化器/判别器及D优化器/epoch/batch/best。G优化器各229个状态项；D优化器已保存但state为空是100k前尚未第一次GAN更新的正常状态，不能捏造已训练D优化器。失败中的部分forward/EMA操作未当完整更新保留。首轮各999个完整更新需重放，worker/crop/RNG重放可能非bitwise；第二次无额外完整更新损失。总目标仍500000，不从零重开或增加步数。

重复共享OOM后，仅这四个已诊断单元改为等待真正空闲卡。新增scripts/supervise_champion12_idle.py仅给冻结原supervisor.main的启动GPU快照函数加等待适配：有任何compute PID即等待，即使显存够也不派发；无PID且free>=8192MiB才返回真实快照。原supervisor继续执行原10GiB盘门槛、原私有Popen进程组/child.wait、原完整last恢复、无自动重试。启动后适配器不再被调用，不查询GPU/磁盘、不因其它作业出现而主动停止。此例外只适用于本次重复实际OOM后的受影响四组，不推广到正常任务的排他策略；无驻留计时，无改batch，无额外GPU smoke/profile。两项CPU假快照测试2.48s通过，未进行GPU测试。若后续仍实际退出，须先留证诊断，不自动重新挂起或形成无限重试。

冻结源码/初态及SETUP审计不改。CHAMPION12_LAUNCH.audit由不可变首轮归档的epoch1正batch/有限loss、初始metadata、三次真实验证和99000 last事后独立补证，明确不是当前仍running的虚构快照。原capture脚本要求当前四组running/resume0且log无异常，当前不满足，故未运行也未修改冻结脚本。

实验仍为D主干2×2：A无新增LN/dims48/64/80；B GRU后逐帧无仿射LN/dims48/64/80；C无新增LN/dims80/64/48；D两者合用。各级256码字/8bit、16kmono/160samples/3bytes/2400bps，10ms成帧+20ms前瞻=30ms；总/decoder MFLOP/s A/C670.36356/287.4112、B/D670.52676/287.4112。seed/data-order20261121，G/VQ2e-4、5kwarmup/cosine1e-5、D2e-4、batch32×2s/8workers；loss wave1/spectral1/SC.25/linear.1/SI.003/commit.1/GAN.05/FM1.5，GAN100k–150k渐增，不变。

各组训练满500k后仅评预登记250k/500k，500k主端点、250k趋势，固定200dev真实码流与四评分，禁止按分数选端点/选择性延长/增加seed。最终比较归一化B−A/D−C、投影顺序C−A/D−B与交互，单seed探索；历史C8 fallback51.667066保留，不晋升v2、不碰sealed、无自动下一批。保护全部历史权重/音频/父来源，原storage1和本地baseline只读。仍只有本轮3小时监控，健康空闲等待静默。

## 原始证据目录

- a_control：首轮 `/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/champion12_a_control/attempt_01_shared_oom.dnb40vbg`；续跑 `/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/champion12_a_control/attempt_02_shared_oom.yvp8wsv9`。
- b_norm：首轮 `/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/champion12_b_norm/attempt_01_shared_oom.sv0nj0xh`；续跑 `/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/champion12_b_norm/attempt_02_shared_oom.ly6632nu`。
- c_front：首轮 `/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/champion12_c_front/attempt_01_shared_oom.fg6g6dml`；续跑 `/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/champion12_c_front/attempt_02_shared_oom.a3ql518s`。
- d_both：首轮 `/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/champion12_d_both/attempt_01_shared_oom.6_61_qw_`；续跑 `/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/champion12_d_both/attempt_02_shared_oom.l5i2hfmt`。

机器记录：[首次故障与完整断点](CHAMPION12_RECOVERY_01.audit)、[首次恢复重挂](CHAMPION12_RECOVERY_01_REARM.audit)、[第二次故障](CHAMPION12_RECOVERY_02.audit)、[实际优化历史补证](CHAMPION12_LAUNCH.audit)。初始化与主方案见CHAMPION12_PLAN.md/CHAMPION12_SETUP.audit。

## 空闲队列已挂起

截至2026-11-22T10:51:28.429602+00:00，四个原窗格均存活，四组状态均为waiting_for_idle_gpu_after_repeated_oom；尚未第三次派发训练。每组仍将从自身99000恢复。队列启动与状态见CHAMPION12_IDLE_REARM.audit、CHAMPION12_IDLE_STATUS.audit；没有重复任务。三小时监控已更新此恢复入口，后续若再次实际退出必须先留证诊断，不自动继续重挂。
