# C11D 冻结模型盲测格式自检：通过

用户于2026-11-25确认仅对根据公开验证结果冻结的C11D500k执行一次编码、解码和格式自检。原始下载包README禁止训练、微调与参数选择，因此本次没有计算盲测质量分、没有比较多个模型或据此改权重；公开200dev分50.24576933222705不是盲测分数，也不构成已完成比赛提交。

## 核验结果
- 远程CPU运行，独立tmux `codec_blind_c11d_20261125` 正常退出0；完成时间UTC 2026-11-25T08:43:06.133388+00:00。
- 50条原音，16kHz单声道PCM16，4,204,525采样点；逐文件原包SHA256SUMS与上传前后归档SHA一致。
- 真实编码产生50个.bin与50个.json，共26,300帧、78,900字节；逐文件严格3×ceil(samples/160)，24bits/10ms=2400bps。
- 真实解码产生50条同名16kHz单声道音频，逐文件采样点数保持原长且全部有限；解码命令只读取冻结权重、码流和五项非信号元数据，不访问原音。
- `validate_submission.py`通过；独立再次核验文件集合、字节数、元数据、原长、有限值，并保存逐文件与树SHA。
- 冻结结构总延迟30ms（10ms成帧+20ms前瞻）、总670.36356/decoder287.4112 MFLOP/s。解析口径，无新增GPU烟测或profile。
- 权重SHA256：`1bafbd40b688e218147ac0544a7dd3baf82d1bdc5d83cf28dec04cf8aee64966`。

## 确切目录
原音：`/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/track2_blind_20261125/source/input`

位流及JSON：`/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/track2_blind_20261125/c11d_frozen/bitstreams`

重建音频：`/var/tmp/hehaoran-codec-champion12.599tkbvr/runs/track2_blind_20261125/c11d_frozen/reconstructed`

完整逐文件审计：[BLIND_C11D_SELF_CHECK_RESULTS.audit](BLIND_C11D_SELF_CHECK_RESULTS.audit)。输入树SHA `98a6f7f541dae80d9f8966c06e1f47e0ed9bbb2c379652e97b1a4bbed3161fce`；位流树SHA `80fe5df993ab5a9f29390aad516c91365f27e405416c6bdd73378ae8857606f7`；重建树SHA `200f8e406149bf9ddb4a69f4b459236d3adaf2f1cc121eba52ef73b5836f40d7`。

原始数据/位流/音频仅保留于runs，不进入Git。没有停止或改变C12/C6训练，没有自动改注册或上传QQ。后续比赛压缩包仍需权重、复现代码、报告PDF及队伍署名等材料。
