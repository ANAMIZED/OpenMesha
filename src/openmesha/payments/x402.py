from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Quote:
    amount_usd: float
    currency: str = "USDC"
    chain: str = "base"
    sim: bool = True

PAYWALLS = {
    "web_search": 0.001,
    "code_exec": 0.005,
    "outcome_fee": 0.05,
}

def quote(service: str) -> Quote:
    amt = PAYWALLS.get(service, 0.01)
    return Quote(amount_usd=amt, sim=True)
