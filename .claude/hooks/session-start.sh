#!/usr/bin/env bash
# SessionStart hook: one short report, added to the session, on whether this machine can build episodes.
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
if out=$(bash tools/setup_env.sh --check 2>&1); then
  echo "Environment check passed: this machine can voice, render and assemble episodes."
else
  echo "Environment check FAILED. Missing:"
  echo "$out" | grep "^MISSING" | sed 's/^MISSING */  - /'
  echo "Run tools/setup_env.sh to install what is missing (docs/HANDOFF.md, 'Setting up an environment')."
fi
exit 0
