# Phase 1 Archive Tick-to-Bar Reconstruction Implementation V0.1 — 2026-09-15

Status: IMPLEMENTED / SYNTHETIC PASS / FULL REGRESSION PASS / REAL-OVERLAP PARITY SMOKE PASS / NO STRATEGY OUTCOME OPENED

Contract:
`docs/PHASE1_ARCHIVE_TICK_TO_BAR_CONTRACT_V0.1_2026-09-15.md`

Implementation:
`src/nexus_xau/replay/tick_bars.py`

Synthetic tests:
`tests/test_tick_bars_replay.py`

## Implemented behavior

- archive Bid geometry only;
- exact UTC minute-aligned requested boundaries required;
- M1 intervals are left-closed/right-open;
- open/high/low/close = first/max/min/last Bid in stable source order;
- equal timestamps allowed;
- exact duplicate ticks retained in `archive_tick_count`;
- zero-tick minutes produce no synthetic bar;
- no forward fill or interpolation;
- archive source year/month/SHA/local path/validator version preserved;
- first/last raw row ordinal preserved per bar;
- mixed provenance inside one M1 bar fails closed;
- Ask changes do not alter geometry OHLC;
- output representation marker: `ARCHIVE_BID_M1_V0.1`.

## Synthetic validation

Targeted Ruff:
`PASS`

Targeted pytest:
`12 passed`

The first synthetic run found:
- two Ruff/style findings;
- one empty-fixture timezone issue in the test harness.
These were corrected before any real-data parity smoke.
No historical strategy outcome was used for correction.

## Full repository regression

Broader Ruff:
`python -m ruff check src tests scripts`

Result:
`PASS`

Full repository pytest:
`PASS`

Progress reached 100%.
Only pre-existing/deprecation-class warnings were emitted.

## Real bounded parity smoke

Archive window:
`[2026-08-02T22:02:00Z, 2026-08-02T23:02:00Z)`
Observed:
- archive ticks: 7,857;
- archive-derived M1 bars: 60;
- common MT5 M1 timestamps: 60;
- total archive_tick_count across bars: 7,857;
- first bar: `2026-08-02T22:02:00Z`;
- last bar: `2026-08-02T23:01:00Z`;
- representation: `ARCHIVE_BID_M1_V0.1`.

Exact component matches out of 60:
- open: 41;
- high: 39;
- low: 32;
- close: 35.

Bars with at least one exact OHLC mismatch: 50.
Maximum observed absolute component differences:
- open: 0.326;
- high: 0.252;
- low: 0.127;
- close: 0.252.

These values reproduce the descriptive evidence measured before implementation freeze.

## Interpretation

The implementation reproduces the frozen UTC minute boundary representation and preserves archive provenance.

The bounded overlap supports timestamp/boundary compatibility in this sample.
It does not establish exact archive-to-current-MT5 price-feed equivalence.

No tolerance threshold was fitted or inferred from the mismatch distribution.
No signal, target/stop result, P&L, Win Rate, or broker-fill claim was opened.

Automatic order sending remains disabled.
V0.1 holdout outcome scoring remains disabled.
## Next bounded task

Before broad historical strategy replay, build/freeze the integration layer that feeds archive-derived M1 bars through the existing higher-timeframe resample and frozen 0700_MINIMAL_V2.0 state machinery while preserving provenance and data-exclusion states.

The first integration validation should remain engineering-only on already-inspected windows and must not open protected holdout scoring.
