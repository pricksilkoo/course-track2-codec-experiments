#!/usr/bin/env python3
"""Verify real optimization starts and append self-contained Chinese launch records."""
from datetime import datetime,timezone
import json,math,re,subprocess
from preflight_champion10 import ROOT,CELLS,read,digest
def main():
    target=ROOT/'CHAMPION10_LAUNCH.audit';assert not target.exists()
    setup=read(ROOT/'CHAMPION10_SETUP.audit');evidence={'created_utc':datetime.now(timezone.utc).isoformat(),'session':'codec_champion10_v1',
      'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'all_four_began_optimization':True,
      'runtime_resource_poll':False,'no_gpu_smoke_per_user':True,'cells':{}}
    for c in CELLS:
        r=ROOT/f'runs/champion10_{c}';sup=read(r/'supervisor_state.json');phase=read(r/'pipeline_phase.json');md=read(r/'run_metadata.json');item=setup['cells'][c]
        assert sup['status']=='running' and not sup['runtime_resource_poll'] and phase['phase']=='training' and phase['resume_step']==0
        assert md['resume_checkpoint'] is None and md['init_checkpoint']==str(ROOT/item['snapshot'])
        assert digest(r/'effective_config.yaml')==item['config_sha256']
        q=r/'pipeline.log'
        with q.open('rb') as f:f.seek(max(0,q.stat().st_size-65536));tail=f.read().decode(errors='replace')
        assert 'Traceback' not in tail and 'out of memory' not in tail.lower()
        matches=re.findall(r'epoch (\d+)/1000:.*?(\d+)/12343.*?loss=([0-9.eE+\-]+)',tail);assert matches,c
        epoch,batch,loss=matches[-1];assert int(batch)>0 and math.isfinite(float(loss))
        evidence['cells'][c]={'supervisor':sup,'phase':phase,'run_metadata':md,'visible_epoch':int(epoch),'visible_batch':int(batch),'visible_loss':float(loss),
          'config_sha256':item['config_sha256'],'snapshot_sha256':item['snapshot_sha256'],'pipeline_tail_sha256':__import__('hashlib').sha256(tail.encode()).hexdigest()}
    assert all(digest(ROOT/p)==h for p,h in setup['unchanged_historical_sha256'].items())
    target.write_text(json.dumps(evidence,indent=2)+'\n')
    table='\n'.join(f"|{c}|{i}|{'/'.join(map(str,setup['cells'][c]['encoder_channels']))}|{setup['cells'][c]['fourier_hidden']}|{setup['cells'][c]['complexity']['total_mflop_per_s']:.5f}|{setup['cells'][c]['complexity']['decoder_mflop_per_s']:.4f}|" for i,c in enumerate(CELLS))
    text="""## CHAMPION10四格容量实验已实际启动（2026-11-10，暂无质量结论）

用户批准结构大致不变、用更多计算容量，四组为新原规模对照/仅编码加宽/仅解码加宽/两端加宽。
同新seed/data-order20261110，从真正未训练codec/RVQ/D step0开始，初始优化器新建；非C9旧seed重跑、非已训练模型微调。
四个tmux codec_champion10_v1监督任务已看到真实epoch1优化和有限loss，证据CHAMPION10_LAUNCH.audit，不只加载。

|cell|GPU|encoder channels|Fourier hidden|total MFLOP/s|decoder MFLOP/s|
|---|---:|---|---:|---:|---:|
"""+table+"""

其余结构全固定：groups8、k7入口、4级stride2/4/4/5、每级3个SnakeBeta/groupk3/dense1x1残差dilation1/3/9，无编码独立TCN。
LN→一次20ms前瞻→GRU160→原3级256码字projectedRVQ dims48/64/80→原2层decoderTCN→Fourier width256/8块/320IRFFT/hop160/当前hop OLA。
只扩中间encoder通道和Fourier hidden160/184；末端160、码本、GRU、前瞻与损失不变。10ms成帧+20ms前瞻=30msTOTAL，16kmono/160samples/3bytes/2400bps。
CPU计数包含GRU矩阵/门、调制、保守IRFFT/OLA及SnakeBeta36op/元素+65/通道/调用，unclassifiedMAC0，总700/decoder300均满足；不是实测算子延迟。
全新A共同来源、不同形状fresh，D编码来自新B其它来自新C；各单因素对照其它tensor精确一致，较宽decoder零输出残差使A/C、B/D step0音频和码流一致。
所有保存初态码本initializedFALSE/EMA0，新source/config/data/core-code哈希冻结SETUP.audit，禁止正式启动后再生成；D种子20361110、GRU/Fourier20461110（GRU内部+1）。

每组500kTOTAL scratch，batch32×2s/8workers、394988train/14596valid。G/VQ2e-4、5kwarmup/cosine1e-5、D2e-4、wd1e-6、clipG1/D10。
沿用L1=1/spectral1/SC.25/linear.1/SI.003/commit.1/GAN.05/FM1.5，GAN100k开始150kfull；不加mel/teacher/bypass或其它新因素。
每25k验证64batches共20真分量，保留20step+best/last；每1000完整更新原子last含模型/EMA/G+D优化器，recovery事件不伪造验证，未启用的逐batch日志不补造。
先训满500k再评测每组250k/500k，恰好8开发搜索模型，按实际总分选、平分取早，非reconstruction-best，无选择性延长/额外种子。
固定同200dev，每节点16197971samples/101286frames/303858真实字节、16kmono原长度有限音频、4评分/CSV/复杂度/checkpointSHA/选中完整GRU-RVQ-synthesis诊断。
同端点B−A/D−C编码容量、C−A/D−B解码容量，n=1不是确认实验；历史C9比较含seed差异。旧C8最佳51.6670665400保留回退，v2冻结46.746343不自动晋升。
遵守用户不做额外GPU烟测/反向profile，新扩容fullGAN峰值未实测；只做必要CPU形状/真实字节/因果/梯度/旧兼容与原子恢复回归，结果见setup日志。
资源只启动前>=8192MiB显存/10GiB磁盘，不足30s容量等候；允许共享，不因其它PID排他。启动后child.wait，无GPU/磁盘实时轮询/主动停止，无batch降低。
真实退出才诊断/留attempt证据，仅恢复受影响组自己的最新last继承EMA/G+D优化器，仍500kTOTAL，worker/crop/RNG重放可能非bitwise；无last披露丢失并回新未训练step0，重复真实共享OOM诊断后等待空闲卡。
本地baseline只读，C4–9归档不重跑、不清理任何历史来源/模型；无sealed新评测。仅一个本批监控，健康进展静默。
计划CHAMPION10_PLAN.md、初态CHAMPION10_SETUP.audit、实际启动CHAMPION10_LAUNCH.audit、4主实验running记录已保存；暂未完成训练、没有质量提升结论。
完成写CHAMPION10_RESULTS.md/.audit，追加历史和中文复盘、限定commit/push，通知全组结果及确切试听目录并删除本批监控；下一批另获批准。
"""
    for name in ['CODEC_EXPERIMENT_REVIEW.md','EXPERIMENT_HISTORY.md']:
        p=ROOT/name;old=p.read_text();assert '## CHAMPION10四格容量实验已实际启动' not in old;p.write_text(old.rstrip()+'\n\n'+text.rstrip()+'\n')
    print('FOUR_REAL_OPTIMIZATIONS_CAPTURED',flush=True)
if __name__=='__main__':main()
