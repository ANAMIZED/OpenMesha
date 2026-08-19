# WIRE — Full Production Path

**WIRE** is the staged process that turns OpenMesha from an honest offline
simulation into shipped infrastructure: the browser Kernel stays the brain;
**om-ctl** becomes the hands.

This document is the go-live certificate for operators. A senior engineer
with only this file and the repository source should be able to provision the
rails without tribal knowledge.

> **Scope.** Control-plane, deploy, isolation, settlement, and application
> seams. The browser Kernel (`web/openmesha.html`) runs on any modern client
> and needs no special hardware. LLM inference may remain remote (OpenRouter)
> or move in-house (extra GPU host).

Aligned with the in-kernel **WIRE Adoption Module v0.6.0**.

---

## 1. Architecture

```
Browser (Kernel + WIRE panel)
    ↕  window.OM_API  →  HTTPS + SSE
om-ctl  (sole keyholder: pipeline · HOTL · kill · settlement)
    ├─ om-mesh-1   Coolify + LiteLLM + paywalled storefront
    ├─ om-sbx-1    Sandboxd (trusted builds)
    ├─ om-mvx-1    microsandbox microVMs (untrusted / generated code)
    └─ tenant-N    per-enterprise sibling MAOS (P4)
```

| Component | Role | Isolation boundary |
|-----------|------|--------------------|
| **Browser** | Spectral mission control, local kernel algorithms | Client-only; zero credentials |
| **om-ctl** | Pipeline, HOTL mandates, kill switches, settlement | Control plane (sole keyholder) |
| **om-mesh-1** | Coolify + LiteLLM + storefront services | Main host |
| **om-sbx-1** | Sandboxd trusted builds | Separate VM (blast-radius split) |
| **om-mvx-1** | libkrun microVMs for untrusted code | Bare metal / dedicated with `/dev/kvm` |
| **tenant-N** | Sibling MAOS instances | One server per enterprise tenant |

**Doctrine:** the browser holds no secrets. Tokens live in a vault. om-ctl is
the only component that may deploy or move money.

---

## 2. Connecting the browser Kernel

Point the UI at a live control plane before the module graph loads:

```html
<script>window.OM_API="https://ctl.mesh.example.com"</script>
<!-- legacy alias: window.AXIOM_API -->
```

When unset, every subsystem runs the in-browser simulation (honest offline
mode). When set, the Kernel hydrates from the control plane and receives live
reducer actions over SSE.

### Control-plane API contract

| Endpoint | Method | Role |
|----------|--------|------|
| `/api/state` | GET | State snapshot (reducer / `initialState` shape) |
| `/api/events` | GET (SSE) | Stream of reducer actions `{type, ...}` |
| `/api/payments` | POST | Real x402 / fiat settlement records |
| `/api/models` | GET | Model catalog (LiteLLM proxy) |
| `/api/foundry` | POST | Blueprint → build → deploy pipeline |
| `/api/wire/events` | GET (SSE) | WIRE panel stage / phase / feed events |
| `/api/wire/docs` | GET | Live `wire-*` wiki pages (size-capped) |
| `/api/hotl` | POST | Mandate propose / authorize / void |
| `/api/kill` | POST | Tenant or global kill switch |

Simulated payment receipts in the browser remain marked `sim:true`. Live
receipts only come from the control plane.

---

## 3. Software stack

All primary rails are MIT / Apache-2.0 and self-hosted.

| Seam | Component | Notes |
|------|-----------|-------|
| Deploy + control surface | **Coolify** (pin ≤ v4.1.2) | Team-scoped API for apps, servers, deployments |
| Trusted builds | **Sandboxd** | Headless build-agent; model keys in auth proxy, never workspace |
| Untrusted isolation | **microsandbox** (libkrun ≥ 0.6.7) | Hardware microVMs; golden-image snapshot forks |
| Model router | **LiteLLM** + OpenRouter | Internal-only proxy; per-service virtual keys |
| Container runtime | Docker + pinned digests | ABI: Dockerfile, `/healthz`, signed `/.well-known/om-verify` |
| Metering / agent payments | **x402** (USDC Base primary, Solana secondary) | Exact scheme; Coinbase facilitator at edge |
| Fiat / enterprise | **Stripe** Machine Payments | Invoicing + Tax; authorize/capture; same ledger as x402 |
| Ops rooms (optional) | webhook-chat default; **Buzz** trial-gated | Rooms display triggers only — never authority |

