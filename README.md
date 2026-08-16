# OpenMesha (OM) — Agentic Operating System

**Open Agentic Operations Mesh**

Unified agentic operating system featuring:
- Spectral mission control
- Voice copilot
- Live LLM council
- Agent economy (x402, metered tools, outcome fees)
- Quantum solvers (QAOA / VQE)
- Agentic security (AgentFence, OWASP Agentic Top-10)
- Recursive self-improvement & Kernel Forge
- PQC migration OS & supply-chain hardening

## Quick start

1. Open `index.html` directly in a modern browser, **or**
2. Serve it statically:
   ```bash
   python -m http.server 8080
   # then visit http://localhost:8080
   ```

The application is a single self-contained HTML file. Runtime modules load from esm.sh (React, Recharts, Lucide). After the first load they are cached.

Offline / simulation mode works fully once the UI modules have been fetched once.

## Architecture notes

- In-browser kernel with real algorithms (Thompson sampling, force-directed memory graph, (1+1)-ES self-improvement, QAOA, etc.)
- Every backend seam is marked `// WIRE:` for live control-plane integration
- Human-on-the-Loop (HOTL) gates for money-moving / irreversible actions
- Kill switch, two-layer AgentFence, append-only knowledge, outcome-fee verification

## Repository contents

| File | Description |
|------|-------------|
| `index.html` | Full production OpenMesha application |
| `README.md` | This file |

## License

Open source — use and extend freely.
