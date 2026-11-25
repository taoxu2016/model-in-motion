# Model in Motion

Animated explainers of statistical models, built with ManimCE. Narration comes first and is voiced offline with
Kokoro; scenes are cut to the voice clips; captions come from exact sentence timings. This repository holds the
logistic fixed-effect arc: 19 episodes, one per module of `docs/blueprints/logistic_fixed_effect_blueprint.md`.

Before a task, read `docs/STATUS.md` (one row per episode) and `docs/DECISIONS.md` (choices waiting on the owner).
The first time, read `docs/HANDOFF.md`: how the work got here and what comes next.

## Layout

- `mim/`: the shared library, one copy for every episode. `common.py` (identity, five-clinic cast, chips, trays,
  beams, narration sync), `kit.py` (rulers, risk chip, step arrow), `lines.py`, `boards.py`, `meters.py`, `piles.py`,
  `funnel.py`, and the numpy-only `crowd.py` and `castfit.py` that numbers files import.
- `tools/`: one copy of each tool; each takes the episode folder as its first argument.
- `logistic_fe/eNN_<slug>/`: one episode. `narration/narration.json` (the script), `audio/` (the voice clips the scenes
  are cut to; committed), `episode/episodeNN.py` (scenes), `eNN_numbers.py` and `.json` (Episode 4 on), `data/`
  (Episode 1), `reference/timings/` (finished episodes only), `README.md`. `build/` is generated and ignored.
- `docs/`: status, decisions, blueprints, and `blueprints/logistic_fixed_effect_analysis/` (the pprof_py scripts behind
  the blueprint's numbers). `renders/finished/`: Episodes 1–3 at 1080p60. `renders/animatics/`: Episodes 4–19 at 720p.

## Commands

From the repository root; `EP` is an episode folder such as `logistic_fe/e04_one_intercept_per_provider`.

    tools/setup_env.sh --check                       # can this machine build? (without --check: install what is missing)
    (cd EP && python3 eNN_numbers.py)               # Episode 4 on: every number, checked; exits 1 on a failed check
    python3 tools/make_voiceover.py EP               # voice the script; unchanged sentences come from audio/cache/
    python3 tools/listen_through.py EP               # the narration as one audio file and a timed script (EP/build/listen/)
    (cd EP && manim -ql --disable_caching --media_dir build/media episode/episodeNN.py S03_Odds)   # one scene, 480p15
    tools/build.sh EP preview                        # voiceover, every scene at 480p15, assembly
    tools/build.sh EP final                          # the same at 1080p60: about 13 minutes per episode on one core
    python3 tools/review.py EP /tmp/sheet.png 480p15 S01_ColdOpen S02_Title:3.0    # a frame near the end of every clip
    python3 tools/contact_sheet.py VIDEO /tmp/frames.png 12.5 40 61.2               # frames at chosen times
    python3 tools/check_repo.py                      # regression test of the finished episodes (several minutes)

Final renders, whole-episode builds and the regression test outlast a normal foreground command: run them in the
background with the log in a file, and poll. Scenes render to `EP/build/media/videos/episodeNN/<quality>/`; assembled
videos, captions and the timed script go to `EP/build/final/`.

## Rules

1. **Narration first.** A script is written, checked, approved by the owner and voiced before scenes are built. When a
   picture needs a different sentence, change the script and re-voice it; never cut scenes against stale audio.
2. **Numbers come from code.** From Episode 4 on, every figure shown or said comes from the episode's `eNN_numbers.json`.
   Never type a number into scene code by hand. In `narration.json`, `text` holds digits and `say` the spoken form.
3. **One copy of shared code.** Change `mim/` and `tools/`; never copy them into an episode. Any change there must pass
   `tools/check_repo.py`.
4. **Finished episodes are frozen.** Episodes 1–3: leave their narration, audio, scenes and reference timings alone
   unless the owner asks. `tools/check_repo.py` must reproduce them exactly.
5. **Gates, in order, for every episode:** script and numbers file reviewed and approved → voiceover and listen-through →
   animatic → animation reviewed in frames from every clip → a watch-through with sound by a person. You cannot hear
   audio: never claim a listen-through or watch-through happened; ask the owner for it.
6. **Ask first** before changing an approved script, re-voicing a finished episode, deleting renders, or pushing.

## Scene code

- One `EpisodeScene` subclass per scene id in `narration.json`, in order, named like `S04_Meter`.
- Each clip is `with self.nar("s4_2") as seg:`, which starts the clip and holds the scene until it ends. Inside, time
  beats with `seg.wait_until(seg.word(k, "phrase"))`, `seg.s(k)` and `seg.e(k)` (sentence k's start and end).
- `seg.word` finds the phrase in the spoken form (`say`) first. A miss prints `[cue not found]` and falls back to the
  sentence start, so grep every render log for it.
- Keep all content above y = −3.0: the burned-in caption box sits below it.
- Take colours, type and motifs from `mim/` (the series-style skill lists them). Observed quantities are solid,
  expected ones dashed; β and what it drives are yellow; each clinic keeps its hue in every episode.
- Clear updaters before a scene's closing fade-out.

## Review loop

Render a scene at 480p15 → make a review sheet of every clip (`tools/review.py`) → read it → fix → repeat. Only then
render at 1080p60, assemble, and read frames of the burned-in file. The frame-reviewer agent gives a second read of a
sheet; the stats-reviewer agent checks scripts and numbers against the blueprint and pprof_py.

## Git

- One commit per episode stage, e.g. `Logistic FE, Episode 04: One Intercept per Provider (finished)`; documents as
  `Docs: …`; rendered videos as `Renders: …`, always in a commit of their own.
- Committed: `audio/segments/`, `audio/manifest.json`, reference timings, renders. Ignored: `build/`, `audio/cache/`.
  Never commit the voice model files or fonts.
- The history carries a placeholder author (see the README). Ask before `git push`.

## Claude Code setup in this repository

Skills: `/produce-episode EP` (animatic to finished), `/revoice EP` (script change to voice and listen-through),
`verify` (runs before commits), `review-frames` and `series-style` (reference). Agents: `stats-reviewer`,
`frame-reviewer`. A session-start hook runs `tools/setup_env.sh --check` and reports what is missing.
