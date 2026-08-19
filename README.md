# OpenMesha (OM)

[![CI](https://github.com/ANAMIZED/OpenMesha/actions/workflows/ci.yml/badge.svg)](https://github.com/ANAMIZED/OpenMesha/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-server-purple.svg)](src/openmesha/mcp/)
[![SDK](https://img.shields.io/badge/SDK-Python-green.svg)](src/openmesha/sdk/)
[![CLI](https://img.shields.io/badge/CLI-openmesha-orange.svg)](src/openmesha/cli.py)
[![API](https://img.shields.io/badge/API-FastAPI-009688.svg)](src/openmesha/api/)
[![x402](https://img.shields.io/badge/x402-commerce-green.svg)](src/openmesha/payments/)

**“Autonomous Local Economic System”**

## 🚀 Live Demo

[![Live Demo](https://img.shields.io/badge/%F0%9F%9A%80%20Live%20Demo-OpenMesha%20Briefing-blue?style=for-the-badge)](https://anamized.github.io/OpenMesha/OpenMesha-Briefing-SingleFile.html)

**Interactive 14-chapter systems briefing** (fully self-contained single file) — kernel, agents, economy, security, quantum, x402, HOTL, and more.

→ [Open the live interactive demo](https://anamized.github.io/OpenMesha/OpenMesha-Briefing-SingleFile.html)

---

OpenMesha is a production-oriented agentic operating system: Super kernel (Thompson router, bitemporal memory, QAOA/VQE, AgentFence, x402, HOTL, PQC) delivered as a self-contained web control plane, plus a Python control plane with OS-like primitives — agents as processes, budgets, multi-agent workflows, MCP, SDK, and CLI.

A senior engineer who has never seen this repository can, using **only** the source and this `README.md`:

1. Deploy the entire system (single command)
2. Exercise every major feature
3. Verify end-to-end correctness via automated checks

**[Support Agentic OS Kernels ($99)](https://buy.stripe.com/bJecN63wObPv6Bf7Zm43S02)** · **[Agentic OS Cycle ($0.75)](https://buy.stripe.com/3cI14o8R8dXD3p3frO43S04)** · **[Public Goods Support](https://donate.stripe.com/00w5kE3wOg5L8Jn2F243S00)**

### Non-custodial USDC (preferred for agents)

| Network | Address | Explorer |
|---------|---------|----------|
| **Base** | `0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438` | [basescan](https://basescan.org/address/0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438) |
| **Ethereum** | `0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438` | [etherscan](https://etherscan.io/address/0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438) |
| **Solana** | `ETQwWf19axArsY493UfC6bxe2BmEzmzvCb58PPnC38A` | [solscan](https://solscan.io/account/ETQwWf19axArsY493UfC6bxe2BmEzmzvCb58PPnC38A) |

*Related:* [rui](https://github.com/ANAMIZED/rui) · [server-os](https://github.com/ANAMIZED/server-os) · [LRSI](https://github.com/ANAMIZED/LRSI) · [OpenGOS](https://github.com/ANAMIZED/OpenGOS)

## Surfaces

| Surface | Entry |
|---------|-------|
| **Live Demo (GitHub Pages)** | [OpenMesha-Briefing-SingleFile.html](https://anamized.github.io/OpenMesha/OpenMesha-Briefing-SingleFile.html) |
| **Web control plane** | [`web/openmesha.html`](web/openmesha.html) |
| REST API | `openmesha-api` / `python -c "from openmesha.main import run; run()"` |
| CLI | `openmesha status` / `openmesha agents ...` / `openmesha workflow` |
| MCP Server | `openmesha-mcp` |
| SDK | `from openmesha.sdk import OpenMeshaClient` |
| Multi-agent workflows | `POST /v1/workflows` · MCP · CLI · `skills/multi-agent-workflow/` |
| Skills | `skills/*/SKILL.md` |
| CI | `.github/workflows/ci.yml` |
| AGENTS.md | Coding-agent contract at repo root |
| **WIRE production path** | [`docs/WIRE.md`](docs/WIRE.md) — full cloud/self-hosted path: architecture, om-ctl API, stack, Foundry economics, settlement, P0–P4 checklists |

## Quick Start

```bash
docker compose up --build
bash scripts/verify.sh
```

- API: http://localhost:8080
- OpenAPI: http://localhost:8080/docs

## Design principles

1. Least privilege by construction
2. Cost is a first-class resource
3. Fail closed (AgentFence + HOTL)
4. Honest offline simulation
5. Deployable with zero tribal knowledge

## License

Apache-2.0
