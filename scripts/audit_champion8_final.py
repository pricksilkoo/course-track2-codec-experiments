#!/usr/bin/env python3
"""Independently audit the four existing zero-update candidates; assemble reports."""
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import soundfile as sf
import torch
import yaml

from prepare_champion8 import ROOT, CELLS, PARENT, PARENT_SHA, REFERENCE, digest, tensors_digest
from audit_champion7_final import audit_metrics, record_check, deltas, METRICS
from ssp_codec.model import CourseCodec
from ssp_codec.config import load_config
from ssp_codec.decoder_interpolation import interpolate_decoder


def read(path):return json.loads(Path(path).read_text())


def append_once(path, marker, content):
    text=path.read_text()
    if marker in text:
        assert text.split(marker,1)[1].strip()==content.strip(), "Preserve existing archive; content changed"
    else:path.write_text(text.rstrip()+"\n\n"+marker+"\n\n"+content.strip()+"\n")


def main():
    torch.set_num_threads(4)
    setup=read(ROOT/"CHAMPION8_SETUP.audit")
    assert tuple(setup["cells"])==CELLS
    assert setup["parent_sha256"]==PARENT_SHA and digest(PARENT)==PARENT_SHA
    assert setup["data_counts"]=={"train":394988,"valid":14596}
    for p,h in setup["source_sha256_unchanged"].items():assert digest(ROOT/p)==h
    for p,h in setup["data_hashes"].items():assert digest(ROOT/p)==h
    originals={p.name:sf.info(p) for p in sorted(REFERENCE.glob("*.wav"))}
    assert len(originals)==200
    for name,h in setup["frozen200_sha256"].items():
        assert digest(REFERENCE/name)==h
        assert originals[name].samplerate==16000 and originals[name].channels==1
    parent=torch.load(PARENT,map_location="cpu",weights_only=False)
    assert parent["global_step"]==500000
    model=CourseCodec(**parent["model_config"])
    params=set(dict(model.named_parameters()))
    psummary=audit_metrics(PARENT.parent.parent/"evaluation/metrics",set(originals))
    assert psummary["objective_quality_score"]==setup["parent_score"]
    log=(ROOT/"EXPERIMENT_LOG.md").read_text()
    registry=ROOT/"model_registry/strong_baseline_v2.json"
    old=read(ROOT/"CHAMPION7_RESULTS.audit")["frozen_v2"]
    assert digest(registry)==old["registry_sha256"]
    reg=read(registry);assert digest(ROOT/reg["checkpoint"])==old["checkpoint_sha256"]
    audit={"created_utc":datetime.now(timezone.utc).isoformat(),
        "git_commit_before_archive":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "kind":"four-point posthoc decoder-only interpolation development search",
        "new_gradient_updates":0,"read_only_audit_no_new_evaluation":True,
        "setup_sha256":digest(ROOT/"CHAMPION8_SETUP.audit"),
        "parent_checkpoint":str(PARENT),"parent_sha256":PARENT_SHA,"parent_summary":psummary,
        "sources_sha256_unchanged":setup["source_sha256_unchanged"],
        "data_counts":setup["data_counts"],"data_hashes":setup["data_hashes"],
        "fixed200_audio_hashes_match_frozen_setup":True,"frozen_v2_unchanged":old,
        "correctness_checks":"8 tiny CPU interpolation checks passed in1.79s; syntax checked. No GPU smoke/backward/training.",
        "cells":{},"completed_experiment_records":{}}
    for c in CELLS:
        run=ROOT/f"runs/champion8_{c}";out=run/"evaluation";e=setup["cells"][c]
        ck=run/"checkpoints/interpolated.pt";sha=digest(ck)
        assert sha==e["checkpoint_sha256"]==(out/"checkpoint.sha256").read_text().split()[0]
        assert (run/"PIPELINE_COMPLETE").is_file() and (out/"ROUNDTRIP_COMPLETE").is_file()
        assert read(run/"supervisor_state.json")["status"]=="complete"
        md=read(run/"run_metadata.json")
        assert md["checkpoint_sha256"]==sha and md["new_gradient_updates"]==0
        assert md["runtime_resource_poll"] is False and md["launch_free_MiB"]>=8192
        assert md["source_sha256"]==setup["source_sha256_unchanged"]
        pipeline=(run/"pipeline.log").read_text()
        assert "Traceback (most recent call last)" not in pipeline and '"status": "failed"' not in pipeline
        cfg=yaml.safe_load((run/"effective_config.yaml").read_text())
        assert digest(run/"effective_config.yaml")==e["config_sha256"]
        expected=load_config(ROOT/f"configs/champion8/{c}.yaml")
        expected["training"]["output_dir"]=str(run)
        assert cfg==expected and cfg["model"]==parent["model_config"]
        lineage=read(run/"lineage.json");assert lineage==e["lineage"]
        state=torch.load(ck,map_location="cpu",weights_only=False)
        assert state["global_step"]==0 and state["inference_only"] is True
        assert "optimizer" not in state and "discriminator" not in state and "discriminator_optimizer" not in state
        assert state["lineage"]==lineage and state["model_config"]==parent["model_config"]
        assert all(torch.isfinite(v).all() for v in state["model"].values() if v.is_floating_point())
        donor=torch.load(lineage["donor_checkpoint"],map_location="cpu",weights_only=False)
        assert donor["global_step"]==100000 and digest(lineage["donor_checkpoint"])==lineage["donor_sha256"]
        mixed,keys=interpolate_decoder(parent["model"],donor["model"],params,lineage["alpha"])
        assert keys==lineage["interpolated_parameter_keys"] and len(keys)==98
        assert all(torch.equal(state["model"][k],v) for k,v in mixed.items())
        frozen=lineage["frozen_tensor_keys"];assert len(frozen)==113
        assert all(torch.equal(state["model"][k],parent["model"][k]) for k in frozen)
        assert tensors_digest(state["model"],frozen)==lineage["frozen_tensors_sha256"]
        assert tensors_digest(state["model"],keys)==lineage["decoder_parameters_sha256"]
        model.load_state_dict(state["model"],strict=True)
        assert not (run/"metrics.jsonl").exists() and not (run/"TRAINING_COMPLETE").exists()
        s=audit_metrics(out/"metrics",set(originals))
        samples=frames=total=0;manifest=hashlib.sha256()
        assert len(list((out/"bitstreams").glob("*.bin")))==len(list((out/"reconstructed").glob("*.wav")))==200
        for name,info in originals.items():
            wav=out/"reconstructed"/name;signal,rate=sf.read(wav,dtype="float32",always_2d=True)
            assert rate==16000 and signal.shape==(info.frames,1) and np.isfinite(signal).all()
            bit=out/"bitstreams"/Path(name).with_suffix(".bin")
            pb=PARENT.parent.parent/"evaluation/bitstreams"/bit.name
            assert bit.read_bytes()==pb.read_bytes()
            side=read(bit.with_suffix(".json"))
            assert side["num_samples"]==info.frames and side["sample_rate"]==16000
            assert side["frame_samples"]==160 and side["bits_per_frame"]==24 and side["bitrate_bps"]==2400
            assert bit.stat().st_size==3*math.ceil(info.frames/160)
            samples+=info.frames;frames+=math.ceil(info.frames/160);total+=bit.stat().st_size
            manifest.update(f"{name} {info.frames} {digest(wav)} {digest(bit)}\n".encode())
        assert (samples,frames,total)==(16197971,101286,303858)
        actual=read(out/"roundtrip_audit.json")
        assert actual=={"files":200,"samples":samples,"frames":frames,"actual_bytes":total,
            "audio_lengths_verified":True,"all200_bitstreams_identical_to_parent":True}
        cost=read(out/"complexity.json");assert cost==e["complexity"]
        assert cost["parameters"]==1868064 and cost["total_mflop_per_s"]<=700 and cost["decoder_mflop_per_s"]<=300
        assert cost["algorithmic_lookahead_ms"]==30 and cost["unclassified_mmac_per_s"]==0 and cost["bitrate_bps"]==2400
        audit["completed_experiment_records"][f"champion8_{c}"]=record_check(log,f"champion8_{c}",sha)
        audit["cells"][c]={"checkpoint":str(ck),"checkpoint_sha256":sha,"lineage":lineage,
            "summary":s,"delta_vs_parent":deltas(s,psummary),"roundtrip":actual,
            "decoded_audio_finite":True,"per_file_audio_and_bitstream_manifest_sha256":manifest.hexdigest(),
            "complexity":cost,"original_dir":str(REFERENCE),"reconstructed_dir":str(out/"reconstructed"),
            "interpolation_and_all_frozen_tensors_independently_verified":True,
            "no_actual_pipeline_failure_or_recovery_observed":True,
            "runtime_resource_poll":False,"launch_free_MiB":md["launch_free_MiB"]}
        del donor,state,mixed
    best=max(CELLS,key=lambda c:audit["cells"][c]["summary"]["objective_quality_score"])
    improved=audit["cells"][best]["delta_vs_parent"]["score"]>0
    winner=audit["cells"][best] if improved else {"checkpoint":str(PARENT),"checkpoint_sha256":PARENT_SHA,
        "summary":psummary,"delta_vs_parent":{"score":0},"reconstructed_dir":str(PARENT.parent.parent/"evaluation/reconstructed")}
    audit["selection"]={"best_new_cell":best,"any_improvement":improved,"selected":"champion8_"+best if improved else "parent_champion6_b_s3407_fourier_gru",
        "checkpoint":winner["checkpoint"],"checkpoint_sha256":winner["checkpoint_sha256"],
        "score":winner["summary"]["objective_quality_score"],"gain_vs_parent":winner["delta_vs_parent"]["score"],
        "reconstructed_dir":winner["reconstructed_dir"],"tie_rule":"keep parent; then preregistered cell order"}
    assert all(digest(ROOT/p)==h for p,h in setup["source_sha256_unchanged"].items())
    assert digest(registry)==old["registry_sha256"] and len(audit["completed_experiment_records"])==4
    (ROOT/"runs/champion8_setup/selection.json").write_text(json.dumps(audit["selection"],indent=2)+"\n")
    (ROOT/"CHAMPION8_RESULTS.audit").write_text(json.dumps(audit,indent=2)+"\n")
    rows=[];change=[]
    for c in CELLS:
        e=audit["cells"][c];s=e["summary"];d=e["delta_vs_parent"]
        rows.append(f"|{c}|{e['lineage']['alpha']:.2f}|{s['objective_quality_score']:.10f}|{d['score']:+.10f}|"+"|".join(f"{s['means'][m]:.8f}" for m in METRICS)+"|")
        change.append(f"|{c}|"+"|".join(f"{d[m]:+.8f}" for m in METRICS)+"|")
    verdict=(f"最高新候选{best}，{winner['summary']['objective_quality_score']:.10f}，比父模型增加{winner['delta_vs_parent']['score']:.10f}。" if improved else
        f"四个候选均未超过父模型；最高新候选{best}为{audit['cells'][best]['summary']['objective_quality_score']:.10f}，保留原51.624336父模型。")
    report=f"""# CHAMPION8结果：四个零训练解码器插值候选

{verdict}

## 设计和来源

父模型CHAMPION6 B500k固定200开发分数51.62433613863932；donor为CHAMPION7 A/B的预登记100k快照（累计600k），分数51.52590320119037/51.53128750969333。
本批无训练、无优化器更新、新增梯度步数0，不是未训练初始化。参数=(1-alpha)父+alpha donor。
只混合98个decoder/synthesis可学习参数，其余113个张量，包括encoder/analysis GRU/latent norm、整个RVQ输入输出投影/码本/EMA及所有buffers逐位保持父模型。
导出inference_only权重，global_step0仅表示后处理新增训练步0，不含误导性的旧优化器/判别器。三份源文件SHA前后不变，完整来源及候选SHA见CHAMPION8_RESULTS.audit/SETUP.audit。

## 全部四个固定开发集搜索点

|候选|donor占比|总分|Δ对父|PESQ|ESTOI|SI-SNR dB|UTMOS|
|---|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

|对父变化|ΔPESQ|ΔESTOI|ΔSI-SNR dB|ΔUTMOS|
|---|---:|---:|---:|---:|
{chr(10).join(change)}

只按总分择优，四分量退步如实列出，不声称全分量支配。只有四个登记系数，没有追加alpha、搜索seed、微调或选择性扩展。
这是同一开发集四点搜索，不是独立测试提升证明；小增益可能有开发集择优偏差。不更改CHAMPION6确认结论。

## 实际码流、接口和审计

每候选实际重新编码/解码200文件，逐文件码流均与父模型字节完全相同（不仅张量冻结），每文件3×ceil(samples/160)字节。
每候选16197971samples、101286frames、303858实际字节；16k单声道、原长度、音频有限。CSV独立重算四分量及总分与summary差<1e-10；4条实验记录complete且对应权重SHA。
所有候选1868064参数、666.3072total/257.632decoder MFLOP/s、2400bps、lookahead30ms、unclassifiedMAC0；包含GRU门/调制/保守IRFFT/OLA。
RVQ及编码逐tensor和全部实际码流不变，未重复跑RVQ GPU消融，父模型完整analysis_gru/synthesis/RVQ诊断仍保留；不能据此声称新decoder的残差代理诊断已重测。
仅运行必要CPU参数检查（8项1.79秒通过）和解析复杂度/真实评测，没有GPU smoke、反向训练或新的25k训练验证记录；未启用的训练日志不补造。
共享资源只启动前检查8GiB显存/10GiB磁盘，运行中无GPU/磁盘轮询、无外部PID触发停止。无训练恢复或RNG重放；本批实际失败/恢复情况见4个pipeline/state记录。
未新增sealed LibriTTS评测，冻结strong_baseline_v2登记/权重保持46.746343不变，未自动晋升；保留所有来源和候选，不清理历史。

## 试听与下一步

原音：`{REFERENCE}`。
本次总分选用模型：`{winner['checkpoint']}`。
选用重建：`{winner['reconstructed_dir']}`。
四候选分别在`runs/champion8_CELL/evaluation/reconstructed/`，文件名与原音相同。
完整证据CHAMPION8_RESULTS.audit、CHAMPION8_SETUP.audit、EXPERIMENT_LOG.md；预注册CHAMPION8_PLAN.md。
本批仅完成这四个零训练候选，不自动增加系数或开始低LR短程微调；下一批训练需用户另行批准。
"""
    (ROOT/"CHAMPION8_RESULTS.md").write_text(report)
    append_once(ROOT/"CODEC_EXPERIMENT_REVIEW.md","## CHAMPION8完整复盘（2026-11-08，零训练解码器插值）",report)
    history=f"""{verdict}
User approved exactly4 posthoc decoder-only parameter interpolations: C7A100k donor.10/.25 and C7B100k donor.10/.25, with trained C6B500k parent51.62433613863932. Zero new optimizer updates;98 decoder parameters mixed/113 tensors frozen, entire encoder/RVQ projections/codebook/EMA/all buffers parent-exact. Inference-only exports never overwrite parents.
All4 fixed200 actual encode/decode/quality/complexity complete and all4 experiment records verified. Each200 bitstreams byte-identical to parent,16197971samples/101286frames/303858bytes,16kmono original lengths/finite audio; independent CSV reaggregation and checkpoint/config/source hashes pass.1868064params,666.3072/257.632MFLOP/s,2400bps/30ms/unclassified0 unchanged. All scores/components/regressions reported in CHAMPION8_RESULTS.md/.audit and self-contained Chinese review. No sealed evaluation, registry promotion, new alpha nodes or automatic training. Next training requires separate approval.
"""
    append_once(ROOT/"EXPERIMENT_HISTORY.md","## CHAMPION8 complete — four zero-training decoder interpolations (2026-11-08)",history)
    print(json.dumps(audit["selection"],indent=2))


if __name__=="__main__":main()
