#!/usr/bin/env bash
# Optional: if you keep gzip/base64 parts under web/parts/, this concatenates them.
# Prefer scripts/publish-web.sh for a true single-file artifact.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PARTS="$ROOT/web/parts"
OUT="$ROOT/web/openmesha.html"
if [[ ! -d "$PARTS" ]]; then
  echo "missing $PARTS"
  exit 1
fi
shopt -s nullglob
files=("$PARTS"/b64_*.txt)
if [[ ${#files[@]} -eq 0 ]]; then
  echo "no b64_*.txt parts in $PARTS — use publish-web.sh instead"
  exit 1
fi
echo "Found ${#files[@]} parts. For a true single-file HTML, run:"
echo "  bash scripts/publish-web.sh /path/to/openmesha-production-3.html"
