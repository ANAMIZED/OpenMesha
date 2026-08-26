#!/bin/sh
set -eu
cd "${APP_DIR:-/app}"
export PYTHONUNBUFFERED=1 OM_LLM_MODE="${OM_LLM_MODE:-mock}"
MODULE="${MCP_MODULE:-openmesha.mcp.server}"
if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi
if ! "$PY" -c "import ${MODULE%%.*}" 2>/dev/null; then
  "$PY" -m pip install --break-system-packages --no-cache-dir . \
    || "$PY" -m pip install --no-cache-dir .
fi
exec "$PY" -m "$MODULE"
