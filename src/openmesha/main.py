from __future__ import annotations
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openmesha.agents.runtime import AgentRuntime
from openmesha.api.routes import router
from openmesha.config import settings
from openmesha.cost.controller import CostController
from openmesha.governance.policy import PolicyEngine
from openmesha.kernel.capabilities import CapabilityRegistry
from openmesha.kernel.memory import MemoryStore
from openmesha.kernel.store import ProcessTable
from openmesha.observability.tracer import Tracer
from openmesha.tools.builtin import register_builtins

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ]
)

class OpenMesha:
    def __init__(self) -> None:
        self.store = ProcessTable()
        self.memory = MemoryStore()
        self.registry = CapabilityRegistry()
        self.cost = CostController()
        self.policy = PolicyEngine()
        self.tracer = Tracer()
        self.tools = register_builtins(self.registry, self.memory)
        self.runtime = AgentRuntime(
            registry=self.registry, memory=self.memory, cost=self.cost,
            policy=self.policy, tracer=self.tracer,
        )

def create_app() -> FastAPI:
    app = FastAPI(
        title="OpenMesha",
        description="Open Agentic Operations Mesh — control plane",
        version="0.1.0",
    )
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.state.os = OpenMesha()
    app.include_router(router)
    return app

app = create_app()

def run() -> None:
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, log_level=settings.log_level.lower())

if __name__ == "__main__":
    run()
