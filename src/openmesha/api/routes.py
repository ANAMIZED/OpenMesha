from __future__ import annotations
from typing import Any
from fastapi import APIRouter, Request, HTTPException
from openmesha.kernel.models import AgentCreate, AgentProcess, Task, WorkflowCreate, Workflow, TaskStatus
from openmesha import __version__

router = APIRouter()

@router.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "service": "openmesha", "version": __version__}

@router.get("/metrics")
def metrics(request: Request) -> dict[str, float]:
    return request.app.state.os.tracer.dump_metrics()

@router.post("/v1/agents")
async def create_agent(body: AgentCreate, request: Request) -> dict[str, Any]:
    os_ = request.app.state.os
    agent = AgentProcess(
        name=body.name, intent=body.intent, budget_usd=body.budget_usd,
        model=body.model, capabilities=body.capabilities,
    )
    tokens = os_.registry.synthesize(agent.capabilities)
    agent.capabilities = [t.name for t in tokens]
    os_.store.create_agent(agent)
    os_.tracer.inc("agents_created")
    os_.tracer.record(agent.id, "system", f"Agent created: {agent.name}")
    return agent.model_dump(mode="json")

@router.get("/v1/agents")
def list_agents(request: Request) -> list[dict[str, Any]]:
    return [a.model_dump(mode="json") for a in request.app.state.os.store.list_agents()]

@router.get("/v1/agents/{agent_id}")
def get_agent(agent_id: str, request: Request) -> dict[str, Any]:
    agent = request.app.state.os.store.get_agent(agent_id)
    if not agent:
        raise HTTPException(404, f"agent not found: {agent_id}")
    return agent.model_dump(mode="json")

@router.post("/v1/agents/{agent_id}/tasks")
async def run_task(agent_id: str, request: Request) -> dict[str, Any]:
    os_ = request.app.state.os
    agent = os_.store.get_agent(agent_id)
    if not agent:
        raise HTTPException(404, f"agent not found: {agent_id}")
    body = await request.json()
    goal = body.get("goal") or ""
    task = Task(agent_id=agent_id, goal=goal)
    os_.store.create_task(task)
    task = await os_.runtime.run_task(agent, task)
    os_.store.update_task(task)
    os_.store.save()
    return task.model_dump(mode="json")

@router.get("/v1/agents/{agent_id}/traces")
def agent_traces(agent_id: str, request: Request) -> list[dict[str, Any]]:
    return request.app.state.os.tracer.agent_traces(agent_id)

@router.get("/v1/cost/ledger")
def cost_ledger(request: Request) -> list[dict[str, Any]]:
    return request.app.state.os.cost.dump()

@router.get("/v1/audit")
def audit_log(request: Request) -> list[dict[str, Any]]:
    return request.app.state.os.policy.dump()

@router.post("/v1/workflows")
async def create_workflow(body: WorkflowCreate, request: Request) -> dict[str, Any]:
    os_ = request.app.state.os
    roles = body.agents or ["planner", "worker"]
    agent_ids: list[str] = []
    per = body.budget_usd / max(len(roles), 1)
    for role in roles:
        agent = AgentProcess(
            name=f"{body.name}-{role}",
            intent=f"Role: {role}. Goal: {body.goal}",
            budget_usd=per,
            model="mock-gpt",
            capabilities=["web_search", "memory_read", "memory_write"],
        )
        tokens = os_.registry.synthesize(agent.capabilities)
        agent.capabilities = [t.name for t in tokens]
        os_.store.create_agent(agent)
        agent_ids.append(agent.id)
        os_.tracer.inc("agents_created")

    wf = Workflow(name=body.name, goal=body.goal, agent_ids=agent_ids)
    os_.store.create_workflow(wf)
    results = []
    for aid in agent_ids:
        agent = os_.store.get_agent(aid)
        assert agent is not None
        task = Task(agent_id=aid, goal=f"[{agent.name}] Contribute to: {body.goal}")
        os_.store.create_task(task)
        task = await os_.runtime.run_task(agent, task)
        os_.store.update_task(task)
        results.append({"agent": agent.name, "result": task.result, "status": str(task.status.value if hasattr(task.status, "value") else task.status)})
    wf.status = TaskStatus.completed
    wf.result = str(results)
    os_.store.save()
    return {"workflow": wf.model_dump(mode="json"), "results": results}

@router.get("/dashboard")
def dashboard() -> dict[str, str]:
    return {"title": "OpenMesha", "message": "Open Agentic Operations Mesh control plane", "web": "/web/openmesha.html"}

@router.get("/api/state")
def api_state(request: Request) -> dict[str, Any]:
    """WIRE seam for the browser control plane."""
    os_ = request.app.state.os
    return {
        "agents": [a.model_dump(mode="json") for a in os_.store.list_agents()],
        "metrics": os_.tracer.dump_metrics(),
        "cost": os_.cost.dump()[-20:],
        "audit": os_.policy.dump()[-20:],
    }
