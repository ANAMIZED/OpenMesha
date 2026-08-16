from __future__ import annotations
from typing import Any

# Fail-closed patterns aligned with OpenMesha AgentFence
_BLOCK = ("wire funds", "ignore previous", "exfiltrate", "drop table", "rm -rf")

class PolicyEngine:
    def __init__(self) -> None:
        self._audit: list[dict[str, Any]] = []

    def check(self, agent_id: str, action: str, text: str = "") -> tuple[bool, str]:
        low = (action + " " + text).lower()
        for pat in _BLOCK:
            if pat in low:
                rec = {"agent_id": agent_id, "action": action, "decision": "deny", "reason": f"AgentFence: {pat}"}
                self._audit.append(rec)
                return False, rec["reason"]
        # money-moving escalates (HOTL) — deny auto-execution offline
        if any(w in low for w in ("pay", "transfer", "purchase", "deploy")):
            rec = {"agent_id": agent_id, "action": action, "decision": "escalate", "reason": "HOTL: irreversible/money-moving"}
            self._audit.append(rec)
            return False, rec["reason"]
        self._audit.append({"agent_id": agent_id, "action": action, "decision": "allow", "reason": "ok"})
        return True, "ok"

    def dump(self) -> list[dict[str, Any]]:
        return list(self._audit)
