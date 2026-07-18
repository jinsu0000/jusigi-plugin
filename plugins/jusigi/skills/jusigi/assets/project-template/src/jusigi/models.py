"""Provider-neutral models used by the deterministic execution boundary."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


Action = Literal["buy", "sell", "hold"]


@dataclass(frozen=True)
class Quote:
    ticker: str
    price: float
    age_seconds: int
    market_open: bool
    source: str


@dataclass(frozen=True)
class OrderIntent:
    intent_id: str
    ticker: str
    action: Action
    quantity: int
    confidence: float
    rationale: str = ""
    risk_flags: tuple[str, ...] = ()


@dataclass
class Account:
    cash_krw: float
    holdings: dict[str, int] = field(default_factory=dict)
    market_values: dict[str, float] = field(default_factory=dict)
    daily_pnl_krw: float = 0
    processed_intent_ids: set[str] = field(default_factory=set)

    @property
    def total_value_krw(self) -> float:
        return self.cash_krw + sum(self.market_values.values())


@dataclass(frozen=True)
class RiskDecision:
    approved: bool
    reason: str
