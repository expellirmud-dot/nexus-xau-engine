# Python Replay Engine Starter — 2026-09-02

Target runtime: Python 3.12.x (developer machine confirmed 3.12.9).

## Purpose

This first scaffold proves the local research pipeline before any cloud/mobile dependency:

`Historical OHLC -> loader -> timeframe builder -> deterministic replay -> detector contracts -> local event/report output`

It intentionally does **not** implement production trading logic whose numeric rules remain unresolved.

## Safety/evidence rules

- Historical timestamps must be timezone-aware; the loader refuses to guess a timezone.
- H4/D1 resampling boundaries are configurable because project timezone/session semantics are still open.
- Replay runs oldest-to-newest and rejects duplicate/unsorted timestamps.
- PAT detector currently fails closed as `WAIT / NOT_IMPLEMENTED` rather than inventing thresholds.
- Raw datasets and generated results are gitignored by default; keep raw source files immutable.
- Log rejected candidates/non-trades in later detector work to reduce selection bias.

## Windows setup

```powershell
cd D:\nexus-xau-engine-repo
git pull
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
nexus-xau smoke
```

Expected smoke output includes:

```text
Replay OK: 3 bars
PAT guard: WAIT / NOT_IMPLEMENTED
```

## Next implementation milestone

1. Confirm actual historical XAUUSD file schema and timezone.
2. Add checksum/metadata manifest for raw files.
3. Load one small continuous M1 Bid/Ask sample.
4. Verify M1 -> M5/H1/H4 aggregation against known candles.
5. Add replay event logging.
6. Implement only source-backed rule components first.
7. Keep ambiguous PAT/support-resistance/M5 thresholds configurable or human-confirmed until evidence closes them.

No Supabase, Vercel, MT5 live execution, or AUTO mode is required for this milestone.