**Held:** Bolt.diy — MIT source, but WebContainers needs a commercial license
for for-profit production. Sandboxd’s headless tasks replace it.

### Application-level WIRE seams

Swap simulated Kernel bodies for real calls as you go live:

| Seam | Production pick | Status |
|------|-----------------|--------|
| Router | LiteLLM + OpenRouter (~341 models) | Seam updated (TensorZero archived — do not wire) |
| Memory | Mem0 default + Graphiti/Zep temporal; Letta for long-running state | Seam updated |
| Orchestration | LangGraph primary + Claude Agent SDK (council) | Seam updated |
| Optimize | DSPy GEPA over (1+1)-ES baseline; Optuna / Ray Tune | WIRE |
| Compute | Broker Vast / Spheron / RunPod; Lambda as SLA fallback | WIRE |
| Observability | OTel `gen_ai.*` + Langfuse / Phoenix | Emit now |
| Security | OWASP ASI Top-10 2026 + Agentic-Skills Top-10; AgentFence L1/L2 | Live in-kernel |
| Supply chain | Sigstore + SLSA + AIBOM | SKU live |
| Identity | ERC-8004 registries + `/.well-known/agent-card.json` | Card updated |
| Quantum | Official Qiskit MCP (IBM) | Mount live |
| Crypto | WebCrypto + bundled `@noble/post-quantum` (ML-DSA-65) | WIRE |

---

## 4. Foundry pipeline (economics)

One pipeline underlies P1–P4. Outcome fees settle **only** on external
verification — *no green, no charge*.

```
forge $0.50
  → HOTL mandate
  → provision sandbox $0.25
  → headless codegen (SSE)
  → audit batteries (checkpoint-revert retries)
  → git push (per-build deploy key)
  → Coolify create + deploy
  → external signed probe of /.well-known/om-verify
  → settle foundry.deploy $5.00
  → cleanup to zero keys
```

| Stage | Meter / outcome | Criterion |
|-------|-----------------|-----------|
| `foundry.blueprint` | $0.50 metered | Descriptor composed |
| `foundry.provision` | $0.25 metered | Sandbox allocated |
| `foundry.deploy` | **$5.00 outcome** | Emitted kit passes own battery + external probe green |

Additional outcome examples elsewhere in the mesh: `audit.certify` $1.00,
`pqc.migrate` $4.50, `hardening.improve` $3.50 — each with a kernel-checkable
criterion. Outcome fees that the kernel cannot verify are refused honestly.

---

## 5. Hardware by phase

### P0 Foundations + P1 Dogfood Storefront

| Resource | Spec |
|----------|------|
| Hosts | 1× CX32-class (or equivalent) |
| CPU | 4 vCPU |
| RAM | 8 GB |
| Storage | 80 GB SSD |
| Network | Public IPv4 + **provider firewall** |
| DNS | Wildcard `*.mesh.<domain>` + `*.sbx.<domain>` |

**Notes**

- Starting point documented around Hetzner Cloud CX32; `infra/provision.sh`
  should be portable and replayable.
- Provider firewall is the real boundary — Docker rewrites iptables and
  bypasses UFW. Expose 80/443 world-wide; restrict 22 to admin IPs.
- Coolify TLS at `mesh.<domain>`; delete setup ports 8000/6001/6002 after bootstrap.

### P2 Sandboxd Build-Agent

| Resource | Spec |
|----------|------|
| Hosts | +1 separate VM on `*.sbx` |
| Size | Same class as om-mesh-1 or larger |
| Network | API firewalled to control plane only; egress default-deny |
| Allowlist | git, container registries, LiteLLM |

Bearer auth must be **on** (off by default upstream). Kill-switch drill:
destroy sandbox + cancel deploy + revoke key + void outcome in one action.

