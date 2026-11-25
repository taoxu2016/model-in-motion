# Model in Motion

Animated explainers of statistical models, built with ManimCE. One repository, one shared library, one folder per episode.

This repository holds the logistic fixed-effect arc of the series: nineteen episodes, one for each module of its
blueprint. Episodes 1 to 3 are finished; Episodes 4 to 19 are animatics (script, checked numbers, voiceover, and one
still board per narration clip).

Start here:

- `docs/STATUS.md`: one row per episode, with its stage, running time, check count and review link.
- `docs/DECISIONS.md`: the 86 choices the fifteen draft scripts are waiting on.
- `renders/animatics/`: the current animatic of every unfinished episode, ready to watch.
- `docs/blueprints/`: the blueprint this arc follows, and the Cox arc's.

## Layout

```
mim/                     the shared library: one copy, imported by every episode
  common.py              series identity (palette, type, logo), the five-clinic cast, chips, trays, beams, narration sync
  kit.py                 rulers, the risk chip, the step arrow (used from Episode 3 on)
  lines.py               the log-odds line panel, the probability curve panel, the beta dial, the gamma sliders (from Episode 4 on)
  boards.py              text styles, marks, the control strip, title and end cards (from Episode 5 on)
  meters.py              the fitting machine: linked sliders, observed-minus-expected meters, dial, height bar (from Episode 6 on)
  crowd.py               the simulated crowd of 200 providers (numpy and scipy only)
  castfit.py             the five-clinic cast and its fixed-effect fit, for number files (numpy only)
  piles.py               histograms of counts, with a marker and a bell-curve overlay (Episodes 13 and 14)
  funnel.py              the funnel plot: ratio against precision, with its two edges (from Episode 15)
tools/                   one copy of each tool; each takes the episode folder as its first argument
  build.sh               voiceover, every scene, assembly
  make_voiceover.py      narration.json -> Kokoro TTS -> one WAV per clip, with exact sentence timings
  assemble.py            scenes + narration -> final video, mastered audio, captions
  review.py              review sheets: frames near the end of every narration clip
  contact_sheet.py       frame grids at chosen times
  listen_through.py      the narration as one audio file with a timestamped script, before any animation
  make_data.py           Episode 1's data files (crowd ranks, luck re-deals)
  check_repo.py          regression test for finished episodes
logistic_fe/
  e01_unfair_comparisons/        5:52   narration/  audio/  data/  episode/episode01.py  reference/timings/
  e02_odds_and_the_s_curve/      5:00   narration/  audio/         episode/episode02.py  reference/timings/
  e03_observed_versus_expected/  3:42   narration/  audio/         episode/episode03.py  reference/timings/
  e04_one_intercept_per_provider/       animatic stage: numbers file, approved script, voiceover, a board per clip
  e05_reading_gamma/                    animatic stage: numbers file, draft script, voiceover, a board per clip
  e06_fitting_by_balance/               animatic stage: numbers file, draft script, voiceover, a board per clip
  e07_climbing_the_hill/                animatic stage: numbers file, draft script, voiceover, a board per clip
  e08_the_arrow_matrix/                 animatic stage: numbers file, draft script, voiceover, a board per clip
  e09_how_sure_are_we/                  animatic stage: numbers file, draft script, voiceover, a board per clip
  e10_no_events_no_peak/                animatic stage: numbers file, draft script, voiceover, a board per clip
  e11_swap_the_curve/                   animatic stage: numbers file, draft script, voiceover, a board per clip
  e12_swap_the_patients/                animatic stage: numbers file, draft script, voiceover, a board per clip
  e13_unequal_coins/                    animatic stage: numbers file, draft script, voiceover, a board per clip
  e14_three_shortcuts/                  animatic stage: numbers file, draft script, voiceover, a board per clip
  e15_the_funnel/                       animatic stage: numbers file, draft script, voiceover, a board per clip
  e16_trusting_the_risk_model/          animatic stage: numbers file, draft script, voiceover, a board per clip
  e17_fixed_or_random/                  animatic stage: numbers file, draft script, voiceover, a board per clip
  e18_too_many_intercepts/              animatic stage: numbers file, draft script, voiceover, a board per clip
  e19_wider_than_chance/                animatic stage: numbers file, draft script, voiceover, a board per clip (the arc's last episode)
docs/
  STATUS.md              one row per episode: stage, script, time, words, clips, checks, review link
  DECISIONS.md           the open choices of the fifteen draft scripts, gathered from their reviews
  blueprints/            the logistic fixed-effect blueprint (Markdown) and the Cox blueprint (PDF)
    logistic_fixed_effect_analysis/   the pprof_py scripts that computed the blueprint's numbers, and their output
renders/
  animatics/             the 720p animatic of Episodes 4 to 19, each with captions and a timed script
```

An episode folder holds only what is its own. Each episode file sets `MIM_EPISODE` to its folder and imports `mim.common`,
so narration, audio, data and build output are always found beside the episode.

