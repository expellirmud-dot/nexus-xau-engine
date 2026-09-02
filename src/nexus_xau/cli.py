from __future__ import annotations

import argparse

import pandas as pd

from nexus_xau.data.mt5_export import export_mt5_m1, parse_aware_datetime
from nexus_xau.detectors.pat import PatDetector
from nexus_xau.replay.engine import ReplayEngine


def _smoke() -> int:
    index = pd.date_range("2026-01-01T00:00:00Z", periods=3, freq="1min")
    bars = pd.DataFrame(
        {
            "open": [100.0, 101.0, 102.0],
            "high": [102.0, 103.0, 104.0],
            "low": [99.0, 100.0, 101.0],
            "close": [101.0, 102.0, 103.0],
        },
        index=index,
    )
    stats = ReplayEngine().run(bars)
    pat = PatDetector().evaluate()
    print(f"Replay OK: {stats.bars_processed} bars")
    print(f"PAT guard: {pat.decision} / {pat.evidence_status}")
    return 0


def _export_mt5(args: argparse.Namespace) -> int:
    result = export_mt5_m1(
        symbol=args.symbol,
        start=parse_aware_datetime(args.start),
        end=parse_aware_datetime(args.end),
        output_path=args.out,
    )
    print(f"MT5 export OK: {result.rows} M1 bars")
    print(f"CSV: {result.csv_path}")
    print(f"Metadata: {result.metadata_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="nexus-xau")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("smoke", help="run a local replay-engine smoke test")

    export_parser = sub.add_parser(
        "export-mt5",
        help="export a reproducible XAUUSD M1 sample from MT5",
    )
    export_parser.add_argument("--symbol", default="XAUUSD")
    export_parser.add_argument(
        "--start",
        required=True,
        help="timezone-aware ISO-8601 start, e.g. 2026-08-24T00:00:00+00:00",
    )
    export_parser.add_argument(
        "--end",
        required=True,
        help="timezone-aware ISO-8601 end, e.g. 2026-08-29T00:00:00+00:00",
    )
    export_parser.add_argument(
        "--out",
        default="data/raw/XAUUSD_M1_mt5_sample.csv",
    )

    args = parser.parse_args()

    if args.command == "smoke":
        return _smoke()
    if args.command == "export-mt5":
        return _export_mt5(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
