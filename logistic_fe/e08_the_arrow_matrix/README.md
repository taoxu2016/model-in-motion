# Model in Motion · The Logistic Fixed-Effect Model · Episode 8: The Arrow Matrix

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M8 (Extended): clinics disturb each other only through the dial, so the information matrix is an
arrowhead; folding each clinic into the corner leaves one small system, and the folded step is Newton's step exactly.

| File | What it is |
|---|---|
| `e08_numbers.py` | Every number the episode shows or says, computed and checked (22 checks). Writes `e08_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode08.py` | Eight scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- The table "at the fit" is pprof_py's final state, with Elm's slider where its fifth step left it (-6.25).
- Rounded to two decimals the fold's pieces sum to 7.28 and 2.92; the exact figures give 7.27 and 2.93. The corner's
  countdown on screen uses exact running values.
- The timed fit (2,000 providers, 205,367 patients) is machine-dependent; the script says only "well under a second".
- `e08_numbers.py` reads Episode 4's and Episode 7's numbers files, and `episode08.py` reads Episode 7's for the map.
  The map helper is duplicated in Episodes 7 and 8 and belongs in `mim/`.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 8: Script for Review".

    python e08_numbers.py                                  # from this folder; about ten seconds, most of it the timed fit
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
