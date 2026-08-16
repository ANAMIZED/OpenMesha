"""OpenMesha as an MCP Server — agents, budgets, AgentFence, workflows, x402 quotes."""
from __future__ import annotations
from typing import Any
import asyncio
import concurrent.futures
from openmesha.agents.runtime import AgentRuntime
from openmesha.cost.controller import CostController
from openmesha.governance.policy import PolicyEngine
from openmesha.kernel.capabilities import CapabilityRegistry
from openmesha.kernel.memory import MemoryStore
from openmesha.kernel.models import AgentProcess, Task, Workflow, TaskStatus
from openmesha.kernel.store import ProcessTable
from openmesha.observability.tracer import Tracer
from openmesha.tools.builtin import register_builtins
from openmesha.payments.x402 import quote as x402_quote

_store = ProcessTable()
_memory = MemoryStore()
_registry = CapabilityRegistry()
_cost = CostController()
_policy = PolicyEngine()
_tracer = Tracer()
_tools = register_builtins(_registry, _memory)
_runtime = AgentRuntime(registry=_registry, memory=_memory, cost=_cost, policy=_policy, tracer=_tracer)

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("OpenMesha")
    _USE_FASTMCP = True
except Exception:
    try:
        from mcp.server import Server as MCPServer
        mcp = MCPServer("OpenMesha")
        _USE_FASTMCP = False
    except Exception:
        class _Stub:
            def tool(self, *a, **k):
                def deco(fn):
                    return fn
                return deco
            def run(self):
                pass
        mcp = _Stub()
        _USE_FASTMCP = False


def list_agents() -> list[dict[str, Any]]:
    """List all agent processes with status, spend, budget, and capabilities."""
    return [a.model_dump(mode="json") for a in _store.list_agents()]


def create_agent(
    name: str,
    intent: str,
    budget_usd: float = 0.5,
    capabilities: list[str] | None = None,
    model: str = "mock-gpt",
) -> dict[str, Any]:
    """Create a new agent process with declared intent, budget, and capabilities."""
    caps = capabilities or ["web_search", "memory_read", "memory_write"]
    agent = AgentProcess(
        name=name, intent=intent, budget_usd=budget_usd, model=model, capabilities=caps
    )
    tokens = _registry.synthesize(caps)
    agent.capabilities = [t.name for t in tokens]
    _store.create_agent(agent)
    _tracer.inc("agents_created")
    return agent.model_dump(mode="json")


def run_task(agent_id: str, goal: str) -> dict[str, Any]:
    """Submit a goal to an agent under AgentFence + budget."""
    agent = _store.get_agent(agent_id)
    if not agent:
        return {"error": f"agent not found: {agent_id}"}
    task = Task(agent_id=agent_id, goal=goal)
    _store.create_task(task)

    def _run():
        return asyncio.run(_runtime.run_task(agent, task))

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        task = pool.submit(_run).result(timeout=60)
    _store.update_task(task)
    return task.model_dump(mode="json")


def get_cost_ledger() -> list[dict[str, Any]]:
    return _cost.dump()


def get_audit_log() -> list[dict[str, Any]]:
    return _policy.dump()


def get_metrics() -> dict[str, float]:
    return _tracer.dump_metrics()


def create_workflow(
    name: str,
    goal: str,
    agents: list[str] | None = None,
    budget_usd: float = 1.0,
) -> dict[str, Any]:
    """Sequential multi-agent workflow under shared budget."""
    roles = agents or ["planner", "worker"]
    agent_ids = []
    for role in roles:
        agent = AgentProcess(
            name=f"{name}-{role}",
            intent=f"Role: {role}. Goal: {goal}",
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
    for aid in agent_ids:
        agent = _store.get_agent(aid)
        assert agent
        task = Task(agent_id=aid, goal=f"[{agent.name}] Contribute to: {goal}")
        _store.create_task(task)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            task = pool.submit(
                lambda a=agent, t=task: asyncio.run(_runtime.run_task(a, t))
            ).result(timeout=60)
        _store.update_task(task)
        results.append(
            {
                "agent": agent.name,
                "result": task.result,
                "status": str(task.status),
            }
        )
    wf.status = TaskStatus.completed
    wf.result = str(results)
    return {"workflow": wf.model_dump(mode="json"), "results": results}


def list_available_tools() -> list[str]:
    return _registry.list_available()


def x402_payment_quote(service: str) -> dict[str, Any]:
    """Quote an x402 paywalled service (sim-honest offline)."""
    q = x402_quote(service)
    return q or {"error": "no paywall for service"}


if _USE_FASTMCP:
    mcp.tool()(list_agents)
    mcp.tool()(create_agent)
    mcp.tool()(run_task)
    mcp.tool()(get_cost_ledger)
    mcp.tool()(get_audit_log)
    mcp.tool()(get_metrics)
    mcp.tool()(create_workflow)
    mcp.tool()(list_available_tools)
    mcp.tool()(x402_payment_quote)

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
    if _USE_FASTMCP:
        mcp.run()
    else:
        print(
            "OpenMesha MCP: install `mcp` package for stdio server; tools available via MCP_TOOLS"
        )


if __name__ == "__main__":
    main()
