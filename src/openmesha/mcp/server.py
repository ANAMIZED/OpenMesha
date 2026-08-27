"""OpenMesha MCP stdio server — agents, budgets, AgentFence, workflows, x402 quotes."""

from __future__ import annotations

import asyncio
import concurrent.futures
from typing import Annotated, Any

from pydantic import Field

from openmesha.agents.runtime import AgentRuntime
from openmesha.cost.controller import CostController
from openmesha.governance.policy import PolicyEngine
from openmesha.kernel.capabilities import CapabilityRegistry
from openmesha.kernel.memory import MemoryStore
from openmesha.kernel.models import AgentProcess, Task, TaskStatus, Workflow
from openmesha.kernel.store import ProcessTable
from openmesha.observability.tracer import Tracer
from openmesha.payments.x402 import quote as x402_quote
from openmesha.tools.builtin import register_builtins

try:
    from fastmcp import FastMCP
except ImportError:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP

_store = ProcessTable()
_memory = MemoryStore()
_registry = CapabilityRegistry()
_cost = CostController()
_policy = PolicyEngine()
_tracer = Tracer()
register_builtins(_registry, _memory)
_runtime = AgentRuntime(
    registry=_registry,
    memory=_memory,
    cost=_cost,
    policy=_policy,
    tracer=_tracer,
)

mcp = FastMCP(
    "OpenMesha",
    instructions=(
        "OpenMesha is an open agentic operations mesh. Use list_agents / create_agent / "
        "run_task for single-agent work, create_workflow for multi-agent runs, and the "
        "get_* tools for cost, audit, and metrics. x402_payment_quote is a read-only "
        "offline quote. Default LLM mode is mock unless OM_LLM_MODE=live."
    ),
)


@mcp.tool()
def list_agents() -> list[dict[str, Any]]:
    """List in-process agent records (id, status, spend, budget, capabilities).

    Use before run_task to discover agent_id values. Read-only snapshot of this
    process. Does not create agents (create_agent) or start work (run_task).
    """
    return [a.model_dump(mode="json") for a in _store.list_agents()]


@mcp.tool()
def create_agent(
    name: Annotated[str, Field(description="Human-readable agent name.")],
    intent: Annotated[str, Field(description="Declared goal the agent is allowed to pursue.")],
    budget_usd: Annotated[float, Field(description="USD spend cap for this agent.")] = 0.5,
    capabilities: Annotated[
        list[str] | None,
        Field(description="Capability names from list_available_tools. Default search+memory."),
    ] = None,
    model: Annotated[str, Field(description="Model id. Default mock-gpt for offline / Glama.")] = "mock-gpt",
) -> dict[str, Any]:
    """Create an agent process with intent, USD budget, and capabilities.

    Returns agent_id for later run_task / list_agents. Does not execute a goal.
    Side effect: writes the in-memory process table. Default model is mock-gpt.
    """
    caps = capabilities or ["web_search", "memory_read", "memory_write"]
    agent = AgentProcess(name=name, intent=intent, budget_usd=budget_usd, model=model, capabilities=caps)
    tokens = _registry.synthesize(caps)
    agent.capabilities = [t.name for t in tokens]
    _store.create_agent(agent)
    _tracer.inc("agents_created")
    return agent.model_dump(mode="json")


@mcp.tool()
def run_task(
    agent_id: Annotated[str, Field(description="Agent id returned by create_agent.")],
    goal: Annotated[str, Field(description="Natural-language goal to execute under budget/policy.")],
) -> dict[str, Any]:
    """Run one goal on an existing agent until completion, policy deny, or budget stop.

    Blocks up to 120s. Missing agent_id returns an error object. Use create_agent first.
    Not for multi-agent orchestration (create_workflow). Side effects: task row + spend.
    """
    agent = _store.get_agent(agent_id)
    if not agent:
        return {"error": f"agent not found: {agent_id}"}
    task = Task(agent_id=agent_id, goal=goal)
    _store.create_task(task)

    def _run() -> Task:
        return asyncio.run(_runtime.run_task(agent, task))

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            task = pool.submit(_run).result(timeout=120)
    except Exception as e:
        return {"error": f"task execution failed: {e}", "agent_id": agent_id, "goal": goal}
    _store.update_task(task)
    _store.save()
    return task.model_dump(mode="json")


