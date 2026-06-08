#!/usr/bin/env bash
# Live preview: render slides/MASTER.md to a CBS-themed reveal.js HTML deck and open it.
# Same markdown + preprocessing as the .pptx build — only the output skin differs.
# Note: reveal.js loads from a CDN, so this needs internet.
set -euo pipefail
cd "$(dirname "$0")/.."

SRC="slides/MASTER.md"
OUT="${1:-build/MASTER.html}"
mkdir -p "$(dirname "$OUT")"

TMP="$(mktemp -t deck).md"
trap 'rm -f "$TMP"' EXIT
python3 scripts/prep_notes.py "$SRC" > "$TMP"

pandoc "$TMP" -f markdown -t revealjs -s -o "$OUT" \
  --slide-level=3 \
  -V revealjs-url=https://cdn.jsdelivr.net/npm/reveal.js@4 \
  -V theme=white \
  -V transition=none \
  --include-in-header=scripts/cbs-theme.html

echo "Preview -> $OUT"
command -v open >/dev/null && open "$OUT" || true
