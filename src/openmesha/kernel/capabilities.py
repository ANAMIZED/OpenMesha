from __future__ import annotations
from dataclasses import dataclass

@dataclass
class CapToken:
    name: str
    description: str = ""

class CapabilityRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, CapToken] = {}

    def register(self, name: str, description: str = "") -> None:
        self._tools[name] = CapToken(name=name, description=description)

    def synthesize(self, names: list[str]) -> list[CapToken]:
        out = []
        for n in names:
            if n in self._tools:
                out.append(self._tools[n])
            else:
                t = CapToken(name=n)
                self._tools[n] = t
                out.append(t)
        return out

    def list_available(self) -> list[str]:
        return sorted(self._tools.keys())
