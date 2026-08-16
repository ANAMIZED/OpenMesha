---
name: cost-control
description: Enforce and inspect token/dollar budgets for OpenMesha agents. Use when the user asks about agent spend, budgets, cost ledgers, or runaway usage.
version: 0.1.0
license: Apache-2.0
tags: [openmesha, cost, budget, tokens]
---

# Cost Control Skill (OpenMesha)

## When to use
- Checking agent or fleet spend
- Setting or verifying budgets

## Workflow
1. List agents via API/CLI/MCP
2. Inspect `GET /v1/cost/ledger` or MCP `get_cost_ledger`
3. Always set explicit `budget_usd` at agent creation

## Rules
- Never create an agent without a budget
- Budget exhaustion is a hard stop
