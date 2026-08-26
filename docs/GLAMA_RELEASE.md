# Glama release — OpenMesha

Quality scoring requires a Glama container that speaks MCP over stdio.

## Repo surface

| Field | Value |
| --- | --- |
| CMD | `openmesha-mcp` |
| Transport | MCP stdio |
| Secrets required to list tools | none |
| LLM | `OM_LLM_MODE=mock` |

## Admin UI

1. Sync https://glama.ai/mcp/servers/ANAMIZED/OpenMesha
2. Dockerfile admin: build steps `["pip install --no-cache-dir -e ."]`
3. CMD arguments: `["openmesha-mcp"]`
4. Deploy → Make Release.
