"""Regression test: re-render episodes at low resolution and compare narration timings with the recorded ones.

Every finished episode keeps reference/timings/*.json, written by its final 1080p60 render. Clip timing depends
on the frame rate, not on resolution, so a 60 fps render at 320 x 180 must reproduce every clip start and every
scene length exactly. A difference means the shared library, the narration audio or the toolchain has changed.

usage: python tools/check_repo.py [EPISODE_FOLDER ...] [--scenes S01_ColdOpen ...] [--tolerance 0.001]
       (no folder: every episode under the repository that has reference/timings)
"""
import argparse, json, subprocess, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def check(ep: Path, scenes, tol):
    stem = next((ep / "episode").glob("episode*.py")).stem
    spec = json.loads((ep / "narration" / "narration.json").read_text())
    worst, bad = 0.0, 0
    wanted = [s["id"] for s in spec["scenes"] if not scenes or s["id"] in scenes]
    if not wanted:                                   # a filter that matches nothing must not read as a pass
        print(f"  no scene here matches {scenes}")
        return 0.0, 1
    for sc in wanted:
        ref = json.loads((ep / "reference" / "timings" / f"{sc}.json").read_text())
        t0 = time.time()
        r = subprocess.run(["manim", "--fps", "60", "-r", "320,180", "--disable_caching", "-v", "ERROR", "--progress_bar", "none",
                            "--media_dir", "build/check_media", f"episode/{stem}.py", sc], cwd=ep, capture_output=True, text=True)
        if r.returncode != 0:
            bad += 1
            print(f"  {sc:20s} RENDER FAILED\n{r.stderr[-1500:]}")
            continue
        new = json.loads((ep / "build" / "timings" / f"{sc}.json").read_text())
        same_ids = [g["id"] for g in new["segments"]] == [g["id"] for g in ref["segments"]]
        d = max([abs(new["duration"] - ref["duration"])] +
                [abs(a["start"] - b["start"]) for a, b in zip(new["segments"], ref["segments"])]) if same_ids else float("inf")
        worst = max(worst, d)
        ok = same_ids and d <= tol
        bad += not ok
        print(f"  {sc:20s} {'ok  ' if ok else 'DIFF'} {len(ref['segments']):2d} clips, {ref['duration']:7.2f} s, "
              f"largest timing difference {d:.4f} s   (rendered in {time.time() - t0:.0f} s)", flush=True)
    return worst, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="*")
    ap.add_argument("--scenes", nargs="*", default=[])
    ap.add_argument("--tolerance", type=float, default=0.001)
    a = ap.parse_args()
    eps = [Path(e).resolve() for e in a.episodes] or sorted(p.parents[1] for p in REPO.glob("*/*/reference/timings"))
    total_bad = 0
    for ep in eps:
        print(ep.relative_to(REPO), flush=True)
        worst, bad = check(ep, a.scenes, a.tolerance)
        total_bad += bad
        print(f"  -> {'all scenes reproduce' if not bad else str(bad) + ' scene(s) differ or failed'}; largest difference {worst:.4f} s", flush=True)
    sys.exit(1 if total_bad else 0)


if __name__ == "__main__":
    main()
