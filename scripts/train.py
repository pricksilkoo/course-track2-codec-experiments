#!/usr/bin/env python3
"""Train the fixed-16-kHz / fixed-2.4-kbps neural codec baseline.

Run directly for one device, or launch with ``torchrun`` for distributed data
parallel training. In the latter case ``WORLD_SIZE`` is set by torchrun and
the script automatically enables DDP.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
import random
import shlex
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import torch.distributed as dist
import torch.nn.functional as F
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.optim import AdamW
from torch.utils.data import DataLoader, DistributedSampler
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ssp_codec.adversarial import (  # noqa: E402
    MultiResolutionSTFTDiscriminator,
    discriminator_hinge_loss,
    feature_matching_loss,
    generator_hinge_loss,
)
from ssp_codec.data import WaveformDataset  # noqa: E402
from ssp_codec.config import apply_overrides, load_config  # noqa: E402
from ssp_codec.losses import multiscale_spectral_loss, negative_si_snr_loss  # noqa: E402
from ssp_codec.model import CourseCodec  # noqa: E402
from ssp_codec.schedules import distillation_factor  # noqa: E402


def build_semantic_teacher(
    config: dict, device: torch.device
) -> tuple[torch.nn.Module, int, torch.Tensor] | None:
    semantic = config.get("semantic_distillation", {})
    if not semantic.get("enabled", False):
        return None
    import torchaudio

    bundle_name = str(semantic.get("bundle", "WAVLM_BASE_PLUS"))
    if not hasattr(torchaudio.pipelines, bundle_name):
        raise ValueError(f"unknown torchaudio semantic teacher bundle: {bundle_name}")
    bundle = getattr(torchaudio.pipelines, bundle_name)
    if bundle.sample_rate != config["audio"]["sample_rate"]:
        raise ValueError("semantic teacher and codec sample rates do not match")
    teacher = bundle.get_model().to(device).eval()
    teacher.requires_grad_(False)
    layer = int(semantic.get("layer", 9))
    teacher_dim = int(semantic.get("feature_dim", 768))
    model_config = config["model"]
    semantic_dim = int(
        model_config.get("minimimi_semantic_dim", model_config["rvq_codebook_dim"])
        if model_config.get("quantizer_type") == "split_rvq"
        else model_config["rvq_codebook_dim"]
    )
    generator = torch.Generator(device="cpu")
    generator.manual_seed(int(config["seed"]) + 91_173)
    projection = torch.randn(teacher_dim, semantic_dim, generator=generator)
    projection, _ = torch.linalg.qr(projection, mode="reduced")
    return teacher, layer, projection.to(device)


def build_waveform_teacher(
    config: dict, device: torch.device
) -> tuple[CourseCodec, dict] | None:
    """Load an optional frozen codec teacher used only during training."""
    distillation = config.get("waveform_distillation", {})
    if not distillation.get("enabled", False):
        return None
    checkpoint = Path(str(distillation["checkpoint"]))
    if not checkpoint.is_absolute():
        checkpoint = ROOT / checkpoint
    state = torch.load(checkpoint, map_location=device, weights_only=False)
    teacher = CourseCodec(**state["model_config"]).to(device)
    teacher.load_state_dict(state["model"])
    teacher.eval()
    teacher.requires_grad_(False)
    return teacher, distillation


def semantic_teacher_targets(
    state: tuple[torch.nn.Module, int, torch.Tensor],
    reference: torch.Tensor,
    frames: int,
) -> torch.Tensor:
    teacher, layer, projection = state
    with torch.no_grad():
        features, _ = teacher.extract_features(reference[:, 0], num_layers=layer)
        target = features[-1]
        target = F.interpolate(
            target.transpose(1, 2), size=frames, mode="linear", align_corners=False
        ).transpose(1, 2)
        target = target @ projection.to(dtype=target.dtype)
        return F.normalize(target.float(), dim=-1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/baseline_16k_2p4k.yaml")
    parser.add_argument("--train-dir", help="recursively searched WAV/FLAC directory")
    parser.add_argument("--valid-dir", help="recursively searched WAV/FLAC directory")
    parser.add_argument("--train-manifest", help="one absolute audio path per line")
    parser.add_argument("--valid-manifest", help="one absolute audio path per line")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--output-dir", help="override training.output_dir from the YAML config")
    parser.add_argument(
        "--run-name",
        help="append a named run directory below training.output_dir",
    )
    parser.add_argument(
        "--set",
        dest="config_overrides",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="repeatable dotted config override, for example model.rvq_codebook_dim=32",
    )
    parser.add_argument("--resume", default=None)
    parser.add_argument(
        "--init-checkpoint",
        default=None,
        help="warm-start compatible model/discriminator tensors without optimizer state",
    )
    parser.add_argument("--epochs", type=int, default=None, help="override config")
    parser.add_argument(
        "--max-train-steps",
        type=int,
        default=None,
        help="optional per-epoch batch cap for a fast interface check",
    )
    parser.add_argument(
        "--max-total-steps",
        type=int,
        default=None,
        help="stop after this many optimizer steps across all epochs",
    )
    parser.add_argument(
        "--max-valid-steps",
        type=int,
        default=None,
        help="optional validation batch cap for a fast interface check",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=None,
        help="override DataLoader worker count; use 0 in restricted environments",
    )
    args = parser.parse_args()
    for split in ("train", "valid"):
        directory = getattr(args, f"{split}_dir")
        manifest = getattr(args, f"{split}_manifest")
        if (directory is None) == (manifest is None):
            parser.error(f"provide exactly one of --{split}-dir and --{split}-manifest")
    if args.resume and args.init_checkpoint:
        parser.error("--resume and --init-checkpoint are mutually exclusive")
    return args


def load_compatible_state(
    module: torch.nn.Module,
    source: dict[str, torch.Tensor],
    label: str,
    skip_prefixes: tuple[str, ...] = (),
) -> None:
    """Load matching tensors while reporting intentionally new model parts."""
    target = module.state_dict()
    source = dict(source)
    expanded_lookahead = []
    for key, target_value in target.items():
        source_value = source.get(key)
        if (
            source_value is not None
            and key.endswith("lookahead.depthwise.weight")
            and source_value.ndim == 3
            and target_value.ndim == 3
            and source_value.shape[:2] == target_value.shape[:2]
            and source_value.shape[-1] < target_value.shape[-1]
        ):
            # Preserve the source lookahead function exactly and initialize only
            # the newly exposed future taps to zero. This avoids a discontinuity
            # when a latency-capacity study expands the depthwise kernel.
            expanded = target_value.new_zeros(target_value.shape)
            expanded[..., : source_value.shape[-1]] = source_value
            source[key] = expanded
            expanded_lookahead.append(
                f"{key}:{source_value.shape[-1]}->{target_value.shape[-1]}"
            )
    compatible = {
        key: value
        for key, value in source.items()
        if key in target
        and target[key].shape == value.shape
        and not key.startswith(skip_prefixes)
    }
    incompatible = module.load_state_dict(compatible, strict=False)
    skipped = len(source) - len(compatible)
    print(
        f"Warm-started {label}: {len(compatible)} tensors loaded, "
        f"{skipped} source tensors skipped, {len(incompatible.missing_keys)} new tensors"
    )
    if expanded_lookahead:
        print("Expanded lookahead kernels with zero new taps: " + ", ".join(expanded_lookahead))


def scheduled_learning_rate(
    base_learning_rate: float,
    minimum_learning_rate: float,
    warmup_steps: int,
    step: int,
    total_steps: int,
) -> float:
    """Linear warm-up followed by cosine decay."""
    if warmup_steps > 0 and step <= warmup_steps:
        return base_learning_rate * step / warmup_steps
    if total_steps <= warmup_steps:
        return base_learning_rate
    progress = min(1.0, max(0.0, (step - warmup_steps) / (total_steps - warmup_steps)))
    cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
    return minimum_learning_rate + (base_learning_rate - minimum_learning_rate) * cosine


def distributed_context(requested: str) -> tuple[torch.device, int, int, bool]:
    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    rank = int(os.environ.get("RANK", "0"))
    distributed = world_size > 1
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("--device cuda was requested but CUDA is unavailable")
    use_cuda = torch.cuda.is_available() if requested == "auto" else requested == "cuda"
    if distributed:
        dist.init_process_group(backend="nccl" if use_cuda else "gloo")
        if use_cuda:
            local_rank = int(os.environ["LOCAL_RANK"])
            torch.cuda.set_device(local_rank)
            return torch.device("cuda", local_rank), rank, world_size, True
        return torch.device("cpu"), rank, world_size, True
    return torch.device("cuda" if use_cuda else "cpu"), rank, world_size, False


def make_dataset(args: argparse.Namespace, split: str, config: dict) -> WaveformDataset:
    return WaveformDataset(
        directory=getattr(args, f"{split}_dir"),
        manifest=getattr(args, f"{split}_manifest"),
        sample_rate=config["audio"]["sample_rate"],
        segment_samples=config["audio"]["segment_samples"],
        deterministic=split == "valid",
    )


def adversarial_factor(global_step: int, config: dict) -> float:
    """Linearly introduce GAN losses after a reconstruction-only warm-up."""
    start = int(config["adversarial"]["start_step"])
    warmup = int(config["adversarial"]["warmup_steps"])
    if global_step < start:
        return 0.0
    if warmup <= 0:
        return 1.0
    return min(1.0, (global_step - start + 1) / warmup)


def evaluate(
    model: torch.nn.Module,
    discriminator: MultiResolutionSTFTDiscriminator,
    loader: DataLoader,
    device: torch.device,
    config: dict,
    limit: int,
    distributed: bool,
    gan_factor: float,
) -> tuple[dict[str, float], dict[str, list[float] | list[int]]]:
    model.eval()
    discriminator.eval()
    totals = torch.zeros(6, device=device)
    count = torch.zeros((), device=device)
    code_histogram = torch.zeros((3, 256), device=device)
    with torch.inference_mode():
        for step, reference in enumerate(loader):
            if step >= limit:
                break
            reference = reference.to(device, non_blocking=True)
            reconstructed, indices, quantizer_loss = model(reference)
            waveform_loss = F.l1_loss(reconstructed, reference)
            spectral_loss = multiscale_spectral_loss(
                reconstructed,
                reference,
                config["loss"]["fft_sizes"],
                config["loss"].get("spectral_convergence_weight", 0.0),
                config["loss"].get("linear_magnitude_weight", 0.0),
            )
            if gan_factor > 0.0:
                real_logits, real_features = discriminator(reference)
                fake_logits, fake_features = discriminator(reconstructed)
                adversarial_loss = generator_hinge_loss(fake_logits)
                matching_loss = feature_matching_loss(real_features, fake_features)
                discriminator_loss = discriminator_hinge_loss(real_logits, fake_logits)
            else:
                adversarial_loss = waveform_loss.new_zeros(())
                matching_loss = waveform_loss.new_zeros(())
                discriminator_loss = waveform_loss.new_zeros(())
            totals += torch.stack(
                (
                    waveform_loss,
                    spectral_loss,
                    quantizer_loss,
                    adversarial_loss,
                    matching_loss,
                    discriminator_loss,
                )
            )
            count += 1
            for stage in range(3):
                code_histogram[stage] += torch.bincount(
                    indices[..., stage].reshape(-1), minlength=256
                ).to(code_histogram.dtype)
    if distributed:
        dist.all_reduce(totals, op=dist.ReduceOp.SUM)
        dist.all_reduce(count, op=dist.ReduceOp.SUM)
        dist.all_reduce(code_histogram, op=dist.ReduceOp.SUM)
    if count.item() == 0:
        raise RuntimeError("validation loader yielded no batches")
    probabilities = code_histogram / code_histogram.sum(dim=1, keepdim=True).clamp_min(1)
    perplexity = torch.exp(
        -(probabilities * probabilities.clamp_min(1e-12).log()).sum(dim=1)
    )
    waveform, spectral, commitment, adversarial, matching, discriminator_loss = (
        totals / count
    ).tolist()
    reconstruction = (
        config["loss"]["waveform_l1_weight"] * waveform
        + config["loss"]["spectral_weight"] * spectral
    )
    metrics = {
        "waveform_l1": waveform,
        "spectral": spectral,
        "commitment": commitment,
        "adversarial": adversarial,
        "feature_matching": matching,
        "discriminator": discriminator_loss,
        "adversarial_factor": gan_factor,
        "reconstruction": reconstruction,
        "total": (
            reconstruction
            + commitment
            + gan_factor
            * (
                config["loss"]["adversarial_weight"] * adversarial
                + config["loss"]["feature_matching_weight"] * matching
            )
        ),
    }
    return metrics, {
        "active_codes": [int(value) for value in (code_histogram > 0).sum(dim=1).cpu()],
        "perplexity": [float(value) for value in perplexity.cpu()],
    }


def write_reconstruction_samples(
    model: CourseCodec,
    dataset: WaveformDataset,
    device: torch.device,
    samples_dir: Path,
    count: int,
) -> None:
    """Write fixed validation segments and their reconstructions for listening."""
    samples_dir.mkdir(parents=True, exist_ok=True)
    model.eval()
    with torch.inference_mode():
        for index in range(min(count, len(dataset))):
            reference = dataset[index].unsqueeze(0).to(device)
            indices = model.encode(reference)
            reconstructed = model.decode(indices, reference.size(-1))
            sf.write(
                samples_dir / f"{index:02d}_reference.wav",
                reference[0, 0].cpu().numpy(),
                16_000,
                subtype="PCM_16",
            )
            sf.write(
                samples_dir / f"{index:02d}_reconstructed.wav",
                reconstructed[0, 0].cpu().numpy(),
                16_000,
                subtype="PCM_16",
            )


def validate_and_checkpoint(
    *,
    model: torch.nn.Module,
    base_model: CourseCodec,
    base_discriminator: MultiResolutionSTFTDiscriminator,
    valid_loader: DataLoader,
    valid_set: WaveformDataset,
    device: torch.device,
    config: dict,
    validation_limit: int,
    distributed: bool,
    is_main_process: bool,
    checkpoint_dir: Path,
    epoch: int,
    batch_in_epoch: int,
    global_step: int,
    optimizer: AdamW,
    discriminator_optimizer: AdamW,
    best_validation: float,
    train_loss: float,
    write_snapshot: bool,
) -> float:
    gan_factor = adversarial_factor(global_step, config)
    validation_metrics, validation_usage = evaluate(
        model,
        base_discriminator,
        valid_loader,
        device,
        config,
        validation_limit,
        distributed,
        gan_factor,
    )
    selection_loss = validation_metrics["reconstruction"]
    if is_main_process:
        next_best = min(best_validation, selection_loss)
        state = {
            "epoch": epoch,
            "batch_in_epoch": batch_in_epoch,
            "global_step": global_step,
            "model": base_model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "discriminator": base_discriminator.state_dict(),
            "discriminator_optimizer": discriminator_optimizer.state_dict(),
            "model_config": config["model"],
            "best_validation": next_best,
            "validation_metrics": validation_metrics,
            "quantizer_usage": validation_usage,
            "quantizer_ema_usage": base_model.quantizer.usage_metrics(),
        }
        torch.save(state, checkpoint_dir / "last.pt")
        if write_snapshot:
            torch.save(state, checkpoint_dir / f"step_{global_step:08d}.pt")
            keep = int(config["training"].get("checkpoint_keep_last", 0))
            if keep > 0:
                snapshots = sorted(checkpoint_dir.glob("step_*.pt"))
                for stale in snapshots[:-keep]:
                    stale.unlink()
        if selection_loss < best_validation:
            torch.save(state, checkpoint_dir / "best.pt")
        write_reconstruction_samples(
            base_model,
            valid_set,
            device,
            checkpoint_dir.parent / "samples" / f"step_{global_step:08d}",
            config["training"]["sample_inference_count"],
        )
        log_record = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "epoch": epoch,
            "batch_in_epoch": batch_in_epoch,
            "global_step": global_step,
            "train_loss": train_loss,
            "validation": validation_metrics,
            "quantizer_usage": validation_usage,
            "quantizer_ema_usage": base_model.quantizer.usage_metrics(),
            "best_validation": next_best,
        }
        with (checkpoint_dir.parent / "metrics.jsonl").open(
            "a", encoding="utf-8"
        ) as handle:
            handle.write(json.dumps(log_record, ensure_ascii=False) + "\n")
        print(
            f"epoch={epoch} step={global_step} train_loss={train_loss:.5f} "
            f"val_recon={validation_metrics['reconstruction']:.5f} "
            f"val_wave={validation_metrics['waveform_l1']:.5f} "
            f"val_spec={validation_metrics['spectral']:.5f} "
            f"val_commit={validation_metrics['commitment']:.5f} "
            f"val_adv={validation_metrics['adversarial']:.5f} "
            f"val_fm={validation_metrics['feature_matching']:.5f} "
            f"val_d={validation_metrics['discriminator']:.5f} "
            f"gan_factor={gan_factor:.3f} "
            f"active_codes={validation_usage['active_codes']} "
            f"perplexity={[round(value, 1) for value in validation_usage['perplexity']]}"
        )
    return selection_loss


def main() -> None:
    args = parse_args()
    config = apply_overrides(load_config(args.config), args.config_overrides)
    if args.output_dir:
        config["training"]["output_dir"] = args.output_dir
    if args.run_name:
        config["training"]["output_dir"] = str(
            Path(config["training"]["output_dir"]) / args.run_name
        )
    if config["audio"]["sample_rate"] != 16_000 or config["audio"]["frame_samples"] != 160:
        raise ValueError("the baseline configuration must remain fixed at 16 kHz / 10 ms")
    device, rank, world_size, distributed = distributed_context(args.device)
    is_main_process = rank == 0
    seed = int(config["seed"])
    random.seed(seed + rank)
    np.random.seed(seed + rank)
    torch.manual_seed(seed + rank)

    train_set = make_dataset(args, "train", config)
    valid_set = make_dataset(args, "valid", config)
    train_sampler = (
        DistributedSampler(train_set, num_replicas=world_size, rank=rank, shuffle=True)
        if distributed
        else None
    )
    valid_sampler = (
        DistributedSampler(valid_set, num_replicas=world_size, rank=rank, shuffle=False)
        if distributed
        else None
    )
    num_workers = (
        config["training"]["num_workers"]
        if args.num_workers is None
        else args.num_workers
    )
    loader_options = {
        "batch_size": config["training"]["batch_size"],
        "num_workers": num_workers,
        "pin_memory": device.type == "cuda",
    }
    if num_workers > 0:
        loader_options.update(persistent_workers=True, prefetch_factor=2)
    train_loader = DataLoader(
        train_set,
        sampler=train_sampler,
        shuffle=train_sampler is None,
        drop_last=True,
        **loader_options,
    )
    valid_loader = DataLoader(
        valid_set,
        sampler=valid_sampler,
        shuffle=False,
        drop_last=False,
        **loader_options,
    )

    base_model = CourseCodec(**config["model"]).to(device)
    semantic_teacher = build_semantic_teacher(config, device)
    waveform_teacher = build_waveform_teacher(config, device)
    base_discriminator = MultiResolutionSTFTDiscriminator(
        config["adversarial"]["resolutions"],
        config["adversarial"].get("periods", ()),
    ).to(device)
    resume_state = None
    if args.resume:
        resume_state = torch.load(args.resume, map_location=device, weights_only=False)
        base_model.load_state_dict(resume_state["model"])
        if "discriminator" not in resume_state:
            raise ValueError("resume checkpoint does not contain the GAN discriminator")
        base_discriminator.load_state_dict(resume_state["discriminator"])
    elif args.init_checkpoint:
        initialization_state = torch.load(
            args.init_checkpoint, map_location=device, weights_only=False
        )
        source_model = initialization_state["model"]
        target_model = base_model.state_dict()
        source_quantizer = {
            key: value for key, value in source_model.items() if key.startswith("quantizer.")
        }
        target_quantizer = {
            key: value for key, value in target_model.items() if key.startswith("quantizer.")
        }
        quantizer_changed = (
            source_quantizer.keys() != target_quantizer.keys()
            or any(
                source_quantizer[key].shape != target_quantizer[key].shape
                for key in source_quantizer.keys() & target_quantizer.keys()
            )
        )
        load_compatible_state(
            base_model,
            source_model,
            "codec",
            skip_prefixes=("quantizer.",) if quantizer_changed else (),
        )
        if "discriminator" in initialization_state:
            load_compatible_state(
                base_discriminator,
                initialization_state["discriminator"],
                "discriminator",
            )
    model: torch.nn.Module = base_model
    discriminator: torch.nn.Module = base_discriminator
    if distributed:
        model = DDP(
            base_model,
            device_ids=[device.index] if device.type == "cuda" else None,
            output_device=device.index if device.type == "cuda" else None,
            find_unused_parameters=True,
        )
        discriminator = DDP(
            base_discriminator,
            device_ids=[device.index] if device.type == "cuda" else None,
            output_device=device.index if device.type == "cuda" else None,
        )
    base_learning_rate = float(config["training"]["learning_rate"])
    quantizer_learning_rate = config["training"].get("quantizer_learning_rate")
    if quantizer_learning_rate is None:
        optimizer = AdamW(
            model.parameters(),
            lr=base_learning_rate,
            weight_decay=config["training"]["weight_decay"],
        )
        optimizer.param_groups[0]["group_name"] = "base"
        optimizer.param_groups[0]["lr_scale"] = 1.0
    else:
        quantizer_parameters = list(base_model.quantizer.parameters())
        quantizer_ids = {id(parameter) for parameter in quantizer_parameters}
        base_parameters = [
            parameter for parameter in model.parameters() if id(parameter) not in quantizer_ids
        ]
        optimizer = AdamW(
            [
                {
                    "params": base_parameters,
                    "group_name": "base",
                    "lr_scale": 1.0,
                },
                {
                    "params": quantizer_parameters,
                    "group_name": "quantizer",
                    "lr_scale": float(quantizer_learning_rate) / base_learning_rate,
                },
            ],
            lr=base_learning_rate,
            weight_decay=config["training"]["weight_decay"],
        )
    discriminator_optimizer = AdamW(
        discriminator.parameters(),
        lr=config["adversarial"]["learning_rate"],
        weight_decay=config["training"]["weight_decay"],
    )
    start_epoch = 1
    resume_batch_in_epoch = 0
    global_step = 0
    best_validation = float("inf")
    if resume_state is not None:
        optimizer.load_state_dict(resume_state["optimizer"])
        discriminator_optimizer.load_state_dict(
            resume_state["discriminator_optimizer"]
        )
        start_epoch = int(resume_state["epoch"])
        resume_batch_in_epoch = int(resume_state.get("batch_in_epoch", 0))
        global_step = int(resume_state.get("global_step", 0))
        best_validation = float(resume_state.get("best_validation", best_validation))

    checkpoint_dir = Path(config["training"]["output_dir"]) / "checkpoints"
    if is_main_process:
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        import yaml

        run_dir = checkpoint_dir.parent
        (run_dir / "effective_config.yaml").write_text(
            yaml.safe_dump(config, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        metadata = {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "command": " ".join(shlex.quote(value) for value in sys.argv),
            "torch_version": torch.__version__,
            "world_size": world_size,
            "device": str(device),
            "init_checkpoint": args.init_checkpoint,
            "resume_checkpoint": args.resume,
        }
        (run_dir / "run_metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if distributed:
        dist.barrier()
    epochs = args.epochs or config["training"]["epochs"]
    total_schedule_steps = args.max_total_steps or (epochs * len(train_loader))
    warmup_steps = int(config["training"].get("warmup_steps", 0))
    minimum_learning_rate = float(
        config["training"].get("minimum_learning_rate", config["training"]["learning_rate"])
    )
    validation_limit = (
        config["training"]["validation_limit"]
        if args.max_valid_steps is None
        else args.max_valid_steps
    )
    interval_steps = config["training"]["validation_checkpoint_interval_steps"]
    if interval_steps <= 0:
        raise ValueError("validation_checkpoint_interval_steps must be positive")
    last_validation_step = -1
    reached_max_total_steps = False
    for epoch in range(start_epoch, epochs + 1):
        if train_sampler is not None:
            train_sampler.set_epoch(epoch)
        model.train()
        running: list[float] = []
        progress = tqdm(
            train_loader,
            desc=f"epoch {epoch}/{epochs}",
            unit="batch",
            disable=not is_main_process,
        )
        last_batch_in_epoch = 0
        for step, reference in enumerate(progress):
            if args.max_total_steps is not None and global_step >= args.max_total_steps:
                reached_max_total_steps = True
                break
            if epoch == start_epoch and step < resume_batch_in_epoch:
                continue
            if args.max_train_steps is not None and step >= args.max_train_steps:
                break
            reference = reference.to(device, non_blocking=True)
            if semantic_teacher is None:
                reconstructed, _, quantizer_loss = model(reference)
                semantic_loss = reference.new_zeros(())
            else:
                reconstructed, _, quantizer_loss, auxiliary = model(
                    reference, return_aux=True
                )
                if "semantic" not in auxiliary:
                    raise RuntimeError(
                        "semantic distillation requires an RVQ semantic auxiliary"
                    )
                semantic_target = semantic_teacher_targets(
                    semantic_teacher,
                    reference,
                    auxiliary["semantic"].shape[1],
                )
                semantic_prediction = F.normalize(
                    auxiliary["semantic"].float(), dim=-1
                )
                semantic_loss = (1.0 - (semantic_prediction * semantic_target).sum(dim=-1)).mean()
            waveform_loss = F.l1_loss(reconstructed, reference)
            spectral_loss = multiscale_spectral_loss(
                reconstructed,
                reference,
                config["loss"]["fft_sizes"],
                config["loss"].get("spectral_convergence_weight", 0.0),
                config["loss"].get("linear_magnitude_weight", 0.0),
            )
            reconstruction_loss = (
                config["loss"]["waveform_l1_weight"] * waveform_loss
                + config["loss"]["spectral_weight"] * spectral_loss
            )
            if waveform_teacher is not None:
                teacher, distillation = waveform_teacher
                teacher_factor = distillation_factor(global_step + 1, distillation)
                if teacher_factor:
                    with torch.inference_mode():
                        teacher_reconstruction = teacher(reference)[0]
                    reconstruction_loss = reconstruction_loss + teacher_factor * float(
                        distillation.get("waveform_l1_weight", 0.0)
                    ) * F.l1_loss(reconstructed, teacher_reconstruction)
                    distillation_spectral_weight = float(
                        distillation.get("spectral_weight", 0.0)
                    )
                    if distillation_spectral_weight:
                        reconstruction_loss = reconstruction_loss + (
                            teacher_factor
                            * distillation_spectral_weight
                            * multiscale_spectral_loss(
                                reconstructed,
                                teacher_reconstruction,
                                config["loss"]["fft_sizes"],
                                config["loss"].get(
                                    "spectral_convergence_weight", 0.0
                                ),
                                config["loss"].get("linear_magnitude_weight", 0.0),
                            )
                        )
            si_snr_weight = float(config["loss"].get("si_snr_weight", 0.0))
            if si_snr_weight:
                reconstruction_loss = reconstruction_loss + (
                    si_snr_weight * negative_si_snr_loss(reconstructed, reference)
                )
            gan_factor = adversarial_factor(global_step + 1, config)
            discriminator_loss = reconstructed.new_zeros(())
            adversarial_loss = reconstructed.new_zeros(())
            matching_loss = reconstructed.new_zeros(())
            if gan_factor > 0.0:
                discriminator.train()
                discriminator_optimizer.zero_grad(set_to_none=True)
                discriminator_input = torch.cat(
                    (reference, reconstructed.detach()), dim=0
                )
                combined_logits, _ = discriminator(discriminator_input)
                batch_size = reference.size(0)
                real_logits = [logits[:batch_size] for logits in combined_logits]
                fake_logits = [logits[batch_size:] for logits in combined_logits]
                discriminator_loss = discriminator_hinge_loss(real_logits, fake_logits)
                discriminator_loss.backward()
                torch.nn.utils.clip_grad_norm_(
                    discriminator.parameters(),
                    config["adversarial"]["gradient_clip_norm"],
                )
                discriminator_optimizer.step()

                for parameter in base_discriminator.parameters():
                    parameter.requires_grad_(False)
                with torch.no_grad():
                    _, real_features = base_discriminator(reference)
                fake_logits, fake_features = base_discriminator(reconstructed)
                adversarial_loss = generator_hinge_loss(fake_logits)
                matching_loss = feature_matching_loss(real_features, fake_features)
                for parameter in base_discriminator.parameters():
                    parameter.requires_grad_(True)

            loss = (
                reconstruction_loss
                + quantizer_loss
                + gan_factor
                * (
                    config["loss"]["adversarial_weight"] * adversarial_loss
                    + config["loss"]["feature_matching_weight"] * matching_loss
                )
            )
            if semantic_teacher is not None:
                semantic_config = config["semantic_distillation"]
                semantic_warmup = int(semantic_config.get("warmup_steps", 0))
                semantic_factor = (
                    1.0
                    if semantic_warmup <= 0
                    else min(1.0, (global_step + 1) / semantic_warmup)
                )
                loss = loss + (
                    float(semantic_config.get("weight", 0.1))
                    * semantic_factor
                    * semantic_loss
                )
            current_learning_rate = scheduled_learning_rate(
                base_learning_rate,
                minimum_learning_rate,
                warmup_steps,
                global_step + 1,
                total_schedule_steps,
            )
            quantizer_only_steps = int(
                config["training"].get("quantizer_only_steps", 0)
            )
            for parameter_group in optimizer.param_groups:
                if (
                    parameter_group.get("group_name") == "base"
                    and global_step + 1 <= quantizer_only_steps
                ):
                    parameter_group["lr"] = 0.0
                else:
                    parameter_group["lr"] = (
                        current_learning_rate
                        * float(parameter_group.get("lr_scale", 1.0))
                    )
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                model.parameters(), config["training"]["gradient_clip_norm"]
            )
            optimizer.step()
            global_step += 1
            last_batch_in_epoch = step + 1
            running.append(loss.item())
            if is_main_process:
                progress.set_postfix(
                    loss=f"{np.mean(running[-20:]):.4f}",
                    sem=f"{semantic_loss.item():.3f}",
                )
            if global_step % interval_steps == 0:
                validation = validate_and_checkpoint(
                    model=model,
                    base_model=base_model,
                    base_discriminator=base_discriminator,
                    valid_loader=valid_loader,
                    valid_set=valid_set,
                    device=device,
                    config=config,
                    validation_limit=validation_limit,
                    distributed=distributed,
                    is_main_process=is_main_process,
                    checkpoint_dir=checkpoint_dir,
                    epoch=epoch,
                    batch_in_epoch=last_batch_in_epoch,
                    global_step=global_step,
                    optimizer=optimizer,
                    discriminator_optimizer=discriminator_optimizer,
                    best_validation=best_validation,
                    train_loss=float(np.mean(running)),
                    write_snapshot=True,
                )
                best_validation = min(best_validation, validation)
                last_validation_step = global_step
                model.train()
                if distributed:
                    dist.barrier()
            if args.max_total_steps is not None and global_step >= args.max_total_steps:
                reached_max_total_steps = True
                break
        resume_batch_in_epoch = 0
        # Always validate and preserve the final state, including a bounded
        # ablation that ends between checkpoint intervals.
        if (epoch == epochs or reached_max_total_steps) and global_step != last_validation_step:
            validation = validate_and_checkpoint(
                model=model,
                base_model=base_model,
                base_discriminator=base_discriminator,
                valid_loader=valid_loader,
                valid_set=valid_set,
                device=device,
                config=config,
                validation_limit=validation_limit,
                distributed=distributed,
                is_main_process=is_main_process,
                checkpoint_dir=checkpoint_dir,
                epoch=epoch,
                batch_in_epoch=last_batch_in_epoch,
                global_step=global_step,
                optimizer=optimizer,
                discriminator_optimizer=discriminator_optimizer,
                best_validation=best_validation,
                train_loss=float(np.mean(running)),
                write_snapshot=False,
            )
            best_validation = min(best_validation, validation)
            if distributed:
                dist.barrier()
        if reached_max_total_steps:
            break
    if distributed:
        dist.destroy_process_group()


if __name__ == "__main__":
    main()
