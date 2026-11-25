# Status of the logistic fixed-effect arc

Nineteen episodes, one for each module of the blueprint (`docs/blueprints/logistic_fixed_effect_blueprint.md`).
Episodes 1 to 3 are finished; their 1080p60 videos are in `renders/finished/`. Episodes 4 to 19 are animatics: 16 of them, 79 minutes in all.

This table was generated from the repository on 25 November 2026. Words and clips are counted from each episode's
`narration/narration.json`; times are those of the rendered files; checks are the count printed by each numbers file,
all of which passed on that date (417 checks in total).

| Ep | Title | Blueprint | Tier | Stage | Script | Time | Words | Clips | Checks | Review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Unfair Comparisons | M1 · Act I | Core | Finished | Final | 5:52 | 878 | 38 |  |  |
| 2 | Odds and the S-Curve | M2 · Act I | Core | Finished | Final | 5:00 | 723 | 35 |  |  |
| 3 | Observed versus Expected | M3 · Act I | Core | Finished | Final | 3:42 | 507 | 24 |  |  |
| 4 | One Intercept per Provider | M4 · Act II | Core | Animatic | Approved | 7:19 | 1,092 | 37 | 37 | [doc](https://claude.ai/artifact/CTx3BUU8yhMrfH7d3cWDab) |
| 5 | Reading γ | M5 · Act II | Core | Animatic | Draft | 5:26 | 735 | 19 | 24 | [doc](https://claude.ai/artifact/L35SjQNzgRoUE8gbUHJrXp) |
| 6 | Fitting by Balance | M6 · Act III | Core | Animatic | Draft | 4:48 | 710 | 28 | 24 | [doc](https://claude.ai/artifact/Lq7j8V32pEEta8nK1GRxy2) |
| 7 | Climbing the Hill | M7 · Act III | Core | Animatic | Draft | 4:24 | 660 | 24 | 22 | [doc](https://claude.ai/artifact/AFCL9pJNsfSMQhcjTJs7mQ) |
| 8 | The Arrow Matrix | M8 · Act III | Extended | Animatic | Draft | 4:53 | 690 | 24 | 22 | [doc](https://claude.ai/artifact/L7TPKgtpLP3h5QC7gpTAC6) |
| 9 | How Sure Are We? | M9 · Act III | Core | Animatic | Draft | 5:08 | 705 | 25 | 24 | [doc](https://claude.ai/artifact/UqVkYFxTMt6d4Dp9AJQ9Ai) |
| 10 | No Events, No Peak | M10 · Act III | Extended | Animatic | Draft | 4:32 | 617 | 23 | 36 | [doc](https://claude.ai/artifact/1ppwveVzTHTo5WiUrQFrUE) |
| 11 | Swap the Curve | M11 · Act IV | Core | Animatic | Draft | 5:01 | 662 | 24 | 26 | [doc](https://claude.ai/artifact/UDTXUn14n9YYUXmsSFv3m1) |
| 12 | Swap the Patients | M12 · Act IV | Extended | Animatic | Draft | 4:56 | 649 | 23 | 27 | [doc](https://claude.ai/artifact/CLpwVHZ4XHs7UaLfjFps4x) |
| 13 | Unequal Coins | M13 · Act IV | Core | Animatic | Draft | 5:01 | 689 | 27 | 33 | [doc](https://claude.ai/artifact/A3FmxbMsB9pi3qxitVbSca) |
| 14 | Three Shortcuts | M14 · Act IV | Extended | Animatic | Draft | 4:40 | 615 | 21 | 26 | [doc](https://claude.ai/artifact/5yiMfeQu64TM6qP1nPcgQq) |
| 15 | The Funnel | M15 · Act IV | Core | Animatic | Draft | 4:36 | 671 | 22 | 27 | [doc](https://claude.ai/artifact/QHHJr7eN65HHKzeH86P2GR) |
| 16 | Trusting the Risk Model | M16 · Act V | Extended | Animatic | Draft | 4:45 | 675 | 21 | 24 | [doc](https://claude.ai/artifact/AwJpQAnD5ueHkitz7GM2Tb) |
| 17 | Fixed or Random? | M17 · Act V | Advanced | Animatic | Draft | 4:29 | 601 | 19 | 25 | [doc](https://claude.ai/artifact/BkeDAtbAyoQdALoDg3EmCT) |
| 18 | Too Many Intercepts | M18 · Act V | Advanced | Animatic | Draft | 3:55 | 567 | 17 | 19 | [doc](https://claude.ai/artifact/P71xgjDTSmoxyb5v5kAN2h) |
| 19 | Wider than Chance | M19 · Act V | Advanced | Animatic | Draft | 4:47 | 689 | 21 | 21 | [doc](https://claude.ai/artifact/En4DrP7FPy3p4cmE4oeD8j) |

## What the stages mean

- **Finished.** Animated, rendered at 1080p60, and frozen behind the regression test (`python tools/check_repo.py`).
  The videos were rendered in another workspace and committed to `renders/finished/`.
- **Animatic.** The script, its numbers file and its voiceover exist, and every narration clip has a still board cut to
  the voice. Most of the motion is still to come. The animatics are in `renders/animatics/`, which the renders commit adds.
- **Script: approved or draft.** Each animatic-stage script has a review doc that lists what is verified, what could
  mislead, and the choices it asks for. Only Episode 4's has been approved. The open choices for the other fifteen are
  gathered in `docs/DECISIONS.md`.

## What each animatic-stage episode still needs, in order

1. The script review: read the doc, settle its decisions, approve or revise.
2. A watch-through of the animatic with sound. The boards were reviewed from frames only; pacing, pronunciation and
   whether each board supports its sentence have not been checked by a person.
3. The animation pass, then a 1080p60 render, then `reference/timings/` so the regression test covers the episode.

The review links open Claude Docs that are private to their owner.