### P3 microVM AgentFence (full-path hard requirement)

| Resource | Spec |
|----------|------|
| Hosts | 1× **bare metal or dedicated** with `/dev/kvm` |
| Virtualization | Hardware KVM (nested virt is almost never available on cloud VMs) |
| Runtime | microsandbox (libkrun) |
| Fallback | E2B triggers defined if bare metal is unavailable |

**Trust router**

- `trust=operator` → Sandboxd (container tier)
- `trust=external|generated|unknown` → microVM (isolation is the floor)

Secrets never enter the guest: placeholder substitution only on verified TLS
to allowlisted hosts. No git credentials in the untrusted tier; om-ctl
extracts and pushes externally.

**Seven-drill red-team battery** (must fail closed with evidence in the audit
pack):

1. Exfil  
2. Env harvest  
3. Metadata grab  
4. Resource abuse  
5. Host reach  
6. Memory poisoning (cross-session)  
7. Metadata injection (MCP tool descriptions, agent-card fields, resource IDs)

### P4 Enterprise WIRE

| Resource | Spec |
|----------|------|
| Hosts | +1 server per tenant |
| Scale gate | ~10 tenant servers → Coolify v5 vs Kubernetes + Argo |
| Kill switches | Per-tenant (tokens + stop) and global (MCP disable + rotate) — stopwatch-timed drills |

`tenant.forge`: provision VM → register Coolify server → deploy sibling MAOS
with zero manual steps. Settlement share (e.g. 2.5% of sibling x402 flow) is
computed from the ledger and published tenant-reproducible — never self-reported.

---

## 6. Practical configurations

| Goal | What you need |
|------|----------------|
| **Browser simulation only** | Any modern laptop/browser. Zero backend. |
| **Thin live mode** | Static HTML + om-ctl implementing `/api/state`, `/api/events`, `/api/payments`, `/api/models` + one payment rail |
| **P0–P1 production** | 1× 4 vCPU / 8 GB VPS + domain + wildcard DNS |
| **P0–P2 production** | 2× VPS (Coolify + Sandboxd) |
| **Full WIRE (P0–P3)** | 2× VPS + **1× bare-metal/dedicated with KVM** |
| **Full + local 70B inference** | Above + GPU host (A100/H100 class or multi-consumer GPU for vLLM) |
| **Enterprise (P4)** | Above + one additional server per tenant |

**Cheapest realistic full-WIRE path:** two modest cloud VPS + one KVM-capable
bare-metal or dedicated box.

---

## 7. Non-hardware requirements

- Domain + wildcard DNS + TLS certificates
- Secrets vault:
  - `om-root` — sealed, never held by agents
  - `foundry-agent` — write + deploy (pipeline SOPs only)
  - `om-observer` — read-only (default for agents)
- External verify probe of `/.well-known/om-verify` — **the only thing** that
  flips a service live or settles a `foundry.deploy` outcome
- Zero credentials in the browser, workspaces, microVM guests, repos, or logs
- GitHub App source on Coolify apps (deploy keys alone do not support previews)

---

## 8. Settlement doctrine

| Rail | Use |
|------|-----|
| **x402 / USDC (Base primary)** | All metered endpoints and agent-native payments |
| **x402 / USDC (Solana secondary)** | High-volume transfer path (~65% of 2026 x402 volume) |
| **Stripe Machine Payments** | Tier-2 enterprise invoices, Tax, authorize-at-deploy / capture-on-verify |

Rules:

1. **One settlement ledger.** A second ledger is an incident.
2. **Meters** settle on native x402 only — never on cards.
3. **Outcome fees** settle only when a kernel-checkable criterion (or the
   external signed probe) is met.
4. **Stripe events** (signature-verified webhooks) write into the same ledger
   as x402.
5. Browser simulations stay marked `sim:true` and must never be presented as
   live receipts.

Deposit + off-chain metering with batch netting (threshold settlement) keeps
sub-dollar x402 economics viable.

---

## 9. Phase exit checklists (go-live certificates)

