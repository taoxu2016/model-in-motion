---
name: revoice
description: Re-voice an episode after its script (narration.json) changes, check pronunciation, and prepare a listen-through for the owner.
argument-hint: <episode folder>
disable-model-invocation: true
---

# Re-voice the episode in $ARGUMENTS

1. **Frozen?** If `$ARGUMENTS/reference/timings/` exists, the episode is finished. Stop unless the owner asked for this
   change explicitly; re-voicing it also means re-rendering it and replacing its reference timings.
2. **Script.** `narration/narration.json` parses; every clip has `id`, `visual` and `sentences`; numbers in `text` are
   digits with a spoken form in `say`; the voice block is unchanged (Kokoro `af_heart`, speed 0.92, 0.32 s pauses).
3. **Numbers.** If a figure changed, run the numbers file first; every number in the script must match its JSON.
4. **Pronunciation.** Print the phonemes of every new technical word or name:
   `python3 -c "import os; from kokoro_onnx import Kokoro; m=os.environ.get('KOKORO_MODELS', os.path.expanduser('~/tts_models')); k=Kokoro(m+'/kokoro-v1.0.onnx', m+'/voices-v1.0.bin'); print(k.tokenizer.phonemize('readmitted', 'en-us'))"`
   Respell a word in `pronunciations` when its stress or sound is wrong.
5. **Voice.** `python3 tools/make_voiceover.py $ARGUMENTS` (unchanged sentences come from `audio/cache/`). If it
   stops early, run it again: it resumes. Compare words per minute with the series pace of about 150–160.
6. **Listen-through.** `python3 tools/listen_through.py $ARGUMENTS`, then give the owner the `.m4a` and the timed script
   in `$ARGUMENTS/build/listen/`. You cannot hear it: ask the owner to listen before anything is animated.
7. **Scenes.** If the episode has animation, re-render the scenes whose clips changed length and fix any cue that moved.
8. **Commit** the script and `audio/` together.
