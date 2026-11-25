> **In this repository:** the shared code is in `mim/` and `tools/` at the repository root, not inside this folder.
> Build with `tools/build.sh` (see the root README). The file paths below describe the original standalone bundle.

# Model in Motion · The Logistic Fixed-Effect Model · Episode 2: Odds and the S-Curve

*How risk factors become a probability.* This is module M2 of the logistic fixed-effect blueprint, in the same series identity and pipeline as Episode 1.

| | |
|---|---|
| Running time | 5:00 |
| Picture | 1920 × 1080, 60 fps, H.264 |
| Narration | 723 words, 4:35 of speech, about 158 words per minute |
| Voice | Kokoro neural TTS (offline), voice `af_heart`, speed 0.92: the series narrator |
| Captions | 73 cues: burned in, as a soft track, and as `.srt` / `.vtt` files |

## Files

| File | What it is |
|---|---|
| `ModelInMotion_LogisticFE_E02_OddsAndTheSCurve.mp4` | The finished episode: picture, narration, burned-in captions |
| `..._softsubs.mp4` | The same picture and narration with captions as a switchable track |
| `..._narration.wav` | The mastered narration on its own (48 kHz) |
| `....en.srt`, `....en.vtt`, `....en.ass` | Captions; the `.ass` carries the series caption style |
| `..._script.md` | The narration script with a timestamp on every sentence |
| `source/` | Script, Manim code, tools and per-segment audio |

## The story in nine scenes

| # | Scene | Starts | What the viewer sees |
|---|---|---|---|
| 1 | ColdOpen | 0:00 | Last episode's patient starts at 20% on a probability ruler. Adding points for three risk factors (+25, +30, +35) pushes the chip past the end, to 110%. |
| 2 | Title | 0:33 | Series logo, arc and episode title. |
| 3 | Odds | 0:42 | Ten chips: 2 of 10 is a probability of 20%; 2 against 8 is odds of 0.25. On linked rulers the odds run to 9, 99, 999 as the probability nears 100%. |
| 4 | LogOdds | 1:17 | The odds ruler is lopsided: everyone below 50% sits between 0 and 1. A logarithm spaces 1/4, 1/2, 1, 2, 4 evenly. One patient is tracked on all three rulers. |
| 5 | Steps | 1:54 | One step of +1.39 in log-odds (odds x 4) for four patients: 5%, 20%, 50%, 80% become 17%, 50%, 80%, 94%. |
| 6 | Curve | 2:27 | Equal steps per earlier hospital stay make a straight line in log-odds and an S in probability. Its steepness follows p(1 - p). A beta dial steepens it; a shift slides it sideways. |
| 7 | Cedar | 3:16 | A logistic model fitted by hand: odds 0.25 and 1.5, odds ratio 6, so gamma = -1.39 and beta = 1.79. The risk itself only triples. |
| 8 | RiskChip | 4:00 | The cold-open patient again, with the three factors stacked in log-odds: 94%, not 110%. Chips gain a shaded slice equal to their probability. |
| 9 | Recap | 4:26 | Three recap cards; Cedar's twenty slices pour into a bar of 8.0 expected readmissions, set beside the 8 observed; the end card names episode 3. |

## Design decisions

- **Three rulers before any curve.** Probability, odds and log-odds are drawn as rulers with one patient tracked on all of them, so the logit is seen as a change of ruler before it is named.
- **The wrong method first.** Adding percentage points runs off the end of the probability ruler. The same three factors return in scene 8 on the log-odds ruler and land at 94%.
- **Beta is yellow.** Every step in log-odds, the slope triangle and the dial use the series accent colour, as the blueprint reserves it for beta and what it drives.
- **Four formulas only, each after its picture:** the odds as a ratio of chips, steepness ∝ p(1 − p), β = 1.79 and γ = −1.39 for Cedar, and log-odds = γ + β · (higher risk).
- **The risk chip is introduced as vocabulary.** From here on a chip's shaded slice is its probability; the recap already uses it to add Cedar's slices into an expected count.
- **Room for captions.** All content stays above y = −3.0 in Manim units.

## Where it departs from the blueprint

- The hook is "adding points overshoots 100%" rather than a straight line fitted to 0/1 outcomes. It makes the same point and continues Episode 1's closing image of a patient with several risk factors.
- The S-curve is drawn against a counted risk factor, earlier hospital stays, so that the slope has a plain meaning: one more stay, one more step.
- The cliffhanger points to M3, observed versus expected, by adding up Cedar's slices; the "one clinic's curve, what about five?" question is left for M4.

## Numbers, and which are illustrative

| Quantity | Value |
|---|---|
| 20%, 50%, 80% as odds and as log-odds | 0.25, 1, 4 and −1.39, 0, +1.39 |
| Odds at 90%, 99%, 99.9% | 9, 99, 999 |
| A step of ln 4 = 1.386 from 5%, 20%, 50%, 80% | 17.4%, 50%, 80%, 94.1% |
| Steepness of the S-curve in log-odds | p(1 − p), at most 0.25 at p = 0.5 |
| Cedar (the blueprint's cast): rates, odds, odds ratio | 2/10 = 20% and 6/10 = 60%; 0.25 and 1.5; 6 |
| Cedar's model | γ = ln 0.25 = −1.386, β = ln 6 = 1.792; risk ratio 3 |
| Cedar's expected count | 10 × 0.20 + 10 × 0.60 = 8.0, against 8 observed |
| The patient: baseline and each factor alone (illustrative) | 20%; 45%, 50%, 55% |
| The patient: steps in log-odds, and combined | 1.186, 1.386, 1.587; odds 0.25 × 64 = 16, so 16/17 = 94.1% (45%, 76.6%, 94.1% along the way) |
| Hospital-stays curve (illustrative) | log-odds = −2.8 + 0.7 × stays: 5.7% at 0 stays, 50% at 4, 94.3% at 8 |

The patient's three factors and the hospital-stays curve are invented for illustration. The factors were chosen so that each one alone moves a 20% patient exactly as far as the "points" claimed, which isolates the error: it lies in how the factors combine, not in any single one.

## How it is built

The pipeline is Episode 1's, unchanged: `narration/narration.json` → `tts/make_voiceover.py` → `episode/episode02.py` (nine Manim scenes that cut themselves to the narration and log when each clip starts) → `tools/assemble.py` (concat, master audio from the logged times, captions, soft-subtitle mux, burned-in encode). `episode/common.py` is shared with Episode 1; this episode adds a `Ruler` class, the risk chip and the step arrow in `episode02.py`.

```
python tts/make_voiceover.py
for s in S01_ColdOpen S02_Title S03_Odds S04_LogOdds S05_Steps S06_Curve S07_Cedar S08_RiskChip S09_Recap; do
  manim -qh --disable_caching --media_dir build/media episode/episode02.py $s
done
python tools/assemble.py --quality 1080p60
```

## What was checked, and what was not

- Every scene was rendered at preview quality, reviewed in frames taken at every narration segment, corrected, and re-rendered at 1080p60; frames of the final file were reviewed again with captions on.
- The assembly asserts that no two narration clips overlap and that picture and audio have the same length.
- I cannot listen to audio. Pronunciation was not rechecked for this script beyond the "readmitted" respelling carried over from Episode 1; a listen-through is still needed, in particular for "beta", "log-odds" and the spoken decimals.
