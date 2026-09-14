from __future__ import annotations

import argparse
from pathlib import Path

from nexus_xau.data.mt5_collector_dashboard import serve_dashboard


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local read-only status dashboard for the MT5 tick collector."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
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
    return parser


def main() -> int:
    args = build_parser().parse_args()
    print(
        f"NEXUS XAU collector dashboard: http://{args.host}:{args.port}/ "
        "(read-only)"
    )
    serve_dashboard(
        host=args.host,
        port=args.port,
        status_path=args.status,
        db_path=args.db,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
