# Model in Motion · The Logistic Fixed-Effect Model · Episode 11: Swap the Curve

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M11, the first of Act IV (Measures and flags): keep a clinic's own patients, replace its curve by the
reference clinic's, and count. Observed over expected at the reference is the indirect standardized ratio.

| File | What it is |
|---|---|
| `e11_numbers.py` | Every number the episode shows or says, computed and checked (26 checks). Writes `e11_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode11.py` | Nine scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- This episode pays off Episode 3, which gave Alder 1.4 against the pool and 1.8 against everyone else, and asked for
  "a yardstick no single clinic can bend". The checks recompute both of Episode 3's figures from the cast.
- The boards use the probability panel (`CurvePanel`), where each clinic is a curve; Episodes 4 to 9 used the log-odds
  panel, where each clinic is a line. The script says "curve" throughout.
- The narration rounds to whole percentages (34%, 80%, 18%, 62%); the sums on screen use three decimals so that they
  come to 13.0 and 8.02.
- pprof_py 0.7.0 returns the same expected counts, ratios, rates and Wald interval as the direct calculation.
- `mim/crowd.py` gained `joint_fit`, the crowd's fixed-effect fit by joint Newton steps. Episodes 4 and 9 still carry
  their own copies of that loop.
- `e11_numbers.py` reads Episode 9's numbers file (Alder's interval) and Episode 10's (Elm's printed value and the
  size-weighted average).

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 11: Script for Review".

    python e11_numbers.py                                  # from this folder; a few seconds
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
