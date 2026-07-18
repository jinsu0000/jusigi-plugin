import unittest

from jusigi.models import Account, OrderIntent, Quote
from jusigi.policy import RiskPolicy
from jusigi.risk_gate import RiskGate


def policy(**overrides):
    values = {
        "broker_provider": "dry-run",
        "live_enabled": False,
        "short_selling_enabled": False,
        "minimum_cash_reserve_krw": 100_000,
        "allowlist": frozenset({"005930"}),
        "minimum_confidence": 0.8,
        "max_order_krw": 100_000,
        "max_position_percent": 30,
        "max_orders_per_run": 1,
        "max_daily_loss_krw": 100_000,
        "max_quote_age_seconds": 30,
        "require_market_open": True,
    }
    values.update(overrides)
    return RiskPolicy(**values)


def intent(**overrides):
    values = {"intent_id": "run-1", "ticker": "005930", "action": "buy", "quantity": 1, "confidence": 0.9}
    values.update(overrides)
    return OrderIntent(**values)


def quote(**overrides):
    values = {"ticker": "005930", "price": 50_000, "age_seconds": 5, "market_open": True, "source": "fixture"}
    values.update(overrides)
    return Quote(**values)


def account(**overrides):
    values = {"cash_krw": 1_000_000, "holdings": {}, "market_values": {}, "daily_pnl_krw": 0}
    values.update(overrides)
    return Account(**values)


class RiskGateTests(unittest.TestCase):
    def evaluate(self, proposed=None, market=None, portfolio=None, count=0, configured=None):
        return RiskGate(configured or policy()).evaluate(proposed or intent(), market or quote(), portfolio or account(), count)

    def test_approves_bounded_dry_run(self):
        self.assertTrue(self.evaluate().approved)

    def test_rejects_ticker_outside_allowlist(self):
        self.assertFalse(self.evaluate(proposed=intent(ticker="000660"), market=quote(ticker="000660")).approved)

    def test_rejects_stale_quote(self):
        self.assertFalse(self.evaluate(market=quote(age_seconds=31)).approved)

    def test_rejects_low_confidence(self):
        self.assertFalse(self.evaluate(proposed=intent(confidence=0.79)).approved)

    def test_rejects_closed_market(self):
        self.assertFalse(self.evaluate(market=quote(market_open=False)).approved)

    def test_rejects_duplicate(self):
        self.assertFalse(self.evaluate(portfolio=account(processed_intent_ids={"run-1"})).approved)

    def test_rejects_order_limit(self):
        self.assertFalse(self.evaluate(proposed=intent(quantity=3)).approved)

    def test_rejects_cash_reserve(self):
        self.assertFalse(self.evaluate(portfolio=account(cash_krw=120_000)).approved)

    def test_rejects_position_limit(self):
        concentrated = account(cash_krw=1_000_000, market_values={"005930": 400_000})
        self.assertFalse(self.evaluate(portfolio=concentrated).approved)

    def test_rejects_sell_above_holdings(self):
        self.assertFalse(self.evaluate(proposed=intent(action="sell", quantity=2), portfolio=account(holdings={"005930": 1})).approved)

    def test_rejects_daily_loss_limit(self):
        self.assertFalse(self.evaluate(portfolio=account(daily_pnl_krw=-100_000)).approved)

    def test_rejects_order_count(self):
        self.assertFalse(self.evaluate(count=1).approved)

    def test_rejects_model_risk_flags(self):
        self.assertFalse(self.evaluate(proposed=intent(risk_flags=("conflicting_data",))).approved)

    def test_rejects_live_policy_even_if_constructed(self):
        self.assertFalse(self.evaluate(configured=policy(live_enabled=True)).approved)


if __name__ == "__main__":
    unittest.main()
