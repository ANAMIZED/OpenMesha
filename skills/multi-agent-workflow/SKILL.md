---
name: multi-agent-workflow
description: Orchestrate sequential multi-agent workflows under a shared budget on OpenMesha. Use when a goal needs planner/researcher/worker roles or council-style decomposition.
version: 0.1.0
license: Apache-2.0
tags: [openmesha, multi-agent, workflow, orchestration]
---

# Multi-Agent Workflow Skill (OpenMesha)

## When to use
- Goals that benefit from specialist roles
- Verifying end-to-end multi-agent completion under budget

## Workflow
1. `POST /v1/workflows` or MCP `create_workflow` or CLI `openmesha workflow`
2. Each role gets a slice of the shared budget
3. Collect per-agent results; workflow status must be completed

## Rules
- Always set an explicit budget
- Prefer least-privilege capabilities per role
