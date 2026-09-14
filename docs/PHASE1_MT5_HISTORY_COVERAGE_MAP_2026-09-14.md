# Phase 1 MT5 Historical Coverage Map — 2026-09-14

Status: CURRENT EVIDENCE CHECKPOINT
Mode: READ-ONLY DATA / ORDER SEND DISABLED
Symbol: XAUUSDm

## Purpose

Determine what historical market data is actually accessible through the current Exness Demo -> MT5 terminal -> MetaTrader5 Python route.

This checkpoint separates:

- historical Bid/Ask tick accessibility;
- current terminal-visible M1 OHLC accessibility;
- probe coverage from full continuity;
- terminal/API window limits from broker/server retention claims.

Detailed scan outputs remain local under `results/mt5_coverage/`.

## Mapper

Implementation:

- `src/nexus_xau/data/mt5_coverage.py`
- `scripts/mt5_history_coverage.py`
- `tests/test_mt5_coverage.py`

Implementation checkpoint:

- `1589ff4 data: add restart-safe MT5 history coverage mapper`

Important contract:

- requested interval is interpreted as `[start_utc, end_utc)`;
- rows returned by MT5 outside that interval are recorded but do not count as interval availability;
- Tick and M1 are mapped independently;
- JSONL is appended and flushed per probe so a rerun can resume completed probe keys;
- no order API is used.

## Validation

Tests:

- MT5 coverage unit tests: PASS
- MT5 export/validate related tests: PASS in the implementation checkpoint validation
- Ruff on mapper/CLI/tests: PASS

Live smoke testing found an important API behavior:

- `copy_rates_range` can return a row outside the requested time interval when the requested M1 interval is older than the currently accessible M1 window;
- the end boundary can also be returned inclusively by MT5;
- therefore a successful non-empty response alone is NOT evidence that the requested historical interval exists.

The v0.2 mapper filters returned timestamps to the requested half-open interval before declaring availability.

## Scan A — Weekly coarse map

Durable job:

`XAU-MT5-HISTORY-COVERAGE-V02-20260914`

Range:

- 2022-09-01 through 2026-09-13
- every 7 days
- 12:00 UTC
- 5-minute probe window
- 211 probe dates
- 422 class records (Tick + M1 for each date).

Result summary:

### Historical Bid/Ask ticks

- probes: 211
- AVAILABLE: 27
- EMPTY: 184
- ERROR: 0
- earliest weekly available request: 2026-03-12 12:00 UTC
- latest weekly available request: 2026-09-10 12:00 UTC

### M1 OHLC

- probes: 211
- AVAILABLE in requested interval: 15
- EMPTY in requested interval: 196
- ERROR: 0
- earliest weekly available request: 2026-06-04 12:00 UTC
- latest weekly available request: 2026-09-10 12:00 UTC

## Scan B — Daily refinement

Durable job:

`XAU-MT5-HISTORY-COVERAGE-DAILY-V02-20260914`

Range:

- 2026-02-01 through 2026-09-13
- every calendar day
- 12:00 UTC
- 5-minute probe window
- 225 dates / 450 class records

### Historical Bid/Ask ticks

- AVAILABLE: 131 dates
- EMPTY: 94 dates
- weekday EMPTY: 29
- ERROR: 0
- first daily AVAILABLE request: 2026-03-12 12:00 UTC
- last pre-boundary weekday EMPTY: 2026-03-11
- after 2026-03-12, the only weekday EMPTY at the probe time was 2026-04-03
- 2026-04-03 remains SESSION/HOLIDAY CONTEXT REQUIRED and is not automatically classified as a data gap
- available-probe tick counts: min 598, median 1091, max 12753 per 5-minute window
- non-monotonic timestamp count across available probes: 0
- out-of-request-range tick rows: 0
- repeated millisecond timestamps exist and are not by themselves treated as duplicate tick records

### M1 OHLC

- AVAILABLE: 73 dates
- EMPTY: 152 dates
- weekday EMPTY: 87
- ERROR: 0
- first daily AVAILABLE request: 2026-06-03 12:00 UTC
- last pre-boundary weekday EMPTY: 2026-06-02
- after 2026-06-03 there were no weekday EMPTY probes through 2026-09-11
- every AVAILABLE 5-minute probe contained exactly 5 in-range M1 bars
- non-monotonic timestamps: 0
- duplicate bar timestamps: 0

## Exact accessible tick-history start

