# AGENTS.md — OpenMesha (OM)

This file is the contract for any AI coding agent working on this repository.

## What this project is

OpenMesha is an Open Agentic Operations Mesh — a unified agentic operating system delivered as a self-contained single-file web control plane (spectral mission control, voice copilot, live LLM council, agent economy, quantum solvers, AgentFence security, PQC migration OS, and x402 commerce).

A senior engineer with only the source and `README.md` must be able to open the app, exercise every major surface, and understand every WIRE seam.

## How to run & verify

```bash
# Local (zero install after first module cache)
python -m http.server 8088 --directory web
# open http://127.0.0.1:8088/openmesha.html

# Or Chrome → File → Open File… → web/openmesha.html
```

Acceptance: app boots past the mesh spinner, Overview renders, ambient economy ticks, and the in-browser kernel runs real algorithms (no external control plane required for offline simulation).

## Hard rules for agents

1. Never weaken HOTL, kill switch, AgentFence (two-layer), append-only knowledge, or outcome-fee verification.
2. Fail closed. Money-moving / irreversible actions escalate to human approval.
3. Every backend integration is marked `// WIRE:` — do not pretend live settlement when offline.
4. Sim receipts stay marked `sim:true`. Outcome fees only settle where the kernel verifiably controls the result.
5. Prefer small, focused changes. Update README.md and AGENTS.md when public surfaces change.
6. Do not introduce ambient authority or silent network side-effects on the default offline path.

## Surfaces that must stay working

- Single-file web control plane (`web/openmesha.html`)
- In-browser kernel (router, memory, council, security, commerce, quantum, forge)
- Voice console, command palette, Knowledge Galaxy / Palimpsest projection
- Publish script: `scripts/publish-web.sh`
