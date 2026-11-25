# Model in Motion · The Logistic Fixed-Effect Model · Episode 10: No Events, No Peak

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M10 (an interlude, marked Extended): a clinic with no readmissions has a hill with no top, so the
gamma the software prints only records where the fitting stopped. Anything built on that number breaks; anything
built on the count survives.

| File | What it is |
|---|---|
| `e10_numbers.py` | Every number the episode shows or says, computed and checked (36 checks). Writes `e10_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode10.py` | Eight scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- Most checks run pprof_py 0.7.0 itself, because the episode is about what it prints. They depend on its defaults:
  tolerance 1e-8, a wall (`bound`) of 10, and a screen (`cutoff`) that keeps providers with more than 10 records.
  If a later version changes a default, the printed values for Elm change and the script must follow.
- "Taking turns waits for every slider to settle" is not in the blueprint. It was read from the loop condition of the
  package's Ban routine and confirmed by a run with the wall removed, which is still going at 10,000 rounds.
- The blueprint gives -2.18 for Elm's hill at the reference; the exact value is -2.1702 and the script says -2.17.
- In S07 both walls are drawn ten units from the same middle clinic. In the all-readmitted version of the cast the
  middle clinic becomes Alder, so the package prints +9.35 there; a check covers it.
- `e10_numbers.py` reads Episode 8's numbers file (the joint path) and Episode 9's. It takes about ten seconds, most of
  it the run of 10,000 rounds.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 10: Script for Review".

    python e10_numbers.py                                  # from this folder
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
