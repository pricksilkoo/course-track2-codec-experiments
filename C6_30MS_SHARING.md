# C6-30ms 共享启动政策追加授权

用户于2026-11-24明确要求“你看有空位就一块训吧”，覆盖原仅空闲且项目GPU锁未预留的启动要求。本次只调整已批准单组C6的资源入口，不新增实验。

新入口 scripts/supervise_c6_30ms_shared.py 保留本任务独占supervisor锁、防重复、启动前free>=8192MiB/输出盘>=10GiB、私有Popen进程组及child.wait，不要求compute PID为空，也不申请或改动C12持有的GPU锁。选择满足门槛且剩余显存最大的卡；不足30秒等待。启动后不查GPU/磁盘资源，不主动停训，无自动重试。显存门槛不是fullGAN实测峰值保证。

原等待者确认尚无metadata/pipeline/last、零优化后，保存原日志/状态/config/lineage/入口哈希，再仅结束此等待者并在原tmux窗格替换为共享入口。C12与外部作业均保留。冻结PLAN/SETUP、原supervisor、preflight/launch、训练代码、模型/config、step0、数据、损失、500k预算及唯一500k评分均不变；不重跑preflight或总launch。机器证据见C6_30MS_SHARING.audit，实际优化须另有LAUNCH.audit实证。


C6共享入口已于2026-11-24 08:12UTC在原窗格派发同一原runner，选择GPU2，启动快照空闲17480MiB且存在其它计算PID，符合用户新增共享授权。原等待者零更新、无子pipeline；SIGTERM记录后退出清理读取阻塞，随后仅对其PID发SIGKILL，完全退出并验证锁释放后才重arm。新入口只有一个监督者和runner，无重复实验；此时runner仍加载，metadata/实际有限loss尚未确认，不能称已优化。C12四组不变。见[C6_30MS_SHARING_REARM.audit](C6_30MS_SHARING_REARM.audit)。
