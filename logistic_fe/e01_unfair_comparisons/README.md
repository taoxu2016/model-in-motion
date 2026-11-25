> **In this repository:** the shared code is in `mim/` and `tools/` at the repository root, not inside this folder.
> Build with `tools/build.sh` (see the root README). The file paths below describe the original standalone bundle.

# Model in Motion · The Logistic Fixed-Effect Model · Episode 1: Unfair Comparisons

*Case mix and raw rates.* This is module M1 of the logistic fixed-effect blueprint, built in the series identity the Cox episodes established.

| | |
|---|---|
| Running time | 5:52 |
| Picture | 1920 × 1080, 60 fps, H.264 |
| Narration | 878 words, 5:25 of speech, about 162 words per minute |
| Voice | Kokoro neural TTS (offline), voice `af_heart`, speed 0.92: the series narrator |
| Captions | 80 cues: burned in, as a soft track, and as `.srt` / `.vtt` files |

## Files

| File | What it is |
|---|---|
| `ModelInMotion_LogisticFE_E01_UnfairComparisons.mp4` | The finished episode: picture, narration, burned-in captions |
| `..._softsubs.mp4` | The same picture and narration with captions as a switchable track |
| `..._narration.wav` | The mastered narration on its own (48 kHz) |
| `....en.srt`, `....en.vtt`, `....en.ass` | Captions; the `.ass` carries the series caption style |
| `..._script.md` | The narration script with a timestamp on every sentence |
| `source/` | Everything needed to rebuild: script, Manim code, tools, per-sentence audio |

## The story in nine scenes

| # | Scene | Starts | What the viewer sees |
|---|---|---|---|
| 1 | ColdOpen | 0:00 | Five trays of chips, their raw readmission rates, and the league table they imply. |
| 2 | Title | 0:44 | Series logo, arc and episode title. |
| 3 | CaseMix | 1:00 | Alder and Birch up close. A ring marks each higher-risk patient; sorting the chips shows mirror-image case mixes (24 + 6 against 6 + 24). |
| 4 | LikeWithLike | 1:44 | A three-row scoreboard: Birch is lower among lower-risk patients (17% vs 33%) and higher-risk patients (54% vs 83%), yet higher overall (47% vs 43%). Simpson's paradox is named. |
| 5 | Balance | 2:28 | Each clinic becomes a beam marked 0-100%. Its two piles of chips sit at their group rates; the beam tips until the pivot reaches the balance point, which is the raw rate. |
| 6 | Trade | 3:11 | The chips trade beams. With Birch's patients Alder balances at 73% (Birch had 47%); with Alder's patients Birch balances at 24% (Alder had 43%). |
| 7 | Crowd | 3:46 | 200 simulated providers on a rank-rank plot. Raw rates barely follow true performance (0.16; 142 of 200 in the wrong fifth) but follow case mix (0.58). |
| 8 | Luck | 4:34 | The second problem. If all five clinics were identical, twelve re-deals of the outcomes still move every rate, and the small clinics furthest. |
| 9 | Recap | 5:14 | Three recap cards; the goal (the same patients at every provider); why sorting into piles cannot scale; the teaser for episode 2 and the end card. |

## Design decisions

- **Visual first, no formulas.** The episode's one piece of mathematics, a weighted average, appears as a balance beam: pile position is a group's rate, pile weight is its number of patients, and the balance point is the raw rate. No equation is shown.
- **One vocabulary, set up for the series.** A chip is one patient and is filled if the patient was readmitted. A pale ring marks a higher-risk patient. Hue is the clinic: Alder orange and Birch blue, the pair that swap places. Later modules add the probability sector and the risk axis to the same chip.
- **The wrong method first.** The league table is shown and believed before it is taken apart.
- **The blueprint's cast, unchanged.** Every on-screen number comes from the five clinics and 103 patients of the blueprint, so each can be checked by hand.
- **Hypothetical outcomes look hypothetical.** After the trade the chips turn half-filled: what would have happened to Alder's patients at Birch is not known. The scene keeps each clinic's two group rates and moves only the weights, and the narration says so.
- **A representative run of luck.** The twelve re-deals use one fixed chance, 42/103, for every patient. Their random seed was chosen so that each clinic's lowest and highest result sit close to its exact binomial 95% range; twelve draws picked blindly could have shown a misleadingly narrow or wide spread.
- **Room for captions.** All content stays above y = −3.0 in Manim units, so burned-in captions never cover it.

## Where it departs from the blueprint

