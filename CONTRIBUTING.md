# Contributing to OpenMesha

## The contract

1. Offline / simulation path must continue to boot and exercise the kernel
2. HOTL, kill switch, and AgentFence remain fail-closed
3. Outcome fees only where the kernel verifiably controls the result
4. WIRE seams stay explicitly labeled — no fake live receipts
5. Prefer small, focused changes

Read `AGENTS.md` before changing code.

## Setup

```bash
# Open the single-file control plane
python -m http.server 8088 --directory web
# http://127.0.0.1:8088/openmesha.html
```

## Publishing the full production HTML

```bash
gh auth login   # once
bash scripts/publish-web.sh /path/to/openmesha-production.html
```

## PRs

- Small, focused changes
- Describe why / what / how verified
- Update README.md or AGENTS.md when public surfaces change
