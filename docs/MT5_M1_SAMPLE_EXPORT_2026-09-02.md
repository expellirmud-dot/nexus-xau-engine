# First real MT5 M1 sample — pipeline validation

Date: 2026-09-02

## Goal

Create one small, reproducible, real XAUUSD M1 dataset from the user's MT5 Desktop installation so we can validate:

1. symbol/data access;
2. timestamp handling and UTC normalization;
3. chronological continuity/duplicates;
4. M1 -> M5/H1/H4 resampling boundaries;
5. agreement with known MT5 candles before any trading logic is encoded.

This sample is **not** the final multi-year backtest dataset and is **not** sufficient for win-rate conclusions.

## Chosen first window

Use one completed trading week:

- start: `2026-08-24T00:00:00+00:00`
- end: `2026-08-29T00:00:00+00:00`

The explicit UTC range is intentional. Do not replace it with a local/naive datetime without recording the timezone.

## Windows commands

MT5 Desktop should be installed, logged in, and able to display the target `XAUUSD` symbol.

```powershell
cd D:\nexus-xau-engine-repo
git pull
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,mt5]"
pytest

nexus-xau export-mt5 `
  --symbol XAUUSD `
  --start 2026-08-24T00:00:00+00:00 `
  --end   2026-08-29T00:00:00+00:00 `
  --out data/raw/XAUUSD_M1_MT5_2026-08-24_2026-08-28.csv
```

Expected files:

```text
data/raw/XAUUSD_M1_MT5_2026-08-24_2026-08-28.csv
data/raw/XAUUSD_M1_MT5_2026-08-24_2026-08-28.csv.meta.json
```

The CSV uses the replay-loader-compatible columns:

```text
timestamp,open,high,low,close,volume,spread,real_volume
```

`timestamp` is written in UTC with an explicit offset.

## Important limitation

`MetaTrader5.copy_rates_range()` returns M1 bar data suitable for validating the pipeline and resampling, but this is not equivalent to a final Bid+Ask/tick execution-quality dataset. Spread/slippage/execution studies require stronger source data later.

## Failure handling

If the exporter returns zero rows or cannot select `XAUUSD`, do not rename a different symbol silently. Record the actual broker symbol and investigate it first.

If the export succeeds, do not commit the raw CSV to Git. `data/raw` is intentionally local/ignored.
