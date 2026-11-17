# CHAMPION11 启动与恢复记录

- 预注册 `74bc86e` 和冻结初态 `e047594` 均已在启动前推送。
- 首次启动于 2026-11-17 09:59（北京时间），独立会话 `codec_champion11_v1`。
- D 在 GPU3 上于 CUDA 初始化阶段退出，异常为 `--device cuda was requested but CUDA is unavailable`。没有训练 metadata 或 last，未执行优化更新。NVML 仍识别 GPU3，CUDA 初始化失败的底层原因未确认。
- 保存原始失败日志、配置、谱系、状态与哈希于 `runs/champion11_d_both/attempt_01_cuda_init.bhCCyoFc`。GPU1 同为 NVIDIA A40，启动前容量检查继续由原监督逻辑完成。仅重新武装 D 的原窗格，改用 GPU1 并保留同一个 step 0 和 500000 步预算。A/C 原进程保持运行。
