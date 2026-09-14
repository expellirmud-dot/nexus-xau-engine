# Phase 1 Execution Data Acquisition Probe — 2026-09-14

Status: ENGINEERING PROBE / NO MARKET OUTCOME SCORING

## Purpose

Check whether Phase 1 execution-cost research can obtain real Bid/Ask tick data before inventing a spread/execution model.

This probe used already-inspected historical time only and did not access or score holdout outcomes.

## Existing project capability

The repository already contains:

- MT5 M1 bar exporter: src/nexus_xau/data/mt5_export.py
- multi-year Dukascopy BID M1 pipeline: src/nexus_xau/data/dukascopy_export.py
- broker/feed normalization contract
- captured Exness demo metadata

Current M1 bar data is useful for state/path research but is not full execution-quality Bid/Ask tick history.

## MT5 tick capability

Official MetaTrader5 Python integration supports copy_ticks_range() and returns tick records including Bid, Ask, Last, time/time_msc and flags.

Local probe target:

- symbol: XAUUSDm
- historical range: 2026-08-24 00:00–01:00 UTC
- reason for date choice: previously inspected historical period, not prospective holdout

Local result:

TERMINAL_AUTHORIZATION_FAILED

Observed MT5 error:

(-6, 'Terminal: Authorization failed')

Interpretation:

The probe did not establish that tick history is unavailable.
It established only that the local MT5 terminal session was not authorized for this request at probe time.

## Dukascopy capability

Official Dukascopy historical-data material supports historical Bid/Ask data and historical ticks.

The Project already runtime-verified direct BID M1 retrieval in the existing Dukascopy pipeline.

A direct raw XAUUSD hourly tick probe for the same already-inspected date was attempted from the local machine.

Local result:

NETWORK_PATH_FAILED

Observed local error:

WinError 10054 — connection forcibly closed by remote host during HTTPS handshake.

Interpretation:

This does not establish that Dukascopy tick data is unavailable.
It establishes that this particular direct raw-data network path did not complete from the local machine at probe time.

## Current acquisition paths

Preferred order:

1. re-establish authorized MT5 terminal session and probe copy_ticks_range for historical Bid/Ask ticks;
2. if broker tick history is insufficient, use verified Dukascopy historical Bid/Ask/tick export as an execution-research feed;
3. keep broker-specific and Dukascopy feeds explicitly separate;
4. only construct a synthetic spread/slippage model for residual gaps not covered by observed data.

## Parameter classes

Do not collapse all execution values into one optimization problem.

### Broker/runtime constrained

Examples:

- tick size
- digits
- contract size
- minimum/maximum/step volume
- stop/freeze levels
- account/symbol execution specification

Read these from the target runtime where possible.

### Market-varying observed quantities

Examples:

- Bid/Ask spread
- spread by time/state
- slippage / fill quality where measurable

Prefer empirical distributions from execution-quality data.

### Project engineering conventions

Examples:

- exact replay fill convention when source does not fix one
- ambiguous-bar handling
- close-at-objective representation
- replacement/re-entry accounting

Freeze before outcome scoring and label as Project conventions.

### Risk-policy choices

Examples:

- position sizing
- per-trade risk cap
- account drawdown limits

These are not inferred automatically from a favorable historical result.

## Current conclusion

REAL_BID_ASK_DATA_ROUTE_EXISTS_BUT_LOCAL_ACQUISITION_NOT_YET_CLOSED

Do not invent a constant spread yet.

Next technical step is to obtain one validated historical Bid/Ask tick sample through an authorized/working route, calculate observed spread statistics, and only then decide what execution-cost model is actually necessary.
