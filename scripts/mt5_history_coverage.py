from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from nexus_xau.data.mt5_coverage import scan_mt5_history_coverage


def _date(value: str) -> date:
    return date.fromisoformat(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Probe MT5 XAU history availability without sending orders."
    )
    parser.add_argument("--symbol", default="XAUUSDm")
    parser.add_argument("--start-date", type=_date, required=True)
    parser.add_argument("--end-date", type=_date, required=True)
    parser.add_argument("--step-days", type=int, default=7)
    parser.add_argument("--probe-hour-utc", type=int, default=12)
    parser.add_argument("--window-minutes", type=int, default=5)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = scan_mt5_history_coverage(
        symbol=args.symbol,
        start_date=args.start_date,
        end_date=args.end_date,
        step_days=args.step_days,
        probe_hour_utc=args.probe_hour_utc,
        window_minutes=args.window_minutes,
        output_jsonl=args.output_jsonl,
    )
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
