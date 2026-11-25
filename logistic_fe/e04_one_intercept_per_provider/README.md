# Model in Motion · The Logistic Fixed-Effect Model · Episode 4: One Intercept per Provider

**Status: script approved; animatic pass built. The boards are in place, most of the motion is still to come.**

Blueprint module M4: every clinic gets its own intercept γ, and all clinics share one step β per risk factor.

| File | What it is |
|---|---|
| `e04_numbers.py` | Every number the episode shows or says, computed and checked (37 checks). Writes `e04_numbers.json`. |
| `narration/narration.json` | The approved script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `episode/episode04.py` | Ten scenes, one board per narration clip (animatic pass), on `mim/common.py`, `mim/kit.py` and `mim/lines.py`. |
| `preview_stills.py`, `stills/` | Three key frames sketched from `e04_numbers.json` (matplotlib, review only). |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 4: Script for Review".
The script was approved as written there; `narration/narration.json` carries the same text plus spoken forms of the numbers.

    python e04_numbers.py                                  # from this folder: prints the ledger, exits 1 if a check fails
    python ../../tools/make_voiceover.py .                 # draft voiceover
    python ../../tools/listen_through.py .                 # one audio file and a timestamped script, for a listen

    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: a look at the animatic, animation, a watch-through with sound.

For the animation pass: `episode/episode04.py` still defines its own copies of eight helpers that `mim/boards.py` now
provides (`side`, `big`, `fit_width`, `controls`, `value_tag`, `dim_bracket`, `tick_mark`, `clear`; its `start_ring` is
`ring_at` there). Import them from `mim.boards` instead. The voice also shares the open “readmissions” pronunciation
question in `docs/DECISIONS.md`.
