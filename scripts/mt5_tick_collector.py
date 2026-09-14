from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from nexus_xau.data.mt5_tick_collector import run_live_collector


def _utc_msc(value: str) -> int:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise argparse.ArgumentTypeError("start time must include a timezone/UTC offset")
    return int(parsed.astimezone(UTC).timestamp() * 1000)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only MT5 XAUUSDm tick collector. ORDER SEND DISABLED."
    )
    parser.add_argument("--symbol", default="XAUUSDm")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("data/raw/mt5/XAUUSDm_ticks.sqlite3"),
    )
    parser.add_argument(
        "--status",
        type=Path,
        default=Path("results/mt5_collector/status.json"),
    )
    parser.add_argument(
        "--start-utc",
        type=_utc_msc,
        help=(
            "Explicit initial UTC timestamp with timezone, required only when the "
            "collector database has no prior state."
        ),
    )
    parser.add_argument("--duration-seconds", type=float, required=True)
    parser.add_argument("--poll-seconds", type=float, required=True)
    parser.add_argument("--chunk-seconds", type=int, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        import MetaTrader5 as mt5
    except ImportError as exc:
        raise SystemExit('MetaTrader5 package missing; install project extra "mt5"') from exc

    result = run_live_collector(
        mt5=mt5,
        symbol=args.symbol,
        db_path=args.db,
        status_path=args.status,
        explicit_start_msc=args.start_utc,
        duration_seconds=args.duration_seconds,
        poll_seconds=args.poll_seconds,
        chunk_seconds=args.chunk_seconds,
    )
    print(
        f"{result['state']} {result['mode']} "
        f"rows={result['rows_committed_session']} "
        f"last_msc={result['latest_committed_tick_time_msc']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
