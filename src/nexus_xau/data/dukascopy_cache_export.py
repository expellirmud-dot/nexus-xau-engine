from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from nexus_xau.data.dukascopy_export import decode_dukascopy_m1_bi5, price_divisor_for_symbol


def export_cached_range(*, symbol: str, side: str, start: date, end: date, cache_dir: Path, out: Path) -> dict[str, object]:
    divisor = price_divisor_for_symbol(symbol)
    frames: list[pd.DataFrame] = []
    missing: list[str] = []
    current = start
    while current <= end:
        path = cache_dir / symbol / f"{current.year:04d}" / f"{current.month:02d}" / f"{current.day:02d}" / f"{side}_candles_min_1.bi5"
        if path.exists():
            frame = decode_dukascopy_m1_bi5(path.read_bytes(), day=current, price_divisor=divisor)
            if not frame.empty:
                frames.append(frame)
        else:
            missing.append(current.isoformat())
        current += timedelta(days=1)
    merged = pd.concat(frames, ignore_index=True).sort_values("timestamp") if frames else pd.DataFrame(columns=["timestamp","open","high","low","close","volume"])
    out.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out, index=False, date_format="%Y-%m-%dT%H:%M:%S%z")
    meta = {
        "source": "Dukascopy cached daily M1 candle .bi5 only",
        "symbol": symbol,
        "side": side,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "rows": len(merged),
        "missing_cache_dates": missing,
        "complete_cache_range": not missing,
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    }
    out.with_suffix(out.suffix + ".meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", default="XAUUSD")
    p.add_argument("--side", default="BID")
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    p.add_argument("--cache-dir", default="data/raw/dukascopy/cache")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    meta = export_cached_range(symbol=a.symbol, side=a.side, start=date.fromisoformat(a.start), end=date.fromisoformat(a.end), cache_dir=Path(a.cache_dir), out=Path(a.out))
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
