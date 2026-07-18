# Jusigi Plugin

Jusigi is a free, open-source Codex plugin that helps generate or audit user-controlled GitHub Actions automation for Korean stock research, Telegram reports, paper trading, and deterministic risk controls.

It is a code-generation workflow, not a hosted brokerage or investment-advice service. It never asks users to paste credentials into chat or committed files, and setup never places an order.

## Install

```bash
codex plugin marketplace add jinsu0000/jusigi-plugin
codex plugin add jusigi@jusigi-plugins
```

Invoke the installed Skill explicitly in Codex CLI or the IDE:

```text
Use $jusigi to scaffold Korean stock research and paper-trading automation in my repository.
```

The supported Skill mention is `$jusigi`, not `/jusigi`.

## Safety defaults

- Paper/dry-run only; live trading and short selling are disabled.
- An empty user-approved allowlist blocks all orders.
- Model output is an untrusted proposal and cannot bypass deterministic code.
- Broker adapters fail closed until current official documentation, paper tests, real-time quote validation, idempotency, and reconciliation are complete.
- Users configure credential values directly in GitHub Secrets outside chat.

Version 0.1 ships the reusable repository contract, generator, risk gate, dry-run broker, tests, and scheduled workflow baseline. Provider-specific market/news and broker adapters are completed by Codex during explicit, repository-scoped onboarding.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [SUPPORT.md](SUPPORT.md).

Jusigi is software, not investment advice or a promise of returns. MIT License.
