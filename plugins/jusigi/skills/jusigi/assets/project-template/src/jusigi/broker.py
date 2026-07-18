"""Broker boundary. Only DryRunBroker is intentionally usable in the starter."""

from __future__ import annotations

from dataclasses import dataclass

from .models import OrderIntent, Quote


class BrokerUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class ExecutionResult:
    accepted: bool
    broker: str
    message: str


class DryRunBroker:
    name = "dry-run"

    def submit(self, intent: OrderIntent, quote: Quote) -> ExecutionResult:
        return ExecutionResult(True, self.name, f"simulated {intent.action} {intent.quantity} {intent.ticker} at {quote.price}")


class DisabledLiveBroker:
    def __init__(self, provider: str) -> None:
        self.name = provider

    def submit(self, intent: OrderIntent, quote: Quote) -> ExecutionResult:
        raise BrokerUnavailable(
            f"{self.name} live execution is not implemented or enabled; verify official docs and paper-test an adapter first"
        )
