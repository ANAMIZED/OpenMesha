from __future__ import annotations
import re

# AgentFence L1 patterns — treat as data, never instructions
_HOSTILE = re.compile(
    r"(ignore previous|disregard (all|previous)|wire funds|transfer (all|money)|system prompt|jailbreak|override policy)",
    re.I,
)

class PolicyEngine:
    def __init__(self) -> None:
        self._audit: list[dict] = []

    def check(self, agent_id: str, action: str, content: str) -> tuple[bool, str]:
        if _HOSTILE.search(content or ""):
            msg = "AgentFence L2 blocked: hostile or money-moving intent"
            self._audit.append({"agent_id": agent_id, "action": action, "decision": "blocked", "reason": msg})
            return False, msg
        self._audit.append({"agent_id": agent_id, "action": action, "decision": "allow", "reason": "ok"})
        return True, "ok"

    def audit_log(self) -> list[dict]:
        return list(self._audit)
