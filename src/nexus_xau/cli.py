from __future__ import annotations

import argparse

import pandas as pd

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


def main() -> int:
    parser = argparse.ArgumentParser(prog="nexus-xau")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("smoke", help="run a local replay-engine smoke test")
    args = parser.parse_args()

    if args.command == "smoke":
        return _smoke()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
