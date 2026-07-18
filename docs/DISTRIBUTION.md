# Distribution plan

## 1. GitHub marketplace repository

The repository root contains `.agents/plugins/marketplace.json`, so users can install it with:

```bash
codex plugin marketplace add jinsu0000/jusigi-plugin
codex plugin add jusigi@jusigi-plugins
```

Use a tagged semantic version and GitHub Release after each tested milestone. Keep a Korean-first README, an English README, concrete starter prompts, a short demo, topics, Discussions, and beginner-friendly issues.

## 2. Public Plugins Directory

Submit this as a skills-only plugin after local and external testing. Prepare:

- verified OpenAI developer or business identity
- Apps Management write permission
- public name, descriptions, logo, category, website, support, privacy, and terms URLs
- final skill bundle/ZIP
- starter prompts
- exactly five positive and three negative test cases
- countries/regions, release notes, and policy attestations

The review portal is `https://platform.openai.com/plugins`. Submission starts review; approval and a separate publish action are required before public directory availability.

## 3. Trust before reach

- Publish a 60–90 second Korean demo showing installation, staged onboarding, generated diff, dry-run test, and Telegram result.
- Maintain an explicit feature/status table: scaffold, paper-tested adapters, live-disabled adapters, and independently verified behavior.
- Publish threat model and incident/credential-rotation guidance.
- Ask early users to share only sanitized generated diffs and paper-test results.
- Label beginner issues and maintain a provider-adapter checklist.

[OpenAI's public app guidelines](https://developers.openai.com/apps-sdk/app-guidelines) prohibit execution of investment trades. Keep the directory submission strictly research/paper-oriented, never collect authentication secrets, and do not generate live order endpoints through the public Skill. Approval is still subject to OpenAI review.
