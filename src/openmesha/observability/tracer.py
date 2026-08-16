from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone

class Tracer:
    def __init__(self) -> None:
        self._events: list[dict] = []
        self._counters: dict[str, int] = defaultdict(int)

    def record(self, agent_id: str, kind: str, message: str, extra: dict | None = None) -> None:
        self._events.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "agent_id": agent_id,
            "kind": kind,
            "message": message,
            "extra": extra or {},
        })

    def inc(self, name: str, n: int = 1) -> None:
        self._counters[name] += n

    def metrics(self) -> dict:
        return dict(self._counters)
