> **In this repository:** the shared code is in `mim/` and `tools/` at the repository root, not inside this folder.
> Build with `tools/build.sh` (see the root README). The file paths below describe the original standalone bundle.

# Model in Motion · The Logistic Fixed-Effect Model · Episode 3: Observed versus Expected

*How many readmissions should a clinic have had?* This is module M3 of the logistic fixed-effect blueprint, in the same series identity and pipeline as Episodes 1 and 2.

| | |
|---|---|
| Running time | 3:41 |
| Picture | 1920 × 1080, 60 fps, H.264 |
| Narration | 507 words, 3:21 of speech, about 151 words per minute |
| Voice | Kokoro neural TTS (offline), voice `af_heart`, speed 0.92: the series narrator |
| Captions | 48 cues: burned in, as a soft track, and as `.srt` / `.vtt` files |

## Files

| File | What it is |
|---|---|
| `ModelInMotion_LogisticFE_E03_ObservedVersusExpected.mp4` | The finished episode: picture, narration, burned-in captions |
| `..._softsubs.mp4` | The same picture and narration with captions as a switchable track |
| `..._narration.wav` | The mastered narration on its own (48 kHz) |
| `....en.srt`, `....en.vtt`, `....en.ass` | Captions; the `.ass` carries the series caption style |
| `..._script.md` | The narration script with a timestamp on every sentence |
| `source/` | Script, Manim code, tools and per-segment audio |

## The story in eight scenes

| # | Scene | Starts | What the viewer sees |
|---|---|---|---|
| 1 | ColdOpen | 0:00 | Episode 2's ending, turned into a problem: Cedar's expected 8.0 matched its observed 8 only because the probabilities came from Cedar itself. Expected, according to whom? |
| 2 | Title | 0:27 | Series logo, arc and episode title. |
| 3 | Standard | 0:34 | All 103 patients pooled and sorted by risk: 13 of 57 lower-risk (23%) and 29 of 46 higher-risk (63%) were readmitted. Those two rates are the pooled standard. |
| 4 | Meter | 1:00 | Alder twice: its outcomes, and the slices the standard gives its patients. The slices pour into a dashed bar of 9.3; the 13 readmitted chips line up on the same scale: +3.7, ratio 1.40. |
| 5 | Five | 1:31 | The same for all five clinics: ratios 1.40, 0.85, 0.93, 1.36, 0. Birch, with the higher raw rate, has the lower ratio. The expected counts add up to the 42 observed. |
| 6 | Flaw | 2:03 | Who built the standard: 24 of the pool's 57 lower-risk patients are Alder's, with 8 of its 13 readmissions. Without Alder the rate is 15%, and Alder's ratio is 1.80, not 1.40. |
| 7 | Rule | 2:31 | The risk rule is bent too: the pool's odds ratio is 5.8, but inside clinics it is 10, 10, 6 and 5.9, about 7.5 together, because Birch holds most higher-risk patients and Alder most lower-risk ones. |
| 8 | Recap | 3:05 | Three recap cards; the two things a fair standard needs; the teaser of five parallel lines for episode 4, and the end card. |

## Design decisions

- **Observed is solid, expected is dashed.** Observed counts are rows of solid chips; expected counts are dashed bars, as the series colour code prescribes. Both sit on one scale measured in patients.
- **"A sum of probabilities" is shown literally.** Each patient's slice leaves its risk chip and becomes one piece of the expected bar, so the bar's length is the sum.
- **The method is allowed to work before it is questioned.** The five ratios, the Alder–Birch reversal and the break-even total come first; the two flaws follow.
- **Both flaws get a number.** Leaving Alder out of the pool moves its ratio from 1.40 to 1.80. Comparing risk groups inside clinics gives an odds ratio of about 7.5 against the pool's 5.8.
- **The balance appears once, small.** It names the O − E motif; later episodes use it at full size, when the tilt becomes the score.
- **Room for captions.** All content stays above y = −3.0 in Manim units.

## Where it departs from the blueprint

- The hook is Episode 2's own ending (Cedar's 8.0 against 8), exposed as circular, rather than a recall of Episode 1.
- The blueprint's measuring glass on a pan became a dashed bar on a scale, with a small balance beside it; lengths on one scale compare more easily than a glass with a stack.
- Two numbers were added to make the flaws concrete: the leave-Alder-out ratio and the Mantel–Haenszel odds ratio.
- Two of the blueprint's misconceptions are not addressed on screen: "expected is not a forecast" and "a ratio of 1 means like the standard, not good". They fit Episode 4's recap or a companion page.

## Verified numbers

All are recomputed from the blueprint's cast by the check at the top of the build log.

| Quantity | Value |
|---|---|
| Pooled rates: lower-risk, higher-risk | 13/57 = 22.8%, 29/46 = 63.0% |
| Expected counts: Alder, Birch, Cedar, Dune, Elm | 9.26, 16.50, 8.59, 5.15, 2.51; total 42.0 |
| Observed minus expected | +3.74, −2.50, −0.59, +1.85, −2.51 |
| Observed over expected | 1.40, 0.85, 0.93, 1.36, 0 |
| The pool without Alder | 5/33 = 15.2% and 24/40 = 60%; Alder's expected 7.24, ratio 1.80 |
| Odds ratio, higher against lower risk: pooled | 5.77 |
| The same inside Alder, Dune, Cedar, Birch | 10, 10, 6, 5.91 |
| Within-clinic summary (Mantel–Haenszel) | 7.42; the fixed-effect fit in the blueprint gives 7.51 |

## How it is built

The pipeline is unchanged: `narration/narration.json` → `tts/make_voiceover.py` → `episode/episode03.py` (eight Manim scenes cut to the narration) → `tools/assemble.py`. `episode/common.py` is the shared series module; `episode/kit.py` holds the rulers, risk chip and step arrow introduced in Episode 2.

```
python tts/make_voiceover.py
for s in S01_ColdOpen S02_Title S03_Standard S04_Meter S05_Five S06_Flaw S07_Rule S08_Recap; do
  manim -qh --disable_caching --media_dir build/media episode/episode03.py $s
done
python tools/assemble.py --quality 1080p60
```

## What was checked, and what was not

- This episode was rendered straight to 1080p60, reviewed in frames taken at every narration segment, corrected in two scenes, and those scenes re-rendered; frames of the final file were reviewed again with captions on.
- The assembly asserts that no two narration clips overlap and that picture and audio have the same length.
- I cannot listen to audio. Pronunciation was not rechecked for this script; a listen-through is still needed.
