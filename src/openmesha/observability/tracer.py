from __future__ import annotations
from typing import Any
from collections import defaultdict

class Tracer:
    def __init__(self) -> None:
        self._metrics: dict[str, float] = defaultdict(float)
        self._traces: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def inc(self, key: str, n: float = 1.0) -> None:
        self._metrics[key] += n

    def record(self, agent_id: str, kind: str, msg: str, data: dict | None = None) -> None:
        self._traces[agent_id].append({"kind": kind, "msg": msg, "data": data or {}})

    def dump_metrics(self) -> dict[str, float]:
        return dict(self._metrics)

    def agent_traces(self, agent_id: str) -> list[dict[str, Any]]:
        return list(self._traces.get(agent_id, []))
