# Phase 1 — MT5 Capability Report

Status: ACTIVE LIVE AUDIT
Created: 2026-09-14
Scope: Phase 1
Mode: READ-ONLY AUDIT

## Purpose

Single running report for what the current MT5 Demo environment can expose to the Project.

Classification:
- OBSERVED_FROM_MT5
- PROJECT_DERIVED
- NOT_YET_PROBED
- UNAVAILABLE_OR_BLOCKED

## Current Environment

Observed from MT5/Python:

- terminal connection: PASS
- terminal build: 6182
- Python MetaTrader5 package: 5.0.6180
- external Python access: available
- account type: Demo
- account currency: USD
- leverage: 1:500
- balance: 500 USD
- equity: 500 USD
- margin: 0
- free margin: 500 USD

Account identifiers and passwords are intentionally not recorded here.

## XAUUSDm — Confirmed Specification

Observed from MT5/Python:

- digits: 3
- point: 0.001
- contract size: 100 XAU
- minimum volume: 0.01
- maximum volume: 200
- volume step: 0.01
- spread: floating
- stops level: 0
- freeze level: 0
- base currency: XAU
- profit currency: USD
- margin currency: XAU
- swap long: -534.9
- swap short: 0.0
- execution: market execution

## Live Tick — Confirmed

Example tick observed during this audit:

- Bid: 4291.967
- Ask: 4292.227
- observed spread: 0.260
- millisecond timestamp available
- tick flags available

One tick is not a spread model.

## Capability Audit Matrix

| Area | Status | Current evidence |
|---|---|---|
| Terminal metadata | CONFIRMED | build/connection/API flags readable |
| Account metadata | CONFIRMED | balance/equity/margin/leverage/currency readable |
| Symbol specification | CONFIRMED | price grid/contract/volume/swap/execution readable |
| Live Bid/Ask | CONFIRMED | live tick returned |
| Historical Bid/Ask ticks | CONFIRMED_CURRENT_ROUTE_WINDOW | earliest accessible tick: 2026-03-12T00:00:00.255Z; full continuity not yet proven |
| OHLC M1/M5/H1/H4/D1 | CONFIRMED_WITH_TERMINAL_WINDOW_LIMIT | recent bars confirmed; current M1 depth is bounded by terminal maxbars=100000 |
| Historical spread distribution | CONFIRMED_PARTIAL | real Bid/Ask ticks allow derivation; long lookback not yet mapped |
| Open positions | CONFIRMED | API returned current count |
| Open/pending orders | CONFIRMED | API returned current count |
| Historical orders/deals | CONFIRMED | history API returned records |
| Depth of Market | UNAVAILABLE_OR_BLOCKED | subscription returned false for XAUUSDm |
| Margin calculation | CONFIRMED | calculation returned value |
| Profit calculation | CONFIRMED | calculation returned value |

## Probe Log

### 2026-09-14 — OHLC

M1:
- 10 bars returned successfully
- fields include time, open, high, low, close, tick volume, spread, real volume

M5/H1/H4/D1:
- 3 bars requested for each timeframe
- all four timeframes returned successfully

Interpretation:
MT5 can directly provide the OHLC families needed for Phase 1 state reconstruction, subject to later history-depth checks.

### 2026-09-14 — Recent Bid/Ask tick history

Requested:
- XAUUSDm
- approximately recent 5-minute window

Observed:
- first successful sample: 1,900 ticks
- later sample used for spread summary: 1,954 ticks
- Bid/Ask and millisecond timestamps present

Spread summary for the 1,954-tick sample:
- minimum: ~0.260
- median: ~0.260
- mean: ~0.260
- maximum: ~0.260
- 95th percentile: ~0.260

Interpretation:
Observed Bid/Ask history exists and spread can be derived empirically. This short sample must not be generalized to other times or states.

### 2026-09-14 — Older tick-history probe

Requested start:
- 2026-08-24 00:00 UTC

Observed:
- 10 ticks returned successfully
- first tick approximately Bid 4624.199 / Ask 4624.459
- last returned tick approximately Bid 4624.188 / Ask 4624.448

Interpretation:
The current Demo environment can retrieve Bid/Ask ticks from at least this previously studied historical date.

