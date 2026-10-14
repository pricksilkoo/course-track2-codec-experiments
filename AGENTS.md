# Project Working Agreement

## Repository scope

- This repository, `course-track2-codec-experiments`, is the working repository for all subsequent codec development, experiments, documentation, and Git commits in this project.
- Treat the sibling repository `course-track2-codec-baseline` as a read-only reference. Do not edit, commit, clean, reset, or otherwise mutate it unless the user explicitly requests that exact action.
- Keep experimental changes reproducible through configuration files under `configs/`; avoid hard-coding one-off experiment settings in training code.

## Execution environment

- Training, full evaluation, profiling, and competition runs are performed on the remote server, not on this local machine.
- Use the local machine for code editing, static checks, lightweight smoke tests, and Git operations only.
- Do not install heavyweight local dependencies or adapt the project around local hardware limitations. Write portable commands and document remote-server requirements instead.
- Do not treat local wall-clock timing as competition evidence. Use the analytical complexity report and final measurements from the remote submission environment.
- Run every long-lived remote operation (dataset downloads, environment setup, training, evaluation, and large preprocessing jobs) inside a named `tmux` session or an equivalently persistent supervisor. SSH disconnection must not terminate the job.
- Prefer resumable downloads and checkpoint-aware training. Before starting a new process, check for an existing session, partial archive, completion marker, or `last.pt` checkpoint instead of duplicating work.

## Fixed competition interface

- Audio is mono at 16 kHz.
- One codec frame covers 160 samples, i.e. 10 ms.
- Each frame must produce exactly 24 transmitted bits (3 bytes), yielding 2.4 kbps.
- Total inference complexity must not exceed 700 MFLOP/s.
- Decoder-side complexity must not exceed 300 MFLOP/s.
- Total algorithmic delay must not exceed 30 ms.
- The decoder may use only the submitted bitstream, side metadata allowed by the task, model weights, and submitted code. Never introduce hidden encoder-to-decoder information.

## Experiment discipline

- Preserve `configs/baseline_16k_2p4k.yaml` and compatibility with the retained baseline checkpoint as the regression reference.
- Prefer single-variable ablations before combining changes. Record the effective configuration, seed, data manifests, training steps, checkpoint-selection rule, quality metrics, bitrate, complexity, and delay.
- Before considering a model configuration viable, run `scripts/complexity.py` and check both complexity limits.
- Keep datasets, generated bitstreams, reconstructed audio, and ordinary training runs out of Git. The retained baseline checkpoint is the intentional exception already tracked by the repository.
- Do not silently change the external 3-byte-per-frame format. If an experiment changes internal quantization, its encode/decode round trip must still satisfy the fixed bitstream contract.
- Maintain `EXPERIMENT_LOG.md` for every substantial training run. Record status, Git commit, effective configuration, dataset summary, training validation, final objective metrics, complexity, checkpoint path and checkpoint hash.

## Validation expectations

- Run syntax/static checks after code changes.
- Run the relevant unit or smoke tests when dependencies are available.
- For model changes, verify output shape, exact byte range and frame count, encode/decode round trip, causal behavior where claimed, old-checkpoint compatibility where applicable, and analytical complexity.
- Clearly distinguish checks performed locally from training and final evaluation that still need to run on the remote server.

## Primary references

- `README.md`: experiment workflow and preset overview.
- `大作业 track 2.md`: competition requirements.
- `COURSE_GUIDE.md`: data preparation, training, and evaluation workflow.
- `BASELINE_RESULTS.md`: retained baseline measurements.
