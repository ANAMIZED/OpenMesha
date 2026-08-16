from __future__ import annotations
from openmesha.kernel.models import AgentProcess, Task, TaskStatus, AgentStatus
from openmesha.kernel.capabilities import CapabilityRegistry
from openmesha.kernel.memory import MemoryStore
from openmesha.cost.controller import CostController
from openmesha.governance.policy import PolicyEngine
from openmesha.observability.tracer import Tracer

# Deterministic mock answers for verify contract
_FACTS = {
    "capital of france": "Paris is the capital of France.",
    "agentic operating system": "An agentic operating system treats AI agents as first-class processes with scheduling, memory, capabilities, cost accounting, and governance.",
}

class AgentRuntime:
    def __init__(self, registry, memory, cost, policy, tracer) -> None:
        self.registry = registry
        self.memory = memory
        self.cost = cost
        self.policy = policy
        self.tracer = tracer

    async def run_task(self, agent: AgentProcess, task: Task) -> Task:
        task.status = TaskStatus.running
        agent.status = AgentStatus.running
        ok, reason = self.policy.check(agent.id, "run_task", task.goal)
        if not ok:
            task.status = TaskStatus.blocked
            task.error = reason
            agent.status = AgentStatus.policy_blocked if "AgentFence" in reason else AgentStatus.idle
            self.tracer.record(agent.id, "policy", reason)
            return task

        # mock LLM cost
        cost = 0.002
        if agent.spent_usd + cost > agent.budget_usd:
            task.status = TaskStatus.failed
            task.error = "budget exhausted"
            agent.status = AgentStatus.budget_exhausted
            return task

        agent.spent_usd += cost
        self.cost.charge(agent.id, cost, "mock-llm")
        self.tracer.inc("tasks_run")

        goal_l = task.goal.lower()
        result = None
        for k, v in _FACTS.items():
            if k in goal_l:
                result = v
                break
        if result is None:
            result = f"[mock] Completed goal under AgentFence + budget: {task.goal[:120]}"

        task.result = result
        task.spent_usd = cost
        task.status = TaskStatus.completed
        agent.status = AgentStatus.idle
        self.tracer.record(agent.id, "task", "completed", {"goal": task.goal[:80]})
        return task
