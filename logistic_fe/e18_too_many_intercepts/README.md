# Model in Motion · The Logistic Fixed-Effect Model · Episode 18: Too Many Intercepts

**Status: draft script with its animatic, awaiting review. The boards are in place; most of the motion is still to come.**

Blueprint module M18 (Advanced), the third of Act V: the incidental-parameter problem. With one intercept per provider,
small providers make the shared coefficient come out too steep, by a little more than one over the provider's size.
Conditioning on each provider's total removes the bias and the intercepts with it.

| File | What it is |
|---|---|
| `e18_numbers.py` | Every number the episode shows or says, computed and checked (19 checks). Writes `e18_numbers.json`. |
| `narration/narration.json` | The draft script in the series format: scenes, clips, on-screen notes, spoken forms of numbers. |
| `audio/` | The voiceover the boards are cut to. Unchanged sentences are reused from the cache when the script changes. |
| `episode/episode18.py` | Eight scenes, one board per narration clip (animatic pass). |

Notes for whoever picks this up:
- The experiment is the blueprint's (x ~ N(0, 1), intercepts ~ N(-0.5, 1), a true coefficient of 0.5, 4,000 patients in
  equal providers of 2, 5, 10, 25 or 100), run here for 400 worlds at each size where the blueprint used 100, and with
  the conditional fit on all of them where the blueprint used 40. Seeds are `np.random.default_rng([2026, size])`.
  The figures are steadier and a few differ slightly from the blueprint's: 26%, 12%, 5%, 1% too steep against 24%, 12%,
  6%, 1%; intervals holding the truth 0%, 26%, 71%, 90%, 93% against 0%, 32%, 72%, 85%, 97%.
- The joint fit sets aside providers whose patients all share one outcome (no finite intercept, nothing to say about
  the coefficient). pprof_py holds such providers at a wall instead and returns the same coefficient to five decimals
  (checked on a world of tens with 22 such providers).
- For pairs the joint coefficient is exactly twice the conditional one in every world (0.9229 against 0.4614 on
  screen); the world on screen is the first of the 400, and its single fit of 0.92 is within the scatter (0.11) around
  the average of 1.01.
- The conditional fit is written out here (elementary symmetric polynomials by a short recursion, one-dimensional
  search); pprof_py 0.7.0 has no conditional logistic model.
- Two things learned about pprof_py 0.7.0 while checking: (1) the size screen keeps a provider only if it has MORE than
  `cutoff` patients, so the default of 10 sets aside providers of exactly ten, as Episode 10 already says; (2) when the
  screen sets aside every provider (a world of tens at the default cutoff), `fit` fails with a Cholesky error (SerBIN)
  or a zero-size-array error (BAN) and no message about the screen. Worth a clearer error upstream.
- Two checks support single sentences: 4,000 providers of five are 27% too steep, against 26% for 800 of them; and over
  fifty redraws of the series' crowd the first coefficient is 1.010 times the truth, +-0.003.
- `e18_numbers.py` runs in about ten seconds. The recap scene reads Episode 15's numbers file for its funnel.

The script is reviewed in the Claude Doc "Logistic Fixed-Effect Model · Episode 18: Script for Review".

    python e18_numbers.py                                  # from this folder
    ../../tools/build.sh . preview                         # the animatic: every scene at 480p15, assembled with sound and captions

Still to do, in order: script and animatic review, animation, a watch-through with sound.
