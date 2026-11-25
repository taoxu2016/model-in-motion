# Handoff: from claude.ai to Claude Code

This project was built in a claude.ai Project, "Statistical Model Visual Learning Framework", across several chats:
the blueprint, the first three episodes, the animatics of the other sixteen, and the consolidation into this
repository on 25 November 2026. From here on the repository is the single source of truth and the work continues in
Claude Code. This page is what a new session, or a new person, needs to pick it up.

## Where things stand

As recorded in `docs/STATUS.md` on 25 November 2026:

| Episodes | Stage | What exists |
| --- | --- | --- |
| 1–3 | Finished | Scenes, voice, reference timings; 1080p60 videos in `renders/finished/` |
| 4 | Animatic; script approved as written | Numbers file (37 checks), voice, one board per clip; the animation is still to come |
| 5–19 | Animatic; script in draft | Numbers files, voice and boards; 86 choices open in `docs/DECISIONS.md` |

The plan is to finish the arc episode by episode, in order, through Episode 19. The blueprint
(`docs/blueprints/logistic_fixed_effect_blueprint.md`) plans all nineteen modules; the scripts that computed its numbers
are in `docs/blueprints/logistic_fixed_effect_analysis/`.

## What comes next, in order

1. **Set up an environment** (below), then run `tools/setup_env.sh --check`.
2. **Prove it reproduces the finished work:** `python3 tools/check_repo.py` must match Episodes 1–3 exactly. If it does
   not, find out why before building anything.
3. **Gate 5 for Episodes 1–3 is not recorded as done.** Their voice was checked through the synthesizer's phoneme
   output, not by ear. Watch them with sound (`renders/finished/`). A pronunciation fix means re-voicing a frozen
   episode and refreshing its reference timings, so decide it deliberately; if they have already been watched, record
   that in `docs/STATUS.md`.
4. **Episode 4:** watch `renders/animatics/ModelInMotion_LogisticFE_E04_OneInterceptPerProvider_ANIMATIC_720p.mp4`,
   then run `/produce-episode logistic_fe/e04_one_intercept_per_provider`.
5. **Episodes 5–19:** settle `docs/DECISIONS.md`, ideally in one sitting. For each script in turn: apply its decisions to
   `narration.json` and the numbers file, run `/revoice`, have the stats-reviewer agent check it, approve it, then run
   `/produce-episode`.
6. **Later:** fold the Cox arc into `cox_ph/`, the way this arc's first three episodes were folded in (see the README).

## Setting up an environment

A build needs Python 3.12, ManimCE, LaTeX (`standalone`, `preview`, `amsmath`), `dvisvgm`, ffmpeg with libass, Pango,
the fonts Inter, Inter Display and Lora, and the Kokoro voice files (about 350 MB). `tools/setup_env.sh` installs all of
it on Ubuntu or Debian and is safe to re-run; `--check` only reports. The finished episodes were built on Ubuntu 24.04
with Python 3.12, ffmpeg 6.1 and TeX Live 2023.

**A. GitHub Codespaces (recommended: nothing to install on your own computer).** On the repository page choose
Code → Codespaces → Create codespace on main, or a larger machine type under "New with options" if your plan allows:
renders are CPU-bound. The dev container (`.devcontainer/devcontainer.json`, Ubuntu 24.04) installs the Claude Code CLI
and runs `tools/setup_env.sh` on first start; allow 10–20 minutes for it. Then run `claude` in the terminal and log in.
Videos and review sheets open from the file explorer, which the review loop relies on.

**B. Claude Code on the web (claude.ai/code).** Connect the GitHub repository and edit or add a cloud environment. Its
setup script runs after the repository is cloned and before Claude starts, and its result is cached. Use:

    for d in "$PWD" "$HOME"/* /workspace/* /home/*/*; do [ -f "$d/tools/setup_env.sh" ] && cd "$d" && break; done
    bash tools/setup_env.sh

The default Trusted network level reaches package registries. If the font or voice downloads from GitHub fail, set the
environment's network access to Custom, keep the default list, and add `github.com`, `objects.githubusercontent.com`,
`release-assets.githubusercontent.com` and `raw.githubusercontent.com`. Cloud sessions suit scripts, numbers files and
scene code; their changes come back as branches, so watching a render means committing it or opening the branch in a
Codespace.