## Rules

1. **Narration first.** The script is written, read and voiced before any scene. Scenes are cut to the voice clips.
2. **Numbers come from code.** From Episode 4 on, each episode has a numbers file that computes and checks every figure
   shown or said. Scenes and narration read its JSON; nothing numeric is typed into scene code. The blueprint's
   own numbers come from `docs/blueprints/logistic_fixed_effect_analysis/`.
3. **One copy of shared code.** Shared code lives in `mim/` and `tools/`. Episodes 1 to 3 used byte-identical copies
   of `common.py`, so moving to one copy changed nothing but three import lines per episode.
4. **Finished episodes are frozen behind a test.** See below.

## Build

    tools/build.sh logistic_fe/e03_observed_versus_expected preview     # 480p15
    tools/build.sh logistic_fe/e03_observed_versus_expected final       # 1080p60, about 13 minutes per episode on one core

One scene: `cd logistic_fe/e03_observed_versus_expected && manim -ql --media_dir build/media episode/episode03.py S04_Meter`

## Regression test

    python tools/check_repo.py

Every finished episode keeps `reference/timings/`, written by its final 1080p60 render. The test re-renders each scene at
320 x 180 and 60 fps and compares every clip start and scene length with the reference. Timing depends on the frame rate,
not on resolution, so a match must be exact. The test catches a change in the shared library, the audio or the toolchain.
It does not compare pictures: a layout change that keeps the timing would pass.

Last run, 24 November 2026: all 26 scenes of Episodes 1 to 3 reproduce, largest difference 0.0000 s
(`reference_check_2026-11-24.txt`). `tools/make_data.py` also regenerates Episode 1's two data files byte for byte.

## Gates for a new episode

1. Script and numbers file, reviewed by a statistician before anything is voiced.
2. Voiceover and a listen-through (`tools/listen_through.py`).
3. Animatic: stills with sound.
4. Animation, reviewed in frames from every clip.
5. A watch-through with sound by a person. The model that writes the scenes reviews stills only.

## Audio

Every episode keeps its voice clips in `audio/segments/`, because its pictures are cut to those exact clips: the
finished episodes' animation, and the animatics' boards. `tools/make_voiceover.py` reuses cached sentences, so a
script edit re-voices only what changed.

## Requirements

Python 3.12, `pip install -r requirements.txt`, ffmpeg with libass, LaTeX (`standalone`, `preview`, `amsmath`), `dvisvgm`,
Pango, and the fonts Inter, Inter Display and Lora. The Kokoro voice files (`kokoro-v1.0.onnx`, `voices-v1.0.bin`) come
from the `model-files-v1.0` release of `thewh1teagle/kokoro-onnx`; point `KOKORO_MODELS` at their folder.

`requirements.txt` pins the versions everything here was last built and checked with: ManimCE 0.22.1, pprof_py 0.7.0 at
commit `070f9af`, on ffmpeg 6.1.1 and TeX Live 2023. Rendering a scene needs no voice files, because the voice clips
are in the repository; only re-voicing a changed script does.

## Not in this repository

- **The finished videos of Episodes 1 to 3.** Their sources are here, frozen behind the regression test. The 1080p60
  files were rendered in another workspace; `tools/build.sh logistic_fe/<episode folder> final` rebuilds each.
- **The Cox arc.** Its blueprint is in `docs/blueprints/`. Its first three episodes were built in another workspace,
  each with its own copy of the shared library. Folding them in is the move Episodes 1 to 3 of this arc already made:
  one copy of `mim/`, a few import lines per episode. They would live in `cox_ph/`, beside `logistic_fe/`.
- **The central limit theorem pilot and the least-squares short.** The pilot belongs to a different series
  (Statistics, Visually) with its own library; the short is a single file. Both are separate bundles.
- **The script reviews.** They are Claude Docs, linked from `docs/STATUS.md`. What they verify can be reproduced here:
  each episode's numbers file prints every check when run. What they ask for is in `docs/DECISIONS.md`.
- **The voice model files and the fonts**, for size and licence reasons. See Requirements.
- **Build output.** `build/` and `audio/cache/` are ignored; everything in them can be regenerated.

## Data

Every dataset is simulated in code from fixed seeds: five invented clinics with 103 patients, a crowd of 200
providers, and the experiments built on them. There is no patient-level or restricted data anywhere in this repository.

## History

The work was not under version control while it was made. This repository was assembled from it on 25 November 2026,
so its history is a record of structure, not of time: one commit for the scaffold, one for the shared library and
tools, one for each episode and one for the documents. The rendered animatics are one further commit on top, so that
they can be left out. The scripts behind the blueprint's numbers followed on the same day, in one more commit. The commits carry a placeholder author.
To make them yours before you publish:

    git rebase -r --root --exec "git commit --amend --no-edit --reset-author"

No licence has been chosen yet.
