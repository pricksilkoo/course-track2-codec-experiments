"""Atomic, resume-only snapshots; these are not validation/search endpoints."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path

import torch


def save_checkpoint_atomic(state, path):
    """Leave the previous checkpoint intact if saving is interrupted."""
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    torch.save(state, temporary)
    with temporary.open("rb") as handle:
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def save_recovery_checkpoint(*, checkpoint_dir, model, discriminator,
                             optimizer, discriminator_optimizer, model_config,
                             epoch, batch_in_epoch, global_step, best_validation):
    """Save only completed updates, without inventing validation measurements."""
    state = {
        "checkpoint_kind": "recovery_only",
        "epoch": epoch, "batch_in_epoch": batch_in_epoch,
        "global_step": global_step, "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "discriminator": discriminator.state_dict(),
        "discriminator_optimizer": discriminator_optimizer.state_dict(),
        "model_config": model_config, "best_validation": best_validation,
    }
    save_checkpoint_atomic(state, checkpoint_dir / "last.pt")
    event = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
             "checkpoint_kind": "recovery_only", "global_step": global_step,
             "epoch": epoch, "batch_in_epoch": batch_in_epoch}
    with (checkpoint_dir.parent / "recovery_checkpoints.jsonl").open("a") as handle:
        handle.write(json.dumps(event) + "\n")


def recovery_due(global_step, interval_steps, validation_interval):
    if interval_steps < 0:
        raise ValueError("recovery_checkpoint_interval_steps must be nonnegative")
    return (interval_steps > 0 and global_step > 0
            and global_step % interval_steps == 0
            and global_step % validation_interval != 0)
