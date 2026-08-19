# Changelog

## [Unreleased]

### Docs

- Expanded [`docs/WIRE.md`](docs/WIRE.md) into the full cloud/self-hosted production path guide: om-ctl API contract, stack seams, Foundry pipeline economics, settlement doctrine, P0–P4 exit checklists, version pins, and thin-live vs full-path configurations (aligned with WIRE Adoption Module v0.6.0).

## [0.1.0] — 2026-08-16

### Added

- Python control plane: FastAPI REST API, CLI, SDK, MCP server
- Agent processes with budgets, capabilities, AgentFence policy
- Multi-agent workflows under shared budget
- Cost ledger + audit log
- Five SKILL.md packages (agentfence, x402, multi-agent, cost, governance)
- scripts/verify.sh end-to-end contract
- Docker Compose deploy
- Web control plane publish path (scripts/publish-web.sh)
