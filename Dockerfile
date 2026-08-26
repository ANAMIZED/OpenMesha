# Glama inspects MCP over stdio. Do not start openmesha-api here.
# Admin generator: build ["pip install --no-cache-dir ."]
#                  CMD   ["python", "-m", "openmesha.mcp.server"]
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    OM_DATA_DIR=/app/data \
    OM_LLM_MODE=mock

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir . \
    && mkdir -p /app/data \
    && useradd --create-home --uid 10001 --shell /usr/sbin/nologin mcp \
    && chown -R mcp:mcp /app

USER mcp

CMD ["python", "-m", "openmesha.mcp.server"]
