from __future__ import annotations
from openmesha.kernel.capabilities import CapabilityRegistry
from openmesha.kernel.memory import MemoryStore

def register_builtins(registry: CapabilityRegistry, memory: MemoryStore) -> dict:
    tools = {
        "web_search": lambda q: f"[mock search] results for: {q}",
        "memory_read": lambda k: memory.read(k) or "",
        "memory_write": lambda k, v="": (memory.write(k, v), "ok")[1],
        "security_scan": lambda t: {"verdict": "blocked" if "ignore previous" in t.lower() else "clean"},
        "route_decide": lambda: {"model": "mock-gpt", "policy": "thompson"},
        "compute_quote": lambda hrs=10: {"spot": hrs * 1.9, "on_demand": hrs * 4.9},
    }
    for name, fn in tools.items():
        registry.register(name, description=f"builtin:{name}")
    registry.register("payment", description="x402 payment capability — HOTL gated")
    return tools
