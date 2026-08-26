# Glama admin — OpenMesha

Glama generates FROM debian:trixie-slim. It does not use the repo Dockerfile.

## Form values

1. Sync Server. Pinned SHA empty.
2. Base image: debian:trixie-slim
3. Python version: 3.12 (do not leave unused)
4. Build steps:

```json
["apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-venv && python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir ."]
```

5. CMD arguments:

```json
["/opt/venv/bin/python", "-m", "openmesha.mcp"]
```

Fallback CMD:

```json
["sh", "scripts/glama-stdio.sh"]
```

6. Env schema: `{"type":"object","properties":{},"required":[]}`
7. Placeholders: `{}`

Do not CMD openmesha-api.
