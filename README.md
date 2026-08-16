# OpenMesha (OM)

[![CI](https://github.com/ANAMIZED/openmesha/actions/workflows/ci.yml/badge.svg)](https://github.com/ANAMIZED/openmesha/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-ready-purple.svg)](AGENTS.md)
[![x402](https://img.shields.io/badge/x402-commerce-green.svg)](AGENTS.md)

**Open Agentic Operations Mesh**

OpenMesha is a unified agentic operating system delivered as a self-contained single-file web control plane: spectral mission control, voice copilot, live LLM council, agent economy, quantum solvers, AgentFence security, PQC migration OS, and recursive self-improvement.

A senior engineer who has never seen this repository can, using **only** the source and this `README.md`:

1. Open the control plane (zero install after first module cache)
2. Exercise every major surface offline
3. Understand every backend seam marked `// WIRE:`

No prior context, design docs, or tribal knowledge required.

## Quick Start

```bash
python -m http.server 8088 --directory web
# http://127.0.0.1:8088/openmesha.html
```

Or Chrome → **File → Open File…** → `web/openmesha.html` (after publishing the full build).

Default mode is **offline in-browser kernel** (real algorithms, simulated settlement). Point `window.OM_API` at a control plane to go live.

## Web control plane (zero install)

Single-file operator console — spectral mission control, voice, council, commerce, security, quantum, forge.

**Canonical file:** `web/openmesha.html`

### Publish the full production HTML to GitHub (one command)

```bash
gh auth login   # once
bash scripts/publish-web.sh /path/to/openmesha-production-3.html
```

### Open locally

```bash
python -m http.server 8088 --directory web
# http://127.0.0.1:8088/openmesha.html
```

| Surface | Notes |
|---------|--------|
| Kernel | Model router (Thompson / UCB1 / contextual), bitemporal memory, council, forge |
| Security | AgentFence L1/L2, OWASP Agentic Top-10, Petri fitness, kill switch |
| Commerce | x402 (Base / Solana / fiat rails), outcome fees, deposit metering |
| Quantum | QAOA MaxCut, VQE, solver routing with classical baseline honesty |
| Governance | HOTL mandates, Control Tower, policy-as-code posture |
| Learning | Palimpsest journal projection, Knowledge Galaxy |

**Acceptance (web):** open the file → spinner clears → Overview + ambient economy tick → offline simulation fully live.

## Surfaces

| Surface | Entry |
|---------|-------|
| **Web control plane** | `web/openmesha.html` (offline, self-contained) |
| AGENTS.md | Coding-agent contract at repo root |
| Publish script | `scripts/publish-web.sh` |

## Design principles

1. Fail closed (HOTL + kill switch + AgentFence)
2. Cost and outcomes are first-class (meter + verify)
3. Honest offline simulation (sim receipts marked; WIRE seams explicit)
4. Deployable with zero tribal knowledge
5. Knowledge is append-only; trust is earned, never bought

## License

Apache-2.0