Two direct `copy_ticks_from(..., count=1)` probes were run.

Starting request at 2026-03-01 UTC:

- returned rows: 1
- first accessible tick: `2026-03-12T00:00:00.255Z`

Starting request at 2022-09-01 UTC:

- returned rows: 1
- first accessible tick: `2026-03-12T00:00:00.255Z`

Current evidence therefore supports:

**The earliest tick accessible through the current MT5/Python route is 2026-03-12T00:00:00.255Z.**

This is a statement about the currently accessible route. It is not proof that the broker never possessed older tick data.

## M1 terminal-window boundary

Runtime terminal metadata:

- `maxbars = 100000`

Direct `copy_rates_from_pos` probe:

- request count 50,000 -> 50,000 M1 bars
- earliest returned bar: 2026-07-24 01:57 UTC

Direct near-limit probe:

- request count 99,999 -> 99,999 M1 bars
- earliest returned bar: `2026-06-03T10:20:00Z`
- latest returned bar at probe time: 2026-09-14 11:15 UTC
- MT5 status: Success

A count of 100,000 returned `Invalid params`; 99,999 succeeded.

Interpretation:

The current Python-visible M1 history window is operationally bounded by the terminal's Max Bars setting/window. Therefore failure to retrieve M1 before 2026-06-03 through the current terminal MUST NOT be interpreted as proof that broker/server M1 retention begins on that date.

## Reconciliation with earlier probes

Earlier exploratory probes recorded:

- some old M1 requests as "data returned" for dates such as 2026-04-01 and 2025-09-15;
- a 2026-06-01 tick probe as zero rows.

Those observations remain part of Project history, but their earlier interpretation is narrowed.

### Old M1 interpretation

The earlier probe did not validate that the returned bar timestamp was inside the requested interval.

The new mapper demonstrated that MT5 can return an out-of-request M1 row. Therefore:

**OLD CLAIM: old requested date returned a row -> M1 exists on that date**

is NOT a valid inference.

Current evidence instead says:

- current terminal-visible M1 history is limited to the approximately 100,000-bar window;
- older broker/server M1 availability is still not established by this route/configuration.

### Old 2026-06-01 tick zero result

Current direct probing now returns historical ticks for 2026-06-01 12:00 UTC.

Why the earlier call returned zero is not established. Possible history synchronization/loading differences are not promoted to fact.

The current route evidence supersedes the old zero-row observation for present accessibility.

## What this proves

1. The MT5/Python route exposes historical Bid/Ask ticks with millisecond timestamps.
2. Current accessible tick history begins exactly at 2026-03-12T00:00:00.255Z under direct `copy_ticks_from` probing.
3. Daily noon probes show broad weekday tick availability after that boundary, with one weekday-empty date still requiring session/holiday classification.
4. Current Python-visible M1 history is constrained by the terminal Max Bars window; 99,999 M1 bars reach to 2026-06-03T10:20Z at the time of testing.
5. A non-empty MT5 response must be timestamp-validated against the requested interval before it is counted as historical coverage.

## What this does NOT prove

1. It does not prove every tick is present continuously from 2026-03-12 onward.
2. It does not prove every intraday interval is available merely because the 12:00 UTC probe is available.
3. It does not prove the broker has no older tick history outside the current route.
4. It does not establish direct broker-server API access independent of MT5.
5. It does not establish historical slippage, commission, or complete transaction-cost truth.
6. It does not establish multi-year execution-quality Bid/Ask data.
7. It does not authorize holdout outcome scoring.

## Engineering consequence

For Phase 1:

- observed MT5 Bid/Ask should be used whenever the requested interval is inside the validated accessible tick window;
- multi-year execution-quality proof remains blocked because the accessible tick window is much shorter than the multi-year research horizon;
- M1 historical depth must not be judged from the current 100,000-bar terminal window alone;
- forward collection remains useful to preserve broker-specific Bid/Ask history beyond future retention changes;
- collector design should be restart-safe and should backfill from MT5 history where available;
- unrecoverable intervals must be recorded as gaps, never fabricated.

## Next action

1. declare the Phase 1 forward-collection observation/storage requirement using this coverage evidence;
2. specify the restart-safe read-only collector contract;
3. preserve full raw Bid/Ask ticks when collecting forward;
4. separately decide whether multi-year economic proof needs an external execution-quality feed or an explicitly declared residual execution model;
5. keep automatic execution and holdout scoring disabled.
