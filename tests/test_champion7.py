"""CPU-only orchestration checks; no GPU process or external signal is used."""
import importlib.util
from pathlib import Path
import signal
import sys
from unittest.mock import Mock

import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_hash_and_checkpoint_step(tmp_path):
    runner = module("run_champion7_experiment")
    data = tmp_path / "abc"
    data.write_bytes(b"abc")
    assert runner.digest(data) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    state = tmp_path / "state.pt"
    torch.save({"global_step": 25000}, state)
    assert runner.checkpoint_step(state) == 25000


def test_score_search_and_earliest_tie():
    runner = module("run_champion7_experiment")
    records = [{"additional_step": step, "summary": {"objective_quality_score": score}}
        for step, score in [(100000, 52.0), (25000, 51.9), (50000, 52.0), (75000, 51.0)]]
    assert runner.select_endpoint(records)["additional_step"] == 50000


def test_reject_unregistered_run(monkeypatch):
    runner = module("run_champion7_experiment")
    monkeypatch.setattr(sys, "argv", ["runner", "champion6_b_s3407_fourier_gru", "0", "anything", "100000"])
    with pytest.raises(ValueError):
        runner.main()


def test_reject_changed_budget(monkeypatch):
    runner = module("run_champion7_experiment")
    monkeypatch.setattr(sys, "argv", ["runner", "champion7_a_continue", "0", "configs/champion7/a_continue.yaml", "200000"])
    with pytest.raises(ValueError):
        runner.main()


def test_reject_mismatched_cell_config(monkeypatch):
    runner = module("run_champion7_experiment")
    monkeypatch.setattr(sys, "argv", ["runner", "champion7_a_continue", "0", "configs/champion7/d_both.yaml", "100000"])
    with pytest.raises(AssertionError):
        runner.main()


def test_never_duplicate_completed_run(monkeypatch, tmp_path):
    runner = module("run_champion7_experiment")
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    run = tmp_path / "runs/champion7_a_continue"
    run.mkdir(parents=True)
    (run / "PIPELINE_COMPLETE").touch()
    monkeypatch.setattr(sys, "argv", ["runner", "champion7_a_continue", "0", "configs/champion7/a_continue.yaml", "100000"])
    forbidden = Mock(side_effect=AssertionError("Must not launch a subprocess"))
    monkeypatch.setattr(runner.subprocess, "run", forbidden)
    runner.main()
    forbidden.assert_not_called()


def test_supervisor_signals_only_private_group(monkeypatch):
    supervisor = module("supervise_champion7")
    child = Mock()
    child.pid = 12345
    child.poll.return_value = None
    send = Mock()
    monkeypatch.setattr(supervisor.os, "killpg", send)
    supervisor.stop_own_pipeline(child)
    send.assert_called_once_with(child.pid, signal.SIGTERM)
    child.wait.assert_called_once_with(timeout=30)
