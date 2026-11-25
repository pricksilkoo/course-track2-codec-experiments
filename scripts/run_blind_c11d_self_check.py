#!/usr/bin/env python3
"""One explicitly frozen C11D blind encode/decode/format check. No quality scoring."""
import datetime, fcntl, hashlib, json, os, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/track2_blind_20261125"

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    lock = (RUN / ".self_check.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if (RUN / "SELF_CHECK_COMPLETE").exists():
        return
    plan = json.loads((RUN / "frozen_plan.json").read_text())
    ck = Path(plan["checkpoint"])
    assert digest(ck) == plan["checkpoint_sha256"]
    out = Path(plan["outputs"])
    out.mkdir(exist_ok=True)
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONNOUSERSITE": "1", "OMP_NUM_THREADS": "4", "MKL_NUM_THREADS": "4", "OPENBLAS_NUM_THREADS": "4"}
    def command(*args):
        print("RUN", *map(str,args), flush=True)
        subprocess.run([str(ROOT / ".venv-codec/bin/python"), *map(str,args)], cwd=ROOT, env=env, check=True)
    command("scripts/encode.py", "--checkpoint", ck, "--input-dir", plan["reference_dir"], "--output-dir", out / "bitstreams", "--device", "cpu")
    command("scripts/decode.py", "--checkpoint", ck, "--bitstream-dir", out / "bitstreams", "--output-dir", out / "reconstructed", "--device", "cpu")
    command("scripts/validate_submission.py", "--input-dir", plan["reference_dir"], "--bitstream-dir", out / "bitstreams", "--output-dir", out / "reconstructed")
    import numpy as np
    import soundfile as sf
    expected = {x["file"] for x in plan["files"]}
    assert {x.name for x in (out / "reconstructed").glob("*.wav")} == expected
    assert {x.stem for x in (out / "bitstreams").glob("*.bin")} == {Path(x).stem for x in expected}
    assert {x.stem for x in (out / "bitstreams").glob("*.json")} == {Path(x).stem for x in expected}
    evidence = []
    for row in plan["files"]:
        ref = Path(plan["reference_dir"]) / row["file"]
        wav = out / "reconstructed" / row["file"]
        bits = out / "bitstreams" / Path(row["file"]).with_suffix(".bin")
        meta = bits.with_suffix(".json")
        assert digest(ref) == row["sha256"]
        audio, rate = sf.read(wav, dtype="float32", always_2d=True)
        assert rate == 16000 and audio.shape == (row["samples"], 1) and np.isfinite(audio).all()
        assert bits.stat().st_size == row["expected_bytes"]
        m = json.loads(meta.read_text())
        assert m == {"sample_rate":16000,"num_samples":row["samples"],"frame_samples":160,"bits_per_frame":24,"bitrate_bps":2400}
        evidence.append({**row, "actual_bytes": bits.stat().st_size, "bitstream_sha256": digest(bits), "metadata_sha256": digest(meta), "reconstructed_sha256": digest(wav), "finite_audio": True})
    def tree_hash(key):
        return hashlib.sha256("".join(x["file"] + " " + x[key] + "\n" for x in evidence).encode()).hexdigest()
    audit = {"completed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "scope":plan["user_approved_scope"], "checkpoint":str(ck),"checkpoint_sha256":digest(ck),"archive_sha256":plan["archive_sha256"],"original_folder":plan["reference_dir"],"bitstream_folder":str(out/"bitstreams"),"reconstructed_folder":str(out/"reconstructed"),"files":len(evidence),"samples":sum(x["samples"] for x in evidence),"frames":sum(x["actual_bytes"] for x in evidence)//3,"actual_bytes":sum(x["actual_bytes"] for x in evidence),"total_delay_ms":30,"total_mflop_per_s":plan["complexity"]["total_mflop_per_s"],"decoder_mflop_per_s":plan["complexity"]["decoder_mflop_per_s"],"public200dev_score":50.24576933222705,"blind_quality_metrics_computed":False,"blind_model_selection_performed":False,"cpu_only":True,"input_tree_sha256":tree_hash("sha256"),"bitstream_tree_sha256":tree_hash("bitstream_sha256"),"reconstructed_tree_sha256":tree_hash("reconstructed_sha256"),"per_file":evidence}
    assert audit["files"]==50 and audit["samples"]==4204525 and audit["frames"]==26300 and audit["actual_bytes"]==78900
    (RUN/"self_check.audit.json").write_text(json.dumps(audit,indent=2)+"\n")
    (ROOT/"BLIND_C11D_SELF_CHECK_RESULTS.audit").write_text(json.dumps(audit,indent=2)+"\n")
    (RUN/"SELF_CHECK_COMPLETE").touch()
    print("SELF_CHECK_COMPLETE", json.dumps({k:v for k,v in audit.items() if k!="per_file"}),flush=True)

if __name__ == "__main__":
    main()
