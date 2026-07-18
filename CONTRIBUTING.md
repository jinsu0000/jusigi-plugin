# Contributing

Contributions are welcome, especially deterministic risk tests, Korean broker paper-environment adapters, data-freshness checks, and Korean documentation.

## Rules

- Do not include credentials, real account/portfolio data, certificates, or raw broker payloads with identifiers.
- Use synthetic fixtures and network-free unit tests.
- Keep live trading disabled in examples and CI.
- Link official provider documentation and record the verification date for provider behavior.
- Do not weaken the allowlist, freshness, cash, quantity, position, session, duplicate-order, or loss checks.
- Keep model output separated from broker execution.

## Check a change

```bash
python -m compileall -q plugins/jusigi/skills/jusigi/scripts
python plugins/jusigi/skills/jusigi/scripts/scaffold.py --target /tmp/jusigi-test --broker dry-run
python plugins/jusigi/skills/jusigi/scripts/validate_target.py /tmp/jusigi-test
python -m pip install -r /tmp/jusigi-test/requirements.txt
PYTHONPATH=/tmp/jusigi-test/src python -m unittest discover -s /tmp/jusigi-test/tests -v
```

Open an issue before a large provider integration so its paper/live scope, official references, and test fixtures can be agreed first.
