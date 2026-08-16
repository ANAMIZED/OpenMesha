#!/usr/bin/env bash
# Publish the full single-file OpenMesha web control plane to GitHub (requires: gh auth login).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILE="${1:-$ROOT/web/openmesha.html}"
test -f "$FILE" || { echo "missing $FILE — pass the path to the production HTML"; exit 1; }
SIZE=$(wc -c < "$FILE" | tr -d ' ')
echo "Publishing $FILE ($SIZE bytes) -> web/openmesha.html"
CONTENT_B64=$(base64 -w0 < "$FILE" 2>/dev/null || base64 < "$FILE" | tr -d '\n')
SHA=$(gh api repos/ANAMIZED/openmesha/contents/web/openmesha.html --jq .sha 2>/dev/null || true)
ARGS=(--method PUT repos/ANAMIZED/openmesha/contents/web/openmesha.html
  -f message="feat: full OpenMesha web control plane (${SIZE} bytes)"
  -f content="$CONTENT_B64"
  -f branch=main)
if [[ -n "${SHA:-}" ]]; then ARGS+=(-f sha="$SHA"); fi
gh api "${ARGS[@]}"
echo "Done."
echo "Open: https://github.com/ANAMIZED/openmesha/blob/main/web/openmesha.html"
echo "Or:   python -m http.server 8088 --directory web"
