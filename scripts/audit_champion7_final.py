#!/usr/bin/env python3
"""Audit existing CHAMPION7 evidence and assemble results; no training/evaluation."""
from datetime import datetime, timezone
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess

import numpy as np
import soundfile as sf
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
CELLS = ("a_continue", "b_si", "c_gan", "d_both")
STEPS = (25000, 50000, 75000, 100000)
METRICS = ("PESQ", "ESTOI", "SI_SNR", "UTMOS")
PARENT_SHA = "c2793275e34cb758cacb8ccc04f685c92b40c0bfc3fbd0973e710a72e1b8aa23"
REFERENCE = ROOT/"runs/fast_b64_2s_v1/validation_200"


def digest(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
    return h.hexdigest()


def read(p):return json.loads(Path(p).read_text())


def record_check(text,name,sha):
    start=f"<!-- experiment:{name}:start -->";end=f"<!-- experiment:{name}:end -->"
    assert text.count(start)==text.count(end)==1, name
    section=text.split(start,1)[1].split(end,1)[0]
    assert "- Status: `complete`" in section and sha in section,name
    return hashlib.sha256(section.encode()).hexdigest()


def deltas(s,p):
    return {**{k:s["means"][k]-p["means"][k] for k in METRICS},
            "score":s["objective_quality_score"]-p["objective_quality_score"]}


def clip(x):return min(1.0,max(0.0,x))


def audit_metrics(directory,names):
    s=read(directory/"summary.json")
    rows=list(csv.DictReader((directory/"per_file.csv").open()))
    assert len(rows)==200 and {r["file"] for r in rows}==names
    assert s["files"]==200 and s["utmos_skipped"] is False
    means={k:statistics.fmean(float(r[k]) for r in rows) for k in METRICS}
    assert all(math.isfinite(float(r[k])) for r in rows for k in METRICS)
    for k in METRICS:assert abs(means[k]-s["means"][k])<1e-10
    score=statistics.fmean(25*(clip((float(r["PESQ"])-1)/3.5)+clip(float(r["ESTOI"]))+
        clip((float(r["SI_SNR"])+10)/40)+clip((float(r["UTMOS"])-1)/4)) for r in rows)
    assert abs(score-s["objective_quality_score"])<1e-10
    return s


def bitstream_audio_audit(output, originals):
    bins=sorted((output/"bitstreams").glob("*.bin"));decoded=sorted((output/"reconstructed").glob("*.wav"))
    assert len(bins)==len(decoded)==200
    total=samples=frames=0;manifest=hashlib.sha256()
    for name,info in originals.items():
        path=output/"reconstructed"/name
        signal,rate=sf.read(path,dtype="float32",always_2d=True)
        assert rate==16000 and signal.shape==(info.frames,1) and np.isfinite(signal).all()
        bit=output/"bitstreams"/Path(name).with_suffix(".bin")
        side=read(bit.with_suffix(".json"))
        assert side["num_samples"]==info.frames
        expected=math.ceil(info.frames/160)
        assert bit.stat().st_size==3*expected
        total+=bit.stat().st_size;samples+=info.frames;frames+=expected
        manifest.update(f"{name} {info.frames} {digest(path)} {digest(bit)}\n".encode())
    assert (samples,frames,total)==(16197971,101286,303858)
    evidence=read(output/"roundtrip_audit.json")
    assert evidence=={"files":200,"samples":samples,"actual_bytes":total,"frames":frames,"audio_lengths_verified":True}
    return {**evidence,"decoded_audio_finite":True,"each_file_3bytes_per_ceil160_verified":True,
            "decoded_audio_and_bitstream_manifest_sha256":manifest.hexdigest()}


def main():
    torch.set_num_threads(4)
    setup=read(ROOT/"CHAMPION7_SETUP.audit")
    assert setup["endpoints"]==list(STEPS) and setup["data_counts"]=={"train":394988,"valid":14596}
    assert setup["parent_trained_global_step"]==500000 and setup["parent_sha256"]==PARENT_SHA
    assert setup["codec_discriminator_and_RVQ_EMA_inherited"] is True and setup["optimizer_state_inherited"] is False
    parent=ROOT/setup["parent"];assert digest(parent)==PARENT_SHA
    pstate=torch.load(parent,map_location="cpu",weights_only=False);assert pstate["global_step"]==500000;del pstate
    summary=read(ROOT/"runs/champion6_b_s3407_fourier_gru/evaluation/metrics/summary.json")
    assert summary["objective_quality_score"]==51.62433613863932
    registry=ROOT/"model_registry/strong_baseline_v2.json";regsha=digest(registry);reg=read(registry)
    assert reg["selection_metrics"]["objective_quality_score"]==46.746343068256394
    assert digest(ROOT/reg["checkpoint"])==reg["checkpoint_sha256"]
    for path,sha in setup["data_hashes"].items():assert digest(ROOT/path)==sha
    originals={p.name:sf.info(p) for p in sorted(REFERENCE.glob("*.wav"))}
    assert len(originals)==200 and sum(i.frames for i in originals.values())==16197971
    for name,sha in setup["fixed200_sha256"].items():
        assert digest(REFERENCE/name)==sha and originals[name].samplerate==16000 and originals[name].channels==1
    recovery=read(ROOT/"CHAMPION7_RECOVERY04.audit")
    log=(ROOT/"EXPERIMENT_LOG.md").read_text()
    audit={"created_utc":datetime.now(timezone.utc).isoformat(),
        "git_commit_before_archive":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "kind":"16-node exploratory development score search; not confirmation",
        "read_only_verification_no_new_training_or_evaluation":True,
        "parent":{"checkpoint":str(parent),"sha256":PARENT_SHA,"global_step":500000,"summary":summary},
        "frozen_v2":{"registry_sha256":regsha,"checkpoint_sha256":reg["checkpoint_sha256"],"score":reg["selection_metrics"]["objective_quality_score"]},
        "data_counts":setup["data_counts"],"data_hashes":setup["data_hashes"],
        "fixed200_hashes_match_frozen_setup":True,
        "evidence_audits_sha256":{p.name:digest(p) for p in [ROOT/"CHAMPION7_SETUP.audit",ROOT/"CHAMPION7_PROFILE.audit",ROOT/"CHAMPION7_SHARED_RESTART.audit",ROOT/"CHAMPION7_RESOURCE_POLICY05.audit",*[ROOT/f"CHAMPION7_RECOVERY0{i}.audit" for i in (1,2,3,4)]]},
        "cells":{},"completed_experiment_records":{}}
    for c in CELLS:
        run=ROOT/f"runs/champion7_{c}"
        assert (run/"TRAINING_COMPLETE").is_file() and (run/"PIPELINE_COMPLETE").is_file()
        assert read(run/"supervisor_state.json")["status"]=="complete"
        cfg=yaml.safe_load((run/"effective_config.yaml").read_text())
        normalized=copy.deepcopy(cfg);assert normalized["training"].pop("recovery_checkpoint_interval_steps")==1000
        assert normalized==setup["cells"][c]["effective_config"]
        assert cfg["model"]==setup["cells"][c]["effective_config"]["model"]
        lineage=read(run/"lineage.json");assert lineage==setup["cells"][c]["lineage"]
        assert lineage["all_codec_and_discriminator_tensors_verified_identical_to_parent"] is True
        md=read(run/"run_metadata.json");assert md["resume_checkpoint"]==str(run/"checkpoints/last.pt")
        assert "--max-total-steps 100000" in md["command"] and "--init-checkpoint" not in md["command"]
        archived=run/"attempts/attempt04_shared_memory_guard/checkpoints/last.pt"
        assert digest(archived)==recovery["cells"][c]["resume_checkpoint_sha256"]
        policy=read(run/"recovery_policy.json")
        assert policy["launch_free_MiB"]==8192 and policy["runtime_resource_poll"] is False
        validations=[json.loads(l) for l in (run/"metrics.jsonl").read_text().splitlines()]
        assert [v["global_step"] for v in validations]==list(STEPS)
        for v in validations:
            assert v["validation"]["adversarial_factor"]==1.0
            assert all(math.isfinite(x) for x in v["validation"].values())
        events=[json.loads(l) for l in (run/"recovery_checkpoints.jsonl").read_text().splitlines()]
        assert events and all(e["checkpoint_kind"]=="recovery_only" and e["global_step"]%1000==0 and e["global_step"]%25000!=0 for e in events)
        assert not (run/"training_components.jsonl").exists()
        selection=read(run/"selection.json");assert len(selection["candidates"])==4
        assert [x["additional_step"] for x in selection["candidates"]]==list(STEPS)
        nodes=[]
        last=torch.load(run/"checkpoints/last.pt",map_location="cpu",weights_only=False)
        assert last["global_step"]==100000 and "validation_metrics" in last
        assert last["optimizer"]["state"] and last["discriminator_optimizer"]["state"]
        for step in STEPS:
            ckpath=run/"checkpoints"/f"step_{step:08d}.pt";sha=digest(ckpath)
            state=torch.load(ckpath,map_location="cpu",weights_only=False)
            assert state["global_step"]==step and state["model_config"]==cfg["model"]
            assert len(state["model"])==211 and state["discriminator"] and state["optimizer"]["state"] and state["discriminator_optimizer"]["state"]
            if step==100000:
                for field in ("model","discriminator"):
                    assert all(torch.equal(v,last[field][k]) for k,v in state[field].items())
            del state
            out=run/"evaluation"/f"step_{step:08d}"
            assert (out/"checkpoint.sha256").read_text().split()[0]==sha
            s=audit_metrics(out/"metrics",set(originals));actual=bitstream_audio_audit(out,originals)
            cost=read(out/"complexity.json")
            assert cost==setup["cells"][c]["complexity"]
            assert cost["parameters"]==1868064 and cost["total_mflop_per_s"]<=700 and cost["decoder_mflop_per_s"]<=300
            assert cost["algorithmic_lookahead_ms"]==30 and cost["unclassified_mmac_per_s"]==0 and cost["bitrate_bps"]==2400
            planned=selection["candidates"][STEPS.index(step)]
            assert planned["checkpoint_sha256"]==sha and planned["summary"]==s
            name=f"champion7_{c}_step{step:06d}"
            audit["completed_experiment_records"][name]=record_check(log,name,sha)
            nodes.append({"additional_step":step,"cumulative_step":500000+step,"checkpoint":str(ckpath),
                "checkpoint_sha256":sha,"evaluation":str(out),"summary":s,"deltas_vs_parent":deltas(s,summary),
                "roundtrip":actual,"complexity":cost,
                "metrics_per_file_sha256":digest(out/"metrics/per_file.csv")})
        chosen=max(nodes,key=lambda n:(n["summary"]["objective_quality_score"],-n["additional_step"]))
        assert chosen["checkpoint_sha256"]==selection["selected"]["checkpoint_sha256"]
        rvq=read(Path(chosen["evaluation"])/"rvq_diagnostics.json")
        assert rvq["checkpoint_global_step"]==chosen["additional_step"]
        assert (rvq["files"],rvq["samples"],rvq["frames"])==(200,16197971,101286)
        assert len(rvq["occupancy"])==len(rvq["residual_quantization"])==len(rvq["partial_reconstruction"])==3
        assert all(x["active_codes"]==256 for x in rvq["occupancy"])
        assert abs(rvq["partial_reconstruction"][-1]["si_snr_db_mean_per_file"]-chosen["summary"]["means"]["SI_SNR"])<1e-4
        main_name=f"champion7_{c}"
        audit["completed_experiment_records"][main_name]=record_check(log,main_name,chosen["checkpoint_sha256"])
        audit["cells"][c]={"initial_trained_parent_lineage":lineage,"effective_config":cfg,
            "effective_config_sha256":digest(run/"effective_config.yaml"),"latest_run_metadata":md,
            "resume_from_local_step":recovery["cells"][c]["resume_global_step"],
            "resume_sha256":digest(archived),"non_bitwise_worker_crop_rng_replay":True,
            "training_validations":validations,"recovery_save_events":events,
            "last_checkpoint_sha256":digest(run/"checkpoints/last.pt"),"last_global_step":last["global_step"],
            "last_and_final_step_model_discriminator_tensors_identical":True,
            "best_reconstruction_checkpoint_preserved_not_selected":(run/"checkpoints/best.pt").exists(),
            "nodes":nodes,"selected_additional_step":chosen["additional_step"],"selected":chosen,
            "selected_full_path_rvq":rvq,"selected_rvq_diagnostics_sha256":digest(Path(chosen["evaluation"])/"rvq_diagnostics.json")}
        del last
        print(f"AUDITED {c}:4 nodes,4 validations,real200-file roundtrips and full RVQ",flush=True)
    assert len(audit["completed_experiment_records"])==20
    path_code=(ROOT/"scripts/diagnose_rvq.py").read_text()
    assert "model.analysis_gru(embeddings)" in path_code and "model.decoder(model.synthesis_conv2former(synthesized))" in path_code
    allnodes=[n for c in audit["cells"].values() for n in c["nodes"]]
    best=max(allnodes,key=lambda n:n["summary"]["objective_quality_score"])
    assert len(allnodes)==16 and best["summary"]["objective_quality_score"]<summary["objective_quality_score"]
    assert digest(parent)==PARENT_SHA and digest(registry)==regsha
    audit.update(total_searched_nodes=16,complete_records=20,best_new=best,overall_kept="unchanged parent CHAMPION6 B500k51.62433613863932",
        best_new_gain_vs_parent=best["deltas_vs_parent"]["score"],no_new_sealed_evaluation=True,
        no_baseline_promotion=True,no_next_batch_started=True,
        rvq_full_analysis_gru_and_synthesis_source_sha256=digest(ROOT/"scripts/diagnose_rvq.py"))
    (ROOT/"CHAMPION7_RESULTS.audit").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n")
    write_markdown(audit)
    print(json.dumps({"best_new":best["summary"]["objective_quality_score"],"gain":best["deltas_vs_parent"]["score"],"selected":{k:v["selected"]["summary"]["objective_quality_score"] for k,v in audit["cells"].items()},"records":20}),flush=True)


def write_markdown(a):
    lines=["# CHAMPION7：四组涨分微调完整结果", "", "完成日期：2026-11-07。四组均完成追加100000步，全部16个预登记节点及20条实验记录完成。", "",
        "结论：**本批没有超过父模型**。新模型最高B=51.5312875097，比未改变的父模型51.6243361386低0.0930486289。保留父模型作为当前最高分回退项；不晋升冻结v2、不自动启动下一批。", "",
        "## 口径与训练", "", "这是比赛固定200文件开发集上的四节点择优探索，不是固定终点确认或盲测结论；不套用旧46.25控制门槛或+.15/分量否决规则。每组固定追加25k/50k/75k/100k评测，合计16个权重，无新增节点、换种子或选择性延长。", "",
        "四组共同从已训练CHAMPION6 B500k、51.624336父权重热启动，完整继承codec/RVQ EMA/判别器；新阶段最初重建优化器。资源中断后的真正--resume恢复模型和两个优化器，不再重置，也不从父权重重来。", "",
        f"父权重：`{a['parent']['checkpoint']}`；SHA256 `{PARENT_SHA}`。", "",
        "seed/data-order20261106，batch32×2秒、8workers，394988训练/14596验证；G与VQ投影LR5e-5，1000步warmup后cosine到1e-5，D固定5e-5；fullGAN从局部0起，clip G1/D10、weight_decay1e-6、FM1.5。每25k验证64批。A SI.003/GAN.05；B .010/.05；C .003/.10；D .010/.10。", "",
        "## 每组选中结果", "", "|组|SI/GAN|追加/累计步|总分|对父Δ分|PESQ|ESTOI|SI-SNR dB|UTMOS|", "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for c,x in a["cells"].items():
        n=x["selected"];s=n["summary"];m=s["means"];cfg=x["effective_config"]["loss"]
        lines.append(f"|{c}|{cfg['si_snr_weight']}/{cfg['adversarial_weight']}|{n['additional_step']}/{n['cumulative_step']}|{s['objective_quality_score']:.10f}|{n['deltas_vs_parent']['score']:+.10f}|{m['PESQ']:.8f}|{m['ESTOI']:.8f}|{m['SI_SNR']:.8f}|{m['UTMOS']:.8f}|")
    m=a["parent"]["summary"]["means"]
    lines += [f"|原父模型|.003/.05|0/500000|51.6243361386|0|{m['PESQ']:.8f}|{m['ESTOI']:.8f}|{m['SI_SNR']:.8f}|{m['UTMOS']:.8f}|", "", "### 选中结果相对父模型的全部分量变化", "", "|组|ΔPESQ|ΔESTOI|ΔSI-SNR dB|ΔUTMOS|", "|---|---:|---:|---:|---:|"]
    for c,x in a["cells"].items():
        d=x["selected"]["deltas_vs_parent"];lines.append(f"|{c}|{d['PESQ']:+.8f}|{d['ESTOI']:+.8f}|{d['SI_SNR']:+.8f}|{d['UTMOS']:+.8f}|")
    lines += ["", "A略增ESTOI/UTMOS但PESQ/SI-SNR退步；B提升SI-SNR但其余三项下降，总分仍略低。GAN加倍的C/D在本次父权重、预算下更差，结果不支持沿这条分支直接加码。这里只描述本轮观察，不推广为普遍loss规律，也不把资源恢复后的非逐bit轨迹当成严格因果消融。", "",
        "## 全部16个节点（不隐藏较差结果）", "", "|组|追加步|总分|Δ父分|PESQ|ESTOI|SI-SNR dB|UTMOS|", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for c,x in a["cells"].items():
        for n in x["nodes"]:
            s=n["summary"];m=s["means"];lines.append(f"|{c}|{n['additional_step']}|{s['objective_quality_score']:.10f}|{n['deltas_vs_parent']['score']:+.10f}|{m['PESQ']:.8f}|{m['ESTOI']:.8f}|{m['SI_SNR']:.8f}|{m['UTMOS']:.8f}|")
    lines += ["", "## 质量、码流和约束审计", "", "逐文件重新读取已有per_file.csv，按课程先逐文件归一化/裁剪再取平均重算总分，和summary差异<1e-10；不是从全体均值反推裁剪后的分数。所有16节点都有完整PESQ/ESTOI/SI-SNR/UTMOS，无skip-UTMOS。", "",
        "每节点实查200个原音/解码音频和200个码流：16197971原始采样点，101286帧，303858实际字节；每文件严格3×ceil(samples/160)字节，解码16kHz单声道、原始长度且全部有限。审计保存每节点音频/码流清单摘要及全部checkpoint/指标SHA。", "",
        "架构保持1868064参数，总666.3072/解码257.632MFLOP/s，24bit/10ms=2400bps，lookahead30ms、unclassifiedMAC0；计入GRU gates、调制、保守IRFFT/OLA。四组模型配置和数据哈希匹配原SETUP，只允许后加1000步恢复I/O配置及等价输出路径。", "",
        "## 完整RVQ诊断", "", "四个选中模型均有全200文件诊断，路径包含encoder/latent norm/analysis TCN/analysis_gru、RVQ、synthesis temporal/完整decoder及refinement。三层码本全部256个码字活跃。", "", "|组|perplexity(1/2/3)|仅1/2/3级SI-SNR dB|各级残差相对下降|", "|---|---|---|---|"]
    for c,x in a["cells"].items():
        r=x["selected_full_path_rvq"]
        lines.append(f"|{c}|{' / '.join(f'{v["perplexity"]:.3f}' for v in r['occupancy'])}|{' / '.join(f'{v["si_snr_db_mean_per_file"]:.5f}' for v in r['partial_reconstruction'])}|{' / '.join(f'{v["relative_reduction"]:+.5f}' for v in r['residual_quantization'])}|")
    lines += ["", "前缀1/2级解码明显差于完整3级；第2级残差代理MSE有反向变化，C/D第3级也有小幅反向变化。保留原始诊断，不把投影码本/端到端目标下的代理MSE直接解释成质量贡献。稀疏plug-in联合熵有下偏，不能用24减该数断言浪费了多少bit，也不擅自改变码率。", "",
        "## 实际训练记录与恢复历史", "", "四组均有真实25k/50k/75k/100k共16次验证、GAN factor1；原始waveform/STFT/commitment/adv/FM/disc/total、码本占用和EMA记录保存在各metrics.jsonl及本audit。未启用独立逐batch training_components.jsonl，不补造缺失历史；恢复专用保存事件另存recovery_checkpoints.jsonl。", "",
        "初始共享attempt01约35分钟/可见约6000步未到首次保存，更新丢弃；attempt02在加载阶段因旧独占规则停止，无新优化；attempt03约1575批/6分40秒未保存，更新丢弃。这些不计入成品继承步数。旧档案和setup/profile均未重建。", "",
        "恢复I/O启用后的attempt04于11月7日01:07因实际显存跌破当时8GiB线停止，已有last A75000/B76000/C73000/D73000，丢弃可见未保存更新约376/228/451/677步。完整权重/优化器/EMA及日志SHA存RECOVERY04和attempt04归档。", "",
        "用户随后明确取消实时资源检测：仅启动前GPUfree>=8GiB/磁盘>=10GiB，启动后不再GPU/磁盘实时轮询、不会因外部PID或剩余显存主动停训，保留每1000步原子保存。policy05只替换了无训练子进程的等待器，没有额外优化丢失；恢复worker裁剪/RNG不是逐bit重放。", "",
        "曾通过原35项回归+7项流程及后续56项CPU检查；用户要求直接跑后未新增GPU测试。独立恢复短测被用户要求取消，保留日志但不称通过，正式初始化从未使用smoke更新。已有四组完整fullGAN两步profile证据保持。", "",
        "## 权重与试听路径", "", "原音目录：`"+str(REFERENCE)+"`。", "", "当前仍保留的最高分父模型重建：`"+str(ROOT/"runs/champion6_b_s3407_fourier_gru/evaluation/reconstructed")+"`。", "", "本批最高分B的重建：`"+a["best_new"]["evaluation"]+"/reconstructed`。", "", "|组|选中checkpoint SHA256|重建目录|", "|---|---|---|"]
    for c,x in a["cells"].items():
        n=x["selected"];lines.append(f"|{c}|`{n['checkpoint_sha256']}`|`{n['evaluation']}/reconstructed`|")
    lines += ["", "全部16个step快照、best/last和历史parent/teacher/averaging等均保留，不做清理。冻结strong_baseline_v2仍46.7463430683，登记和checkpoint SHA未改。未新增sealed LibriTTS评测、未自动晋升或启动下一批。", "",
        "本批使用同一父模型/单一新阶段种子，且反复在同一开发集选模；不能据此给出种子泛化不确定性或盲测结论。下一批须先由用户批准新方案。当前结束并删除本批监控。", "",
        "证据：CHAMPION7_PLAN.md、SETUP/PROFILE/SHARED_RESTART/RECOVERY01–04/RESOURCE_POLICY05.audit，CHAMPION7_RESULTS.audit，EXPERIMENT_LOG.md中16节点+4主记录。"]
    (ROOT/"CHAMPION7_RESULTS.md").write_text("\n".join(lines)+"\n")


if __name__=="__main__":main()
