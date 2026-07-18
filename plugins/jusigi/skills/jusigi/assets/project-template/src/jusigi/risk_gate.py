"""Deterministic checks between any proposal and any broker."""

from __future__ import annotations

from .models import Account, OrderIntent, Quote, RiskDecision
from .policy import RiskPolicy


class RiskGate:
    def __init__(self, policy: RiskPolicy) -> None:
        self.policy = policy

    def evaluate(self, intent: OrderIntent, quote: Quote, account: Account, orders_this_run: int) -> RiskDecision:
        if intent.action == "hold":
            return RiskDecision(False, "hold creates no order")
        if self.policy.live_enabled:
            return RiskDecision(False, "starter never permits live trading")
        if intent.intent_id in account.processed_intent_ids:
            return RiskDecision(False, "duplicate intent_id")
        if intent.ticker != quote.ticker or intent.ticker not in self.policy.allowlist:
            return RiskDecision(False, "ticker is outside the approved allowlist")
        if intent.action not in {"buy", "sell"} or intent.quantity <= 0:
            return RiskDecision(False, "invalid action or quantity")
        if intent.confidence < self.policy.minimum_confidence:
            return RiskDecision(False, "confidence is below policy")
        if intent.risk_flags:
            return RiskDecision(False, "proposal contains risk flags")
        if quote.price <= 0 or quote.age_seconds > self.policy.max_quote_age_seconds:
            return RiskDecision(False, "quote is invalid or stale")
        if self.policy.require_market_open and not quote.market_open:
            return RiskDecision(False, "market is closed")
        if orders_this_run >= self.policy.max_orders_per_run:
            return RiskDecision(False, "maximum orders per run reached")
        if account.daily_pnl_krw <= -self.policy.max_daily_loss_krw:
            return RiskDecision(False, "daily loss limit reached")

        order_value = quote.price * intent.quantity
        if order_value > self.policy.max_order_krw:
            return RiskDecision(False, "order value exceeds policy")
        if intent.action == "sell" and intent.quantity > account.holdings.get(intent.ticker, 0):
            return RiskDecision(False, "sell quantity exceeds holdings")
        if intent.action == "buy":
            if account.cash_krw - order_value < self.policy.minimum_cash_reserve_krw:
                return RiskDecision(False, "cash reserve would be breached")
            projected_total = max(account.total_value_krw, account.cash_krw)
            current_value = account.market_values.get(intent.ticker, 0)
            projected_percent = (current_value + order_value) / projected_total * 100 if projected_total else 100
            if projected_percent > self.policy.max_position_percent:
                return RiskDecision(False, "position limit would be breached")
        return RiskDecision(True, "approved for dry-run only")
