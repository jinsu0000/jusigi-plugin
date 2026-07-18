"""Health, report, and deterministic paper-trade entry points."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict

from .broker import DryRunBroker
from .models import Account, OrderIntent, Quote
from .notifier import notify
from .policy import load_policy
from .risk_gate import RiskGate


def json_env(name: str) -> dict:
    raw = os.getenv(name)
    if not raw:
        raise ValueError(f"{name} is not configured; add a tested data/model adapter or a paper fixture")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a JSON object")
    return value


def run_healthcheck(policy_path: str) -> None:
    policy = load_policy(policy_path)
    print(json.dumps({"status": "ok", "broker": policy.broker_provider, "live_enabled": policy.live_enabled, "allowlist_count": len(policy.allowlist)}))


def run_report(policy_path: str) -> None:
    policy = load_policy(policy_path)
    message = (
        "Jusigi report scaffold is healthy. "
        f"broker={policy.broker_provider}, live=false, allowlist={len(policy.allowlist)}. "
        "Implement and verify current market/news adapters before using this as a market report."
    )
    print(message)
    notify(message)


def run_paper_trade(policy_path: str) -> None:
    policy = load_policy(policy_path)
    intent = OrderIntent(**json_env("JUSIGI_ORDER_INTENT_JSON"))
    quote = Quote(**json_env("JUSIGI_QUOTE_JSON"))
    account_data = json_env("JUSIGI_ACCOUNT_JSON")
    account_data["processed_intent_ids"] = set(account_data.get("processed_intent_ids", []))
    account = Account(**account_data)
    decision = RiskGate(policy).evaluate(intent, quote, account, orders_this_run=0)
    result = {"risk": asdict(decision), "execution": None}
    if decision.approved:
        result["execution"] = asdict(DryRunBroker().submit(intent, quote))
    message = json.dumps(result, ensure_ascii=False)
    print(message)
    notify(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("healthcheck", "report", "paper-trade"))
    parser.add_argument("--policy", default="config/investment-policy.yaml")
    args = parser.parse_args()
    {"healthcheck": run_healthcheck, "report": run_report, "paper-trade": run_paper_trade}[args.command](args.policy)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
