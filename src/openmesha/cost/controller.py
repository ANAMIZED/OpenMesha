from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class LedgerEntry:
    agent_id: str
    amount_usd: float
    reason: str
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class CostController:
    def __init__(self) -> None:
        self._ledger: list[LedgerEntry] = []

    def charge(self, agent_id: str, amount_usd: float, reason: str) -> None:
        self._ledger.append(LedgerEntry(agent_id=agent_id, amount_usd=amount_usd, reason=reason))

    def ledger(self) -> list[dict]:
        return [{"agent_id": e.agent_id, "amount_usd": e.amount_usd, "reason": e.reason, "ts": e.ts} for e in self._ledger]
