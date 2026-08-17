# OpenMesha (OM)

[![CI](https://github.com/ANAMIZED/openmesha/actions/workflows/ci.yml/badge.svg)](https://github.com/ANAMIZED/openmesha/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-server-purple.svg)](src/openmesha/mcp/)
[![x402](https://img.shields.io/badge/x402-commerce-green.svg)](src/openmesha/payments/)

**Open Agentic Operations Mesh**

OpenMesha is a production-oriented agentic operating system: an in-browser kernel (Thompson router, bitemporal memory, QAOA/VQE, AgentFence, x402, HOTL, PQC) delivered as a self-contained web control plane, plus a Python control plane with OS-like primitives — agents as processes, budgets, multi-agent workflows, MCP, SDK, and CLI.

A senior engineer who has never seen this repository can, using **only** the source and this `README.md`:

1. Deploy the entire system (single command)
2. Exercise every major feature
3. Verify end-to-end correctness via automated checks

**[Support Public Goods](https://donate.stripe.com/00w5kE3wOg5L8Jn2F243S00)** · **[Support Agentic OS Kernels ($99)](https://buy.stripe.com/bJecN63wObPv6Bf7Zm43S02)**

## Quick Start (Python control plane)

```bash
docker compose up --build
# another terminal
bash scripts/verify.sh
```

- API: http://localhost:8080
- Health: http://localhost:8080/health
- OpenAPI: http://localhost:8080/docs

Default mode is **offline mock LLM** (deterministic, free).

## Quick Start (Web control plane)

```bash
python -m http.server 8088 --directory web
# open http://127.0.0.1:8088/openmesha.html
```

The loader fetches `web/parts/b64_*.txt` (gzip+base64 of the ~535 KB production build), decompresses in-browser via `DecompressionStream`, and boots the full mesh. Or publish a true single-file:

```bash
gh auth login   # once
bash scripts/publish-web.sh /path/to/openmesha-production-3.html
```

## Surfaces

| Surface | Entry |
|---------|-------|
| **Web control plane** | `web/openmesha.html` (runtime loader + parts, or published single file) |
| REST API | `openmesha-api` / `python -c "from openmesha.main import run; run()"` |
| CLI | `openmesha status` / `openmesha agents ...` / `openmesha workflow` |
| MCP Server | `openmesha-mcp` |
| SDK | `from openmesha.sdk import OpenMeshaClient` |
| Skills | `skills/*/SKILL.md` (agentfence, x402-payments, multi-agent-workflow, cost-control, governance-hotl) |
| Multi-agent workflows | `POST /v1/workflows` · MCP `create_workflow` · CLI |
| AGENTS.md | Coding-agent contract at repo root |

## Verify contract

```bash
bash scripts/verify.sh
```

Covers API, cost, governance, AgentFence, multi-agent workflows, SDK, CLI, MCP, skills, and AGENTS.md (15 checks).

## Design principles

1. Least privilege by construction (capabilities from intent)
2. Cost is a first-class resource
3. Fail closed (AgentFence + HOTL)
4. Honest offline simulation (`sim` receipts; WIRE seams explicit)
5. Deployable with zero tribal knowledge

## License

Apache-2.0
