# Model in Motion · The Logistic Fixed-Effect Model · Episode 5: Reading γ

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M5: a gap between two clinics' γ is an odds ratio for patients who look the same on paper.
What it does to a probability depends on the patient, and only gaps survive a change of coding.

| File | What it is |
|---|---|
| `e05_numbers.py` | Every number the episode shows or says, computed and checked (24 checks). Writes `e05_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode05.py` | Seven scenes, one board per narration clip (animatic pass), on `mim/lines.py` and `mim/boards.py`. |

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 5: Script for Review".

    python e05_numbers.py                                  # from this folder: prints the ledger, exits 1 if a check fails
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
