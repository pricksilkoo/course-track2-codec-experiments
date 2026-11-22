from pathlib import Path
import importlib.util,sys,json
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import supervise_champion12_idle as idle

def test_shared_gpu_stays_waiting_even_when_memory_would_fit(tmp_path,monkeypatch):
    calls=[]
    class Waiting(Exception):pass
    def snapshot(gpu):calls.append(gpu);return 45488,45000,[123]
    monkeypatch.setattr(idle.time,'sleep',lambda seconds:(_ for _ in ()).throw(Waiting()))
    gate=idle.make_idle_gate(snapshot,tmp_path)
    with pytest.raises(Waiting):gate(2)
    record=json.loads((tmp_path/'supervisor_state.json').read_text())
    assert calls==[2] and record['existing_gpu_pids']==[123]
    assert record['status']=='waiting_for_idle_gpu_after_repeated_oom'
    assert not record['runtime_resource_poll']

def test_idle_gpu_returns_real_snapshot_without_runtime_poll(tmp_path,monkeypatch):
    monkeypatch.setattr(idle.time,'sleep',lambda _:pytest.fail('idle startup should not dwell'))
    calls=[]
    def snapshot(gpu):calls.append(gpu);return 45488,45000,[]
    assert idle.make_idle_gate(snapshot,tmp_path)(3)==(45488,45000,[])
    assert calls==[3] and not (tmp_path/'supervisor_state.json').exists()
