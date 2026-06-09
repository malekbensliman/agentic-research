#!/usr/bin/env bash
# Real-time preview: re-render slides/MASTER.md -> CBS-themed reveal.js on every
# save, served with live-reload so the browser refreshes automatically.
# Needs: pandoc, python3, and node/npx (browser-sync is fetched on first run).
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p build

render() {
  local tmp; tmp="$(mktemp -t deck).md"
  python3 scripts/prep_notes.py slides/MASTER.md > "$tmp"
  pandoc "$tmp" -f markdown -t revealjs -s -o build/MASTER.html \
    --slide-level=3 --resource-path=slides -V revealjs-url=https://cdn.jsdelivr.net/npm/reveal.js@4 \
    -V theme=white -V transition=none -V hash=true \
    --include-in-header=scripts/cbs-theme.html \
    && echo "rendered $(date +%T)" || echo "render error (fix and save again)"
  rm -f "$tmp"
}

render
echo "starting live server (first run fetches browser-sync)…"
npx --yes browser-sync start --server build --startPath MASTER.html \
  --files "build/MASTER.html" --no-notify &
BS=$!
trap 'kill "$BS" 2>/dev/null' EXIT INT TERM

echo "Editing slides/MASTER.md now auto-refreshes the browser. Ctrl-C to stop."
sig() { stat -f %m slides/MASTER.md scripts/cbs-theme.html 2>/dev/null | tr '\n' ' '; }
last="$(sig)"
while true; do
  sleep 1
  cur="$(sig)"
  [ "$cur" != "$last" ] && { last="$cur"; render; }
done
