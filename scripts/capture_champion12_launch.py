#!/usr/bin/env python3
"""Capture actual finite-loss optimization once, without GPU/disk queries."""
from datetime import datetime,timezone
import hashlib,json,math,re,subprocess
from preflight_champion12 import ROOT,CELLS,read,digest
from run_champion7_experiment import record

def main():
    target=ROOT/'CHAMPION12_LAUNCH.audit'
    assert not target.exists()
    setup=read(ROOT/'CHAMPION12_SETUP.audit')
    evidence={'created_utc':datetime.now(timezone.utc).isoformat(),'session':'codec_champion12_v1',
        'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'all_four_began_optimization':True,'runtime_resource_poll':False,'cells':{}}
    for c in CELLS:
        run=ROOT/f'runs/champion12_{c}';v=setup['cells'][c]
        sup=read(run/'supervisor_state.json');phase=read(run/'pipeline_phase.json');md=read(run/'run_metadata.json')
        assert sup['status']=='running' and phase['phase']=='training' and phase['resume_step']==0
        assert not sup['runtime_resource_poll'] and md['resume_checkpoint'] is None
        assert md['init_checkpoint']==str(ROOT/v['snapshot'])
        assert digest(run/'effective_config.yaml')==v['config_sha256']
        p=run/'pipeline.log'
        with p.open('rb') as f:f.seek(max(0,p.stat().st_size-65536));tail=f.read().decode(errors='replace')
        assert 'Traceback' not in tail and 'out of memory' not in tail.lower()
        matches=re.findall(r'epoch (\d+)/1000:.*?(\d+)/12343.*?loss=([0-9.eE+\-]+)',tail)
        assert matches,c
        epoch,batch,loss=matches[-1];assert int(batch)>0 and math.isfinite(float(loss))
        evidence['cells'][c]={'supervisor':sup,'phase':phase,'run_metadata':md,
            'visible_epoch':int(epoch),'visible_batch':int(batch),'visible_loss':float(loss),
            'config_sha256':v['config_sha256'],'snapshot_sha256':v['snapshot_sha256'],
            'pipeline_tail_sha256':hashlib.sha256(tail.encode()).hexdigest()}
    assert all(digest(ROOT/p)==h for p,h in setup['unchanged_historical_sha256'].items())
    target.write_text(json.dumps(evidence,indent=2)+'\n')
    for c in CELLS:
        run=ROOT/f'runs/champion12_{c}';v=setup['cells'][c]
        record(run,run.name,'running',checkpoint=ROOT/v['snapshot'],
            note=f'CHAMPION12 real finite-loss optimization observed; postGRU={v["effective_config"]["model"]["quantizer_input_normalization"]}, dims={v["effective_config"]["model"]["projected_stage_dims"]}; fresh scratch seed20261121, 500k primary, 250k diagnostic. CHAMPION12_PLAN.md/SETUP.audit/LAUNCH.audit.')
    table='\n'.join(f'|{c}|{i}|{v["visible_batch"]}|{v["visible_loss"]:.6f}|' for i,(c,v) in enumerate(evidence['cells'].items()))
    text='''## CHAMPION12 四组已实际优化（暂无质量结论）

四卡 2×2：D 主干固定，A 对照，B 在 GRU 后 RVQ 前加无仿射逐帧 LN，C 将投影维度 48/64/80 改为 80/64/48，D 同时采用两项。每级仍 256 码字、8bit，三级 24bit、2400bps，总延迟30ms。
不是码本塌缩修复的既定结论，而是量化尺度衔接/各级投影容量顺序假设检验；旧诊断三级活跃256，潜在残差MSE非单调不等于波形质量退化。

|cell|GPU|已观察 epoch1 batch|有限loss|
|---|---:|---:|---:|
'''+table+'''
所有组从新冻结 step0 开始；seed/data-order20261121，判别器20361121、GRU/Fourier20461121（GRU内部+1），初始EMA0且未初始化，初始优化器全新。A/B tensor精确相同，C/D相同；C把A未训练量化投影/码本按2/1/0重排，其它张量精确相同，无历史学习权重。
原loss/数据和训练计划不变：500k TOTAL、batch32×2s、8workers、394988train/14596valid，25k/64batches真实验证共20条，保留20步快照+best/last，1000完整更新atomic last。GAN100k起渐增，150k全启用。
总/解码 MFLOP/s A/C 670.36356/287.4112，B/D 670.52676/287.4112；新增LN按10D+32/帧显式计入；解析口径而非实测延迟。CPU回归见SETUP；无额外GPU smoke或反向profile，fullGAN峰值未测。
先训满再评250k/500k，共8节点，500k固定主结果，250k趋势，不按分数选步数。固定200dev，真实3字节码流编码解码、完整四指标/CSV/逐文件音频与位流哈希/含新增LN完整RVQ诊断。
主对照归一化B−A/D−C、投影顺序C−A/D−B及交互；单seed探索，不能当多seed确认。历史C8 51.667066保留fallback，不晋升v2、不碰sealed。
仅启动前>=8192MiB显存和>=10GiB输出盘，允许共享；启动后不查GPU/磁盘、不主动停训、不自动重试。实际退出才保存证据并诊断，只恢复受影响组自身完整last，仍500k预算，披露回滚和非bitwise重放；无last从自身未训练step0前先诊断披露丢失。
独立工作区、历史/原storage1只读；3小时巡检，健康推进静默。完成终审80快照/80验证/8节点+4主及所有哈希并写RESULTS/审计、历史/中文复盘，推main相关记录；无自动下一批。详见CHAMPION12_PLAN.md、CHAMPION12_SETUP.audit、CHAMPION12_LAUNCH.audit。
'''
    for name in ['EXPERIMENT_HISTORY.md','CODEC_EXPERIMENT_REVIEW.md']:
        p=ROOT/name;s=p.read_text();assert '## CHAMPION12 四组已实际优化' not in s
        p.write_text(s.rstrip()+'\n\n'+text.strip()+'\n')
    print('FOUR_REAL_OPTIMIZATIONS_CAPTURED',flush=True)
if __name__=='__main__':main()
