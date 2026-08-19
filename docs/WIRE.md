# WIRE — Hardware & Full Production Path

This document specifies the **exact** hardware, topology, and phased
checklist required to run OpenMesha’s full WIRE production path
(self-hosted / local). It is derived from the in-kernel WIRE adoption
module and the phase exit criteria that flip services live.

A senior engineer with only this file and the repository source should be
able to provision the rails without tribal knowledge.

> **Scope.** This covers the control-plane + deploy + isolation rails.
> The browser Kernel (`web/openmesha.html`) runs on any modern client and
> needs no special hardware. LLM inference may remain remote (OpenRouter)
> or be brought in-house (extra GPU host).

---

## Architecture

| Component | Role | Isolation boundary |
|-----------|------|--------------------|
| **Browser** (Kernel + WIRE panel) | UI / spectral mission control | Client-only |
| **om-ctl** | Sole keyholder: pipeline, HOTL mandates, kill switches, settlement | Control plane |
| **om-mesh-1** | Coolify + LiteLLM + storefront | Main host |
| **om-sbx-1** | Sandboxd (trusted builds) | Separate VM (blast-radius split) |
| **om-mvx-1** | microsandbox / libkrun microVMs (untrusted code) | Bare metal / dedicated with `/dev/kvm` |
| **Per-tenant servers** (P4) | Sibling MAOS instances | One server per enterprise tenant |

Data flow:

```
Browser  ↔  om-ctl  →  om-mesh-1 (Coolify + LiteLLM + storefront)
                    →  om-sbx-1  (trusted builds)
                    →  om-mvx-1  (untrusted code in microVMs)
                    →  tenant-N  (enterprise siblings)
```

---

## Hardware by phase

### P0 Foundations + P1 Dogfood Storefront

Minimum viable production surface.

| Resource | Spec |
|----------|------|
| **Hosts** | 1× CX32-class (or equivalent) |
| **CPU** | 4 vCPU (shared or dedicated) |
| **RAM** | 8 GB |
| **Storage** | 80 GB SSD |
| **Network** | Public IPv4 + provider firewall |
| **DNS** | Wildcard `*.mesh.<domain>` + `*.sbx.<domain>` |

**Notes**

- The documented starting point is a Hetzner Cloud **CX32**
  (`infra/provision.sh` is designed to be portable/replayable).
- Provider firewall is the real boundary — Docker rewrites iptables and
  bypasses UFW. Expose 80/443 world-wide; restrict 22 to admin IPs.
- Coolify TLS terminates at `mesh.<domain>`; setup ports
  (8000/6001/6002) must be deleted after bootstrap.

### P2 Sandboxd Build-Agent

| Resource | Spec |
|----------|------|
| **Hosts** | +1 separate VM on `*.sbx` (blast-radius split from Coolify) |
| **Size** | Same class as om-mesh-1 or larger |
| **Network** | API firewalled to control plane only; egress default-deny |
| **Allowlist** | git, container registries, LiteLLM |

Bearer auth must be **on** (off by default upstream). Kill-switch drill:
destroy sandbox + cancel deploy + revoke key + void outcome in one action.

### P3 microVM AgentFence (full-path hard requirement)

| Resource | Spec |
|----------|------|
| **Hosts** | 1× **bare metal or dedicated** with `/dev/kvm` |
| **Virtualization** | Hardware KVM (nested virt is almost never available on cloud VMs) |
| **Runtime** | microsandbox (libkrun, Apache-2.0, MCP-native) |
| **Fallback** | E2B triggers defined if bare metal is unavailable |

**Trust router**

- `trust=operator` → Sandboxd (container tier)
- `trust=external|generated|unknown` → microVM (isolation is the floor)

Secrets never enter the guest: placeholder substitution only on verified
TLS to allowlisted hosts. No git credentials in the untrusted tier;
om-ctl extracts and pushes externally.

### P4 Enterprise WIRE

| Resource | Spec |
|----------|------|
| **Hosts** | +1 server per tenant (Foundry provisions → registers in Coolify → deploys sibling) |
| **Scale gate** | ~10 tenant servers → decide Coolify v5 vs Kubernetes + Argo |
| **Kill switches** | Per-tenant (tokens + stop) and global (MCP disable + rotate) — stopwatch-timed drills |

---

## Software stack (all MIT / Apache-2.0, self-hosted)

| Seam | Component | Notes |
|------|-----------|-------|
| Deploy + control surface | **Coolify** | Team-scoped API creates apps, servers, deployments |
| Trusted builds | **Sandboxd** | Headless build-agent; model keys live in its auth proxy, never the workspace |
| Untrusted isolation | **microsandbox** (libkrun) | Hardware microVMs; golden-image snapshot forks |
| Model router | **LiteLLM** (+ OpenRouter or local) | One bill, per-service virtual keys |
| Container runtime | Docker + pinned digests | Service ABI: Dockerfile, `/healthz`, signed `/.well-known/om-verify` |
| Fiat / enterprise rail (optional) | Stripe | Invoicing + Tax; authorize/capture outcome settlement; same ledger as x402 |
| Ops rooms (optional) | webhook-chat default; Buzz trial-gated | Rooms never hold authority or credentials |

