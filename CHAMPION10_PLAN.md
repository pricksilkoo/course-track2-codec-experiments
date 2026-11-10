# CHAMPION10：结构不变的四格容量消融（2026-11-10）

用户批准四组实验：新原规模对照、只加宽编码器、只加宽解码器、两端加宽。
本批只研究容量，核心模型代码不用改；CHAMPION4–9均已归档，不重启、不覆盖。
新对照使用新seed20261110，与本批其它三组匹配，不是重复CHAMPION9旧seed。

|cell|GPU|encoder channels|Fourier hidden|
|---|---:|---|---:|
|a_base|0|8/16/32/64/160|160|
|b_enc|1|8/24/40/80/160|160|
|c_dec|2|8/16/32/64/160|184|
|d_both|3|8/24/40/80/160|184|

编码器均groups8，无独立TCN；k7入口、4级stride2/4/4/5、每级3个dilation1/3/9的SnakeBeta/groupk3/dense1x1残差均不变。
LN→一次20ms有限前瞻→单向残差GRU160→原projected RVQ3×256 dims48/64/80；末端160维不变。
解码器均原2层因果TCN，Fourier width256、8调制块、320IRFFT/hop160/当前hop OLA不变，仅hidden160/184。
16kmono、160sample10ms、24bit3bytes2400bps；10ms成帧+20ms前瞻=30msTOTAL，不增加未来缓存/隐藏信息。
解析复杂度目标联合组650–680、decoder280–290，硬上限700/300；包含GRU矩阵/门、调制、保守IRFFT/OLA与SnakeBeta36op/元素+65/通道/调用，unclassifiedMAC0。
这些是统一解析口径，不冒称实测sin/exp延迟。CPU计数实值写SETUP.audit；不做额外GPU烟测/fullGAN反向profile，新扩容峰值未测。

## 真正未训练初态与公平对照

四组全新codec/RVQ/判别器global_step0；无learned C6/7/8/9、无smoke初态，正式初始化仅runs/champion10_setup/step0_CELL.pt。
seed/data-order20261110、D20361110、GRU/Fourier20461110（GRU内部+1）。A共同未训练source；相同形状复制A；新增形状新构造；D编码器来自新B、其它来自新C。
B−A、D−C只变编码器容量，C−A、D−B只变decoderhidden；非变化部分逐tensor相同，D不混合任何学得权重。
较宽decoder的零输出残差初态使A/C、B/D step0音频/码流完全一致；源快照码本initialized全FALSE、EMAupdate_count0、初始G/D优化器新建。
setup/source/config/code/data哈希与共享键一次冻结，正式启动后禁止重新生成。

## 固定训练和评价

沿用CHAMPION9全部训练因素，唯一批次共同变化是新seed与两个容量因子：每组500000TOTAL scratch steps，batch32×2s、8workers、394988train/14596valid。
G/VQ lr2e-4，5000warmup/cosine1e-5，D固定2e-4、wd1e-6、clipG1/D10；原L1=1/spectral1/SC.25/linear.1/SI.003/commit.1/GAN.05/FM1.5。
jointcodecRVQ从0；GAN<100k关闭、100k–150k渐增、之后full。不加mel/teacher/bypass/新损失、不训练dev。
每25k验证64batches共20条真实分量，保留全部20个step快照+best/last；每1000完整更新原子last含模型/全部RVQEMA/buffers/G+D优化器/epoch/batch/step/best。
recovery_only不伪造验证、不额外生成搜索权重；未启用逐minibatch分量日志，保留真实pipeline和25k记录。
恰好8个开发搜索模型：每组250k/500k；必须先训满500k再评测二节点，实际总分最高者选中、平分取早，非reconstruction-best。
相同固定200dev（runs/fast_b64_2s_v1/validation_200），每节点200files/16197971samples/101286frames/303858实际bytes；逐文件3ceil(samples/160)、16kmono、原长度有限音频。
全部8分数/4分量/退步/CSV重算、checkpoint/config/source/data哈希、复杂度/总延迟/选中完整encoder-lookahead-GRU-RVQ-synthesis诊断。
同端点B−A、D−C与C−A、D−B独立报告；同seed n=1开发探索，不是多seed确认。历史C9比较还含seed差，不能当纯容量效果。
历史最好C8 c_from_b10=51.66706654001837 SHA a5cffa2dfcf39fc69b36b84e8ca238e7cbd9408ee008a1042bb7bbb253e4eb19保留回退；C9最好49.710980709050375作为历史参照。
不加节点/种子/选择性延长/自动strong_baseline_v2晋升（冻结46.746343），无sealed LibriTTS新评测，不自动下一批。

## 执行、资源与恢复

远端repo唯一工作区，本地baseline只读；tmux codec_champion10_v1，四组run/GPU锁防重；旧launch/queue脚本永不重用。
用户最终共享政策：只启动前显存free>=8192MiB、disk>=10GiB，不足每30s容量等待；其它PID不影响共享资格。
启动后child.wait，无GPU/磁盘实时资源轮询，无8GiB运行底线或20GiB门槛、无外部PID排他/600s等待；只管理自有私有pipeline组。
真实退出后诊断/归档受影响log/config/metadata/lineage/last/recovery/metrics再恢复，禁止盲目无限重试或降低batch。
仅受影响未完成组用最新真实last，恢复EMA和G+D优化器，500kTOTAL不重置；无last需披露未保存进度丢失并从本批未训练step0重启。
worker/crop/RNG重放非bitwise，披露丢弃更新；重复实际共享OOM才在诊断后排队真正空闲GPU，不动其它用户任务。
保持一个监控，健康/容量等待不打扰；实际失败/恢复/质量结果/完成/需用户决定才通知。
无下载/清理，保护所有历史parent/teacher/comparison/averaging/scratch/C4–10best/final/评分节点；历史301文件清理不重复。
完成审计8节点+4主complete记录，写CHAMPION10_RESULTS.md/.audit，追加EXPERIMENT_HISTORY和自包含中文CODEC_EXPERIMENT_REVIEW，限定范围commit/push main、不amend/丢弃无关改动。
通知四组全部选中分数/最好增益/因素与分量取舍、GitHub链接、原音和四组确切重建目录；归档后删除仅本批监控，下一批另获批准。