- The blueprint's see-saw beat became two scenes, the balance and the trade, because the trade is where "the same patients" is first felt.
- The paradox is named (Simpson's), so viewers can look it up.
- "Shake the trays" is a stated experiment: identical clinics, the outcomes re-dealt.
- The episode runs about six minutes against the nine planned for M1; the interactive case-mix slider is left for a companion page.

## Verified numbers

| Quantity | Value |
|---|---|
| Raw rates: Alder, Birch, Cedar, Dune, Elm | 13/30 = 43%, 14/30 = 47%, 8/20 = 40%, 7/12 = 58%, 0/11 = 0% |
| Lower-risk patients: Alder, Birch | 8/24 = 33%, 1/6 = 17% |
| Higher-risk patients: Alder, Birch | 5/6 = 83%, 13/24 = 54% |
| Alder's group rates on Birch's mix (6 + 24) | (6 × 8/24 + 24 × 5/6) / 30 = 73.3% |
| Birch's group rates on Alder's mix (24 + 6) | (24 × 1/6 + 6 × 13/24) / 30 = 24.2% |
| Crowd: rank correlation of raw rate with true effect, and with case mix | 0.164 and 0.578 |
| Crowd: providers in a different fifth by raw rate than by true effect | 142 of 200 |
| Luck: common chance, and re-dealt ranges (Alder, Birch, Cedar, Dune, Elm) | 42/103 = 0.408; 23–60%, 23–57%, 15–55%, 25–67%, 9–73% |
| Luck: exact binomial 95% ranges for 30, 20, 12 and 11 patients | 23–60%, 20–60%, 17–67%, 9–73% |

The crowd is the blueprint's simulation (200 providers, 28,848 patients, seed 2026, τ = 0.3) regenerated by `tools/make_data.py`, which prints these statistics.

## How it is built

```
narration/narration.json ──► tts/make_voiceover.py ──► audio/segments/*.wav + audio/manifest.json
   (script, visual notes,        (Kokoro, one call per sentence,     (exact sentence offsets)
    pronunciation fixes)           fixed pauses)
                                                  │
tools/make_data.py ──► data/crowd.json, data/luck.json
                                                  │
episode/common.py + episode/episode01.py (9 Manim scenes) ◄──┘
   with self.nar("s5_3") as seg:                       # starts the clip, holds the scene until it ends
       seg.wait_until(seg.word(0, "so its balance point"))   # cue an animation to a phrase
        │  one mp4 per scene + build/timings/<Scene>.json (when each clip really started)
        ▼
tools/assemble.py ──► concat picture · master audio from the logged start times · loudnorm
                      · SRT/VTT/ASS from sentence offsets · soft-subtitle mux · burned-in encode
```

- **One clock for everything.** Each scene logs when every narration clip actually starts on Manim's render clock. The master audio and every caption are placed from those logs, so picture, voice and captions cannot drift, even where an animation overruns its clip.
- **Phrase-level cues.** `seg.word(k, "phrase")` estimates when a phrase is spoken from its character position in a sentence whose start and end are exact. That is accurate to a few tenths of a second, enough for visual beats.
- **Numbers read aloud.** Captions show "43%"; a `say` field gives the narrator "forty-three percent". "Readmitted" is respelled "re-admitted" for the synthesizer, which otherwise stresses the first syllable.
- **The tipping beam.** The beam, its labels and its piles form one group that is redrawn every frame as a rotated copy of its rest state; the tilt is proportional to the distance between the pivot and the true balance point, so the beam can only level where the arithmetic says it should.

## Rebuild

```
pip install manim kokoro-onnx soundfile            # plus ffmpeg, LaTeX and Pango for ManimCE
# put kokoro-v1.0.onnx and voices-v1.0.bin from github.com/thewh1teagle/kokoro-onnx/releases in ~/tts_models
python tools/make_data.py                          # crowd ranks and luck re-deals
python tts/make_voiceover.py                       # narration clips and timing manifest
for s in S01_ColdOpen S02_Title S03_CaseMix S04_LikeWithLike S05_Balance S06_Trade S07_Crowd S08_Luck S09_Recap; do
  manim -qh --disable_caching --media_dir build/media episode/episode01.py $s
done
python tools/assemble.py --quality 1080p60         # build/final/
```

Tested with ManimCE 0.22.1, Python 3.12, kokoro-onnx, and the fonts Inter, Inter Display and Lora. The 1080p60 render took about 13 minutes on one core.

## What was checked, and what was not

- Every scene was rendered at preview quality, reviewed in frames taken at every narration segment, corrected, and re-rendered at 1080p60; frames of the final file were reviewed again with captions on.
- The assembly asserts that no two narration clips overlap and that the picture and the audio have the same length.
- I cannot listen to audio. The voice is the one used for the Cox episodes; pronunciation was checked through the synthesizer's phoneme output, not by ear. A listen-through is the one review this episode still needs.
