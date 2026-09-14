from __future__ import annotations

import argparse
from pathlib import Path

from nexus_xau.data.mt5_collector_corner import run_corner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Small always-on-top desktop status for the MT5 collector."
    )
    parser.add_argument(
        "--status",
        type=Path,
        default=Path("results/mt5_collector/status.json"),
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("data/raw/mt5/XAUUSDm_ticks.sqlite3"),
    )
    parser.add_argument(
        "--dashboard-url",
        default="http://127.0.0.1:8765/",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    run_corner(
        status_path=args.status,
        db_path=args.db,
        dashboard_url=args.dashboard_url,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
