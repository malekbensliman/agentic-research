#!/usr/bin/env bash
# Render the workshop master deck (markdown) into a CBS-branded .pptx via Pandoc.
# Usage: scripts/build.sh [output.pptx]   (default: build/MASTER.pptx)
set -euo pipefail
cd "$(dirname "$0")/.."

SRC="slides/MASTER.md"
REF="templates/cbs-template.pptx"
OUT="${1:-build/MASTER.pptx}"

[ -f "$SRC" ] || { echo "missing $SRC"; exit 1; }
[ -f "$REF" ] || { echo "missing reference template $REF"; exit 1; }
mkdir -p "$(dirname "$OUT")"

TMP="$(mktemp -t deck).md"
trap 'rm -f "$TMP"' EXIT
python3 scripts/prep_notes.py "$SRC" > "$TMP"

pandoc "$TMP" -f markdown -o "$OUT" --slide-level=3 --reference-doc="$REF"
echo "Rendered -> $OUT"
