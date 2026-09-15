# Phase 1 Archive -> 0700 Minimal V2 Integration Implementation V0.2 — 2026-09-15

Status: IMPLEMENTED / SYNTHETIC PASS / FULL REGRESSION PASS / REAL ENGINEERING PREP SMOKE PASS / REAL V2 STATE FAIL-CLOSED / NO OUTCOME SCORING

Current contract:
`docs/PHASE1_ARCHIVE_V2_INTEGRATION_CONTRACT_V0.2_2026-09-15.md`

Superseded pre-outcome contract:
`docs/PHASE1_ARCHIVE_V2_INTEGRATION_CONTRACT_V0.1_2026-09-15.md`

Implementation:
- `src/nexus_xau/research/minimal_v2_0700.py`
- `src/nexus_xau/replay/v2_integration.py`

Synthetic tests:
- `tests/test_archive_v2_integration.py`
- `tests/test_minimal_v2_0700.py`

## Purpose

Connect validated archive-derived M1 geometry to the frozen `0700_MINIMAL_V2.0` state machinery without changing V2 semantics, inventing warmup, relabeling archive data as MT5, or exposing protected outcomes.

## Frame-based V2 entry point

The existing file-based V2 entry point remains available.

A frame-based entry point was added so archive M1 can enter the same V2 core without temporary CSV export.

Frozen compatibility behavior:
- file loader still normalizes timestamp/OHLC as before;
- frame entry normalizes timezone-aware M1 to UTC, validates OHLC and duplicate timestamps, and preserves optional volume filtering;
- both routes call the same V2 core;
- source descriptor / metadata descriptor / SHA fields remain explicit.

Synthetic parity confirms file-based and frame-based entry points produce identical V2 outputs/report when supplied the same normalized input and source identity.

No PAT, origin, target, point-check, Daily Frame, action-state or 07:00 rule changed.

## Archive integration preparation

`prepare_archive_v2_input` now:
- requires eligible archive window status;
- rejects empty/no-tick input;
- requires exact 4-hour UTC request boundaries under V0.2;
- requires every M1 row to remain inside the requested half-open window;
- requires exact `ARCHIVE_BID_M1_V0.1` representation on every row;
- requires source year/month/SHA provenance columns;
- requires observed M1 month/SHA tuples to be covered by the source-month provenance envelope;
- preserves a deep copy of archive M1;
- derives only M5 and H4 using existing `resample_ohlc`;
- carries source family, symbol, window, continuity marker, source months, SHA values and validator versions in an integration envelope.

Current V2 does not gain H1/D1 dependencies.

## V0.2 pre-outcome correction

During synthetic integration work, before any real V2 state run, interface inspection exposed a request-boundary defect in V0.1:

A request that starts or ends inside an H4 interval can cause resampling to produce a request-truncated H4/M5 edge bar that appears structurally complete to V2.

No strategy outcome was inspected to find this.

V0.2 therefore superseded V0.1 and freezes:
- exact 4-hour UTC request boundaries;
- row-within-window enforcement;
- observed M1 provenance-envelope consistency.

No tolerance, broker-session offset or warmup duration was introduced.

## Origin-history seed gate

The current V2 H4 origin has no frozen fixed expiry.

Therefore an arbitrary finite historical warmup cannot be proven sufficient to reconstruct all potentially active origins at the start of a real archive window.

Implemented seed handling:
- `SYNTHETIC_COMPLETE`: allowed for controlled fixtures;
- `CONTINUATION_CHECKPOINT`: explicitly reserved but not implemented;
- `UNSEEDED_REAL_WINDOW`: fail closed with `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`.

This prevents a bounded real archive window from silently assuming that no pre-window H4 origin exists.

## Synthetic validation

Targeted Ruff:
`PASS`

Collected targeted tests:
- archive V2 integration: 14;
- existing Minimal V2: 16.

Targeted pytest:
`PASS`

Covered integration invariants include:
- file/frame V2 parity;
- M5/H4 direct-resample identity;
- archive M1 immutability;
- no H1/D1 dependency;
- synthetic seed acceptance;
- real unseeded rejection;
- continuation-checkpoint explicit not-implemented status;
- empty window rejection;
- wrong/null representation rejection;
- 4-hour boundary rejection;
- row-outside-window rejection;
- source provenance mismatch rejection;
- source month/SHA envelope preservation;
- no economic/P&L fields added.

## Full repository regression

Broader Ruff:
`python -m ruff check src tests scripts`

Result:
`PASS`

Full repository pytest:
`PASS`

Progress reached 100%.

Only pre-existing/deprecation-class warnings were observed.

## Real archive engineering smoke

Already validated representative source month:
`2026-08`

V0.2-aligned requested window:
`[2026-08-03T00:00:00Z, 2026-08-03T04:00:00Z)`

Observed:
- archive ticks: 60,324;
- archive-derived M1 bars: 240;
- M5 bars: 48;
- H4 bars: 1;
- first M1: `2026-08-03T00:00:00Z`;
- last M1: `2026-08-03T03:59:00Z`;
- source month: 2026-08;
- source SHA prefix: `baa514c5a942`;
- derived timeframes: M5, H4;
- integration contract marker: `PHASE1_ARCHIVE_V2_INTEGRATION_V0.2`;
- continuity marker: `KNOWN_GAPS_ENFORCED_FULL_CONTINUITY_NOT_PROVEN`.

A deliberate real-window V2-state call with `UNSEEDED_REAL_WINDOW` was blocked before canonical V2 state creation:

`DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`

No real archive V2 day/candidate outcome was produced.

## Claim boundary

Still not established:
- complete origin-history initialization at archive start;
- full every-tick continuity;
- exact archive-to-current Exness Demo/MT5 feed identity;
- historical broker fills/slippage;
- account-specific commission/fee/swap truth;
- exact trade-stop geometry;
- Win Rate, expectancy or profitability.

Automatic order sending remains disabled.
Protected holdout scoring remains disabled.

## Next bounded task

Audit existing pre-archive historical sources/state machinery for a defensible origin-history initialization route.

Priority:
1. inspect existing local historical coverage before `2015-08-10`;
2. determine whether any pre-archive source can seed V2 origin state while retaining explicit cross-feed provenance and without claiming exact feed identity;
3. separately design a restart-safe continuation checkpoint for sequential replay after an initial seed exists;
4. if no defensible initial seed can be established, preserve `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED` rather than inventing a warmup duration.
