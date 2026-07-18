#!/usr/bin/env python3
"""Copy the safe Jusigi starter into a user-authorized repository."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


BROKERS = ("dry-run", "kis", "ls", "shinhan")
TEXT_EXTENSIONS = {"", ".md", ".py", ".txt", ".yaml", ".yml", ".toml", ".example"}
CRON_PATTERN = re.compile(r"^[0-9*/?,\- ]+$")


def parse_ratio(value: str) -> int:
    ratio = int(value)
    if not 0 <= ratio <= 100:
        raise argparse.ArgumentTypeError("ratio must be between 0 and 100")
    return ratio


def parse_cron(value: str) -> str:
    if not CRON_PATTERN.fullmatch(value) or len(value.split()) != 5:
        raise argparse.ArgumentTypeError("cron must contain five safe POSIX fields")
    return value


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--broker", choices=BROKERS, default="dry-run")
    parser.add_argument("--core-ratio", type=parse_ratio, default=50)
    parser.add_argument("--report-cron", type=parse_cron, default="5 0,3,7 * * 1-5")
    parser.add_argument("--trade-cron", type=parse_cron, default="10 0-6 * * 1-5")
    parser.add_argument("--force", action="store_true", help="overwrite colliding files")
    parser.add_argument("--dry-run", action="store_true", help="show planned paths only")
    return parser.parse_args()


def render(source: Path, replacements: dict[str, str]) -> bytes:
    content = source.read_bytes()
    if source.suffix in TEXT_EXTENSIONS or source.name.startswith("."):
        text = content.decode("utf-8")
        for key, value in replacements.items():
            text = text.replace(key, value)
        return text.encode("utf-8")
    return content


def main() -> int:
    args = arguments()
    target = args.target.expanduser().resolve()
    template = Path(__file__).resolve().parent.parent / "assets" / "project-template"
    if not template.is_dir():
        print(f"template is missing: {template}", file=sys.stderr)
        return 2

    if target == Path(target.anchor):
        print("refusing to write to a filesystem root", file=sys.stderr)
        return 2
    target.mkdir(parents=True, exist_ok=True)

    files = sorted(path for path in template.rglob("*") if path.is_file())
    collisions = [target / path.relative_to(template) for path in files if (target / path.relative_to(template)).exists()]
    if collisions and not args.force:
        print("refusing to overwrite existing files:", file=sys.stderr)
        for path in collisions:
            print(f"- {path}", file=sys.stderr)
        return 3

    replacements = {
        "__JUSIGI_BROKER__": args.broker,
        "__JUSIGI_CORE_RATIO__": str(args.core_ratio),
        "__JUSIGI_SATELLITE_RATIO__": str(100 - args.core_ratio),
        "__JUSIGI_REPORT_CRON__": args.report_cron,
        "__JUSIGI_TRADE_CRON__": args.trade_cron,
    }
    for source in files:
        destination = target / source.relative_to(template)
        print(destination)
        if args.dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(render(source, replacements))
        shutil.copymode(source, destination)

    print(f"generated {len(files)} files; broker={args.broker}; live trading remains disabled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
