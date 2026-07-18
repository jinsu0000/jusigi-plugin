"""Load non-secret investment policy and reject unsafe configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class PolicyError(ValueError):
    pass


@dataclass(frozen=True)
class RiskPolicy:
    broker_provider: str
    live_enabled: bool
    short_selling_enabled: bool
    minimum_cash_reserve_krw: float
    allowlist: frozenset[str]
    minimum_confidence: float
    max_order_krw: float
    max_position_percent: float
    max_orders_per_run: int
    max_daily_loss_krw: float
    max_quote_age_seconds: int
    require_market_open: bool


def _mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PolicyError(f"{name} must be a mapping")
    return value


def _boolean(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise PolicyError(f"{name} must be true or false")
    return value


def load_policy(path: str | Path) -> RiskPolicy:
    value = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    root = _mapping(value, "policy")
    mode = _mapping(root.get("mode"), "mode")
    allocation = _mapping(root.get("allocation"), "allocation")
    universe = _mapping(root.get("universe"), "universe")
    risk = _mapping(root.get("risk"), "risk")

    core = int(allocation.get("core_percent", -1))
    satellite = int(allocation.get("satellite_percent", -1))
    if core < 0 or satellite < 0 or core + satellite != 100:
        raise PolicyError("core_percent and satellite_percent must total 100")

    live_enabled = _boolean(mode.get("live_enabled", False), "mode.live_enabled")
    if live_enabled:
        raise PolicyError("starter policy cannot enable live trading")
    if _boolean(mode.get("short_selling_enabled", False), "mode.short_selling_enabled"):
        raise PolicyError("starter policy cannot enable short selling")

    allowlist_value = universe.get("allowlist", [])
    if not isinstance(allowlist_value, list) or not all(isinstance(item, str) for item in allowlist_value):
        raise PolicyError("universe.allowlist must be a string list")

    policy = RiskPolicy(
        broker_provider=str(mode.get("broker_provider", "dry-run")),
        live_enabled=live_enabled,
        short_selling_enabled=False,
        minimum_cash_reserve_krw=float(allocation.get("minimum_cash_reserve_krw", 0)),
        allowlist=frozenset(item.strip().upper() for item in allowlist_value if item.strip()),
        minimum_confidence=float(risk.get("minimum_confidence", 0.8)),
        max_order_krw=float(risk.get("max_order_krw", 0)),
        max_position_percent=float(risk.get("max_position_percent", 0)),
        max_orders_per_run=int(risk.get("max_orders_per_run", 0)),
        max_daily_loss_krw=float(risk.get("max_daily_loss_krw", 0)),
        max_quote_age_seconds=int(risk.get("max_quote_age_seconds", 0)),
        require_market_open=_boolean(risk.get("require_market_open", True), "risk.require_market_open"),
    )
    if not 0 <= policy.minimum_confidence <= 1:
        raise PolicyError("minimum_confidence must be between 0 and 1")
    if policy.max_order_krw <= 0 or not 0 < policy.max_position_percent <= 100:
        raise PolicyError("order and position limits must be positive")
    if policy.max_orders_per_run < 1 or policy.max_quote_age_seconds < 0 or policy.max_daily_loss_krw <= 0:
        raise PolicyError("order count and quote age limits are invalid")
    return policy
