from __future__ import annotations

import argparse
import json
from pathlib import Path

from nexus_xau.data.exness_tick_archive import scan_exness_archive_coverage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Map Exness-branded XAU tick archive object availability without "
            "downloading market outcomes or sending orders."
        )
    )
    parser.add_argument("--symbol", default="XAUUSDm")
    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--end-year", type=int, required=True)
    parser.add_argument("--months", type=int, nargs="*")
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = scan_exness_archive_coverage(
        symbol=args.symbol,
        start_year=args.start_year,
        end_year=args.end_year,
        months=args.months,
        output_jsonl=args.output_jsonl,
        timeout_seconds=args.timeout_seconds,
    )
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["summary"]["status_counts"].get("ERROR", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
