from __future__ import annotations
from typing import Any

class CostController:
    def __init__(self) -> None:
        self._ledger: list[dict[str, Any]] = []

    def charge(self, agent_id: str, amount_usd: float, reason: str) -> float:
        self._ledger.append({"agent_id": agent_id, "amount_usd": amount_usd, "reason": reason})
        return amount_usd

    def dump(self) -> list[dict[str, Any]]:
        return list(self._ledger)
