#!/bin/bash
# Build one episode end to end: voiceover, every scene, assembly.
# usage: tools/build.sh EPISODE_FOLDER [preview|final]        preview = 480p15, final = 1080p60
set -e
EP=$(cd "$1" && pwd); MODE=${2:-preview}; REPO=$(cd "$(dirname "$0")/.." && pwd)
STEM=$(basename "$EP"/episode/episode*.py .py)
if [ "$MODE" = final ]; then Q=-qh; QN=1080p60; else Q=-ql; QN=480p15; fi
python3 "$REPO/tools/make_voiceover.py" "$EP"
cd "$EP"
for S in $(python3 -c "import json; print(' '.join(s['id'] for s in json.load(open('narration/narration.json'))['scenes']))"); do
  manim $Q --disable_caching --media_dir build/media "episode/$STEM.py" "$S"
done
python3 "$REPO/tools/assemble.py" "$EP" --quality $QN
