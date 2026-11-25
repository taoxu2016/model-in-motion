# Model in Motion · The Logistic Fixed-Effect Model · Episode 14: Three Shortcuts

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M14 (Extended): three approximations to Episode 13's exact test. The score test lays a bell curve over
the pile; the Wald test measures the gap between sliders in standard errors; the bootstrap rebuilds the pile by
simulation. All three agree with the exact verdict on Alder, and each has a place where it fails.

| File | What it is |
|---|---|
| `e14_numbers.py` | Every number the episode shows or says, computed and checked (26 checks). Writes `e14_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode14.py` | Nine scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- The script uses working names, "bell curve", "ruler" and "flipping", and says each formal name once: score test,
  Wald test, bootstrap. It is the first decision in the script doc.
- `mim/piles.py` now holds the histogram helper (`Hist`), with a bell-curve overlay added. Episode 13 imports it too;
  two of its scenes were re-rendered to confirm identical timings.
- `mim/crowd.py` gained `case_mix_se`, the standard error at the average case mix for a fitted crowd.
- The flipping figure, 3.8%, comes from the series seed (2026); pprof_py's own bootstrap gives 3.9%. The narration
  says "this run".
- The calibration reuses Episode 13's fifty level crowds (10,000 tests). Among the 2,770 providers under 50 patients
  it flags 4.7% (exact), 4.9% (score) and 4.0% (Wald). The blueprint's larger run gives 4.6%, 4.7% and 4.0%.
- pprof_py 0.7.0 returns the same z, p and intervals for the score and Wald tests as the direct calculations.
- `e14_numbers.py` reads the numbers files of Episodes 9, 10, 11 and 13. It runs in about five seconds.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 14: Script for Review".

    python e14_numbers.py                                  # from this folder
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
