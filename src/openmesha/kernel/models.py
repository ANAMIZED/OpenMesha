from __future__ import annotations
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime, timezone

def _id(prefix: str = "ag") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

class AgentStatus(str, Enum):
    idle = "idle"
    running = "running"
    stopped = "stopped"
    budget_exhausted = "budget_exhausted"
    policy_blocked = "policy_blocked"

class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    blocked = "blocked"

class AgentCreate(BaseModel):
    name: str
    intent: str
    budget_usd: float = 0.5
    model: str = "mock-gpt"
    capabilities: list[str] = Field(default_factory=lambda: ["memory_read", "memory_write", "web_search"])

class AgentProcess(BaseModel):
    id: str = Field(default_factory=lambda: _id("ag"))
    name: str
    intent: str
    budget_usd: float = 0.5
    spent_usd: float = 0.0
    model: str = "mock-gpt"
    capabilities: list[str] = Field(default_factory=list)
    status: AgentStatus = AgentStatus.idle
    created_at: str = Field(default_factory=_now)

class Task(BaseModel):
    id: str = Field(default_factory=lambda: _id("task"))
    agent_id: str
    goal: str
    status: TaskStatus = TaskStatus.pending
    result: Optional[str] = None
    error: Optional[str] = None
    spent_usd: float = 0.0
    created_at: str = Field(default_factory=_now)

class WorkflowCreate(BaseModel):
    name: str
    goal: str
    agents: list[str] = Field(default_factory=lambda: ["planner", "worker"])
    budget_usd: float = 1.0

class Workflow(BaseModel):
    id: str = Field(default_factory=lambda: _id("wf"))
    name: str
    goal: str
    agent_ids: list[str] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.pending
    result: Optional[str] = None
    created_at: str = Field(default_factory=_now)
