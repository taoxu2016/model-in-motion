# Model in Motion · The Logistic Fixed-Effect Model · Episode 16: Trusting the Risk Model

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M16 (Extended), the first of Act V: every provider's observed-minus-expected meter is level under any
fixed-effect fit, so the model has to be checked on other groups: tenths of predicted risk, and halves within a provider.

| File | What it is |
|---|---|
| `e16_numbers.py` | Every number the episode shows or says, computed and checked (24 checks). Writes `e16_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode16.py` | Nine scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- Three experiments, all on the series' crowd (seed 2026) with its own patients and its own uniform draws
  (`np.random.default_rng(2027).random(N)`, which reproduces the crowd's outcomes exactly), so each differs from the
  crowd as it is only in the one thing changed: (A) the crowd as it is; (B) 0.3 (x1^2 - 1) added to the true log-odds,
  fitted without and then with a squared term; (C) the largest provider (484 patients) given a slope of 1.6 and an
  intercept 0.35 lower.
- The blueprint does not record the draws behind (B) and (C), and its figures could not be reproduced exactly from any
  stream tried. This file's figures are used throughout; the script doc lists both sets side by side. The largest gaps:
  the steeper-slope provider (143 against the blueprint's 135; halves 18 against 41.2 and 125 against 101.8, where the
  blueprint has 18 against 29.2 and 117 against 105.8) and the unusual-case-mix excess (16% against 13%).
- `mim/crowd.py` gained `fit_fixed_effects(X, y, prov)`, the crowd's fit for any number of covariates; `joint_fit` now
  calls it. Earlier episodes' numbers files give the same results.
- The meters are the series' own (`mim.meters.Meter`); a tenth's meter tilts by six times (ratio - 1), and the angle
  saturates, so the printed ratio carries the value.
- The AUC board shows the first four of 200,000 sampled pairs in full (three in the right order) and the first thousand
  as squares (738 in the right order, against an AUC of 0.739). A sample of forty gave 23, which would have misled.
- "The gain says providers differ, not that the risk rule got better" rests on one check: ranking patients by the fitted
  rule alone gives an AUC of 0.717, the same as a fit without provider terms.
- `e16_numbers.py` runs in about three seconds.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 16: Script for Review".

    python e16_numbers.py                                  # from this folder
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
