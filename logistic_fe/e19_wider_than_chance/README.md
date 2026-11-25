# Model in Motion · The Logistic Fixed-Effect Model · Episode 19: Wider than Chance

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**
**This is the last episode of the arc.** Its final scene closes the series and its end card names no next episode.

Blueprint module M19 (Advanced), the last of Act V and of the blueprint: overdispersion and the empirical null. When
providers truly differ a little, their z-values spread wider than chance, most for large providers, and a test of
"exactly at the reference" flags a quarter of them. The empirical null asks instead whether a provider is unusual
among providers.

| File | What it is |
|---|---|
| `e19_numbers.py` | Every number the episode shows or says, computed and checked (21 checks). Writes `e19_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode19.py` | Nine scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- The fits, the exact tests, the funnel limits and the empirical null are pprof_py 0.7.0's own
  (`LogisticFixedEffectModel.test`, `.funnel_limits`, `pprof_py.inference.EmpiricalNull.fitter(size=..., n_groups=3)`).
  The series' own exact test flags the same providers at every setting of the knob. Almost every figure matches the
  blueprint to the digit; the numbers file takes about a minute because it fits and tests 44 crowds.
- The knob is `simulate(seed=2026, tau=...)` at 0, 0.1, 0.2 and 0.3: the same 194 ordinary providers and six planted
  ones each time. Counts in the cold open are the funnel's (49 of 194 outside, the score test's picture, as in Episode
  15); from S03 on they are the exact test's (48).
- The funnel's widened limits come from a null fitted to the score test's z-values (spreads 1.15, 1.60, 2.21), not the
  exact test's (1.14, 1.60, 2.18): the funnel is the score test's picture. The limits are re-centred as well as
  widened: 1 + (centre -+ 1.96 spreads) / sqrt(precision), checked against the package to 1e-8.
- One place corrects the blueprint. It says that at a knob of zero the estimated null is too narrow and flags more.
  That is true of the crowd on screen (20 flags against 11) but not on average: over twenty redraws at zero the
  empirical null flags 4.1% of ordinary providers and the standard test 4.7%. The script says the fitted curve "can
  miss"; the doc lists this as a decision.
- Redraws use seeds 4000 + 10 j, as elsewhere in the series; the blueprint's own redraws are not recorded (it has
  24.4% and 5.7% where this file has 22.6% and 4.6%).
- `mim/boards.py` gained `series_end_card(scene, clip, line)` for an arc's final episode. The cold open reads Episode
  15's numbers file for its two funnels.
- The spread of z at a knob of 0.2 is 1.405: the board prints 1.41, the blueprint 1.40.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 19: Script for Review".

    python e19_numbers.py                                  # from this folder (about a minute)
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
