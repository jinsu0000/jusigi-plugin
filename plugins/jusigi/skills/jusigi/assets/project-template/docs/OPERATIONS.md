# Operations guide

## Runtime state

- Broker selected during scaffolding: `__JUSIGI_BROKER__`
- Live orders: disabled
- Paper order entry: implemented only for deterministic JSON fixtures until market/model adapters are added and tested
- Persistent idempotency: not implemented; therefore unsuitable for live orders

## Required setup

1. Review `config/investment-policy.yaml` and add only user-approved symbols.
2. Run CI and `healthcheck` locally.
3. Implement market, news, account, and provider adapters from current official documentation.
4. Record each source URL, verification date, data freshness, rate limit, paper/live distinction, and account eligibility here.
5. Paper-test failures, timeouts, duplicate responses, partial fills, reconciliation, and Telegram outages.

## Pause and rollback

- Disable `market-report.yml` and `paper-trade.yml` from the GitHub Actions UI or CLI.
- Keep `mode.live_enabled: false`.
- Remove or rotate affected GitHub Secrets after suspected exposure.
- Reconcile broker open orders and fills directly with the broker before resuming.
- Revert the exact automation commit only after preserving incident evidence.

## Scheduling

Report cron (UTC): `__JUSIGI_REPORT_CRON__`

Paper-trade cron (UTC): `__JUSIGI_TRADE_CRON__`

GitHub scheduled jobs are best-effort. They can be delayed or dropped during high load and run only from the default branch. Do not use them as the sole clock or reconciliation system for live trading.
