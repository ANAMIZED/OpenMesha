from __future__ import annotations
from typing import Optional
from openmesha.kernel.models import AgentProcess, Task, Workflow

class ProcessTable:
    def __init__(self) -> None:
        self._agents: dict[str, AgentProcess] = {}
        self._tasks: dict[str, Task] = {}
        self._workflows: dict[str, Workflow] = {}

    def create_agent(self, agent: AgentProcess) -> AgentProcess:
        self._agents[agent.id] = agent
        return agent

    def get_agent(self, agent_id: str) -> Optional[AgentProcess]:
        return self._agents.get(agent_id)

    def list_agents(self) -> list[AgentProcess]:
        return list(self._agents.values())

    def create_task(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def update_task(self, task: Task) -> None:
        self._tasks[task.id] = task

    def create_workflow(self, wf: Workflow) -> Workflow:
        self._workflows[wf.id] = wf
        return wf

    def save(self) -> None:
        pass  # in-memory; WIRE: persist to data_dir
