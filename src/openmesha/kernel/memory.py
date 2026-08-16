from __future__ import annotations

class MemoryStore:
    def __init__(self) -> None:
        self._kv: dict[str, str] = {}

    def write(self, key: str, value: str) -> None:
        self._kv[key] = value

    def read(self, key: str) -> str | None:
        return self._kv.get(key)

    def search(self, q: str) -> list[tuple[str, str]]:
        ql = q.lower()
        return [(k, v) for k, v in self._kv.items() if ql in k.lower() or ql in v.lower()]
