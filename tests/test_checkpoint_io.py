from pathlib import Path
import json
import sys

import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ssp_codec.checkpoint_io import save_checkpoint_atomic, save_recovery_checkpoint, recovery_due


def test_atomic_failure_preserves_previous_last(tmp_path, monkeypatch):
    path = tmp_path / "last.pt"
    save_checkpoint_atomic({"global_step": 1000}, path)
    def broken_save(state, temporary):
        Path(temporary).write_bytes(b"partial")
        raise OSError("interrupted write")
    monkeypatch.setattr(torch, "save", broken_save)
    with pytest.raises(OSError):
        save_checkpoint_atomic({"global_step": 2000}, path)
    assert torch.load(path, weights_only=False)["global_step"] == 1000


def test_recovery_roundtrip_complete_optimizer_and_buffers(tmp_path):
    model = torch.nn.Linear(2, 2)
    model.register_buffer("ema", torch.tensor([3.0]))
    disc = torch.nn.Linear(2, 1)
    opt = torch.optim.AdamW(model.parameters())
    dopt = torch.optim.AdamW(disc.parameters())
    model(torch.ones(1, 2)).sum().backward(); opt.step()
    disc(torch.ones(1, 2)).sum().backward(); dopt.step()
    before = torch.get_rng_state().clone()
    directory = tmp_path / "checkpoints"; directory.mkdir()
    save_recovery_checkpoint(checkpoint_dir=directory, model=model, discriminator=disc,
        optimizer=opt, discriminator_optimizer=dopt, model_config={"test": True},
        epoch=2, batch_in_epoch=17, global_step=1000, best_validation=1.23)
    assert torch.equal(before, torch.get_rng_state())
    state = torch.load(directory / "last.pt", weights_only=False)
    assert state["checkpoint_kind"] == "recovery_only"
    assert state["global_step"] == 1000 and state["batch_in_epoch"] == 17
    assert state["epoch"] == 2 and state["best_validation"] == 1.23
    assert "validation_metrics" not in state
    assert "quantizer_usage" not in state
    clone = torch.nn.Linear(2, 2); clone.register_buffer("ema", torch.zeros(1))
    clone.load_state_dict(state["model"])
    assert torch.equal(clone.ema, model.ema)
    opt2 = torch.optim.AdamW(clone.parameters()); opt2.load_state_dict(state["optimizer"])
    dclone = torch.nn.Linear(2, 1); dclone.load_state_dict(state["discriminator"])
    dopt2 = torch.optim.AdamW(dclone.parameters()); dopt2.load_state_dict(state["discriminator_optimizer"])
    assert all(int(s["step"]) == 1 for s in opt2.state.values())
    assert all(int(s["step"]) == 1 for s in dopt2.state.values())
    assert list(directory.iterdir()) == [directory / "last.pt"]
    assert not (tmp_path / "metrics.jsonl").exists()
    event = json.loads((tmp_path / "recovery_checkpoints.jsonl").read_text())
    assert event["global_step"] == 1000


@pytest.mark.parametrize("step,interval,expected", [(1000,0,False),(999,1000,False),
    (1000,1000,True),(25000,1000,False),(100000,1000,False),(0,1000,False)])
def test_recovery_does_not_expand_validation_search(step, interval, expected):
    assert recovery_due(step, interval, 25000) is expected


def test_negative_interval_rejected():
    with pytest.raises(ValueError): recovery_due(1000, -1, 25000)
