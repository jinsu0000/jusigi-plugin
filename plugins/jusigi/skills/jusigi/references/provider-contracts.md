# Provider adapter contract

Provider APIs and eligibility change. Before implementing any adapter, use current official documentation and record the source URL and verification date in the generated operations guide.

## Required broker protocol

Implement explicit methods for:

- authentication/token refresh
- real-time quote with provider timestamp
- account balance and buying power
- holdings and average prices
- open orders and recent fills
- submit order with client idempotency key when supported
- query/cancel order
- paper/live environment identity

Normalize responses into internal models. Keep provider transaction codes and endpoints isolated inside the adapter.

## Fail-closed contract

Raise a typed unavailable/ambiguous error rather than returning zero or an empty collection when authentication, balance, quote freshness, or order status cannot be established. Never retry order submission automatically after a timeout unless reconciliation proves that no order exists.

## Provider selection

- `dry-run`: always available; must never make broker network calls.
- `kis`: generate an adapter only after verifying current KIS Developers paper/live capabilities and account eligibility.
- `ls`: generate an adapter only after verifying current LS Securities OpenAPI paper/live capabilities and GitHub-hosted runner compatibility.
- `shinhan`: verify the currently offered Shinhan retail API and runtime requirements. Do not assume a Windows/ActiveX or HTTP interface from memory.

If official documents are unavailable or ambiguous, leave a typed stub that fails closed and explain the blocker.
