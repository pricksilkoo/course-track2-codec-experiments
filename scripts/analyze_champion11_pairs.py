import csv,json
from pathlib import Path
import numpy as np
from collections import defaultdict
frozen=json.loads(Path("CHAMPION10_SETUP.audit").read_text())["fixed200_sha256"]
metrics=["score","PESQ","ESTOI","SI_SNR","UTMOS"]
def values(cell):
    folder=Path(f"runs/champion10_{cell}/evaluation/step_00500000/metrics")
    rows=list(csv.DictReader((folder/"per_file.csv").open()))
    data={r["file"]:[float(r[m]) for m in metrics[1:]] for r in rows}
    assert len(rows)==len(data)==200 and data.keys()==frozen.keys()
    raw=np.array([data[name] for name in sorted(data)])
    score=25*np.clip((raw-np.array([1,0,-10,1]))/np.array([3.5,1,40,4]),0,1).sum(axis=1)
    a=np.column_stack((score,raw))
    record=json.loads((folder/"summary.json").read_text())
    np.testing.assert_allclose(a.mean(axis=0),[record["objective_quality_score"],*(record["means"][m] for m in metrics[1:])],rtol=0,atol=1e-10)
    return a
seed=20261117
indices=np.random.default_rng(seed).integers(0,200,(20000,200))
a,c,d=map(values,["a_base","c_dec","d_both"])
ev={}
for label,diff in (("C-A",c-a),("D-C",d-c)):
    samples=diff[indices].mean(axis=1)
    ev[label]={m:dict(mean=float(diff[:,i].mean()),percentile95=np.quantile(samples[:,i],[.025,.975]).tolist(),positive_files=int((diff[:,i]>0).sum())) for i,m in enumerate(metrics)}
    scores=np.sort(diff[:,0])
    ev[label]["leave_out_largest_10_score_deltas_mean"]=float(scores[:-10].mean())
print(json.dumps({"source":"CHAMPION10 500k frozen 200 dev files","resampling":"paired file-level percentile bootstrap; descriptive on this dev set, does not measure seed variability or account for speaker dependence","seed":seed,"replicates":20000,"contrasts":ev},indent=2))
