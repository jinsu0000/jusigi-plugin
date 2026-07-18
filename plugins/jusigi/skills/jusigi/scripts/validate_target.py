#!/usr/bin/env python3
"""Validate safety-critical files in a generated Jusigi target."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED = (
    "AGENTS.md",
    "config/investment-policy.yaml",
    ".github/workflows/ci.yml",
    ".github/workflows/market-report.yml",
    ".github/workflows/paper-trade.yml",
    "src/jusigi/risk_gate.py",
    "tests/test_risk_gate.py",
)
SECRET_PATTERNS = (
    re.compile(r"gh[oprsu]_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    policy_path = root / "config/investment-policy.yaml"
    if policy_path.is_file():
        policy = policy_path.read_text(encoding="utf-8")
        if "live_enabled: false" not in policy:
            errors.append("policy must contain live_enabled: false")
        if "short_selling_enabled: false" not in policy:
            errors.append("policy must contain short_selling_enabled: false")

    ignored = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in ignored for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                errors.append(f"possible secret pattern: {path.relative_to(root)}:{line_number}")

    if errors:
        print("validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("target validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
