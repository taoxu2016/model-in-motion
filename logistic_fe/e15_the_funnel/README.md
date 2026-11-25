# Model in Motion · The Logistic Fixed-Effect Model · Episode 15: The Funnel

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M15 (Core), the last of Act IV: each provider's ratio plotted against its precision, with two curved
edges, 1 +- 1.96 / sqrt(precision), that mark what luck allows. Outside the funnel is the score test's flag.

| File | What it is |
|---|---|
| `e15_numbers.py` | Every number the episode shows or says, computed and checked (27 checks). Writes `e15_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode15.py` | Nine scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- The cold open is not in the blueprint. It shows the level crowd (194 identical providers and six planted 0.8 from the
  reference) as a league table and asks the viewer to pick the six. The top three and bottom three contain two of them.
  All three truly worse providers are in the top ten (ranks 1, 4, 8), which the script does not say; it is the first
  decision in the script doc.
- Two crowds are used: the level crowd (`simulate(seed=2026, tau=0.0, plant=0.8)`) for S01, S05, S06 and S07, and the
  series' usual crowd (`tau=0.3`) for S08, where 49 of the 194 ordinary providers lie outside the funnel.
- `mim/funnel.py` holds the chart. Precision is on a square-root scale so that the cast (precision 2 to 39) and the
  crowd (2 to 334) both fit; the edges are drawn from the one formula.
- The caterpillar in S07 uses exact intervals for all 200 providers, computed here by test inversion; an interval
  leaves out 1 exactly when the exact test flags the provider (14 of 200).
- pprof_py 0.7.0's `funnel_limits` returns the same limits and flags for the cast.
- `e15_numbers.py` reads Episode 13's and Episode 14's numbers files. It runs in about six seconds.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 15: Script for Review".

    python e15_numbers.py                                  # from this folder
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
