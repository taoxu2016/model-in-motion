"""Assemble the episode from the rendered scenes.

  1. timeline   scene offsets from the rendered files; clip start times from build/timings/<Scene>.json
  2. audio      every narration clip placed at its logged start; loudness-normalized master (48 kHz)
  3. captions   cues from exact sentence offsets -> .srt, .vtt and a styled .ass (series caption style)
  4. script     the narration script with timestamps (markdown)
  5. video      picture = lossless concat of the scenes; soft-subtitle MP4 (no re-encode);
                burned-in MP4 (one re-encode)

usage: python tools/assemble.py [--quality 1080p60] [--stage prep|burn|all]
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

import numpy as np
import soundfile as sf

if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
    sys.exit("usage: python tools/assemble.py EPISODE_FOLDER [--quality 1080p60] [--stage prep|burn|all]")
ROOT = Path(sys.argv.pop(1)).resolve()                       # the episode folder
STEM = next((ROOT / "episode").glob("episode*.py")).stem     # Manim names its video folder after the episode file
SPEC = json.loads((ROOT / "narration" / "narration.json").read_text())
MANIFEST = json.loads((ROOT / "audio" / "manifest.json").read_text())
NAME = SPEC["name"]
SCENES = [s["id"] for s in SPEC["scenes"]]
SR = 24_000
TITLE = f'{SPEC["series"]} \u00b7 {SPEC["arc"]} \u00b7 Episode {SPEC["episode"]}: {SPEC["title"]}'


def run(cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def probe(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(path)]).decode())


def ts(t, sep=","):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def ts_ass(t):
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360_000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def wrap(text, width=46):
    """One line, or two balanced lines."""
    if len(text) <= width:
        return [text]
    words, best = text.split(), None
    for k in range(1, len(words)):
        a, b = " ".join(words[:k]), " ".join(words[k:])
        score = abs(len(a) - len(b)) + 100 * (len(a) > width) + 100 * (len(b) > width)
        if best is None or score < best[0]:
            best = (score, [a, b])
    return best[1]


def chunks(text, limit=88):
    """Split a sentence into caption-sized pieces, at punctuation where possible."""
    if len(text) <= limit:
        return [text]
    best = None
    for m in re.finditer(r"(?<=[.?!:;,]) ", text):
        k = m.start()
        score = abs(k - len(text) / 2) + (0 if text[k - 1] in ".?!:" else 8)
        if best is None or score < best[0]:
            best = (score, k)
    k = best[1] if best else text.rfind(" ", 0, len(text) // 2 + 12)
    return chunks(text[:k].strip(), limit) + chunks(text[k:].strip(), limit)


def build_cues(timeline):
    cues = []
    for g in timeline:
        for sen in g["sentences"]:
            parts = chunks(sen["text"])
            total = sum(len(p) for p in parts)
            t, span = g["t"] + sen["start"], sen["end"] - sen["start"]
            for p in parts:
                d = span * len(p) / total
                cues.append({"start": t, "end": t + d, "text": p})
                t += d
    for a, b in zip(cues, cues[1:]):
        a["end"] = min(a["end"] + 0.35, b["start"] - 0.04)
    cues[-1]["end"] += 0.35
    return cues


def write_subs(cues, out):
    srt, vtt = [], ["WEBVTT", ""]
    for k, c in enumerate(cues, 1):
        lines = wrap(c["text"])
        srt += [str(k), f'{ts(c["start"])} --> {ts(c["end"])}', *lines, ""]
        vtt += [f'{ts(c["start"], ".")} --> {ts(c["end"], ".")}', *lines, ""]
    (out / f"{NAME}.en.srt").write_text("\n".join(srt), encoding="utf-8")
    (out / f"{NAME}.en.vtt").write_text("\n".join(vtt), encoding="utf-8")
    # ASS for burn-in: Inter, warm off-white text on a translucent ink box (the series caption style)
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 2",
           "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
           "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
           "MarginR, MarginV, Encoding",
           "Style: Caption,Inter,40,&H00E4EEF3,&H000000FF,&H2A100B07,&H00000000,0,0,0,0,100,100,0.3,0,3,9,0,2,200,200,26,1",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for c in cues:
        ass.append(f'Dialogue: 0,{ts_ass(c["start"])},{ts_ass(c["end"])},Caption,,0,0,0,,' + "\\N".join(wrap(c["text"])))
    (out / f"{NAME}.en.ass").write_text("\n".join(ass) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality", default="1080p60")
    ap.add_argument("--stage", default="all", choices=["prep", "burn", "all"])
    a = ap.parse_args()
    vids = ROOT / "build" / "media" / "videos" / STEM / a.quality
    out = ROOT / "build" / "final"
    out.mkdir(parents=True, exist_ok=True)
    master = out / f"{NAME}_narration.wav"

    if a.stage in ("prep", "all"):
        # 1. timeline
        timeline, scene_rows, offset = [], [], 0.0
        for s in SCENES:
            log = json.loads((ROOT / "build" / "timings" / f"{s}.json").read_text())
            dur = probe(vids / f"{s}.mp4")
            if abs(dur - log["duration"]) > 0.05:
                print(f"  note: {s} file {dur:.3f}s vs logged {log['duration']:.3f}s")
            for g in log["segments"]:
                timeline.append({"scene": s, "id": g["id"], "t": offset + g["start"], "dur": g["duration"],
                                 "sentences": MANIFEST[g["id"]]["sentences"]})
            scene_rows.append((s, offset, dur))
            offset += dur
        total = offset
        gaps = [b["t"] - (a_["t"] + a_["dur"]) for a_, b in zip(timeline, timeline[1:])]
        print(f"timeline: {len(SCENES)} scenes, {len(timeline)} clips, {total:.2f}s; smallest gap between clips {min(gaps):.2f}s")
        assert min(gaps) > -0.01, "narration clips overlap"

        # 2. master audio
        buf = np.zeros(int(total * SR) + SR, dtype=np.float32)
        for g in timeline:
            wav, sr = sf.read(ROOT / MANIFEST[g["id"]]["file"], dtype="float32")
            assert sr == SR
            i0 = int(round(g["t"] * SR))
            buf[i0:i0 + len(wav)] += wav
        raw = out / "narration_raw.wav"
        sf.write(raw, buf[:int(total * SR)], SR, subtype="PCM_16")
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", master])

        # 3. captions
        cues = build_cues(timeline)
        write_subs(cues, out)
        longest = max(len(line) for c in cues for line in wrap(c["text"]))
        print(f"captions: {len(cues)} cues, longest line {longest} characters, "
              f"longest cue {max(c['end'] - c['start'] for c in cues):.1f}s")

        # 4. timestamped script
        visual = {g["id"]: g["visual"] for sc in SPEC["scenes"] for g in sc["segments"]}
        chapter = {sc["id"]: sc["chapter"] for sc in SPEC["scenes"]}
        words = sum(len(s["text"].split()) for g in timeline for s in g["sentences"])
        md = [f"# {TITLE}", "", f"*{SPEC['subtitle']}*", "",
              f"Narration script with timestamps. {words} words, running time {ts(total, '.')[3:8]}. "
              f"Voice: {SPEC['voice']['engine']}, `{SPEC['voice']['name']}`, speed {SPEC['voice']['speed']}.", ""]
        last = None
        for g in timeline:
            if g["scene"] != last:
                start = next(o for s, o, _ in scene_rows if s == g["scene"])
                head = g["scene"] + (f" \u00b7 {chapter[g['scene']]}" if chapter[g["scene"]] else "")
                md += [f"## {head}  ({ts(start, '.')[3:8]})", ""]
                last = g["scene"]
            md += [f"**{ts(g['t'], '.')[3:10]} \u00b7 {g['id']}** \u2014 *{visual[g['id']]}*", ""]
            md += [f"> [{ts(g['t'] + s['start'], '.')[3:10]}] {s['text']}  " for s in g["sentences"]] + [""]
        (out / f"{NAME}_script.md").write_text("\n".join(md), encoding="utf-8")
        (out / "timeline.json").write_text(json.dumps({"total": total, "scenes": scene_rows, "clips": [
            {k: g[k] for k in ("scene", "id", "t", "dur")} for g in timeline]}, indent=1))

        # 5. picture, and the soft-subtitle version (video stream copied, not re-encoded)
        lst = out / "concat.txt"
        lst.write_text("".join(f"file '{vids / s}.mp4'\n" for s in SCENES))
        picture = out / "picture.mp4"
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-an", "-c:v", "copy", picture])
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", picture, "-i", master, "-i", out / f"{NAME}.en.srt",
             "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text",
             "-metadata:s:s:0", "language=eng", "-metadata:s:a:0", "language=eng", "-metadata", f"title={TITLE}",
             "-shortest", "-movflags", "+faststart", out / f"{NAME}_softsubs.mp4"])
        print(f"prep done: picture {probe(picture):.2f}s, audio {probe(master):.2f}s")

    if a.stage in ("burn", "all"):
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", out / "picture.mp4", "-i", master,
             "-vf", f"ass={out / (NAME + '.en.ass')}", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
             "-metadata", f"title={TITLE}", out / f"{NAME}.mp4"])
        print("burn done")


if __name__ == "__main__":
    main()
