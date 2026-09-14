# Phase 1 Exness Representative Archive + MT5 Overlap Validation — 2026-09-14

Status: REPRESENTATIVE DOWNLOAD VALIDATED / OVERLAP DESCRIPTIVELY CONSISTENT / FEED EQUIVALENCE NOT CLAIMED
Mode: READ-ONLY DATA / ORDER SEND DISABLED

## Purpose

Validate representative Exness-branded XAUUSDm archive files across the observed 2015-2026 coverage span, correct any validator defects before bulk acquisition, and compare one already-inspected 2026 interval against the current MT5 XAUUSDm route without inventing an equivalence tolerance.

## Representative months

Selection was frozen before validation based on coverage position, not market outcome:

- 2015-08 — earliest AVAILABLE month;
- 2021-03 — midpoint AVAILABLE month in the 134-month coverage set;
- 2026-08 — recent month with current-route MT5 overlap.

Durable jobs:

- XAU-EXNESS-REPRESENTATIVE-DOWNLOAD-V01-20260914
- XAU-EXNESS-REPRESENTATIVE-REVALIDATE-V02-20260914

Both completed with exit code 0.

## Validator correction

V0.1 found provider mismatch on every row because the CSV header uses `Exness` while row values use lowercase `exness`.

Raw inspection across 2015, 2021, 2022 sample, and 2026 confirmed the same lowercase row token.

The validator was corrected to case-insensitive provider comparison and versioned as:

`EXNESS_ARCHIVE_VALIDATOR_V0.2`

The original V0.1 manifest records were preserved. V0.2 appended corrected records.

## V0.2 representative observations

### 2015-08

- ZIP bytes: 9,931,122
- rows: 1,440,303
- first tick: 2015-08-10T00:00:00Z
- last tick: 2015-08-31T23:59:40Z
- distinct UTC dates: 19
- provider mismatch: 0
- symbol mismatch: 0
- Ask < Bid: 0
- non-finite: 0
- timestamp regression: 0
- consecutive equal timestamp: 657,310
- consecutive exact duplicate row: 0

Important: archive month availability does not imply full-calendar-month coverage. This first available month begins on August 10, not August 1.

The high equal-timestamp count is an observed characteristic of this older file; exact consecutive duplicate rows were zero. No deduplication rule is inferred from this observation.

### 2021-03

- ZIP bytes: 23,939,381
- rows: 2,563,601
- first tick: 2021-03-01T00:00:08.568Z
- last tick: 2021-03-31T23:59:58.550Z
- distinct UTC dates: 26
- provider mismatch: 0
- symbol mismatch: 0
- Ask < Bid: 0
- non-finite: 0
- timestamp regression: 0
- consecutive equal timestamp: 0
- consecutive exact duplicate row: 0

### 2026-08

- ZIP bytes: 61,510,630
- rows: 6,493,208
- first tick: 2026-08-02T22:01:30.647Z
- last tick: 2026-08-31T23:59:59.806Z
- distinct UTC dates: 26
- provider mismatch: 0
- symbol mismatch: 0
- Ask < Bid: 0
- non-finite: 0
- timestamp regression: 0
- consecutive equal timestamp: 29,000
- consecutive exact duplicate row: 12,313

Exact duplicates are preserved in raw acquisition. Whether a later replay representation deduplicates any rows is a separate engineering decision and is not decided here.

## Current MT5 overlap probe

Frozen interval:

`2026-08-24T00:00:00Z -> 2026-08-24T00:05:00Z`

Interval semantics:

`[start, end)`

This date/window had already been inspected in the MT5 capability work. No outcome scoring was performed.

### Exness-branded archive

- rows: 2,533
- unique millisecond timestamps: 2,518
- Bid min / median / max: 4620.140 / 4623.149 / 4628.111
- spread min / median / max: 0.260 / 0.260 / 0.340
- timestamp regressions: 0

### Current Exness Demo MT5 route

- rows: 2,499
- unique millisecond timestamps: 2,485
- Bid min / median / max: 4620.141 / 4623.153 / 4628.049
- spread min / median / max: 0.260 / 0.260 / 0.340
- timestamp regressions: 0

### Cross-feed descriptive relation

- exact millisecond timestamp-set intersection: 26
- median Bid difference (MT5 minus archive): +0.004
- observed spread median and min/max range matched in this five-minute window
- tick counts and price ranges were close but not identical

Safe interpretation:

`DESCRIPTIVELY_CONSISTENT_BROKER_FAMILY_MARKET_DATA / EXACT_FEED_EQUIVALENCE_NOT_ESTABLISHED`

This supports continuing archive acquisition as a separate historical market-data feed.

It does not establish:

- exact tick-for-tick identity;
- target-server equivalence;
- historical fills/slippage;
- universal spread;
- profitability.

## Bulk acquisition decision

Representative file integrity passed after validator correction, and the bounded 2026 overlap is descriptively consistent with the current MT5 route while remaining measurably non-identical.

Therefore bulk acquisition of all months classified `AVAILABLE` by the coverage map may proceed as a data-engineering task.

Bulk acquisition must:

- remain durable/restart-safe;
- keep archive and MT5 provenance separate;
- preserve raw ZIPs;
- append per-month validation manifest records;
- skip already validated current-version months;
- preserve anomalies instead of fabricating or silently fixing them;
- avoid outcome scoring and order execution.

Automatic order sending remains disabled.
Protected holdout scoring remains disabled.

## Operator batching update — 2026-09-15

Project owner selected annual acquisition batches instead of one 134-month job.

Operational rule:
- submit one durable job per calendar year;
- within each year, process only months whose coverage status is AVAILABLE;
- reuse current-validator manifest entries and local ZIPs, so already validated months are not downloaded again;
- reconcile validation/anomaly evidence at the end of each year before submitting the next year;
- preserve raw data and prior manifest history;
- do not infer continuity from year completion alone.

The downloader CLI supports `--year YYYY` for this batching mode.
