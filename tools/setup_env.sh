#!/usr/bin/env bash
# Install, or check, everything this repository needs to build episodes, on Ubuntu or Debian.
#
#   tools/setup_env.sh                 install whatever is missing; safe to re-run
#   tools/setup_env.sh --check         report what is missing, and exit 1 if anything is
#   tools/setup_env.sh --only STEP     one step: apt | python | fonts | voice   (add --force to redo fonts or voice)
#
# Python packages go into the active virtualenv if there is one, otherwise into the system Python, as in the dev
# container and cloud environments this is written for. The voice files go to $KOKORO_MODELS (default ~/tts_models),
# where tools/make_voiceover.py looks. Fonts go to $MIM_FONT_DIR (default /usr/local/share/fonts/mim, or
# ~/.local/share/fonts/mim without root or sudo).
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODELS="${KOKORO_MODELS:-$HOME/tts_models}"
KOKORO_URL="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"
INTER_URL="https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip"
LORA_URL="https://github.com/google/fonts/raw/main/ofl/lora"
APT_PACKAGES="python3 python3-dev python3-pip python3-venv build-essential pkg-config libcairo2-dev libpango1.0-dev
  ffmpeg texlive texlive-latex-extra preview-latex-style dvisvgm fontconfig curl unzip git"
declare -A VOICE_BYTES=([kokoro-v1.0.onnx]=325532387 [voices-v1.0.bin]=28214398)

if [ "$(id -u)" = 0 ]; then SUDO=""; elif command -v sudo >/dev/null 2>&1; then SUDO="sudo -H"; else SUDO=""; fi
MODE=install; ONLY=""; FORCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --check) MODE=check ;;
    --only) ONLY="${2:-}"; shift ;;
    --force) FORCE=1 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

has_font() { fc-list : family 2>/dev/null | tr ',' '\n' | grep -x "$1" > /dev/null; }   # no grep -q: with pipefail it can fail on SIGPIPE
missing=0
ok()   { echo "ok       $1"; }
miss() { echo "MISSING  $1"; missing=$((missing + 1)); }

check() {
  missing=0
  if command -v python3 >/dev/null 2>&1; then
    ok "python3 $(python3 -c 'import platform; print(platform.python_version())')"
    python3 - << 'PY' || missing=$((missing + 1))
import importlib, sys
need = ["manim", "kokoro_onnx", "soundfile", "numpy", "scipy", "pandas", "PIL", "matplotlib", "statsmodels", "sklearn", "pprof_py"]
bad = []
for m in need:
    try:
        importlib.import_module(m)
    except Exception:
        bad.append(m)
print(f"MISSING  python packages: {', '.join(bad)} (pip install -r requirements.txt)" if bad else "ok       python packages")
sys.exit(1 if bad else 0)
PY
  else
    miss "python3"
  fi
  command -v ffmpeg >/dev/null 2>&1 && { ffmpeg -hide_banner -filters 2>/dev/null | grep " ass " > /dev/null && ok "ffmpeg with libass" || miss "ffmpeg built with libass"; } || miss "ffmpeg"
  command -v latex >/dev/null 2>&1 && ok "latex" || miss "latex (texlive)"
  command -v dvisvgm >/dev/null 2>&1 && ok "dvisvgm" || miss "dvisvgm"
  for f in standalone.cls preview.sty amsmath.sty; do
    [ -n "$(kpsewhich "$f" 2>/dev/null)" ] && ok "LaTeX $f" || miss "LaTeX $f"
  done
  for f in "Inter" "Inter Display" "Lora"; do has_font "$f" && ok "font $f" || miss "font $f"; done
  for f in kokoro-v1.0.onnx voices-v1.0.bin; do
    [ "$(stat -c %s "$MODELS/$f" 2>/dev/null || echo 0)" = "${VOICE_BYTES[$f]}" ] && ok "voice file $MODELS/$f" || miss "voice file $MODELS/$f"
  done
  return $(( missing > 0 ))
}

step_apt() {
  command -v apt-get >/dev/null 2>&1 || { echo "apt-get not found: install the system packages by hand (docs/HANDOFF.md)"; return 1; }
  echo "== system packages"
  $SUDO apt-get update -qq && $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y -qq $APT_PACKAGES
}

step_python() {
  echo "== Python packages (requirements.txt)"
  if [ -n "${VIRTUAL_ENV:-}" ]; then
    python3 -m pip install -q -r "$REPO/requirements.txt"
  else
    $SUDO env PIP_BREAK_SYSTEM_PACKAGES=1 PIP_ROOT_USER_ACTION=ignore python3 -m pip install -q -r "$REPO/requirements.txt"
  fi
}

step_fonts() {
  local dir="${MIM_FONT_DIR:-}" fs tmp
  if [ -z "$dir" ]; then
    if [ "$(id -u)" = 0 ] || [ -n "$SUDO" ]; then dir=/usr/local/share/fonts/mim; else dir="$HOME/.local/share/fonts/mim"; fi
  fi
  case "$dir" in "$HOME"/*|/tmp/*) fs="" ;; *) fs="$SUDO" ;; esac
  tmp=$(mktemp -d)
  echo "== fonts -> $dir"
  if [ "$FORCE" = 1 ] || ! has_font "Inter" || ! has_font "Inter Display"; then
    curl -fsSL --retry 3 -o "$tmp/inter.zip" "$INTER_URL" && unzip -q -j "$tmp/inter.zip" 'extras/ttf/*.ttf' -d "$tmp/inter" \
      && $fs mkdir -p "$dir" && $fs cp "$tmp"/inter/*.ttf "$dir"/ || echo "font download failed: Inter"
  fi
  if [ "$FORCE" = 1 ] || ! has_font "Lora"; then
    curl -fsSL --retry 3 -o "$tmp/Lora-Variable.ttf" "$LORA_URL/Lora%5Bwght%5D.ttf" \
      && curl -fsSL --retry 3 -o "$tmp/Lora-Italic-Variable.ttf" "$LORA_URL/Lora-Italic%5Bwght%5D.ttf" \
      && $fs mkdir -p "$dir" && $fs cp "$tmp"/Lora-*.ttf "$dir"/ || echo "font download failed: Lora"
  fi
  $fs fc-cache -f >/dev/null 2>&1 || true
  rm -rf "$tmp"
}

step_voice() {
  echo "== Kokoro voice files -> $MODELS"
  mkdir -p "$MODELS"
  for f in kokoro-v1.0.onnx voices-v1.0.bin; do
    if [ "$FORCE" = 0 ] && [ "$(stat -c %s "$MODELS/$f" 2>/dev/null || echo 0)" = "${VOICE_BYTES[$f]}" ]; then continue; fi
    curl -fL --retry 3 -s -o "$MODELS/$f.part" "$KOKORO_URL/$f" && mv "$MODELS/$f.part" "$MODELS/$f" || echo "voice download failed: $f"
  done
}

if [ "$MODE" = check ]; then check; exit $?; fi
want() { [ -z "$ONLY" ] || [ "$ONLY" = "$1" ]; }
want apt && step_apt
want python && step_python
want fonts && step_fonts
want voice && step_voice
echo "== check"
check
