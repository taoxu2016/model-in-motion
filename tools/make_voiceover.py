"""Generate the narration audio for an episode.

Reads narration/narration.json, synthesizes every sentence with Kokoro (offline neural TTS),
joins sentences into one WAV per segment with fixed pauses, and writes audio/manifest.json:

    {segment_id: {"file": ..., "duration": s, "sentences": [{"text", "start", "end"}, ...]}}

Sentence offsets are exact (they come from the synthesized sample counts), so subtitles built
from the manifest stay in sync without any forced alignment.

Usage:  python tools/make_voiceover.py EPISODE_FOLDER [--models DIR]      (or set KOKORO_MODELS)
Models: kokoro-v1.0.onnx and voices-v1.0.bin from github.com/thewh1teagle/kokoro-onnx/releases
"""
import argparse, hashlib, json, os, re
from pathlib import Path

import numpy as np
import soundfile as sf

import sys

if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
    sys.exit("usage: python tools/make_voiceover.py EPISODE_FOLDER [--models DIR]")
ROOT = Path(sys.argv.pop(1)).resolve()                       # the episode folder
SR = 24_000


def apply_pronunciations(text: str, table: dict) -> str:
    for word, spoken in table.items():
        text = re.sub(rf"(?<![\w-]){re.escape(word)}(?![\w-])", spoken, text)
    return text.replace("\u201c", "").replace("\u201d", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=os.environ.get("KOKORO_MODELS", str(Path.home() / "tts_models")))
    args = ap.parse_args()

    from kokoro_onnx import Kokoro
    spec = json.loads((ROOT / "narration" / "narration.json").read_text())
    v = spec["voice"]
    tts = Kokoro(str(Path(args.models) / "kokoro-v1.0.onnx"), str(Path(args.models) / "voices-v1.0.bin"))

    cache = ROOT / "audio" / "cache"; cache.mkdir(parents=True, exist_ok=True)
    segdir = ROOT / "audio" / "segments"; segdir.mkdir(parents=True, exist_ok=True)
    pause = np.zeros(int(v["pause_between_sentences"] * SR), dtype=np.float32)
    tail = np.zeros(int(v["tail_pad"] * SR), dtype=np.float32)

    manifest, total = {}, 0.0
    for scene in spec["scenes"]:
        for seg in scene["segments"]:
            pieces, sentences, t = [], [], 0.0
            for k, s in enumerate(seg["sentences"]):
                say = apply_pronunciations(s.get("say", s["text"]), spec["pronunciations"])
                key = hashlib.sha1(f'{v["name"]}|{v["speed"]}|{say}'.encode()).hexdigest()[:16]
                f = cache / f"{key}.wav"
                if f.exists():
                    audio, _ = sf.read(f, dtype="float32")
                else:
                    audio, sr = tts.create(say, voice=v["name"], speed=v["speed"], lang=v["lang"])
                    assert sr == SR
                    sf.write(f, audio, SR, subtype="PCM_16")
                if k:
                    pieces.append(pause); t += len(pause) / SR
                d = len(audio) / SR
                sentences.append({"text": s["text"], "start": round(t, 3), "end": round(t + d, 3)})
                pieces.append(audio.astype(np.float32)); t += d
            pieces.append(tail)
            wav = np.concatenate(pieces)
            out = segdir / f'{seg["id"]}.wav'
            sf.write(out, wav, SR, subtype="PCM_16")
            dur = len(wav) / SR
            manifest[seg["id"]] = {"scene": scene["id"], "file": str(out.relative_to(ROOT)),
                                   "duration": round(dur, 3), "sentences": sentences}
            total += dur
            print(f'{seg["id"]:6s} {dur:6.2f}s  ({len(seg["sentences"])} sentences)', flush=True)
    (ROOT / "audio" / "manifest.json").write_text(json.dumps(manifest, indent=1))
    words = sum(len(s["text"].split()) for sc in spec["scenes"] for sg in sc["segments"] for s in sg["sentences"])
    print(f"total speech {total:.1f}s for {words} words -> {60 * words / total:.0f} wpm")


if __name__ == "__main__":
    main()
