# Model in Motion · The Logistic Fixed-Effect Model · Episode 9: How Sure Are We?

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M9: the curvature of the hill gives the dial's standard error; a clinic's uncertainty is its own plus
a share of the dial's; a fair comparison reads every clinic at the average case mix.

| File | What it is |
|---|---|
| `e09_numbers.py` | Every number the episode shows or says, computed and checked (24 checks). Writes `e09_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode09.py` | Nine scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- Three standard errors per clinic are in play: on its own, read at zero, and at the average case mix. The caterpillar
  and the crowd use the last, which is pprof_py's `variances_['gamma_case_mix']`; a check compares the two.
- Two figures sit on a rounding boundary: zero is 3.45 standard errors from the top (said as "about three and a half"),
  and Alder's standard error three units away is 1.885 (said as 1.9).
- The bands in S06 are pointwise 95% bands round each fitted line, drawn from the same variance formula.
- `e09_numbers.py` reads Episode 6's numbers file for the hill and Episode 8's for where Elm's slider stopped.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 9: Script for Review".

    python e09_numbers.py                                  # from this folder; a few seconds
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
