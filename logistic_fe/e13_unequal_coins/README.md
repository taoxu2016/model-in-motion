# Model in Motion · The Logistic Fixed-Effect Model · Episode 13: Unequal Coins

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M13 (Core): the exact test. If a clinic were like the reference, each of its patients would be a coin
with their own reference chance; the number of readmissions then has a distribution that can be built exactly, and its
tail beyond the observed count is the p-value. Turned inside out, the same test gives an interval.

| File | What it is |
|---|---|
| `e13_numbers.py` | Every number the episode shows or says, computed and checked (33 checks). Writes `e13_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode13.py` | Ten scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- `mim/castfit.py` gained `coin_pmf` (the coin-by-coin build) and `mid_p` (the two-sided mid-p). The numbers file and
  the scenes both use them; in S08 the pile and its p-value are rebuilt live as gamma slides.
- The flips in S03 use the series seed, 2026: the first three rounds give 3, 5 and 3, and the narration says so. A
  different seed needs a different sentence.
- The p-value is the mid-p that pprof_py 0.7.0 reports: half the bar at the observed count plus everything beyond,
  doubled. The package returns the same five p-values, the same single flag and the same intervals.
- The identical-coins scene uses Alder, where the verdict flips (3.5% becomes 5.2%). The blueprint uses Dune's
  variances, 2.29 against 2.88, which are checked here too.
- The calibration is 50 level crowds, 10,000 tests: 4.81% flagged. The blueprint ran 100 crowds and reports 4.99%.
  Its seeds are not recorded, so this file uses its own (3000, 3010, ...).
- `e13_numbers.py` reads Episode 11's numbers file for the reference and the shortcut interval. It runs in about
  five seconds.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 13: Script for Review".

    python e13_numbers.py                                  # from this folder
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
