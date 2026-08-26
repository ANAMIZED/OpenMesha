#!/bin/sh
# Glama wraps: mcp-proxy -- sh scripts/glama-stdio.sh
# Generated image is debian:trixie-slim (PEP 668). Prefer a venv.
set -eu
cd "${APP_DIR:-/app}"
export PYTHONUNBUFFERED=1
export OM_LLM_MODE="${OM_LLM_MODE:-mock}"
export OM_DATA_DIR="${OM_DATA_DIR:-/app/data}"
mkdir -p "$OM_DATA_DIR" || true

if [ -x /opt/venv/bin/python ]; then
  exec /opt/venv/bin/python -m openmesha.mcp
fi

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python

if "$PY" -c "import openmesha.mcp.server" 2>/dev/null; then
  exec "$PY" -m openmesha.mcp
fi

VENV="${OM_VENV:-/tmp/openmesha-venv}"
if [ ! -x "$VENV/bin/python" ]; then
  "$PY" -m venv "$VENV"
  "$VENV/bin/pip" install --no-cache-dir .
fi
exec "$VENV/bin/python" -m openmesha.mcp
