# Phase 1 Exness XAUUSDm Tick Archive Downloader / Validator V0.1 — 2026-09-14

Status: IMPLEMENTED / TARGETED TESTS PASS / PRE-REPRESENTATIVE-DOWNLOAD FREEZE
Scope: Phase 1
Mode: READ-ONLY EXTERNAL DATA / ORDER SEND DISABLED

## Purpose

Download real Exness-branded monthly `XAUUSDm` Bid/Ask tick archives only after month-level availability has been mapped, and validate each downloaded file before using it as research/execution-data evidence.

This tool is an acquisition/validation layer. It does not score trading outcomes and does not authorize execution.

## Implementation

Module:
- `src/nexus_xau/data/exness_tick_archive_download.py`

CLI:
- `scripts/exness_tick_archive_download.py`

Tests:
- `tests/test_exness_tick_archive_download.py`

Coverage authority:
- `results/exness_tick_archive/XAUUSDm_coverage_2015_2026.jsonl`

## Download contract

For each requested month:

1. require `AVAILABLE` status in the frozen coverage map;
2. build the exact expected monthly archive URL;
3. download to a `.part` file and resume with HTTP Range when the server supports partial content;
4. atomically replace the final ZIP only after the transfer completes;
5. verify reported size when coverage metadata provides it;
6. compute SHA-256;
7. run ZIP integrity validation;
8. require exactly one CSV member;
9. require the documented schema:
   - `Exness`
   - `Symbol`
   - `Timestamp`
   - `Bid`
   - `Ask`
10. stream all rows without loading a full month into memory;
11. record row count, first/last timestamp, distinct UTC dates, provider/symbol mismatch, Ask < Bid, non-finite values, timestamp regression, equal timestamps, and consecutive duplicate rows;
12. append a fsynced validation manifest record;
13. reuse a prior `VALIDATED` record when the validated local file still exists with the recorded size.

## Local storage

Monthly ZIP root:
- `data/raw/exness_tick_history/archive/XAUUSDm/YYYY/`

Validation manifest:
- `results/exness_tick_archive/download_validation_manifest.jsonl`

These are local data/result artifacts and should remain outside Git unless project policy changes.

## Representative batch freeze

Before any 134-month bulk download, validate three deterministic coverage positions:

- `2015-08` — earliest AVAILABLE month;
- `2021-03` — midpoint AVAILABLE month in the 134-month coverage set;
- `2026-08` — recent month inside the current MT5 historical-overlap era, suitable for later cross-feed comparison.

Selection is based on coverage position/provenance needs, not market outcome.

## Validation evidence

Targeted Ruff:
- PASS

Targeted tests:
- 7/7 PASS using repository-local pytest basetemp.

Tests include:
- coverage mapper behavior;
- archive URL construction;
- ZIP/CSV streaming validation;
- manifest reuse without network re-download.

## Interpretation boundary

A validated archive month proves that:

- the expected file was retrievable;
- file size/hash/integrity were recorded;
- the CSV structure and internal chronological/data-quality checks passed as observed.

It does not prove:

- every expected broker tick exists;
- exact equivalence to the current Exness Demo/MT5 server;
- fill/slippage truth;
- commissions;
- profitability;
- a universal spread model.

## Next action

Run the representative three-month download/validation as a durable job.

If all three validate, cross-compare the 2026-08 archive with an overlapping current MT5 XAUUSDm interval while preserving feed/server identities. Only then expand to the remaining AVAILABLE months with durable item-level progress.

Automatic order sending remains disabled.
Protected holdout scoring remains disabled.
