# CHAMPION12 启动状态

截至 2026-11-21T11:27:28.095501+00:00，一次性启动器已派发四个独立持久监督任务。预登记32afc9b和冻结初态审计79c5941均已先推main，未重复启动。每组通过8192MiB启动门槛并允许与外部任务共享，之后不查询GPU/磁盘、不主动停止。

|cell|GPU|监督者|实际训练证据|
|---|---:|---|---|
|a_control|0|running|初始化/加载，尚无优化证据|
|b_norm|1|running|初始化/加载，尚无优化证据|
|c_front|2|running|初始化/加载，尚无优化证据|
|d_both|3|running|初始化/加载，尚无优化证据|

不能仅依据 pipeline_phase=training 或监督者running宣称优化已开始；实际epoch/batch与有限loss齐备后才生成CHAMPION12_LAUNCH.audit。原始状态见CHAMPION12_QUEUE.audit。全部94项CPU回归通过；四组全新global_step0/RVQ未初始化EMA0、初始优化器新，非历史权重继续训练。

四组为D主干对照、GRU后无仿射逐帧LN、投影维度前后级交换、两者组合。总/解码MFLOP/s A/C670.36356/287.4112，B/D670.52676/287.4112，全部30ms、2400bps。各500k从头、500k固定主端点，250k诊断，不按分数选权重；完整训练、损失、数据、四项指标与因果字节接口见[预登记](CHAMPION12_PLAN.md)、[初态审计](CHAMPION12_SETUP.audit)。
本轮所有写入在独立工作区 /var/tmp/hehaoran-codec-champion12.599tkbvr，历史/原storage1与本地baseline只读。仅一个3小时巡检codec-champion12-monitor，健康推进保持静默；实际失败先保全证据诊断再按自身last恢复，无自动重试或下一批。完成独立审计与结果发布后删除本巡检。

## 后续状态（2026-11-22）

本页上述内容为初次派发时快照。后续已实际优化并两次共享OOM，完整last为99000；最新恢复排队与证据见[CHAMPION12_RECOVERY.md](CHAMPION12_RECOVERY.md)，不能把原初始化快照作为当前状态。
