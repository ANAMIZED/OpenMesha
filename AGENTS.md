# AGENTS.md — OpenMesha (OM)

This file is the contract for any AI coding agent working on this repository.

## What this project is

OpenMesha is an Open Agentic Operations Mesh: a unified agentic operating system with
(1) an in-browser kernel (spectral mission control, Thompson/UCB router, bitemporal memory graph, QAOA/VQE, AgentFence, x402 metering, HOTL, PQC) delivered as a self-contained single-file web control plane, and
(2) a Python control-plane package providing REST API, CLI, SDK, MCP server, multi-agent workflows, cost control, governance, and skills.

A senior engineer with only the source and `README.md` must be able to deploy it, exercise every surface, and verify end-to-end via `scripts/verify.sh`.

## How to run & verify

```bash
# Python control plane
docker compose up --build
# another terminal
bash scripts/verify.sh

# Web control plane (after parts or publish)
python -m http.server 8088 --directory web
# open http://127.0.0.1:8088/openmesha.html
```

Unit tests: `PYTHONPATH=src pytest -q`

## Hard rules for agents

1. Never break the verify contract (`scripts/verify.sh` must stay green).
2. Fail closed — AgentFence + HOTL stay hard; never weaken kill-switch or escalation.
3. Capabilities only — no ambient authority.
4. Cost is first-class — meter before every LLM call; respect budgets.
5. Keep the mock LLM deterministic; no external network on the default/mock path.
6. Outcome fees / money-moving paths remain HOTL-gated; sim receipts stay marked `sim:true`.
7. Prefer small, focused changes. Update README.md and AGENTS.md when public surfaces change.
8. Web WIRE seams stay explicit; offline path must remain fully functional.

## Surfaces that must stay working

- REST API (`/health`, `/v1/agents`, `/v1/workflows`, `/v1/cost/ledger`, `/v1/audit`, `/metrics`)
- CLI (`openmesha status`, `openmesha agents …`, `openmesha workflow`)
- MCP Server (`openmesha-mcp` + tool registry: create_agent, run_task, create_workflow, x402_payment_quote, …)
- SDK (`from openmesha.sdk import OpenMeshaClient`)
- Skills (`skills/agentfence`, `x402-payments`, `multi-agent-workflow`, `cost-control`, `governance-hotl`)
- Multi-agent workflows (planner/researcher style under shared budget)
- Web control plane (`web/openmesha.html` + `web/parts/b64_*.txt` loader or published single file)
- `scripts/verify.sh` (15-check contract)
