from __future__ import annotations

import argparse
import json
from pathlib import Path

from nexus_xau.data.exness_tick_archive import latest_records_by_month, load_existing_records
from nexus_xau.data.exness_tick_archive_download import download_and_validate_month


def parse_month(value: str) -> tuple[int, int]:
    try:
        year_text, month_text = value.split("-", 1)
        year = int(year_text)
        month = int(month_text)
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("month must be YYYY-MM") from exc
    if not 1 <= month <= 12:
        raise argparse.ArgumentTypeError("month must be YYYY-MM with month 01..12")
    return year, month


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download and stream-validate Exness-branded monthly XAUUSDm tick archives."
    )
    parser.add_argument("--symbol", default="XAUUSDm")
    parser.add_argument("--month", dest="months", action="append", type=parse_month, required=True)
    parser.add_argument(
        "--coverage-jsonl",
        type=Path,
        default=Path("results/exness_tick_archive/XAUUSDm_coverage_2015_2026.jsonl"),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("data/raw/exness_tick_history/archive"),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("results/exness_tick_archive/download_validation_manifest.jsonl"),
    )
    parser.add_argument("--timeout-seconds", type=float, default=60.0)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    coverage = latest_records_by_month(load_existing_records(args.coverage_jsonl))
    results: list[dict[str, object]] = []

    for year, month in args.months:
        entry = coverage.get((args.symbol, year, month))
        if entry is None or entry.status != "AVAILABLE":
            raise SystemExit(f"{year:04d}-{month:02d} is not AVAILABLE in coverage map")
        record = download_and_validate_month(
            symbol=args.symbol,
            year=year,
            month=month,
            output_root=args.output_root,
            manifest_path=args.manifest,
            expected_size=entry.file_size,
            timeout_seconds=args.timeout_seconds,
        )
        results.append(
            {
                "month": f"{year:04d}-{month:02d}",
                "status": record.status,
                "rows": record.row_count,
                "bytes": record.actual_size,
                "sha256": record.sha256,
                "first": record.first_timestamp,
                "last": record.last_timestamp,
                "path": record.local_path,
            }
        )

    print(json.dumps({"validated": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
