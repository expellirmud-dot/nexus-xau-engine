from __future__ import annotations

import argparse
import json
from pathlib import Path

import MetaTrader5 as mt5

from nexus_xau.data.mt5_cost_evidence import probe_mt5_cost_evidence


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capture read-only MT5 commission/fee/swap observability evidence."
    )
    parser.add_argument("--symbol", default="XAUUSDm")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/mt5_cost_evidence/current_runtime_v01.json"),
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = probe_mt5_cost_evidence(mt5, symbol=args.symbol)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())