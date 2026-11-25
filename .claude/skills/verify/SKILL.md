---
name: verify
description: The checks that must pass before a commit in this repository, scoped to what changed. Use before every commit, and when asked to verify, test or check the repository.
---

# Verify before committing

List what will be committed (`git status --short`, `git diff --cached --name-only`, and any unstaged files you are
about to add). Run only the checks that apply. If any fails, do not commit: report it.

| What changed | Check |
| --- | --- |
| Python files | `python3 -m py_compile <files>` |
| JSON files | each parses: `python3 -m json.tool <file> > /dev/null` |
| An episode's numbers file, or the numbers in its narration | `cd EP && python3 eNN_numbers.py` exits 0, and the script's numbers match its JSON |
| `narration/narration.json` | the voice is current (check below); if not, `/revoice` first |
| An episode's scene code | every changed scene renders at 480p15 with no traceback and no `[cue not found]` |
| `mim/`, `tools/`, or anything in a finished episode (one with `reference/timings/`) | `python3 tools/check_repo.py` passes exactly; it takes several minutes, so run it in the background |
| `renders/` | every MP4 has its `.en.srt`, `.en.vtt` and `_script.md`, named like the files already there |

Is the voice current? The manifest must hold the script's clips and sentence texts:

    python3 - EP << 'PY'
    import json, sys
    from pathlib import Path
    ep = Path(sys.argv[1])
    spec = json.loads((ep / "narration/narration.json").read_text())
    man = json.loads((ep / "audio/manifest.json").read_text())
    stale = [g["id"] for sc in spec["scenes"] for g in sc["segments"]
             if [s["text"] for s in g["sentences"]] != [s["text"] for s in man.get(g["id"], {}).get("sentences", [])]]
    print("voice matches the script" if not stale else f"re-voice needed for: {stale}")
    sys.exit(1 if stale else 0)
    PY

This compares displayed text only. A change to `say` or `pronunciations` alone also needs `/revoice`.

Documentation-only changes need none of this.
