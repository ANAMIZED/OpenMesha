# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Report responsibly via a private GitHub security advisory.

Include description, reproduction steps, and impact (AgentFence bypass, HOTL bypass, secret leakage, supply-chain / skill injection).

## Security model

- Two-layer AgentFence (ingest scan + act gate)
- Human-on-the-Loop for irreversible / money-moving actions
- Kill switch at Control Tower
- Append-only knowledge; outcome fees only on kernel-verified criteria
- Default path is offline simulation (no secrets required in the browser)
- Control-plane credentials never live in the page (observe-only WIRE panel)
