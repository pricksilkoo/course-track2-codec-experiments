"""Pure time/state tests, no sleeping, GPU calls, training, or signals."""
import importlib.util
from pathlib import Path


def gate():
    path = Path(__file__).resolve().parents[1] / "scripts/supervise_champion7.py"
    spec = importlib.util.spec_from_file_location("idle_supervisor", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.CapacityWindow()


def test_busy_device_never_eligible_even_with_free_memory():
    g = gate()
    assert not g.ready(0, 45000, [123])
    assert not g.ready(10000, 45000, [123])
    assert g.since is None


def test_ten_minute_continuous_idle_required():
    g = gate()
    assert not g.ready(10, 45000, [])
    assert not g.ready(609.9, 45000, [])
    assert g.ready(610, 45000, [])


def test_other_job_arrival_resets_timer():
    g = gate()
    assert not g.ready(0, 45000, [])
    assert not g.ready(599, 45000, [123])
    assert not g.ready(600, 45000, [])
    assert not g.ready(1199, 45000, [])
    assert g.ready(1200, 45000, [])


def test_memory_shortage_also_resets_timer():
    g = gate()
    assert not g.ready(0, 45000, [])
    assert not g.ready(599, 20479, [])
    assert not g.ready(600, 45000, [])
    assert g.ready(1200, 45000, [])


def test_existing_explicit_shared_mode_still_requires_stability():
    g = gate()
    assert not g.ready(0, 23000, [123], True)
    assert not g.ready(4.9, 23000, [123], True)
    assert g.ready(5, 23000, [123], True)
