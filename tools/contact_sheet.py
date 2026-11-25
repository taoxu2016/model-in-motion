"""Tile frames from a video into one review image.  usage: contact_sheet.py VIDEO OUT.png t1 t2 ... [--cols 3 --w 640]"""
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw


def main():
    args = sys.argv[1:]
    cols, w = 3, 640
    if "--cols" in args:
        i = args.index("--cols"); cols = int(args[i + 1]); del args[i:i + 2]
    if "--w" in args:
        i = args.index("--w"); w = int(args[i + 1]); del args[i:i + 2]
    video, out, times = args[0], args[1], [float(t) for t in args[2:]]
    tiles = []
    with tempfile.TemporaryDirectory() as d:
        for k, t in enumerate(times):
            f = Path(d) / f"{k}.png"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                            "-vf", f"scale={w}:-1", str(f)], check=True)
            im = Image.open(f).convert("RGB")
            dr = ImageDraw.Draw(im)
            dr.rectangle([0, 0, 92, 22], fill=(0, 0, 0))
            dr.text((5, 4), f"t={t:6.2f}s", fill=(255, 255, 0))
            tiles.append(im)
    h = tiles[0].height
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols - 1) * 6, rows * h + (rows - 1) * 6), (60, 60, 60))
    for k, im in enumerate(tiles):
        sheet.paste(im, ((k % cols) * (w + 6), (k // cols) * (h + 6)))
    sheet.save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
