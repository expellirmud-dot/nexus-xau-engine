from __future__ import annotations

import argparse

import pandas as pd

from nexus_xau.data.audit import audit_ohlc_csv
from nexus_xau.data.mt5_export import export_mt5_m1, parse_aware_datetime
from nexus_xau.data.mt5_validate import validate_resample_against_mt5
from nexus_xau.detectors.pat import PatDetector
from nexus_xau.replay.engine import ReplayEngine
from nexus_xau.research.pat_topology_scan import run_pat_topology_research


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


def _audit_csv(args: argparse.Namespace) -> int:
    result = audit_ohlc_csv(
        args.input,
        processed_dir=args.processed_dir,
        report_path=args.report,
    )
    print(f"Dataset audit OK: {result.rows} M1 bars")
    print(f"UTC range: {result.start_utc} -> {result.end_utc}")
    print(f"1-minute steps: {result.one_minute_steps}")
    print(f"Gaps > 1 minute: {result.gaps_over_one_minute}")
    print(f"Largest gap: {result.largest_gap_seconds:.0f}s")
    for gap in result.gap_records:
        print(
            "Gap: "
            f"{gap.previous_utc} -> {gap.next_utc} "
            f"({gap.gap_seconds:.0f}s, missing_m1={gap.missing_m1_slots})"
        )
    print(
        "Resampled bars: "
        f"M5={result.m5_bars} / H1={result.h1_bars} / "
        f"H4={result.h4_bars} / D1={result.d1_bars}"
    )
    if args.processed_dir:
        print(f"Processed: {args.processed_dir}")
    if args.report:
        print(f"Report: {args.report}")
    return 0


def _validate_mt5_resample(args: argparse.Namespace) -> int:
    result = validate_resample_against_mt5(
        args.input,
        symbol=args.symbol,
        report_path=args.report,
        tolerance=args.tolerance,
    )
    print(f"MT5 resample validation: {result.symbol}")
    print(f"UTC range: {result.start_utc} -> {result.end_utc}")
    for item in result.comparisons:
        print(
            f"{item.timeframe}: local={item.local_bars} mt5={item.mt5_bars} "
            f"common={item.common_timestamps} only_local={item.only_local_timestamps} "
            f"only_mt5={item.only_mt5_timestamps} mismatches={item.ohlc_mismatch_rows} "
            f"max_diff={item.max_abs_ohlc_diff:.12g}"
        )
    if args.report:
        print(f"Report: {args.report}")
    return 0


def _scan_pat_topology(args: argparse.Namespace) -> int:
    result = run_pat_topology_research(
        args.input,
        report_path=args.report,
        hits_path=args.hits,
    )
    print("PAT research scan: COLOR TOPOLOGY ONLY / NOT A SIGNAL")
    print(f"UTC range: {result.start_utc} -> {result.end_utc}")
    for item in result.summaries:
        print(
            f"{item.timeframe}: bars={item.bars} "
            f"PAT2 BUY={item.pat2_buy_color_candidates} SELL={item.pat2_sell_color_candidates} "
            f"PAT3 BUY={item.pat3_buy_color_candidates} SELL={item.pat3_sell_color_candidates}"
        )
    print(f"Total topology hits: {result.total_hits}")
    print(
        "Omitted by design: S/R location, >50% basis/tolerance, "
        "PAT3 small-body/equal-wick thresholds, PAT1 geometry."
    )
    if args.report:
        print(f"Report: {args.report}")
    if args.hits:
        print(f"Hits: {args.hits}")
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

    audit_parser = sub.add_parser(
        "audit-csv",
        help="audit an M1 OHLC CSV and build M5/H1/H4/D1 validation outputs",
    )
    audit_parser.add_argument("--input", required=True)
    audit_parser.add_argument("--processed-dir", default=None)
    audit_parser.add_argument("--report", default=None)

    validate_parser = sub.add_parser(
        "validate-mt5-resample",
        help="compare local M1->M5/H1/H4/D1 bars with MT5 native timeframe bars",
    )
    validate_parser.add_argument("--input", required=True)
    validate_parser.add_argument("--symbol", required=True)
    validate_parser.add_argument("--report", default=None)
    validate_parser.add_argument("--tolerance", type=float, default=1e-9)

    scan_parser = sub.add_parser(
        "scan-pat-topology",
        help="research-only PAT2/PAT3 candle-color topology scan across M1/M5/H1/H4/D1",
    )
    scan_parser.add_argument("--input", required=True)
    scan_parser.add_argument("--report", default=None)
    scan_parser.add_argument("--hits", default=None)

    args = parser.parse_args()

    if args.command == "smoke":
        return _smoke()
    if args.command == "export-mt5":
        return _export_mt5(args)
    if args.command == "audit-csv":
        return _audit_csv(args)
    if args.command == "validate-mt5-resample":
        return _validate_mt5_resample(args)
    if args.command == "scan-pat-topology":
        return _scan_pat_topology(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
