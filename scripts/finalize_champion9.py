#!/usr/bin/env python3
"""Read-only independent evidence audit; generate CHAMPION9 final reports, no training."""
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

import numpy as np
import soundfile as sf
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
CELLS = ('a_g4_d0', 'b_g8_d0', 'c_g4_d2', 'd_g8_d2')
REF = ROOT / 'runs/fast_b64_2s_v1/validation_200'
KEYS = ('PESQ', 'ESTOI', 'SI_SNR', 'UTMOS')
torch.set_num_threads(1)


def read(p):
    return json.loads(Path(p).read_text())


def digest(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def finite(x):
    if isinstance(x, torch.Tensor):
        return not (x.is_floating_point() or x.is_complex()) or bool(torch.isfinite(x).all())
    if isinstance(x, dict):
        return all(finite(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return all(finite(v) for v in x)
    return not isinstance(x, float) or math.isfinite(x)


def checkpoint(p, step, cfg):
    s = torch.load(p, map_location='cpu', weights_only=False)
    assert s['global_step'] == step and s['model_config'] == cfg and finite(s), p
    assert s['optimizer']['state'] and s['discriminator'] and s['discriminator_optimizer'] is not None
    if step >= 100000:
        assert s['discriminator_optimizer']['state']
    assert int(s['model']['quantizer.update_count']) == step
    assert all(bool(s['model'][f'quantizer.stages.{i}.initialized']) for i in range(3))
    for i in range(3):
        for key in ('codebook', 'ema_cluster_size', 'ema_embed_sum'):
            assert f'quantizer.stages.{i}.{key}' in s['model']
    result = dict(sha256=digest(p), global_step=step, checkpoint_kind=s.get('checkpoint_kind', 'validation'),
                  epoch=s['epoch'], batch_in_epoch=s['batch_in_epoch'], all_states_finite=True,
                  optimizer_states=len(s['optimizer']['state']),
                  discriminator_optimizer_states=len(s['discriminator_optimizer']['state']),
                  rvq_update_count=int(s['model']['quantizer.update_count']))
    del s
    return result


def main():
    assert not (ROOT / 'CHAMPION9_RESULTS.audit').exists(), 'Never overwrite completed archive'
    setup = read(ROOT / 'CHAMPION9_SETUP.audit')
    log = (ROOT / 'EXPERIMENT_LOG.md').read_text()
    report = dict(created_utc=datetime.now(timezone.utc).isoformat(),
                  git_commit_before_archive=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                  kind='four-cell scratch grouped encoder / decoder TCN, fixed two-node dev search, n=1 seed',
                  independent_audit_no_new_training_or_quality_evaluation=True,
                  setup_sha256=digest(ROOT / 'CHAMPION9_SETUP.audit'),
                  launch_sha256=digest(ROOT / 'CHAMPION9_LAUNCH.audit'),
                  auditor_sha256=digest(Path(__file__)), data_counts=setup['data_counts'],
                  data_hashes=setup['data_hashes'], source_step0_sha256=setup['source_step0_sha256'],
                  code_sha256=setup['code_sha256'], fixed200_sha256=setup['fixed200_sha256'],
                  historical_sha256=setup['unchanged_historical_sha256'], cells={}, nodes=[], records={})
    assert not setup['trained'] and setup['global_step'] == 0 and setup['training_steps'] == 500000
    for group in ('data_hashes', 'code_sha256', 'unchanged_historical_sha256'):
        assert all(digest(ROOT / name) == h for name, h in setup[group].items()), group
    assert digest(ROOT / 'runs/champion9_setup/source_step0.pt') == setup['source_step0_sha256']
    refs = sorted(REF.glob('*.wav'))
    assert len(refs) == 200 and {q.name for q in refs} == set(setup['fixed200_sha256'])
    assert all(digest(q) == setup['fixed200_sha256'][q.name] for q in refs)
    initial_models = {}
    for c in CELLS:
        print('AUDIT', c, flush=True)
        r = ROOT / f'runs/champion9_{c}'
        spec = setup['cells'][c]
        assert (r / 'TRAINING_COMPLETE').exists() and (r / 'PIPELINE_COMPLETE').exists()
        assert digest(r / 'effective_config.yaml') == spec['config_sha256']
        cfg = yaml.safe_load((r / 'effective_config.yaml').read_text())
        assert cfg == spec['effective_config']
        assert digest(ROOT / spec['snapshot']) == spec['snapshot_sha256']
        init = torch.load(ROOT / spec['snapshot'], map_location='cpu', weights_only=False)
        assert init['global_step'] == 0 and finite(init)
        assert int(init['model']['quantizer.update_count']) == 0
        assert all(not bool(init['model'][f'quantizer.stages.{i}.initialized']) for i in range(3))
        initial_models[c] = init['model']
        meta = read(r / 'run_metadata.json'); lineage = read(r / 'lineage.json')
        assert meta['resume_checkpoint'] is None and meta['init_checkpoint'] == str(ROOT / spec['snapshot'])
        assert not lineage['trained_initialization'] and lineage['global_step'] == 0
        assert lineage['snapshot_sha256'] == spec['snapshot_sha256']
        supervisor = read(r / 'supervisor_state.json')
        assert supervisor['status'] == 'complete' and supervisor['runtime_resource_poll'] is False
        assert not (r / 'resume_events.jsonl').exists()
        attempts = list((r / 'attempts').glob('*'))
        assert not attempts, attempts
        rows = [json.loads(x) for x in (r / 'metrics.jsonl').read_text().splitlines() if x.strip()]
        assert [x['global_step'] for x in rows] == list(range(25000, 500001, 25000)) and finite(rows)
        for row in rows:
            expected = min(1.0, max(0.0, (row['global_step'] - 100000 + 1) / 50000))
            assert abs(row['validation']['adversarial_factor'] - expected) < 1e-10
        recovery = [json.loads(x) for x in (r / 'recovery_checkpoints.jsonl').read_text().splitlines() if x.strip()]
        assert [x['global_step'] for x in recovery] == [s for s in range(1000, 500001, 1000) if s % 25000]
        assert all(x['checkpoint_kind'] == 'recovery_only' for x in recovery)
        assert len(list((r / 'checkpoints').glob('step_*.pt'))) == 20
        weights = {str(s): checkpoint(r / 'checkpoints' / f'step_{s:08d}.pt', s, cfg['model'])
                   for s in range(25000, 500001, 25000)}
        weights['last'] = checkpoint(r / 'checkpoints/last.pt', 500000, cfg['model'])
        best = torch.load(r / 'checkpoints/best.pt', map_location='cpu', weights_only=False)
        beststep = best['global_step']; del best
        weights['best'] = checkpoint(r / 'checkpoints/best.pt', beststep, cfg['model'])
        # Stream rather than loading giant carriage-return progress lines into memory.
        error_terms = (b'Traceback (most recent call last)', b'CUDA out of memory', b'loss=nan', b'loss=inf')
        with (r / 'pipeline.log').open('rb') as f:
            overlap = b''
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                data = overlap + chunk
                assert not any(term in data for term in error_terms), c
                overlap = data[-100:]
        proof = {n: digest(r / n) for n in ('effective_config.yaml', 'run_metadata.json', 'lineage.json',
                  'supervisor_state.json', 'supervisor.log', 'pipeline_phase.json', 'pipeline.log',
                  'metrics.jsonl', 'recovery_checkpoints.jsonl', 'selection.json', 'TRAINING_COMPLETE', 'PIPELINE_COMPLETE')}
        cr = dict(groups=spec['groups'], decoder_tcn=spec['decoder_tcn_layers'], initialization_sha256=spec['snapshot_sha256'],
                  effective_config=cfg, metadata=meta, lineage=lineage, supervisor=supervisor,
                  weights=weights, validations=rows, recovery_events=recovery, evidence_sha256=proof,
                  actual_resume_count=0, actual_failure_count=0, discarded_unsaved_updates=0,
                  no_minibatch_components_log=not (r / 'training_components.jsonl').exists(), nodes=[])
        selection = read(r / 'selection.json')
        for step in (250000, 500000):
            o = r / 'evaluation' / f'step_{step:08d}'
            assert (o / 'checkpoint.sha256').read_text().split()[0] == weights[str(step)]['sha256']
            summary = read(o / 'metrics/summary.json')
            rowscsv = list(csv.DictReader((o / 'metrics/per_file.csv').open()))
            assert len(rowscsv) == 200 and {x['file'] for x in rowscsv} == {q.name for q in refs}
            vals = [{k: float(x[k]) for k in KEYS} for x in rowscsv]
            assert finite(vals) and summary['files'] == 200 and not summary['utmos_skipped']
            means = {k: sum(v[k] for v in vals) / 200 for k in KEYS}
            assert all(abs(means[k] - summary['means'][k]) < 1e-10 for k in KEYS)
            def clip(x): return min(1, max(0, x))
            contributions = dict(zip(KEYS, [sum(25 * clip((v['PESQ'] - 1) / 3.5) for v in vals) / 200,
                sum(25 * clip(v['ESTOI']) for v in vals) / 200,
                sum(25 * clip((v['SI_SNR'] + 10) / 40) for v in vals) / 200,
                sum(25 * clip((v['UTMOS'] - 1) / 4) for v in vals) / 200]))
            score = sum(contributions.values())
            assert abs(score - summary['objective_quality_score']) < 1e-10
            assert len(list((o / 'bitstreams').glob('*.bin'))) == len(list((o / 'reconstructed').glob('*.wav'))) == 200
            perfile = []
            for q in refs:
                relative = q.name; info = sf.info(q); y, sr = sf.read(o / 'reconstructed' / relative, always_2d=True)
                n = info.frames; frames = (n + 159) // 160; b = o / 'bitstreams' / q.with_suffix('.bin').name
                metadata = read(b.with_suffix('.json'))
                assert info.samplerate == sr == 16000 and info.channels == y.shape[1] == 1 and len(y) == n and np.isfinite(y).all()
                assert b.stat().st_size == 3 * frames
                assert metadata == dict(sample_rate=16000, num_samples=n, frame_samples=160, bits_per_frame=24, bitrate_bps=2400)
                perfile.append(dict(file=relative, samples=n, frames=frames, bytes=b.stat().st_size,
                                    bitstream_sha256=digest(b), metadata_sha256=digest(b.with_suffix('.json')),
                                    reconstructed_sha256=digest(o / 'reconstructed' / relative)))
            assert (sum(x['samples'] for x in perfile), sum(x['frames'] for x in perfile), sum(x['bytes'] for x in perfile)) == (16197971, 101286, 303858)
            assert read(o / 'roundtrip_audit.json') == dict(files=200, samples=16197971, actual_bytes=303858, frames=101286, audio_lengths_verified=True)
            cost = read(o / 'complexity.json'); assert cost == spec['complexity']
            assert cost['total_mflop_per_s'] <= 700 and cost['decoder_mflop_per_s'] <= 300
            assert cost['unclassified_mmac_per_s'] == 0 and cost['total_algorithmic_delay_ms'] == 30
            candidate = next(x for x in selection['candidates'] if x['step'] == step)
            assert candidate['checkpoint_sha256'] == weights[str(step)]['sha256'] and candidate['summary'] == summary
            node = dict(cell=c, step=step, score=summary['objective_quality_score'], means=means,
                        component_points=contributions, checkpoint_sha256=weights[str(step)]['sha256'],
                        evaluation_dir=str(o), complexity=cost, roundtrip=read(o / 'roundtrip_audit.json'), per_file=perfile,
                        artifact_sha256={str(q.relative_to(o)): digest(q) for q in [o / 'metrics/per_file.csv', o / 'metrics/summary.json', o / 'complexity.json', o / 'roundtrip_audit.json']})
            cr['nodes'].append(node); report['nodes'].append(node)
            name = f'champion9_{c}_step{step:06d}'
            block = log.split(f'<!-- experiment:{name}:start -->')[1].split(f'<!-- experiment:{name}:end -->')[0]
            assert '- Status: `complete`' in block and node['checkpoint_sha256'] in block
            assert f'| Course objective score | {node["score"]:.4f} |' in block
            report['records'][name] = dict(complete=True, sha256=hashlib.sha256(block.encode()).hexdigest())
        chosen = max(cr['nodes'], key=lambda x: (x['score'], -x['step']))
        assert selection['selected']['step'] == chosen['step']
        rvq_path = Path(chosen['evaluation_dir']) / 'rvq_diagnostics.json'; rvq = read(rvq_path)
        assert finite(rvq) and rvq['checkpoint_global_step'] == chosen['step']
        assert (rvq['files'], rvq['samples'], rvq['frames']) == (200, 16197971, 101286)
        assert all(x['active_codes'] == 256 for x in rvq['occupancy'])
        assert abs(rvq['partial_reconstruction'][-1]['si_snr_db_mean_per_file'] - chosen['means']['SI_SNR']) < 1e-4
        cr.update(selected_step=chosen['step'], selected_score=chosen['score'], selected_checkpoint=selection['selected']['checkpoint'],
                  rvq_diagnostics=rvq, rvq_sha256=digest(rvq_path), complexity=spec['complexity'])
        name = f'champion9_{c}'; block = log.split(f'<!-- experiment:{name}:start -->')[1].split(f'<!-- experiment:{name}:end -->')[0]
        assert '- Status: `complete`' in block and chosen['checkpoint_sha256'] in block
        assert f'| Course objective score | {chosen["score"]:.4f} |' in block
        report['records'][name] = dict(complete=True, sha256=hashlib.sha256(block.encode()).hexdigest())
        report['cells'][c] = cr
    for x, y in [('a_g4_d0', 'c_g4_d2'), ('b_g8_d0', 'd_g8_d2')]:
        common = set(initial_models[x]) & set(initial_models[y])
        assert all(torch.equal(initial_models[x][k], initial_models[y][k]) for k in common)
    fallback = read(ROOT / 'CHAMPION8_RESULTS.audit')['selection']
    assert digest(Path(fallback['checkpoint'])) == fallback['checkpoint_sha256']
    fallback_summary = read(Path(fallback['reconstructed_dir']).parent / 'metrics/summary.json')
    report['fallback'] = dict(**fallback, summary=fallback_summary, retained_unchanged=True, automatically_promoted_v2=False)
    report['matched_contrasts'] = []
    for step in (250000, 500000):
        nodes = {x['cell']: x for x in report['nodes'] if x['step'] == step}
        for high, low, factor in [('c_g4_d2','a_g4_d0','decoder TCN, groups4'), ('d_g8_d2','b_g8_d0','decoder TCN, groups8'),
                                  ('b_g8_d0','a_g4_d0','groups8 minus4, decoder0'), ('d_g8_d2','c_g4_d2','groups8 minus4, decoder2')]:
            report['matched_contrasts'].append(dict(step=step, contrast=f'{high}-{low}', factor=factor,
                 score_delta=nodes[high]['score']-nodes[low]['score'], means_delta={k:nodes[high]['means'][k]-nodes[low]['means'][k] for k in KEYS}))
    best = max(report['nodes'], key=lambda x:x['score'])
    report['selection'] = dict(best_new_cell=best['cell'], best_new_step=best['step'], best_new_score=best['score'],
        gain_vs_historical_best=best['score']-fallback['score'], selected_overall=fallback['selected'],
        new_batch_does_not_replace_fallback=True, all_four_selected_steps=500000)
    assert len(report['records']) == 12 and len(report['nodes']) == 8
    report['checks_passed'] = True
    (ROOT / 'CHAMPION9_RESULTS.audit').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    write_docs(report)
    print('AUDIT_COMPLETE', json.dumps(report['selection']), flush=True)


def write_docs(a):
    table = ['|cell|step|总分|Δ历史最好|PESQ|ESTOI|SI-SNR dB|UTMOS|', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for n in a['nodes']:
        table.append(f"|{n['cell']}|{n['step']}|{n['score']:.10f}|{n['score']-a['fallback']['score']:+.10f}|" + '|'.join(f"{n['means'][k]:.8f}" for k in KEYS)+'|')
    contrasts = ['|step|对照|Δ总分|ΔPESQ|ΔESTOI|ΔSI-SNR|ΔUTMOS|', '|---:|---|---:|---:|---:|---:|---:|']
    for n in a['matched_contrasts']:
        contrasts.append(f"|{n['step']}|{n['contrast']}|{n['score_delta']:+.8f}|"+'|'.join(f"{n['means_delta'][k]:+.8f}" for k in KEYS)+'|')
    costs = ['|cell|参数|总MFLOP/s|decoder MFLOP/s|总算法延迟|', '|---|---:|---:|---:|---:|']
    losses = ['|cell|最后train loss|wave L1|spectral|commit|G adv|FM|D|reconstruction|总validation|', '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    rvq = ['|cell|3级perplexity|3级潜在MSE相对降幅|1/2/3级SI-SNR dB|', '|---|---|---|---|']
    paths = []
    for c, r in a['cells'].items():
        cost = r['complexity']; v = r['validations'][-1]['validation']; d = r['rvq_diagnostics']
        costs.append(f"|{c}|{cost['parameters']}|{cost['total_mflop_per_s']:.4f}|{cost['decoder_mflop_per_s']:.3f}|30ms|")
        losses.append(f"|{c}|{r['validations'][-1]['train_loss']:.8f}|"+'|'.join(f'{v[k]:.8f}' for k in ['waveform_l1','spectral','commitment','adversarial','feature_matching','discriminator','reconstruction','total'])+'|')
        rvq.append(f"|{c}|"+'/'.join(f"{x['perplexity']:.3f}" for x in d['occupancy'])+'|'+ '/'.join(f"{100*x['relative_reduction']:+.3f}%" for x in d['residual_quantization'])+'|'+ '/'.join(f"{x['si_snr_db_mean_per_file']:.5f}" for x in d['partial_reconstruction'])+'|')
        paths.append(f"- {c}选中权重：`{r['selected_checkpoint']}`；SHA `{r['weights']['500000']['sha256']}`。\n  重建：`{ROOT}/runs/champion9_{c}/evaluation/step_00500000/reconstructed`。")
    best = a['selection']
    body = f'''# CHAMPION9结果：分组卷积编码器从头训练、解码器TCN消融

## 结论与实验边界

四组全部从未训练step0完成500000总步，无失败、无恢复、无丢弃更新；每组20次真实训练验证，20份step快照与best/last均保留。
所有组按预登记250k/500k两点开发总分择优，均选500k。A/B/C/D选中分数依次47.9394438295/48.6240098787/49.3182054970/49.7109807091。
本批最好D（groups8、decoderTCN2）{best['best_new_score']:.10f}，相对历史最好51.6670665400下降{abs(best['gain_vs_historical_best']):.10f}分，四项均退步；保留CHAMPION8 c_from_b10作为整体回退。
在相同步数下，解码器TCN两个分组条件都增加总分；4→8组也均增加总分，但SI-SNR均下降，不能称全分量更好。
新编码器/激活/前瞻与历史均不同，新旧对比不是单因素。单seed20261108、固定200开发集搜索，非多seed或独立测试确认，不能宣称统计显著。
没有额外节点、延长、teacher、dev训练、sealed LibriTTS或自动晋升；strong_baseline_v2登记仍46.746343，不开始下一批。

## 模型、初始化与训练（自包含）

16k单声道→k7左因果入口→4级分组残差/下采样，通道8/16/32/64/160、步幅2/4/4/5。
每级3个残差单元、膨胀1/3/9：SnakeBeta→grouped k3→SnakeBeta→dense1x1混组→skip；下采样kernel2s、leftpad=s。
逐帧LN→一次2帧20ms有限前瞻→单向残差GRU160→原projected RVQ3×256、投影48/64/80。
编码独立TCN全为0（analysis_temporal.blocks为空）；decoderTCN0/2后接原Fourier256/hidden160/8因果调制块、320IRFFT/hop160/当前hop OLA。
这是公开冠军思想的可复现适配，不冒称逐层复刻。所有解码权重也从头训练，结构保持不等于冻结旧模型。
10ms成帧+20ms前瞻=30ms总算法延迟；解码不等下一个latent，160samples/帧、24bit/3bytes、2400bps，无隐藏旁路。

codec/RVQ/D真正全新构造global_step0；正式初态仅runs/champion9_setup/step0_CELL.pt，NOT C6/7/8或smoke。
seed/data-order20261108；D20361108；GRU/Fourier20461108（GRU内部+1）；新增decoderTCN20561108。
初态码本initialized全FALSE、EMAupdate_count0；A/C、B/D相同键逐tensor一致，零输出新TCN令配对step0码流/音频一致；不同group空间卷积形状独立构造。
初始优化器新建；本批实际未发生resume。setup/source/config/data/core-code原证据冻结未再生成，最终逐hash复核通过。

每组500000 TOTAL scratch steps、batch32×2s、8workers、394988训练/14596验证（VCTK40208/4247，LibriTTS354780/10349），非训练dev。
G/VQ lr2e-4，5000 warmup/cosine到1e-5，D固定2e-4、wd1e-6、clipG1/D10。
L1=1/spectral1/SC.25/linear.1/SI.003/commit.1/GAN.05/FM1.5；jointcodecRVQ从0，GAN<100k关闭，100k–150k渐增，之后full。
真实验证100k factor.00002、125k .50002、150k及以后1.0（实现按完成更新计入+1）。每25k验证64batches共20次，完整分量在audit。
每1000次完整G/D更新原子last、temp+fsync+replace；每组480个recovery_only事件、20次验证，未伪造metrics或新增搜索权重。
逐minibatch training_components日志未启用，不能从验证补造；保留原始pipeline与80条真实验证分量。
资源按用户最终政策共享，仅启动前>=8192MiB显存/10GiB磁盘检查，运行中无GPU/磁盘轮询或主动停训。未干预其它任务。
四个原tmux监督任务均exit0/complete；无重复启动、无actual OOM/Traceback/恢复，未保存更新丢失0；若未来恢复worker/crop/RNG仍可能非bitwise。

## 全部8个预登记开发搜索节点

'''+'\n'.join(table)+'''

总分逐文件分别clip归一化再均值，不是先平均分量再裁剪：25×[clip((PESQ−1)/3.5)+clip(ESTOI)+clip((SI-SNR+10)/40)+clip((UTMOS−1)/4)]。
全部CSV四均值与总分独立重算误差<1e-10；每个节点完整四分量，不只呈现最好行。

## 同一步数的因素对照

'''+'\n'.join(contrasts)+'''

500k时decoderTCN：C−A +1.37876167，四分量均升；D−B +1.08697083，PESQ/ESTOI/UTMOS升、SI-SNR−.01815252dB。
500k时groups8−4：B−A +.68456605、D−C +.39277521，均以PESQ/ESTOI/UTMOS改善换取SI-SNR下降。
250k亦同向总分，不能据单seed宣称可普遍复现。500k相对250k四组均提高，但预定预算已经耗尽，不据趋势自动延长。

## 约束、独立证据与真实损失

'''+'\n'.join(costs)+'''

总/decoder均满足700/300限制，unclassifiedMAC0。包括GRU矩阵及门、调制、保守IRFFT/OLA；新增SnakeBeta按36op/元素+65/通道/次（sin/exp预算32）。
解析运算口径不是实测超越函数延迟，其他历史激活/归一化约定未改。CPU因果/字节/兼容64项13.75s和语法检查启动前通过，遵守用户要求无额外GPU smoke/反向profile；新架构fullGAN峰值未测，不能引用C7旧profile替代。
最终审计为只读CPU证据复核，不重复训练或重跑质量评分。8节点×200文件实际码流每节点303858bytes/101286frames/16197971samples；逐文件3×ceil(samples/160)、16kmono原长度、有限音频。
每个节点checkpoint、CSV/summary/复杂度/roundtrip及1600组bitstream/metadata/重建音频SHA、所有80step/best/last、step0/source/数据/核心代码和12条complete记录均验证；细节在CHAMPION9_RESULTS.audit。

以下为500k真实训练验证及末段训练loss，不是200开发集四项评分，也非逐batch分量：

'''+'\n'.join(losses)+'''

## 完整路径RVQ诊断

四个选中节点均沿encoder→LN→lookahead→analysis_gru→projectedRVQ→可选decoderTCN→完整Fourier/synthesis运行，非跳过GRU代理；三层均256个活跃码字。

'''+'\n'.join(rvq)+'''

潜在MSE降幅并不保证波形目标单调：如D第3级潜在MSE反升约2.99%，但三层波形SI-SNR由−.344升至6.333dB；不能据此删除码本。
所有组三层partial结果与实码流SI-SNR差<1e-4dB。稀疏plug-in联合熵受log2(frames)上限/向下偏差影响，不把24减该值解读为可用空闲容量。

## 权重、试听与归档

原音：`'''+str(REF)+'''`。

'''+'\n'.join(paths)+f'''

整体仍选历史模型：`{a['fallback']['checkpoint']}`，SHA `{a['fallback']['checkpoint_sha256']}`。
历史重建：`{a['fallback']['reconstructed_dir']}`，分数51.6670665400，四项PESQ/ESTOI/SI-SNR/UTMOS分别'''+ '/'.join(f"{a['fallback']['summary']['means'][k]:.8f}" for k in KEYS)+'''.
本批最好D四项相对历史均低，未替换历史结论/权重/注册项。两个节点的原始bitstreams/reconstructed/metrics均留在各run/evaluation/step_00250000或step_00500000，文件名与原音一致。
保留所有历史来源/teacher/comparison/averaging/scratch和C4–9所有best/final/评测快照；本次无下载/清理/删除任何模型文件。
结果CHAMPION9_RESULTS.md/.audit，初始化CHAMPION9_SETUP.audit，启动CHAMPION9_LAUNCH.audit，预登记CHAMPION9_PLAN.md，完整记录EXPERIMENT_LOG.md。
本批归档完成后删除仅codec-champion9-monitor这一个监控，不启动下一批；下一实验需用户另行批准。
'''
    (ROOT / 'CHAMPION9_RESULTS.md').write_text(body)
    marker = '\n\n<!-- CHAMPION9_FINAL_ARCHIVE -->\n\n'
    for name in ('EXPERIMENT_HISTORY.md', 'CODEC_EXPERIMENT_REVIEW.md'):
        q = ROOT / name; old = q.read_text()
        assert marker not in old
        q.write_text(old.rstrip() + marker + body + '\n')


if __name__ == '__main__':
    main()
