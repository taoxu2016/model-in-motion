# Model in Motion · The Logistic Fixed-Effect Model · Episode 6: Fitting by Balance

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M6: a guess is scored by the probability it gave to what happened (the likelihood), the slope of
that height in each clinic's γ is the clinic's observed minus expected, and the fit is where every meter is level.

| File | What it is |
|---|---|
| `e06_numbers.py` | Every number the episode shows or says, computed and checked (24 checks). Writes `e06_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode06.py` | Eight scenes, one board per narration clip (animatic pass), built on `mim/meters.py`. |

The machine on screen (`mim.meters.FitMachine`) computes its own readings from the slider and dial positions.
That is how one draft sentence was caught: it said only Dune's meter responds to Dune's slider, and the dial's
meter moved too.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 6: Script for Review".

    python e06_numbers.py                                  # from this folder: prints the ledger, exits 1 if a check fails
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
