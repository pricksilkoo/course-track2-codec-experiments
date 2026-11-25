# 冻结C11D：单次盲测质量自测

用户在单模型格式自检之后明确要求查看分数，本次仅对已冻结且未改动的C11D500k重建计算一次质量指标，没有比较其它权重、训练、微调或据盲测分数重新选择模型。教师统一环境评测才是最终成绩。

| 指标 | 50文件均值 |
|---|---:|
| PESQ-WB | 1.7965279460 |
| ESTOI | 0.6929488933 |
| SI-SNR dB | 5.8082468993 |
| UTMOS | 1.6802431917 |
| 逐文件裁剪归一四项等权总分 | 37.1448819223 |

50条CSV独立重聚合与summary一致，四项均真实计算，UTMOS未跳过且使用已有缓存，无下载。CPU独立tmux `codec_blind_c11d_score_20261125` 正常退出0。完成UTC 2026-11-25T08:48:47.650159+00:00。

权重SHA256 `1bafbd40b688e218147ac0544a7dd3baf82d1bdc5d83cf28dec04cf8aee64966`。输入、码流、重建均沿用此前通过自检的文件，逐输入/重建SHA复核未变。原始/位流/音频目录及字节审计见[格式自检](BLIND_C11D_SELF_CHECK_RESULTS.md)；本次机器审计见[BLIND_C11D_SCORE_RESULTS.audit](BLIND_C11D_SCORE_RESULTS.audit)。

远程CSV：`/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/track2_blind_20261125/c11d_frozen/metrics/per_file.csv`。

公开200dev的50.24576933222705与本次50条盲测来自不同集合，不能当作同一集合上的模型退步或凭此推断具体失真原因。此次结果不用于参数选择，不自动追加其它盲测模型比较，不自动晋升或提交。
