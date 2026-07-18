# Safety and secrets

## Required architecture

Use this one-way path:

`market/account data -> sanitized context -> model proposal -> schema validation -> deterministic RiskGate -> broker adapter -> reconciliation -> Telegram`

No prompt, news article, model response, Telegram message, or issue content may invoke the broker directly.

## Live-order prerequisites

Keep the live order path unavailable until all are implemented and tested:

- official live API access and current provider documentation
- real-time quote source and freshness threshold
- balance, buying power, open-order, and filled-order reconciliation
- stable idempotency key persisted outside an ephemeral runner
- market calendar, session, volatility interruption, and holiday handling
- allowlist, quantity, cash, position, daily loss, order count, and price-deviation limits
- retry classification that never blindly repeats an ambiguous order request
- kill switch and documented rollback
- paper-environment and contract tests

GitHub Actions runners are ephemeral. An in-memory or runner-local file is not adequate duplicate-order protection for live trading.

## Secret rules

- Never accept secret values in chat, prompts, issues, commits, workflow inputs, logs, artifacts, cache keys, or Telegram.
- Use GitHub Actions Secrets or environment Secrets. Use Variables only for non-secret policy.
- Workflows must use minimal `permissions`, `persist-credentials: false`, timeouts, and concurrency groups.
- Never run untrusted pull-request code with broker or Telegram secrets.
- Never expose secrets to model input. Sanitize raw broker responses and identifiers before logging or analysis.
- Examples contain obvious placeholders and secret names only.

## Public-repository warning

A public automation repository must contain no portfolio, account, tax, identity, or credential data. Forked scheduled workflows start disabled, but pull requests and workflow changes still require careful review. Keep production deployment environments and live credentials outside public defaults.
