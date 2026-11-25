# Model in Motion · The Logistic Fixed-Effect Model · Episode 7: Climbing the Hill

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M7: a Newton step for one clinic is tilt over wobble, (O − E) / V; sliders can step together, the
dial steps in turn, and alternating the two blocks climbs a diagonal ridge by staircase.

| File | What it is |
|---|---|
| `e07_numbers.py` | Every number the episode shows or says, computed and checked (22 checks). Writes `e07_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode07.py` | Seven scenes, one board per narration clip (animatic pass). |

The alternating fit in `e07_numbers.py` follows pprof_py's `BanAlgorithm` line for line, and the package returns the
same 21 rounds and the same β. Round counts by coding of the risk factor: 54 as recorded (0 and 1), 3,125 five units
higher, 21 centred first (what pprof_py does). The routines stop a little short of the top (up to 0.0002 in β), which
is why the script says routes climb "toward" it.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 7: Script for Review".

    python e07_numbers.py                                  # from this folder; reads Episode 6's numbers file for the hill
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
