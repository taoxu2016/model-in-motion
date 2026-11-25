"""A listen-through of an episode's narration, before any animation exists.

Joins the voiceover clips in script order, with the series' pause between clips and a longer one between scenes,
and writes build/listen/<name>_draft_narration.m4a (and .wav) plus a script with a timestamp on every clip.

usage: python tools/listen_through.py EPISODE_FOLDER [--gap 0.35] [--scene-gap 1.2]
"""
import argparse, json, subprocess, sys
from pathlib import Path

import numpy as np
import soundfile as sf

if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
    sys.exit("usage: python tools/listen_through.py EPISODE_FOLDER [--gap 0.35] [--scene-gap 1.2]")
ROOT = Path(sys.argv.pop(1)).resolve()


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gap", type=float, default=0.35)
    ap.add_argument("--scene-gap", type=float, default=1.2)
    a = ap.parse_args()
    spec = json.loads((ROOT / "narration" / "narration.json").read_text())
    man = json.loads((ROOT / "audio" / "manifest.json").read_text())
    out = ROOT / "build" / "listen"; out.mkdir(parents=True, exist_ok=True)
    chunks, t, sr, md = [], 0.0, None, [f"# {spec['title']}: draft narration", ""]
    for sc in spec["scenes"]:
        md += [f"## {sc['id']}" + (f" · {sc['chapter']}" if sc.get("chapter") else ""), ""]
        for g in sc["segments"]:
            wav, r = sf.read(ROOT / man[g["id"]]["file"], dtype="float32")
            sr = sr or r
            assert r == sr, "clips differ in sample rate"
            md.append(f"`{mmss(t)}` **{g['id']}** {' '.join(s['text'] for s in g['sentences'])}")
            md.append("")
            chunks += [wav, np.zeros(int(a.gap * sr), dtype="float32")]
            t += len(wav) / sr + a.gap
        chunks.append(np.zeros(int(a.scene_gap * sr), dtype="float32")); t += a.scene_gap
    wav_path = out / f"{spec['name']}_draft_narration.wav"
    sf.write(wav_path, np.concatenate(chunks), sr)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-c:a", "aac", "-b:a", "160k", str(wav_path.with_suffix(".m4a"))], check=True)
    speech = sum(v["duration"] for v in man.values())
    md[1:1] = ["", f"*{mmss(t)} with pauses; {mmss(speech)} of speech; {sum(len(s['text'].split()) for sc in spec['scenes'] for g in sc['segments'] for s in g['sentences'])} words.*"]
    (out / f"{spec['name']}_draft_script.md").write_text("\n".join(md), encoding="utf-8")
    print(f"listen-through: {mmss(t)} with pauses, {mmss(speech)} of speech -> {wav_path.with_suffix('.m4a')}")


if __name__ == "__main__":
    main()
