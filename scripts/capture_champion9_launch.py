#!/usr/bin/env python3
"""Archive verified launch/progress evidence; no GPU queries and no training changes."""
from datetime import datetime,timezone
import json
import math
from pathlib import Path
import re
import subprocess

from preflight_champion9 import ROOT,CELLS,STEPS,read,digest


def main():
    target=ROOT/"CHAMPION9_LAUNCH.audit"
    if target.exists():raise RuntimeError("Preserve initial launch archive")
    setup=read(ROOT/"CHAMPION9_SETUP.audit")
    evidence={"created_utc":datetime.now(timezone.utc).isoformat(),"session":"codec_champion9_v1",
        "git_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "all_four_began_optimization":True,"no_gpu_smoke_per_user":True,"runtime_resource_poll":False,"cells":{}}
    for c in CELLS:
        run=ROOT/f"runs/champion9_{c}";item=setup["cells"][c]
        sup=read(run/"supervisor_state.json");phase=read(run/"pipeline_phase.json");md=read(run/"run_metadata.json")
        assert sup["status"]=="running" and phase["phase"]=="training" and phase["resume_step"]==0
        assert sup["runtime_resource_poll"] is False and sup["sharing_authorized"] is True
        assert md["init_checkpoint"]==str(ROOT/item["snapshot"]) and md["resume_checkpoint"] is None
        assert "--max-total-steps 500000" in md["command"]
        assert digest(run/"effective_config.yaml")==item["config_sha256"]
        assert digest(ROOT/item["snapshot"])==item["snapshot_sha256"]
        path=run/"pipeline.log"
        with path.open("rb") as f:
            f.seek(max(0,path.stat().st_size-65536));tail=f.read().decode(errors="replace")
        assert "Traceback (most recent call last)" not in tail and "out of memory" not in tail.lower()
        progress=re.findall(r"epoch (\d+)/1000:.*?(\d+)/12343.*?loss=([0-9.eE+\-]+)",tail)
        assert progress,c
        epoch,batch,loss=progress[-1];assert int(batch)>0 and math.isfinite(float(loss))
        evidence["cells"][c]={"supervisor":sup,"phase":phase,"run_metadata":md,
            "visible_epoch":int(epoch),"visible_batch":int(batch),"visible_loss":float(loss),
            "config_sha256":digest(run/"effective_config.yaml"),"snapshot_sha256":item["snapshot_sha256"],
            "pipeline_tail_sha256":__import__("hashlib").sha256(tail.encode()).hexdigest()}
    assert all(digest(ROOT/p)==h for p,h in setup["unchanged_historical_sha256"].items())
    target.write_text(json.dumps(evidence,indent=2)+"\n")
    table="\n".join(f"|{c}|{i}|{setup['cells'][c]['groups']}|{setup['cells'][c]['decoder_tcn_layers']}|{setup['cells'][c]['complexity']['total_mflop_per_s']:.4f}|{setup['cells'][c]['complexity']['decoder_mflop_per_s']:.3f}|" for i,c in enumerate(CELLS))
    review=f"""## CHAMPION9新建模实验已启动（2026-11-08，结果尚待训练）

用户最终批准编码器全部取消独立latent TCN，仅比较分组卷积4/8与解码端TCN0/2层。
四组于北京时间2026-11-08约10:36在tmux codec_champion9_v1正式启动，实际epoch1优化进展、有限loss、
step0来源/config/metadata和启动前容量证据在CHAMPION9_LAUNCH.audit；不是只排队或只加载。

|cell|GPU|encoder groups|decoder TCN层数|total MFLOP/s|decoder MFLOP/s|
|---|---:|---:|---:|---:|---:|
{table}

新编码器：16kmono→k7因果入口→通道8/16/32/64/160、步幅2/4/4/5的4级残差下采样。
每级3个残差单元，膨胀1/3/9，SnakeBeta→分组k3卷积→SnakeBeta→dense1x1混组→残差；
下采样前另有SnakeBeta、kernel2stride和左padding=stride。随后逐帧LayerNorm→一次前瞻→单向残差GRU160→
原projected RVQ（3级256码字、48/64/80维）。编码analysis_temporal只含前瞻，blocks为空，不含独立TCN。
解码端可选原2层因果TCN，再接同一Fourier结构（256宽、160hidden、8因果调制块、320点IRFFT/hop160/OLA）。
所有权重随各组一起从头训练，“解码器不变”指结构不改，不是冻结旧权重。

这是对比赛冠军公开分组残差卷积/GRU思路的课程适配，并非其24k/20ms/不同码本的逐层复现。
前瞻预算统一改为2帧20ms，加10ms packet成帧=30ms总算法延迟，不把原报告30ms总延迟错当额外前瞻30ms。
历史51.667分数仅作回退参照，不能将新旧差异归因于单一因素；四组内部前瞻/损失等完全一致。
每10ms恰好3bytes/24bit=2400bps，解码不读下一帧；CPU前缀/扰动与实际码流测试验证边界和原长度。
计算量除Conv/Linear/GRU/RVQ外，计入GRU门、调制、保守IRFFT/OLA，以及SnakeBeta每元素36和每通道每调用65
操作的透明预算（sin/exp各按32），不是实测超越函数延迟；unclassifiedMAC0，各组均满足总700/decoder300限制。

seed/data-order20261108，所有codec/RVQ和D均新构造，global_step0；GRU/Fourier种子20461108（GRU内部+1），
D种子20361108，新decoderTCN种子20561108。相同形状初态配对共享，分组卷积形状不同时单独构造；
A/C、B/D共有模型张量相同，新增TCN为零输出残差，step0码流/音频一致。所有码本尚未kmeans、EMA更新计数0。
正式init只来自runs/champion9_setup/step0_CELL.pt，绝非C6/C7/C8已训练权重或烟测权重；源快照和历史模型哈希保留。

各组500000总步、batch32×2s/8workers、同394988train/14596valid，G/VQ lr2e-4、5k warmup/cosine到1e-5，
沿用原重建/SI=.003/GAN=.05/FM1.5等损失，GAN100k开始、150k full，不添加teacher/bypass/mel或其它训练因素。
每25k验证64batches，共20次，保留全部20个step/best/last；每1000步原子恢复last不伪造验证。
恰好8个开发评分权重：每组250k/500k，先训满再评测两个预定快照，按真实总分择优、平分取早，非reconstruction-best。
相同固定200dev真实编码/解码和4项评分、303858bytes/101286frames/16197971samples、选中完整RVQ诊断及8节点+4主记录。
本批n=1训练种子，是开发分数搜索，不是多seed确认；无新增sealed评测或自动v2晋升，不自动开下一批。

必要CPU回归64项13.75秒通过，静态语法检查通过；遵守用户要求未做GPU烟测/fullGAN反向profile，不能冒称新架构显存峰值已测。
启动时四张A40都空闲约45GiB。延续用户资源政策：允许共享、启动前显存>=8192MiB/磁盘>=10GiB，之后不轮询GPU/磁盘，
不因他人PID或显存下降主动停训；每1000步恢复保存，真实退出后诊断，不盲目无限重试、不改batch/预算或干预外部进程。
恢复只用本组最新last并继承两个optimizer/EMA；worker/crop/RNG重放可能非bitwise，需记录丢弃进度和attempt证据。
本地baseline只读，所有训练在远端；计划CHAMPION9_PLAN.md，初态审计CHAMPION9_SETUP.audit，4条主记录当前running。
目前没有训练完成或质量提升结论。后续完成写CHAMPION9_RESULTS.md/.audit、更新历史/本复盘并推送；原51.667和所有历史权重均保留。
"""
    for filename in ("CODEC_EXPERIMENT_REVIEW.md","EXPERIMENT_HISTORY.md"):
        path=ROOT/filename;text=path.read_text()
        assert "## CHAMPION9新建模实验已启动" not in text
        path.write_text(text.rstrip()+"\n\n"+review.rstrip()+"\n")
    print("Four actual optimization starts archived; history/review appended, no quality results yet")


if __name__=="__main__":main()
