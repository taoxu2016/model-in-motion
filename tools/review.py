"""Review sheets: tile frames taken near the end of every narration segment (and at extra offsets).
usage: review.py EPISODE_FOLDER OUT.png QUALITY SCENE[:extra_t,extra_t...] ...     e.g. review.py /tmp/a.png 480p15 S01_ColdOpen S02_Title:3.0
"""
import json, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw

if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
    sys.exit("usage: python tools/review.py EPISODE_FOLDER OUT.png QUALITY SCENE[:t,t...] ...")
ROOT = Path(sys.argv.pop(1)).resolve()                       # the episode folder
STEM = next((ROOT / "episode").glob("episode*.py")).stem     # Manim names its video folder after the episode file


def main():
    out, quality, specs = sys.argv[1], sys.argv[2], sys.argv[3:]
    w, cols, shots = 640, 3, []
    for spec in specs:
        scene, _, extra = spec.partition(":")
        log = json.loads((ROOT / "build" / "timings" / f"{scene}.json").read_text())
        segs = log["segments"]
        for k, g in enumerate(segs):
            nxt = segs[k + 1]["start"] if k + 1 < len(segs) else log["duration"] - 1.2
            shots.append((scene, max(g["start"] + 0.2, nxt - 0.25), g["id"]))
        shots += [(scene, float(t), "extra") for t in extra.split(",") if t]
    shots.sort(key=lambda s: (specs.index(next(x for x in specs if x.startswith(s[0]))), s[1]))
    tiles = []
    with tempfile.TemporaryDirectory() as d:
        for k, (scene, t, label) in enumerate(shots):
            video = ROOT / "build" / "media" / "videos" / STEM / quality / f"{scene}.mp4"
            f = Path(d) / f"{k}.png"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
                            "-vf", f"scale={w}:-1", str(f)], check=True)
            im = Image.open(f).convert("RGB")
            dr = ImageDraw.Draw(im)
            tag = f"{scene[:3]} {label} t={t:.1f}"
            dr.rectangle([0, 0, 8 + 6.2 * len(tag), 16], fill=(0, 0, 0))
            dr.text((4, 2), tag, fill=(255, 255, 0))
            tiles.append(im)
    h = tiles[0].height
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols - 1) * 6, rows * h + (rows - 1) * 6), (60, 60, 60))
    for k, im in enumerate(tiles):
        sheet.paste(im, ((k % cols) * (w + 6), (k // cols) * (h + 6)))
    sheet.save(out)
    print(out, sheet.size, len(tiles), "tiles")


if __name__ == "__main__":
    main()
