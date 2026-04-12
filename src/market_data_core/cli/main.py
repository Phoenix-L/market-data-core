"""Minimal CLI scaffold.

Commands intentionally return informative placeholders during bootstrap.
"""

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(prog="market-data-core")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("ingest", help="Ingest bars (placeholder)")
    sub.add_parser("validate", help="Validate dataset (placeholder)")
    sub.add_parser("inspect", help="Inspect dataset (placeholder)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    print(f"{args.command}: not implemented yet (bootstrap placeholder)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
