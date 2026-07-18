# Onboarding contract

Collect decisions, never credentials. Ask one compact stage at a time and write the accepted answers to `config/investment-policy.yaml` and the operations guide.

## Stage 1: repository

- Authorized local path or `owner/repository`
- Target branch and whether Codex may create a branch/commit/push
- Existing or new project

Inspect current changes before editing. A repository URL does not by itself authorize changing visibility, repository settings, Secrets, environments, or branch protection.

## Stage 2: integrations

- Broker: `dry-run`, `kis`, `ls`, or `shinhan`
- Intended outcome: research-only or paper trading
- Market scope: Korean equities/ETFs only by default
- Optional OpenAI analysis: yes/no
- Optional Telegram notification: yes/no

Return secret names, not prompts for values. Typical names are `OPENAI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, and provider-specific paper-environment fields defined from current official documentation. Do not collect or implement live-order credentials.

## Stage 3: policy

- Core/satellite percentages; default 50/50 only when the user declines to choose
- Investment horizon and rebalance cadence
- Maximum loss/drawdown behavior
- Minimum cash reserve
- Maximum amount per order and per day
- Maximum position weight and orders per run
- Approved ticker allowlist and forbidden products
- Whether newly discovered symbols require manual approval; default yes

Do not infer suitability from age, occupation, or other sensitive traits. Do not recommend a security. Translate the user's explicit choices into deterministic limits.

## Stage 4: schedule

- Report times in `Asia/Seoul`; suggested 09:05, 12:05, 16:05 weekdays
- Paper evaluation cadence; suggested hourly at minute 10 during market hours
- Holiday behavior and manual pause procedure

GitHub schedule is not an exact timer. Offset jobs from minute zero, include `workflow_dispatch`, use concurrency controls, and document possible delay/drop behavior.

## Stage 5: confirmation

Show a concise summary before material repository or GitHub mutations. Explicitly state:

- paper/dry-run status
- live adapter status
- approved symbols and limits
- files/workflows to create or change
- Secrets/Variables names the user must configure outside chat
