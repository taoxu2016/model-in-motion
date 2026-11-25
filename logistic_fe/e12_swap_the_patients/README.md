# Model in Motion · The Logistic Fixed-Effect Model · Episode 12: Swap the Patients

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M12 (Extended): keep each clinic's curve and apply it to everyone's patients. The direct rate puts all
clinics on one case mix, where Episode 11's ratio judged each on its own.

| File | What it is |
|---|---|
| `e12_numbers.py` | Every number the episode shows or says, computed and checked (27 checks). Writes `e12_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode12.py` | Nine scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- The episode opens on the swap of places (Alder's ratio 1.62 against Dune's 1.46, though Dune's curve is the higher)
  and explains it before defining the direct rate. The blueprint has the definition first and the swap fourth.
- Alder's and Dune's fitted curves are only 0.07 apart on the log-odds ruler, far inside their uncertainty. The script
  takes the fitted curves as given and does not say so; it is the third decision in the script doc. On screen the two
  curves nearly coincide, so S01 adds a lens.
- Three figures go beyond the blueprint, each with a check: the multiples of the reference at each risk level, Dune's
  1.68 with Alder's patients, and Alder's 1.45 against the reference clinic's direct rate.
- The blueprint's direct ratio against the observed total (1.34 for Alder, 0.92 for Cedar) is computed and not used.
- pprof_py 0.7.0 returns the same expected counts, ratios and rates as the direct calculation.
- `e12_numbers.py` reads Episode 10's and Episode 11's numbers files; `episode12.py` reads them too, for Elm's two
  direct rates and Alder's expected count at the reference.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 12: Script for Review".

    python e12_numbers.py                                  # from this folder; a few seconds
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