Held: Bolt.diy — MIT source, but WebContainers requires a commercial
license for for-profit production. Sandboxd’s headless tasks replaced it.

---

## Practical local / self-hosted configurations

| Goal | What you need |
|------|----------------|
| **Browser simulation only** | Any modern laptop/browser. Zero backend. |
| **P0–P1 production** | 1× 4 vCPU / 8 GB VPS (CX32-class) + domain + wildcard DNS |
| **P0–P2 production** | 2× VPS (Coolify + Sandboxd) |
| **Full WIRE (P0–P3)** | 2× VPS + **1× bare-metal/dedicated with KVM** |
| **Full + local 70B inference** | Above + GPU host (A100/H100 class or multi-consumer GPU for vLLM) |
| **Enterprise (P4)** | Above + one additional server per tenant |

**Cheapest realistic full-WIRE path:** two modest cloud VPS + one
KVM-capable bare-metal/dedicated box.

---

## Non-hardware requirements

- Domain + wildcard DNS + TLS certificates
- Secrets vault:
  - `om-root` — sealed, never held by agents
  - `foundry-agent` — write + deploy (pipeline SOPs only)
  - `om-observer` — read-only (default for agents)
- External verify probe of `/.well-known/om-verify` — **the only thing**
  that flips a service live or settles a `foundry.deploy` outcome
  (“no green, no charge”)
- Zero credentials in the browser, workspaces, microVM guests, repos, or logs

---

## Phase exit checklists (go-live certificates)

These are the criteria that the WIRE panel and control plane treat as
phase-complete. Treat them as the acceptance tests for each stage.

### P0 — Foundations

- [ ] CX32 (or equivalent) provisioned via portable `infra/provision.sh`
- [ ] Provider firewall = boundary; 80/443 world, 22 admin-IP only
- [ ] Coolify TLS at `mesh.<domain>`; setup ports deleted
- [ ] Wildcard DNS: `*.mesh` (live) + `*.sbx` (reserved)
- [ ] Tokens in vault: om-root sealed, foundry-agent, om-observer
- [ ] MCP registered observe-only behind AgentFence
- [ ] Notifications → ops feed; clean-state snapshot + backups on

### P1 — Dogfood Storefront

- [ ] Service ABI: pinned-digest Dockerfile, `/healthz`, signed `/.well-known/om-verify`
- [ ] GitHub App source installed (previews require it)
- [ ] LiteLLM internal-only; per-service virtual keys for spend attribution
- [ ] Apps created via Coolify API (Foundry inherits the scripts)
- [ ] Bulk envs before first deploy; auto-deploy webhook verified
- [ ] External signed probe flips live — “Coolify healthy” is not verified
- [ ] Rollback drill < 5 min; deliberate failure correctly refused
- [ ] Triple feed live: x402 in ↔ LiteLLM spend ↔ host cost

### P2 — Sandboxd Build-Agent

- [ ] Separate VM on `*.sbx`
- [ ] Bearer auth ON, TLS, API firewalled to control plane
- [ ] Host egress default-deny with allowlist
- [ ] Pipeline: forge → sandbox → tasks SSE → audits green → push → Coolify deploy
- [ ] External probe verifies → settle `foundry.deploy` (no green, no charge)
- [ ] HOTL mandate gate before every deploy call
- [ ] Kill switch drilled mid-build
- [ ] Repo mirrored + version pinned

### P3 — microVM AgentFence

- [ ] `/dev/kvm` confirmed on bare metal / dedicated
- [ ] microsandbox trial; E2B fallback triggers defined
- [ ] Trust router: operator → Sandboxd; external|generated → microVM
- [ ] Secret-substitution pattern adopted
- [ ] Per-build egress allowlists + outbound logs → audit packs
- [ ] Seven-drill red-team battery fails closed with evidence

### P4 — Enterprise WIRE

- [ ] Server-per-tenant: Foundry provisions → Coolify register → deploy sibling
- [ ] Tenant + global kill switches drilled
- [ ] Audit packs: Coolify log + egress log + x402 ledger per deployment
- [ ] Scale gate at ~10 tenants evaluated
- [ ] Policy-as-code (routing, egress, HOTL thresholds, settlement) mandate-gated

---

## Safety invariants (do not weaken)

1. **No credentials in the browser or untrusted tier.**
2. **Never deploy without a fresh HOTL approval id.**
3. **Never settle on platform status alone** — only the external signed
   probe of `/.well-known/om-verify` is settlement evidence.
4. **Unknown trust → microVM.** Isolation is the floor, not a feature.
5. **Meters on native x402; Tier-2 revenue on the fiat adapter; one
   settlement ledger.** A second ledger is an incident.

---

## Related surfaces

| Surface | Location |
|---------|----------|
| Web control plane + WIRE panel | `web/openmesha.html` |
| Agent contract | [`AGENTS.md`](../AGENTS.md) |
| Verify script | `scripts/verify.sh` |
| Security policy | [`SECURITY.md`](../SECURITY.md) |
| Skills (AgentFence, HOTL, x402) | `skills/*/` |

---

*Last aligned with the in-kernel WIRE Adoption Module (v0.6.0) phase
checklists and topology. Update this document when phase exit criteria
or host sizing change.*
