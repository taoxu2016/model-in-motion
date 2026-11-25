# Model in Motion · The Logistic Fixed-Effect Model · Episode 17: Fixed or Random?

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M17 (Advanced), the second of Act V: the random-effect alternative. It pulls each provider's estimate
toward a common centre by its reliability, which buys accuracy on average and costs two things: true outliers are drawn
in, and the errors follow the case mix when performance and case mix are linked.

| File | What it is |
|---|---|
| `e17_numbers.py` | Every number the episode shows or says, computed and checked (25 checks). Writes `e17_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode17.py` | Nine scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- The random-effect fits are pprof_py 0.7.0's `LogisticRandomEffectModel` (about a second and a half for the crowd's
  28,848 patients). Its fitted spread for the crowd is 0.3325; reliability times the fixed-effect estimate reproduces
  its random effects with correlation 0.999.
- Errors are errors of position: a provider's estimate about the median estimate, against its true effect about the
  median truth. That definition reproduces the blueprint's figures (0.280 and 0.196; 0.403 and 0.250).
- The cast in S03 goes beyond the blueprint, which gives only Dune's reliability of 0.20. Here the same pull is carried
  through all five clinics: each clinic's most likely effect if effects are draws from a bell curve centred on the
  cast's reference (Cedar's -1.52) with the crowd's spread, the risk rule held at the fixed-effect estimate. That gives
  Dune -1.33, Alder -1.18 (the order flips) and Elm -1.71. pprof_py's own random-effect fit of the five clinics (spread
  0.41) gives the same order and -1.65 for Elm. It is the first decision in the script doc.
- The flags in S06 compare two different tests: the exact test at the median reference for fixed effects, and the
  package's test of each random effect against its own standard error.
- The no-link crowd is `simulate(seed=2026, rho=0.0)`: the same draws with the link between effect and case mix
  removed. `mim/crowd.py`'s `simulate` gained the `rho` argument for this (default unchanged) and now also returns `u`.
- Fixed-effect values are drawn in paper white and random-effect values in accent yellow in every scene.
- `e17_numbers.py` reads Episode 9's numbers file for the cast's standard errors. It runs in about six seconds.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 17: Script for Review".

    python e17_numbers.py                                  # from this folder
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
