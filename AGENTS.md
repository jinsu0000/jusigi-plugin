# Jusigi plugin development guidance

## Repository layout

- `.agents/plugins/marketplace.json` is the public marketplace catalog.
- `plugins/jusigi/.codex-plugin/plugin.json` is the plugin manifest.
- `plugins/jusigi/skills/jusigi/SKILL.md` is the workflow contract.
- `plugins/jusigi/skills/jusigi/references/` contains instructions loaded only when needed.
- `plugins/jusigi/skills/jusigi/scripts/` contains deterministic scaffold and validation helpers.
- `plugins/jusigi/skills/jusigi/assets/project-template/` is copied into user-authorized repositories.
- `submission/` contains public review fixtures, not runtime credentials.

## Product boundary

Jusigi generates and audits source code in user-controlled repositories. It is not a hosted broker, signal service, investment adviser, or secret-collection interface.

## Safety invariants

- Never ask for, store, log, commit, or echo credential values or real account/portfolio data.
- Never add, generate, modify, or enable a live investment-trade endpoint in this public plugin.
- Keep the generated template live-disabled, short-selling-disabled, and allowlist-deny-by-default.
- Keep model output separated from deterministic risk checks and broker execution.
- Preserve the five positive and three negative public-submission cases unless submission requirements change.
- Examples and tests use synthetic data and no network access.

## Validation

```bash
python -m compileall -q plugins/jusigi/skills/jusigi/scripts
python plugins/jusigi/skills/jusigi/scripts/scaffold.py --target /tmp/jusigi-generated --broker dry-run --core-ratio 50
python plugins/jusigi/skills/jusigi/scripts/validate_target.py /tmp/jusigi-generated
PYTHONPATH=/tmp/jusigi-generated/src python -m unittest discover -s /tmp/jusigi-generated/tests -v
```

Also run the installed `skill-creator` and `plugin-creator` validators before releases. Review workflow permissions and scan the repository for secret patterns without printing candidate values.

## Release checklist

- Update manifest semver and release notes.
- Test marketplace installation in a clean environment.
- Forward-test all submission cases.
- Verify public privacy, terms, support, and security links.
- State provider maturity accurately and describe only research or paper-environment support.
