from __future__ import annotations
from typing import Any

PAYWALLS = {
    "route.decide": 0.01,
    "security.scan": 0.04,
    "compute.quote": 0.02,
    "council.deliberate": 0.25,
}

def quote(service: str) -> dict[str, Any] | None:
    if service not in PAYWALLS:
        return None
    return {"service": service, "amount_usd": PAYWALLS[service], "asset": "USDC", "network": "base", "sim": True}

def settle_sim(service: str) -> dict[str, Any]:
    q = quote(service)
    if not q:
        return {"ok": False, "error": "no paywall"}
    return {"ok": True, "tx": {**q, "status": "simulated"}, "sim": True}
