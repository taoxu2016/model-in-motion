---
name: produce-episode
description: Take one episode of the logistic fixed-effect arc from approved script and animatic to a finished 1080p60 video, gate by gate. Use when the owner asks to animate, finish or produce an episode.
argument-hint: <episode folder, e.g. logistic_fe/e04_one_intercept_per_provider>
disable-model-invocation: true
---

# Produce the episode in $ARGUMENTS

Work through the stages in order, report briefly after each, and stop where a stage says to ask.

## 0. Preconditions (stop and report if any fails)

- `docs/STATUS.md` shows this episode's script as Approved or Final. If it is in draft, list its open choices from
  `docs/DECISIONS.md` and stop.
- The numbers file passes: `cd $ARGUMENTS && python3 eNN_numbers.py` exits 0.
- `audio/manifest.json` matches `narration/narration.json` (the verify skill has the check). If not, run `/revoice` first.
- `tools/setup_env.sh --check` passes.

## 1. Read

- The episode's `README.md`, `narration/narration.json` (every clip's `visual` note), the numbers JSON, and its entry
  in `docs/DECISIONS.md`.
- Its module in the blueprint: learning objective, mathematics, animation sequence, misconceptions; and the module's
  rows in Step 5's accuracy audit.
- The closing scene of the previous episode and the opening of the next one, for continuity.
- The `mim/` modules the animatic imports. Reuse the vocabulary before inventing (series-style skill).

## 2. Plan

Per scene: what moves on each clip, which keys of the numbers JSON it shows, what carries over from the scene before.
If the plan departs from the blueprint entry or the clip's `visual` note, show it to the owner before writing code.

## 3. Build, one scene at a time

1. Replace the animatic boards in `episode/episodeNN.py` with animation, keeping the `with self.nar(...)` structure
   clip for clip. Every number on screen comes from the numbers JSON.
2. Render the scene alone at 480p15, logging to a file:
   `cd $ARGUMENTS && manim -ql --disable_caching --media_dir build/media episode/episodeNN.py SXX_Name > /tmp/SXX.log 2>&1`
3. The log has no traceback and no `[cue not found]`.
4. Make a review sheet (`python3 tools/review.py $ARGUMENTS /tmp/SXX.png 480p15 SXX_Name`, adding `:t1,t2` for
   mid-clip moments) and read it with the review-frames checklist. Fix and repeat until it is clean.

## 4. Whole-episode preview

Run `tools/build.sh $ARGUMENTS preview` in the background and poll. Read sheets of every scene; ask the frame-reviewer
agent for a second read. Tell the owner the preview is ready in `$ARGUMENTS/build/final/`, and wait for their look.

## 5. Final render

Once the owner is happy with the preview: `tools/build.sh $ARGUMENTS final` in the background (about 13 minutes per
episode on one core). Then read a contact sheet of the burned-in MP4 at 10–12 moments across the episode: captions must
never cover content.

## 6. Freeze and record

- Copy `build/timings/*.json` to `reference/timings/`: this puts the episode under `tools/check_repo.py`.
- Update the episode's `README.md` (status, running time, design decisions, departures from the blueprint, verified
  numbers) and its row in `docs/STATUS.md`.
- Copy the burned-in MP4, `.en.srt`, `.en.vtt` and `_script.md` from `build/final/` to `renders/finished/`, named like
  the files already there. Remove the episode's animatic from `renders/animatics/` only if the owner agrees.
- Run the verify skill.

## 7. Commit and hand over

- Commit the episode as `Logistic FE, Episode NN: Title (finished)`, and the renders in a separate `Renders: …`
  commit. Ask before pushing.
- Tell the owner what to listen and look for in the watch-through with sound (gate 5): new pronunciations, tight
  timing, and anything you could not judge from stills.