@mcp.tool()
def get_cost_ledger() -> list[dict[str, Any]]:
    """Return the token/$ cost ledger for this process.

    Use to audit spend after run_task. Read-only. Not get_audit_log or get_metrics.
    """
    return _cost.dump()


@mcp.tool()
def get_audit_log() -> list[dict[str, Any]]:
    """Return governance allow/deny records from AgentFence.

    Use after a blocked run_task. Read-only. Not the dollar ledger (get_cost_ledger).
    """
    return _policy.dump()


@mcp.tool()
def get_metrics() -> dict[str, float]:
    """Return runtime counters (agents created, tasks).

    Use for health checks. Read-only. Does not include cost rows or policy events.
    """
    return _tracer.dump_metrics()


@mcp.tool()
def create_workflow(
    name: Annotated[str, Field(description="Workflow name.")],
    goal: Annotated[str, Field(description="Shared goal given to each specialist agent.")],
    agents: Annotated[
        list[str] | None,
        Field(description="Role names. Default planner then worker."),
    ] = None,
    budget_usd: Annotated[float, Field(description="Shared USD budget split across roles.")] = 1.0,
) -> dict[str, Any]:
    """Create specialist agents and run a sequential multi-agent workflow.

    Default roles are planner then worker, sharing budget_usd. Use when a goal needs
    more than one agent. Do not use to run a single existing agent (run_task).
    Side effects: creates agents + tasks and marks the workflow completed.
    """
    roles = agents or ["planner", "worker"]
    agent_ids: list[str] = []
    for role in roles:
        agent = AgentProcess(
            name=f"{name}-{role}",
            intent=f"Role: {role}. Overall goal: {goal}. Stay within budget.",
            budget_usd=budget_usd / max(len(roles), 1),
            model="mock-gpt",
            capabilities=["web_search", "memory_read", "memory_write"],
        )
        tokens = _registry.synthesize(agent.capabilities)
        agent.capabilities = [t.name for t in tokens]
        _store.create_agent(agent)
        agent_ids.append(agent.id)
        _tracer.inc("agents_created")

    wf = Workflow(name=name, goal=goal, agent_ids=agent_ids)
    _store.create_workflow(wf)
    results = []

    def _run_one(agent: AgentProcess, task: Task) -> Task:
        return asyncio.run(_runtime.run_task(agent, task))

    for aid in agent_ids:
        agent = _store.get_agent(aid)
        assert agent is not None
        task = Task(agent_id=aid, goal=f"[{agent.name}] Contribute to: {goal}")
        _store.create_task(task)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            task = pool.submit(_run_one, agent, task).result(timeout=120)
        _store.update_task(task)
        results.append({"agent": agent.name, "result": task.result, "status": str(task.status)})

    wf.status = TaskStatus.completed
    wf.result = str(results)
    _store.save()
    return {"workflow": wf.model_dump(mode="json"), "results": results}


@mcp.tool()
def list_available_tools() -> list[str]:
    """List capability names that can be granted to agents.

    Use before create_agent to choose the capabilities argument. Read-only.
    """
    return _registry.list_available()


@mcp.tool()
def x402_payment_quote(
    service: Annotated[str, Field(description="Paywalled service name to quote.")],
) -> dict[str, Any]:
    """Return an offline x402 payment quote for a named service.

    Read-only simulation. Does not charge or call a facilitator. Missing services
    return an error object. Not create_agent or run_task.
    """
    q = x402_quote(service)
    return q or {"error": "no paywall for service", "service": service}


# Catalog used by unit tests and agent contracts. FastMCP wraps the callables
# but the names must stay stable for CI collection.
MCP_TOOLS = {
    "list_agents": list_agents,
    "create_agent": create_agent,
    "run_task": run_task,
    "get_cost_ledger": get_cost_ledger,
    "get_audit_log": get_audit_log,
    "get_metrics": get_metrics,
    "create_workflow": create_workflow,
    "list_available_tools": list_available_tools,
    "x402_payment_quote": x402_payment_quote,
}


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
