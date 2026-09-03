# Dukascopy Multi-Year XAUUSD Research Data Pipeline — 2026-09-03

Status: ACTIVE ENGINEERING / RESEARCH-DATA FOUNDATION

## Goal

Create a restart-safe multi-year XAUUSD M1 research dataset without requiring the project owner to manually export one day at a time from the Dukascopy Historical Data Export web page.

This dataset is for research, hypothesis testing, rule decoding and held-out validation. It is not assumed identical to the eventual Exness/MT5 execution feed.

## Source

Dukascopy Historical Data Export exposes historical quotes and allows BID / ASK selection in the web UI.

For automatic retrieval, the project now uses Dukascopy daily compressed M1 candle files under the public datafeed path:

```text
https://datafeed.dukascopy.com/datafeed/{SYMBOL}/{YYYY}/{ZERO_BASED_MONTH}/{DD}/BID_candles_min_1.bi5
```

Example for XAUUSD, 2022-09-01:

```text
.../XAUUSD/2022/08/01/BID_candles_min_1.bi5
```

Important: the path month is zero-based; September is `08`.

## Decoder

New module:

```text
src/nexus_xau/data/dukascopy_export.py
```

Daily M1 candle record layout used by the decoder:

```text
>5If
seconds_from_UTC_day_start
open_raw
close_raw
low_raw
high_raw
volume_float32
```

For XAUUSD the currently registered price divisor is:

```text
1000.0
```

The output is normalized to:

```text
timestamp,open,high,low,close,volume
```

with UTC-aware timestamps.

Unknown instruments do not receive a guessed divisor; they require an explicit divisor.

## Restart-safe behavior

Daily compressed `.bi5` files are cached under local/gitignored research storage.

Default cache:

```text
data/raw/dukascopy/cache/
```

Successful days are reused on rerun, so an interrupted multi-year download can resume without re-downloading completed days.

Network failures are recorded separately from market no-data days. A network failure must not be silently interpreted as a weekend/holiday.

## CLI / direct module usage

Single day:

```powershell
.\.venv\Scripts\python.exe -m nexus_xau.data.dukascopy_export `
  --symbol XAUUSD `
  --side BID `
  --start 2022-09-01 `
  --end 2022-09-01 `
  --out data/raw/dukascopy/XAUUSD_M1_BID_2022-09-01.csv
```

Multi-year target:

```powershell
.\.venv\Scripts\python.exe -m nexus_xau.data.dukascopy_export `
  --symbol XAUUSD `
  --side BID `
  --start 2022-09-01 `
  --end 2026-09-01 `
  --out data/raw/dukascopy/XAUUSD_M1_BID_2022-09-01_2026-09-01.csv
```

Date range is inclusive.

## Runtime validation completed

### Dukascopy 2022-09-01 BID

Automatic datafeed retrieval succeeded:

```text
rows = 1440 M1 bars
days_with_data = 1
days_failed = 0
```

This confirms the raw endpoint, LZMA decoder, XAUUSD price scale and UTC timestamp construction are operational for that day.

### Cross-feed check against existing Exness/MT5 data

Comparison date:

```text
2026-08-24 UTC
```

Counts:

```text
Dukascopy BID M1 = 1440
Exness/MT5 XAUUSDm M1 = 1378
common timestamps = 1378
```

Absolute close-price differences on common timestamps:

```text
median = 0.2435 USD
95th percentile = 0.5640 USD
maximum = 1.1510 USD
```

Observed close ranges:

```text
Dukascopy = 4596.425 .. 4681.385
Exness/MT5 = 4596.877 .. 4681.739
```

Interpretation:

- timestamp alignment is correct on the overlapping bars;
- XAUUSD price scaling is correct in magnitude;
- feeds are close but not identical, as expected;
- Dukascopy must therefore remain explicitly tagged as a separate research feed;
- wick-sensitive rules should later receive cross-feed robustness checks before production use.

## ASK status

The Dukascopy web exporter visibly supports ASK data, and the project owner has manually exported ASK files from the web UI.

However, the direct daily `ASK_candles_min_1.bi5` path tested for 2026-08-24 returned no usable M1 bars.

Therefore:

```text
BID direct M1 datafeed = RUNTIME VERIFIED
ASK direct daily M1 datafeed = NOT YET VERIFIED
```

Do not silently fabricate ASK from BID.

If ASK becomes necessary for spread/execution research, use either:

1. verified ASK daily data if a correct endpoint is established; or
2. Dukascopy tick files containing both bid and ask and aggregate them explicitly.

For current candle-pattern / frame / location research, BID is sufficient as the first multi-year research feed.

## Research split policy once multi-year data exists

Do not repeatedly reuse the same final holdout while inventing new hypotheses.

Recommended first partition after data quality validation:

```text
2022-09 -> 2024-08 : hypothesis discovery / rule decoding
2024-09 -> 2025-08 : validation
2025-09 -> 2026-05 : secondary validation / regime check
2026-06 -> 2026-09 : untouched final holdout where practical
```

Exact boundaries may be adjusted before the first multi-year hypothesis is frozen, but once a final holdout is declared it must not be used for iterative rule tuning.

## What this changes

The project no longer needs to treat every unresolved rule as an indefinite evidence-collection blocker.

With multi-year data plus labeled teaching examples, the research loop can become:

```text
UNKNOWN RULE
-> enumerate measurable candidate definitions
-> reject candidates that contradict labeled source examples
-> test surviving candidates over historical data
-> narrow the parameter/rule space
-> validate on fresh periods
-> PROVISIONAL / VALIDATED / REJECTED / INDISTINGUISHABLE
```

Historical performance cannot by itself prove what the instructor originally meant, but it can eliminate implausible variants, show which distinctions matter, and target the next evidence question efficiently.
