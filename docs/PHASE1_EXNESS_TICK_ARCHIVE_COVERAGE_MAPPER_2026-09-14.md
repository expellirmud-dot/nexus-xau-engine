# Phase 1 Exness XAUUSDm Tick Archive Coverage Mapper — 2026-09-14

Status: IMPLEMENTED / TARGETED TESTS PASS / LIVE SMOKE PASS / READ-ONLY METADATA

## Purpose

Map month-level object availability for the Exness-branded `XAUUSDm` historical tick archive before any multi-year bulk download or synthetic execution model.

This tool does **not** score market outcomes and does **not** send orders.

## Implementation

Module:

- `src/nexus_xau/data/exness_tick_archive.py`

CLI:

- `scripts/exness_tick_archive_coverage.py`

Tests:

- `tests/test_exness_tick_archive.py`

Default archive endpoint:

- `https://ticks.ex2archive.com/ticks/`

The endpoint provenance boundary remains the one frozen in:

- `docs/PHASE1_EXNESS_XAUUSDM_TICK_ARCHIVE_SAMPLE_VALIDATION_2026-09-14.md`

Do not silently upgrade it to exact target-server equivalence.

## Mapper contract

The mapper is metadata-only.

For each requested month it records:

- symbol;
- year/month;
- archive directory URL;
- expected monthly filename;
- status;
- observed filename;
- reported file size;
- reported mtime;
- observation timestamp;
- evidence basis;
- acquisition error when applicable.

Statuses:

- `AVAILABLE`
- `YEAR_DIRECTORY_MISSING`
- `MONTH_DIRECTORY_MISSING`
- `EXPECTED_FILE_MISSING`
- `ERROR`

The first four are terminal metadata observations for resume purposes.
`ERROR` is retryable.

## Restart safety

Coverage is appended to JSONL.

Each record is:

- written as one line;
- flushed;
- fsynced.

On resume:

- latest record per `(symbol, year, month)` is used for summary;
- terminal observations are not re-probed;
- prior `ERROR` records remain in history and the month may be retried;
- no historical error is deleted when a later retry succeeds.

This is suitable for a durable multi-year metadata scan.

## Interpretation guard

Archive object availability proves only that the archive listing exposed the expected object at observation time.

It does **not** prove:

- every expected tick exists inside the file;
- tick-level continuity;
- identity with the current Exness Demo / MT5 server;
- historical slippage or fills;
- commissions/cost truth;
- profitability;
- a universal spread.

## Automated validation

Targeted lint:

`python -m ruff check src/nexus_xau/data/exness_tick_archive.py scripts/exness_tick_archive_coverage.py tests/test_exness_tick_archive.py`

Result:

`PASS`

Targeted tests:

`python -m pytest -q tests/test_exness_tick_archive.py --basetemp=results/pytest-tmp-exness-archive`

Result:

`4 passed`

Tests cover:

1. archive directory schema parsing and expected filename construction;
2. available versus missing month/file classification;
3. terminal-record resume behavior plus retry of prior `ERROR`;
4. acquisition-error persistence.

## Live smoke validation

Smoke scope:

- symbol: `XAUUSDm`
- year: 2022
- months: September and October
- output: local gitignored `results/exness_tick_archive/`

First run:

- expected months: 2
- `AVAILABLE`: 2
- total reported ZIP bytes: 45,100,622
- errors: 0

Immediate resume run against the same JSONL:

- latest records: 2
- physical JSONL line count before rerun: 2
- physical JSONL line count after rerun: 2
- no terminal month was appended/re-probed.

Classification:

`IMPLEMENTED_LIVE_SMOKE_RESTART_VALIDATED`

This is not yet a 2015–2026 coverage result.

## Next bounded action

Run the 2015–2026 XAUUSDm month metadata scan under `nexus-durable-work` from a committed revision.

The durable scan should write only local gitignored result files and then be reconciled into a separate evidence checkpoint.

Automatic order execution remains disabled.

Protected holdout scoring remains disabled.
