---
name: x402-payments
description: Quote and settle OpenMesha x402 paywalled services (USDC on Base). Use when metering tool calls, outcome fees, or agent-to-agent settlement.
version: 0.1.0
license: Apache-2.0
tags: [openmesha, x402, payments, commerce]
---

# x402 Payments Skill (OpenMesha)

## When to use
- Pricing a metered tool call
- Inspecting paywalls or simulated settlement receipts

## Workflow
1. Quote via MCP `x402_payment_quote` or PAYWALLS table
2. Offline path marks receipts `sim:true`
3. Live path WIREs to control-plane `/api/payments`

## Rules
- Outcome fees only where the kernel verifies the criterion
- Money-moving actions remain HOTL-gated
