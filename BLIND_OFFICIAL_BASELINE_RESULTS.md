# 官方课程原始基线：固定盲测对照

用户于2026-11-25明确要求原始官方课程baseline作为固定对照。使用仓库跟踪的原始参考权重，SHA256 `4f19d236377b8f5d5c10e4f283d6cc80a35a80f081d5b6f135b605bdc7a6d96a`，逐字节匹配Git保留版本；不是自研strong_baseline_v2或Cisco LRAC权重。没有训练/调参/搜索checkpoint，输入为同一原始50条盲测，不改源音频。

| 指标 | 课程原始baseline | 冻结C11D500k | C11D减baseline |
|---|---:|---:|---:|
| PESQ | 1.4745264697 | 1.7965279460 | +0.3220014763 |
| ESTOI | 0.6182098318 | 0.6929488933 | +0.0747390615 |
| SI_SNR | 1.3141760758 | 5.8082468993 | +4.4940708235 |
| UTMOS | 1.4286415648 | 1.6802431917 | +0.2516016269 |
| 同一50文件逐文件裁剪归一总分 | 28.5950904062 | 37.1448819223 | +8.5497915162 |

四项指标均真实计算，UTMOS未跳过且使用与C11D相同缓存版本。两者同一评分脚本/CPU口径，50条逐文件CSV重算和均值检查通过。baseline真实编码解码/原验证器/独立文件大小、元数据、原长与有限音频检查通过：50files/4204525samples/26300frames/78900bytes。独立tmux codec_blind_official_baseline_20261125正常退出0，无GPU查询/停止现有训练。

baseline结构384189参数、608.768总/244.48解码MFLOP/s、0ms额外前瞻；加10ms成帧总10ms。C11D总30ms、670.36356总/287.4112解码MFLOP/s。双方均在课程延迟及计算量预算内，但容量和延迟不同，这是完整系统固定对照，不是单因素消融。自测分不是教师统一评测的官方成绩，不据此追加盲测模型搜索。

重建目录：`/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/track2_blind_20261125/official_baseline_fixed/reconstructed`。

位流及JSON：`/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/track2_blind_20261125/official_baseline_fixed/bitstreams`。

CSV：`/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/track2_blind_20261125/official_baseline_fixed/metrics/per_file.csv`。

逐文件与树SHA证据见[BLIND_OFFICIAL_BASELINE_RESULTS.audit](BLIND_OFFICIAL_BASELINE_RESULTS.audit)，C11D分数见[BLIND_C11D_SCORE_RESULTS.md](BLIND_C11D_SCORE_RESULTS.md)。
