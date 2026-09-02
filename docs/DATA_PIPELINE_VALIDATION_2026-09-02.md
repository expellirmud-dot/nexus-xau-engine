# Data Pipeline Validation — 2026-09-02

Source class: USER-DIRECT RUNTIME OUTPUT
Environment: Exness demo / server `Exness-MT5Trial6`
Symbol: `XAUUSDm`
Branch: `build/python-replay-engine`

## Result

The first real MT5 M1 sample successfully passed local resampling validation against MT5 native timeframe bars.

Raw local sample:

- symbol: `XAUUSDm`
- UTC request window: `2026-08-24T00:00:00+00:00` to `2026-08-29T00:00:00+00:00`
- actual last bar: `2026-08-28T20:57:00+00:00`
- M1 rows: `6,770`
- raw CSV remains local/gitignored

Audit:

- one-minute steps: `6,765`
- gaps > 1 minute: `4`
- largest gap: `3,780s` (63 minutes)
- resampled bars: `M5=1,356`, `H1=113`, `H4=30`, `D1=5`

Gap records:

1. `2026-08-24T20:57:00+00:00 -> 2026-08-24T22:00:00+00:00` — `3,780s`, missing M1 slots `62`
2. `2026-08-25T20:57:00+00:00 -> 2026-08-25T22:00:00+00:00` — `3,780s`, missing M1 slots `62`
3. `2026-08-26T20:57:00+00:00 -> 2026-08-26T22:00:00+00:00` — `3,780s`, missing M1 slots `62`
4. `2026-08-27T20:57:00+00:00 -> 2026-08-27T22:00:00+00:00` — `3,780s`, missing M1 slots `62`

The repeated same-time daily pattern is **consistent with a broker/session pause**, not random missing-data corruption. This conclusion is environment-specific and should not be generalized to other brokers/servers without verification.

## Native MT5 comparison

Local M1 resampling was compared timestamp-by-timestamp and OHLC-by-OHLC against MT5 native timeframe bars.

```text
M5: local=1356 mt5=1356 common=1356 only_local=0 only_mt5=0 mismatches=0 max_diff=0
H1: local=113  mt5=113  common=113  only_local=0 only_mt5=0 mismatches=0 max_diff=0
H4: local=30   mt5=30   common=30   only_local=0 only_mt5=0 mismatches=0 max_diff=0
D1: local=5    mt5=5    common=5    only_local=0 only_mt5=0 mismatches=0 max_diff=0
```

## Engineering conclusion

For this sample/environment, the following are now validated:

- MT5 Python IPC works;
- M1 historical bar export works;
- timestamps are normalized correctly to UTC;
- M1 chronological order is stable;
- local `M1 -> M5/H1/H4/D1` resampling boundaries match MT5 exactly;
- local OHLC aggregation matches MT5 exactly for every compared bar.

This closes the first data/timeframe foundation milestone.

## What this does NOT prove

This result does not yet prove:

- final execution-quality backtest data quality;
- Bid+Ask tick reconstruction;
- representative spread/slippage;
- equivalence of `XAUUSDm` with eventual production `XAUUSD`;
- trading-rule correctness;
- PAT/SIG/M5-brake detector correctness;
- strategy win rate.

## Next milestone

Proceed to the first source-backed logic layer only:

1. closed-candle semantics;
2. candle feature extraction (color/body/wicks/range/extremes);
3. deterministic PAT window/candle numbering contracts;
4. confirmed post-SIG reference mapping (`PAT1 -> #2`, `PAT2 -> #3`, `PAT3 -> #4`);
5. event/reason logging;
6. leave unresolved PAT thresholds, support/resistance tolerance, and M5 force thresholds parameterized or fail-closed.

Do not start production AUTO execution or claim strategy performance from this five-day sample.
