#!/usr/bin/env bash
set -Eeuo pipefail

# Download the exact corpora expected by prepare_vctk_libritts.py. Archives are
# verified and removed only after successful extraction to limit peak storage.

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
DATA_ROOT="${1:-$REPO_ROOT/data/corpora}"
DOWNLOAD_DIR="$DATA_ROOT/.downloads"
MANIFEST_DIR="$REPO_ROOT/data/manifests/vctk_libritts"

mkdir -p "$DATA_ROOT" "$DOWNLOAD_DIR" "$MANIFEST_DIR"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

free_gib() {
  df -BG --output=avail "$DATA_ROOT" | awk 'NR == 2 {gsub(/G/, "", $1); print $1}'
}

require_free_gib() {
  local required="$1"
  local phase="$2"
  local available
  available="$(free_gib)"
  if (( available < required )); then
    log "Stopping safely before $phase: ${available} GiB free, ${required} GiB required"
    return 70
  fi
}

download_archive() {
  local url="$1"
  local archive="$2"
  local checksum_kind="$3"
  local checksum="$4"

  if [[ -f "$archive" && ! -f "$archive.aria2" ]]; then
    log "Reusing completed archive $(basename "$archive")"
  else
    log "Downloading $(basename "$archive") (free space: $(free_gib) GiB)"
    wget \
      --continue \
      --retry-connrefused \
      --read-timeout=30 \
      --timeout=30 \
      --tries=0 \
      --progress=dot:giga \
      --output-document="$archive" \
      "$url"
  fi

  log "Verifying $(basename "$archive")"
  if [[ "$checksum_kind" == "md5" ]]; then
    printf '%s  %s\n' "$checksum" "$archive" | md5sum --check --status
  elif [[ "$checksum_kind" == "sha256" ]]; then
    printf '%s  %s\n' "$checksum" "$archive" | sha256sum --check --status
  else
    log "Unsupported checksum kind: $checksum_kind"
    return 2
  fi
}

extract_libritts_split() {
  local split="$1"
  local checksum="$2"
  local required_before_download="$3"
  local required_before_extract="$4"
  local target="$DATA_ROOT/LibriTTS/$split"
  local archive="$DOWNLOAD_DIR/$split.tar.gz"
  local url="https://openslr.magicdatatech.com/resources/60/$split.tar.gz"

  if find "$target" -type f -name '*.wav' -print -quit 2>/dev/null | grep -q .; then
    log "Skipping LibriTTS/$split; WAV files already exist"
    return
  fi

  require_free_gib "$required_before_download" "downloading LibriTTS/$split"
  download_archive "$url" "$archive" md5 "$checksum"
  require_free_gib "$required_before_extract" "extracting LibriTTS/$split"
  log "Extracting LibriTTS/$split (free space: $(free_gib) GiB)"
  tar -xzf "$archive" -C "$DATA_ROOT"
  if ! find "$target" -type f -name '*.wav' -print -quit | grep -q .; then
    log "Extraction produced no WAV files in $target"
    return 1
  fi
  rm -f -- "$archive" "$archive.aria2"
  log "Finished LibriTTS/$split"
}

extract_vctk() {
  local target="$DATA_ROOT/VCTK-Corpus-0.92"
  local audio_root="$target/wav48_silence_trimmed"
  local archive="$DOWNLOAD_DIR/VCTK-Corpus-0.92.zip"
  local url="https://datashare.ed.ac.uk/bitstreams/535f4286-e54c-4038-838c-a02285e32cb2/download"
  local checksum="f96258be9fdc2cbff6559541aae7ea4f59df3fcaf5cf963aae5ca647357e359c"

  if find "$audio_root" -type f -name '*_mic1.flac' -print -quit 2>/dev/null | grep -q .; then
    log "Skipping VCTK; mic1 FLAC files already exist"
    return
  fi

  require_free_gib 40 "downloading VCTK"
  download_archive "$url" "$archive" sha256 "$checksum"
  require_free_gib 25 "extracting VCTK"
  mkdir -p "$target"
  log "Extracting only VCTK mic1 trimmed audio (free space: $(free_gib) GiB)"
  unzip -q "$archive" 'wav48_silence_trimmed/*/*_mic1.flac' -d "$target"
  if ! find "$audio_root" -type f -name '*_mic1.flac' -print -quit | grep -q .; then
    log "Extraction produced no mic1 FLAC files in $audio_root"
    return 1
  fi
  rm -f -- "$archive" "$archive.aria2"
  log "Finished VCTK"
}

log "Dataset root: $DATA_ROOT"
log "Initial free space: $(free_gib) GiB"

extract_vctk
extract_libritts_split dev-clean 0c3076c1e5245bb3f0af7d82087ee207 20 12
extract_libritts_split dev-other 815555d8d75995782ac3ccd7f047213d 20 12
extract_libritts_split train-clean-100 4a8c202b78fe1bc0c47916a98f3a2ea8 45 32
extract_libritts_split train-clean-360 a84ef10ddade5fd25df69596a2767b2d 110 80
extract_libritts_split train-other-500 7b181dd5ace343a5f38427999684aa6f 150 105

log "Generating manifests"
python3 "$REPO_ROOT/scripts/prepare_vctk_libritts.py" \
  --vctk-root "$DATA_ROOT/VCTK-Corpus-0.92" \
  --libritts-root "$DATA_ROOT/LibriTTS" \
  --output-dir "$MANIFEST_DIR"

log "Dataset preparation complete (free space: $(free_gib) GiB)"
