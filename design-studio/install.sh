#!/usr/bin/env bash
# Install Liniya Sporta Design Studio skills and subagents for local Codex.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SRC="$ROOT/.agents/skills"
AGENTS_SRC="$ROOT/.codex/agents"
SKILLS_DST="$HOME/.agents/skills"
AGENTS_DST="$HOME/.codex/agents"
mkdir -p "$SKILLS_DST" "$AGENTS_DST"

for source in "$SKILLS_SRC"/ls-*; do
  [ -d "$source" ] || continue
  name="$(basename "$source")"
  dest="$SKILLS_DST/$name"
  if [ -e "$dest" ]; then
    echo "Already installed; keeping existing skill: $dest"
  else
    cp -R "$source" "$dest"
    echo "Installed skill: $name"
  fi
done

for source in "$AGENTS_SRC"/ls_*.toml; do
  [ -f "$source" ] || continue
  name="$(basename "$source")"
  dest="$AGENTS_DST/$name"
  if [ -e "$dest" ]; then
    echo "Already installed; keeping existing agent: $dest"
  else
    cp "$source" "$dest"
    echo "Installed subagent: $name"
  fi
done

echo 'Restart Codex and verify /skills. ChatGPT web plugin installation is separate.'
