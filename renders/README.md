# Renders

`animatics/` holds the current 720p animatic of every animatic-stage episode, as delivered on 24 and 25 November 2026:
narration, captions burned in, and one still board per narration clip. Beside each video are its captions as `.en.srt`
and `.en.vtt`, and `_script.md`, the narration with a timestamp for every sentence and the on-screen note for every clip.

| Ep | File | Time | Size | SHA-256 (first 16) |
| --- | --- | --- | --- | --- |
| 4 | `ModelInMotion_LogisticFE_E04_OneInterceptPerProvider_ANIMATIC_720p.mp4` | 7:19 | 20.0 MB | `260f04a5c18168d9` |
| 5 | `ModelInMotion_LogisticFE_E05_ReadingGamma_ANIMATIC_720p.mp4` | 5:26 | 14.1 MB | `07ccf077d0fb89e5` |
| 6 | `ModelInMotion_LogisticFE_E06_FittingByBalance_ANIMATIC_720p.mp4` | 4:48 | 12.3 MB | `21bf69b185204795` |
| 7 | `ModelInMotion_LogisticFE_E07_ClimbingTheHill_ANIMATIC_720p.mp4` | 4:24 | 11.0 MB | `20759d178c399e9f` |
| 8 | `ModelInMotion_LogisticFE_E08_TheArrowMatrix_ANIMATIC_720p.mp4` | 4:53 | 12.3 MB | `bb9f150205817e52` |
| 9 | `ModelInMotion_LogisticFE_E09_HowSureAreWe_ANIMATIC_720p.mp4` | 5:08 | 11.8 MB | `b5273aa48170a8be` |
| 10 | `ModelInMotion_LogisticFE_E10_NoEventsNoPeak_ANIMATIC_720p.mp4` | 4:32 | 10.5 MB | `e670bc94643a1990` |
| 11 | `ModelInMotion_LogisticFE_E11_SwapTheCurve_ANIMATIC_720p.mp4` | 5:01 | 11.9 MB | `fb5696e568d8e900` |
| 12 | `ModelInMotion_LogisticFE_E12_SwapThePatients_ANIMATIC_720p.mp4` | 4:56 | 11.9 MB | `573648129808fbe1` |
| 13 | `ModelInMotion_LogisticFE_E13_UnequalCoins_ANIMATIC_720p.mp4` | 5:01 | 12.0 MB | `8c5ad7a1dc4f0fdb` |
| 14 | `ModelInMotion_LogisticFE_E14_ThreeShortcuts_ANIMATIC_720p.mp4` | 4:40 | 10.8 MB | `2b99b86db5d5bee8` |
| 15 | `ModelInMotion_LogisticFE_E15_TheFunnel_ANIMATIC_720p.mp4` | 4:36 | 12.1 MB | `4bed4f579336129b` |
| 16 | `ModelInMotion_LogisticFE_E16_TrustingTheRiskModel_ANIMATIC_720p.mp4` | 4:45 | 12.4 MB | `525b9aae906bb3a0` |
| 17 | `ModelInMotion_LogisticFE_E17_FixedOrRandom_ANIMATIC_720p.mp4` | 4:29 | 11.6 MB | `5d1cbecc7a8f7dfa` |
| 18 | `ModelInMotion_LogisticFE_E18_TooManyIntercepts_ANIMATIC_720p.mp4` | 3:55 | 10.9 MB | `2c6d24545cf8c351` |
| 19 | `ModelInMotion_LogisticFE_E19_WiderThanChance_ANIMATIC_720p.mp4` | 4:47 | 12.3 MB | `2b25e3cad93e651b` |

Notes:

- These are outputs, not sources. `tools/build.sh <episode folder> preview` or `tools/assemble.py <episode folder>
  --quality 720p30` rebuilds any of them from the episode folder.
- Each MP4 is the file as delivered. Delivery added a small provenance block (a C2PA `uuid` box at the start of the
  file), so a local rebuild has the same picture and sound but not the same checksum. The picture and sound streams of
  all sixteen were compared with the build output and are identical.
- A video here matches the repository at the commit that added it. After a script or scene changes, re-render and
  replace the file; consider release assets or Git LFS if the history starts to grow.
- The finished 1080p60 videos of Episodes 1 to 3 were rendered in another workspace and are not here.
  `tools/build.sh logistic_fe/<episode folder> final` rebuilds each in about 13 minutes on one core.