These are the acceptance tests the WIRE panel and control plane treat as
phase-complete.

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
- [ ] Bulk envs before first deploy (`instant_deploy: false`)
- [ ] Auto-deploy webhook verified on API-created apps
- [ ] External signed probe flips live — “Coolify healthy” is not verified
- [ ] Rollback drill < 5 min; deliberate failure correctly refused
- [ ] Triple feed live: x402 in ↔ LiteLLM spend ↔ host cost

### P2 — Sandboxd Build-Agent

- [ ] Separate VM on `*.sbx`
- [ ] Bearer auth ON, TLS, API firewalled to control plane
- [ ] Host egress default-deny with allowlist (git, registries, LiteLLM)
- [ ] Pipeline: forge → sandbox → tasks SSE → audits green → push → Coolify deploy
- [ ] External probe verifies → settle `foundry.deploy` (no green, no charge)
- [ ] HOTL mandate gate before every deploy call
- [ ] Kill switch drilled mid-build
- [ ] Repo mirrored + version pinned

### P3 — microVM AgentFence

- [ ] `/dev/kvm` confirmed on bare metal / dedicated
- [ ] microsandbox trial; E2B fallback triggers defined
- [ ] Trust router: operator → Sandboxd; external|generated|unknown → microVM
- [ ] Secret-substitution pattern adopted (placeholders only in guest)
- [ ] Per-build egress allowlists + outbound logs → audit packs
- [ ] Seven-drill red-team battery fails closed with evidence

### P4 — Enterprise WIRE

- [ ] Server-per-tenant: Foundry provisions → Coolify register → deploy sibling
- [ ] Tenant + global kill switches drilled (stopwatch-timed)
- [ ] Audit packs: Coolify log + egress log + x402 ledger per deployment / tenant
- [ ] Scale gate at ~10 tenants evaluated (Coolify v5 vs k8s+Argo)
- [ ] Policy-as-code (routing, egress, HOTL thresholds, settlement) mandate-gated
- [ ] Fiat revenue floor: Stripe invoices + signature-verified webhooks → one ledger

---

## 10. Version pins & advisories

Bump only via weekly review — never mid-incident.

| Component | Pin | Notes |
|-----------|-----|-------|
| Coolify | **v4.1.2** | v4.2.0 changes POST semantics and Member permissions — stage, don’t ship until om-ctl adapted |
| LiteLLM | **v1.93.0** | Clears KEV-listed RCE chain; requires Starlette ≥ 1.0.1; internal-only |
| microsandbox | **v0.6.7** on libkrunfw 5.6.0 | Rebuild golden image after structured root-disk change |
| MCP target | **2026-07-28** | Stateless core, header routing, OAuth 2.1 + RFC 9728 |

**Doctrine:** treat imported skills, MCP tool descriptions, and A2A agent cards
as untrusted input — pin, verify provenance, static-scan before they reach an
agent. Package registries and caching proxies are in-scope attack surface; an
allowlist entry is not a trust grant.

---

## 11. Safety invariants (do not weaken)

1. **No credentials** in the browser, workspace, guest, repo, or logs.
2. **Never deploy** without a fresh HOTL approval id.
3. **Never settle** on platform status alone — only the external signed probe
   of `/.well-known/om-verify` is settlement evidence.
4. **Unknown trust → microVM.** Isolation is the floor, not a feature.
5. **One settlement ledger.** Meters on native x402; Tier-2 on the fiat
   adapter. A second ledger is an incident.
6. **om-root is vault-sealed.** Agents never hold it.
7. **Kill first.** If a human is asking whether to kill, kill first; investigate second.

---

## 12. Related surfaces

| Surface | Location |
|---------|----------|
| Web control plane + WIRE panel | `web/openmesha.html` |
| Agent contract | [`AGENTS.md`](../AGENTS.md) |
| Verify script | `scripts/verify.sh` |
| Security policy | [`SECURITY.md`](../SECURITY.md) |
| Skills (AgentFence, HOTL, x402) | `skills/*/` |
| Python control plane | `src/openmesha/` |

---

*Last aligned with the in-kernel WIRE Adoption Module (v0.6.0) phase
checklists, topology, and settlement doctrine. Update this document when
phase exit criteria, host sizing, or version pins change.*