A much older lookback probe is still unresolved and should be repeated separately.

### 2026-09-14 — Current account state visibility

Observed:
- open positions count: 0
- open/pending orders count: 0

Interpretation:
Positions and current order state are readable.

### 2026-09-14 — Account history visibility

Requested:
- previous 7 days

Observed:
- deals: 1
- historical orders: 0
- the one deal was the 500 USD Demo balance-credit record, not a market trade

Interpretation:
Account history API is readable and can later support supervised Demo audit trails.

### 2026-09-14 — Calculation-only margin/profit

Using current XAUUSDm prices and 0.01 volume:

- current Ask/Bid observed around 4284.280 / 4284.020
- calculated BUY margin: 8.57 USD
- calculated BUY profit for +1.000 price move: 1.00 USD
- calculated SELL profit for -1.000 price move: 1.00 USD

Interpretation:
MT5 can calculate account-specific margin/profit from the current symbol specification without requiring a live market position.

### 2026-09-14 — Depth of Market

Observed:
- market-book subscription for XAUUSDm returned false
- no levels returned

Interpretation:
Do not assume Depth of Market is available for this symbol/account from the Python API.


### 2026-09-14 — Additional history-depth survey

Historical Bid/Ask tick probes:

- 2026-07-01 00:00 UTC, one-minute window: 237 ticks
- 2026-06-30 00:00 UTC, one-minute window: 460 ticks
- 2026-06-15 00:00 UTC, one-minute window: 318 ticks
- 2026-06-01 00:00 UTC, one-minute window: 0 ticks
- 2026-06-01 12:00 UTC, one-minute window: 0 ticks

Historical M1 bar probes:

- 2026-04-01 12:00 UTC: data returned
- 2025-09-15 12:00 UTC: data returned

Interpretation:

- MT5 historical OHLC depth is not the same thing as historical Bid/Ask tick depth.
- Tick history is confirmed for multiple dates from at least mid-June 2026 onward, but a June 1 probe returned no ticks.
- Older M1 bars can still be returned even when older execution ticks are unavailable or incomplete.
- Do not infer continuous tick coverage from a successful probe on one date.
- A proper coverage map must test date windows systematically and record missing intervals.

Phase 1 impact:

State/path reconstruction may have longer usable OHLC history than realistic execution-cost reconstruction from broker ticks.


### 2026-09-14 — Historical access route interpretation

Confirmed route:

- historical bars and historical Bid/Ask ticks are retrievable through the connected MT5 terminal using the MetaTrader5 Python API.

Not established:

- a separate direct Exness historical-data endpoint/API that the Project can query independently of the terminal.

Working interpretation:

The Project should treat the MT5 terminal/API path as the confirmed historical access route. Whether the terminal is satisfying a request from local cache, broker-server synchronization, or both is an implementation detail that has not yet been separately demonstrated for each interval.

Engineering consequence:

- build the history-coverage map against the route we can actually test;
- do not design around an unverified direct-server interface;
- forward collection should be restart-safe and attempt historical gap recovery after restart;
- any interval that cannot be recovered must be recorded explicitly rather than silently filled.

## Phase 1 Impact

Confirmed useful MT5 inputs now include:

1. account and terminal environment
2. broker/runtime symbol specification
3. live Bid/Ask
4. historical Bid/Ask ticks
5. OHLC on multiple timeframes
6. current positions/orders
7. account order/deal history
8. account-specific margin/profit calculations

Primary unresolved data questions:

- what historical Bid/Ask tick intervals are actually present or missing
- how far OHLC bars remain available with acceptable completeness
- whether tick gaps require an external execution-data source or a residual model

This history-depth question should be mapped before deciding whether an external execution-data source or synthetic residual model is still necessary.

### 2026-09-14 — Coverage-map reconciliation

Current authority: `docs/PHASE1_MT5_HISTORY_COVERAGE_MAP_2026-09-14.md`. Exact current-route tick start is 2026-03-12T00:00:00.255Z. Current M1 Python-visible depth is bounded by terminal `maxbars=100000`; older M1 non-empty point probes are not valid interval-availability proof because MT5 can return out-of-request rows. Multi-year execution-quality Bid/Ask proof remains open.
