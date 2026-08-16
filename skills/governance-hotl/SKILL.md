---
name: governance-hotl
description: OpenMesha governance — fail-closed policy, HOTL for irreversible actions, audit log inspection. Use when reviewing denials, escalations, or audit trails.
version: 0.1.0
license: Apache-2.0
tags: [openmesha, governance, hotl, audit, policy]
---

# Governance · HOTL Skill (OpenMesha)

## When to use
- Inspecting why an action was denied or escalated
- Confirming audit log coverage after a security event

## Workflow
1. `GET /v1/audit` or MCP `get_audit_log` or CLI `openmesha audit`
2. Treat `escalate` as requiring human approval before retry
3. Do not bypass policy in mock or live mode

## Rules
- Fail closed
- HOTL for pay/transfer/deploy/delete-class actions
