from __future__ import annotations
from openmesha.kernel.capabilities import CapabilityRegistry
from openmesha.kernel.memory import MemoryStore

def register_builtins(registry: CapabilityRegistry, memory: MemoryStore) -> dict:
    registry.register("web_search", "Search the open web (mock)")
    registry.register("memory_read", "Read from agent memory")
    registry.register("memory_write", "Write to agent memory")
    registry.register("code_exec", "Execute sandboxed code (mock)")

    def web_search(q: str) -> str:
        return f"[mock search] results for: {q}"

    def memory_read(key: str) -> str:
        return memory.read(key) or ""

    def memory_write(key: str, value: str) -> str:
        memory.write(key, value)
        return "ok"

    return {
        "web_search": web_search,
        "memory_read": memory_read,
        "memory_write": memory_write,
    }