**C. Your own computer.** Install Claude Code, then run `tools/setup_env.sh` on Ubuntu or Debian. On macOS, install the
same pieces with Homebrew (ffmpeg, cairo, pango, pkg-config, a TeX distribution with `standalone` and `preview`,
`dvisvgm`, the three fonts), then `pip install -r requirements.txt`, and fetch the voice files as `tools/setup_env.sh`
does.

Claude Code's documentation is at code.claude.com/docs: see "Extend Claude Code" for CLAUDE.md, skills, agents and hooks,
"Cloud environments" for option B, and "Development containers" for option A.

## Working with Claude Code here

- Start sessions at the repository root, so that `CLAUDE.md` and `.claude/` load.
- Ask for a plan before large changes (a new episode's scenes, a change to `mim/`). Keep to one episode per session
  where you can: render logs and review sheets fill a session's context quickly.
- Openings that work:
  - "Read docs/STATUS.md and docs/DECISIONS.md and tell me what is waiting on me."
  - "/produce-episode logistic_fe/e04_one_intercept_per_provider"
  - "Here are my decisions for Episode 6: … Apply them to its script and numbers file, then /revoice it."
  - "Have the stats-reviewer check Episode 9's script and numbers file."
- The script reviews were Claude Docs on claude.ai, linked from `docs/STATUS.md`; they stay there as records. New reviews
  can live beside the episode as `review.md`, with their open choices copied into `docs/DECISIONS.md`.

## Files added for Claude Code

| File | Purpose |
| --- | --- |
| `CLAUDE.md` | What every session loads: layout, commands, rules, scene-code conventions, review loop, git |
| `.claude/settings.json` | Pre-approved build and test commands, `git push` always asks, the session-start hook |
| `.claude/hooks/session-start.sh` | Runs `tools/setup_env.sh --check` and reports into the session what is missing |
| `.claude/skills/produce-episode/` | `/produce-episode EP`: from approved script and animatic to finished, gate by gate |
| `.claude/skills/revoice/` | `/revoice EP`: after a script change, pronunciation, voice, listen-through |
| `.claude/skills/verify/` | The checks that must pass before a commit, scoped to what changed |
| `.claude/skills/review-frames/` | How to make and read review sheets |
| `.claude/skills/series-style/` | The series identity and the vocabulary in `mim/` |
| `.claude/agents/stats-reviewer.md` | An independent statistical check of a script and its numbers file |
| `.claude/agents/frame-reviewer.md` | An independent read of review sheets |
| `.devcontainer/devcontainer.json` | Codespaces or Dev Containers: Ubuntu 24.04, `tools/setup_env.sh`, the Claude Code CLI |
| `tools/setup_env.sh` | Installs or checks everything a build needs, on Ubuntu or Debian |

## What the first three episodes taught

- Write for the ear: digits in `text`, spoken forms in `say`; short sentences; one idea per clip.
- Kokoro misreads some words. Respell them in `pronunciations` ("readmitted" became "re-admitted") after checking the
  phonemes, then ask a person to listen.
- A voice job can die with its parent shell. `make_voiceover.py` caches every sentence, so re-running it resumes.
- A cue phrase must match the spoken form; `[cue not found]` in a render log means a beat fell back to its sentence start.
- `set_opacity` spoils hollow chips. Dim them with an ink veil instead (`column_veil`, `BigTray.veil`).
- `Indicate` recolours what it touches; on a group of several colours, use a scale pulse instead.
- Most fixes after a review sheet were spacing: labels touching a ruler's end, a column too close to the next.
- Preview at 480p15 and read a sheet of every clip before any 1080p60 render.
- GitHub's browser uploader stops at 25 MB per file; push renders with git.

## Outside this repository

- The script reviews (Claude Docs on claude.ai), and the chats and project memory on claude.ai. Anything decided there
  that is not in `docs/STATUS.md` or `docs/DECISIONS.md` is invisible to Claude Code: copy it here if it matters.
- The voice model files and the fonts: `tools/setup_env.sh` downloads them.
- The Cox arc's first three episodes, built in another workspace (see the README).
