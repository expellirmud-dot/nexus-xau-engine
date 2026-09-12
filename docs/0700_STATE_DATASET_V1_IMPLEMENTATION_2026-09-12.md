# 07:00 State Dataset V1 — Implementation Checkpoint — 2026-09-12

Status: IMPLEMENTED / EXPLORATORY FEATURE DATASET / NO CANONICAL RULE PROMOTION

## Purpose

Implement the first executable version of the 07:00 data-discovery design from:

`docs/0700_DATA_DISCOVERY_DESIGN_2026-09-12.md`

This checkpoint answers only whether the project can reconstruct a no-lookahead 07:00 state dataset from existing raw M1 data while preserving unresolved source semantics.

It does **not** answer whether the resulting conditions are profitable or canonical.

## Holdout boundary

The project's operational active worksheet remains RQ-012 for the unopened V0.1 prospective holdout.

This 07:00 dataset is exploratory work on historical development data and is isolated from the V0.1 holdout.

No post-boundary V0.1 outcome was inspected or scored.

## Implementation

New module:

`src/nexus_xau/research/state_0700_dataset_v1.py`

New tests:

`tests/test_state_0700_dataset_v1.py`

Discovery input:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2022-09-01_2023-03-31.csv`

Source SHA256:

`d6247b3d671e051e93876dcf8612f83f14d6dd49b08ba58a243a58049e2eeb55`

Metadata states this cache range is complete with no missing cache dates.

## Source-backed / user-direct semantics retained

- 07:00 Thailand = 00:00 UTC.
- Daily Frame uses the source-backed nearby 0/5 statistical reference and +/-500 project points through the existing project builder.
- H1 nominal teaching run = 1,000 project points.
- H4 nominal teaching run = 1,500 project points.
- D is retained as a possible originating run context, but exact D run distance remains unresolved.
- H1/M30/M15/M5 same-direction agreement is represented as graded confluence; no minimum count is imposed.
- Literal contact with an active point-check is represented as destruction semantics where that concept is applied.

## Research representations retained explicitly

The autonomous PA/SIG detector is not canonical.

V1 uses the existing PAT2-BODY midpoint-pass proxy only as:

`RESEARCH_REPRESENTATION / PAT2_BODY_MIDPOINT_PROXY`

The post-SIG adjacent-candle anchor is likewise used only as a proxy origin representation.

No source priority is invented when multiple origins coexist.

## Output tables

Local generated output root:

`results/0700_STATE_DATASET_V1/DISCOVERY_2022_09_TO_2023_03/`

The large generated CSVs remain local/ignored under repository data policy. Code and this checkpoint preserve how to regenerate them.

### 1. 0700_day_state.csv

One row per active exact 00:00 UTC / 07:00 Thailand boundary.

Rows: 150

Includes:

- cutoff price;
- Daily Frame candidate/reference;
- latest completed H1/H4/D1 OHLC;
- body/range/wick features;
- multiple explicitly labeled 50%-candidate geometries;
- counts of broad and source-partial origin candidates.

### 2. 0700_origin_candidates.csv

Rows: 13,400

Unique proxy origin IDs: 878

Candidate identity is preserved by timeframe and direction.

H1/H4 rows retain nominal run/consumed/remaining fields.

D1 rows retain:

`UNRESOLVED_D1_RUN_DISTANCE`

rather than inventing a target.

### 3. 0700_confirmation_events.csv

Rows: 22,529

Every PAT2-BODY proxy confirmation event after 07:00 is retained chronologically for H1/M30/M15/M5.

The table stores:

- event time and timeframe;
- Daily Frame expected/crossed-side relation;
- exact MTF alignment;
- recent-1-bar and recent-2-bar alignment variants kept separately;
- origin-context counts;
- unresolved M1/M5 brake/retest/frame-standing fields explicitly marked rather than guessed.

No future outcome, P&L, or Win/Loss field is generated.

## Point-check lane and why it was added

A first structural audit showed that using only:

`nominal run not yet completed`

left an average of about 68.8 H1/H4 proxy origins per 07:00 day.

This is too broad to be a useful active-context representation.

Rather than delete these rows or choose a winner, V1 now preserves two lanes:

1. broad nominal-run-incomplete origin population;
2. source-partial survival feature where the proxy point-check has **not** been literally contacted before the 07:00 cutoff.

The point-check lane applies the source-backed literal-contact concept to a research-proxy anchor. It does not promote that proxy to a canonical SIG.

### No-lookahead guard

The full raw path may be precomputed internally for efficiency, but a 07:00 row exposes a point-check touch timestamp only if that touch occurred strictly before that cutoff.

A future touch timestamp is never written into an earlier row.

Audit:

`future_touch_timestamp_leak = 0`

## Discovery feature audit

### Broad H1/H4 nominal-incomplete lane

- rows: 10,318
- days with at least one measurable H1/H4 origin: 149 / 150
- mean count per day: 68.79
- median: 61
- maximum: 131

This population is retained for comparison but is too broad to interpret as active source-valid state.

### Source-partial point-check-survival lane

Across 150 07:00 days:

- surviving H1/H4 origin-day rows: 206
- unique surviving proxy origins: 202
- H1 rows: 97
- H4 rows: 109
- BUY rows: 96
- SELL rows: 110
- days with at least one survivor: 115 / 150
- mean survivor count/day: 1.37
- median: 1
- maximum: 7

Direction state among the 115 days with a survivor:

- BUY only: 37 days
- SELL only: 43 days
- both BUY and SELL survivor contexts: 35 days

Timeframe presence:

- H1 only: 33 days
- H4 only: 39 days
- both H1 and H4 present: 43 days

Per day+direction context:

- H1-only context: 51
- H4-only context: 63
- H1+H4 context: 36

The presence of 35 direction-conflict days and 42 day+direction contexts with multiple surviving origins confirms that V1 must preserve multiple candidates rather than silently choose a priority.

### Survivor descriptive ranges

These are feature distributions, not thresholds.

Origin age:

- median: 4 hours
- p25: 3 hours
- p75: 8 hours
- max observed: 96 hours

Remaining run:

- median: 645.9 project points
- p25: 294.075
- p75: 907.225
- observed range: approximately 7 to 1,500 points

Consumed ratio:

- median: 0.48465
- p25: 0.247275
- p75: 0.7654

No age, remaining-run, or consumed-ratio cutoff is promoted from these observations.

## Confirmation feature audit

Rows: 22,529

By timeframe:

- M5: 14,347
- M15: 4,720
- M30: 2,320
- H1: 1,142

By direction:

- BUY: 11,185
- SELL: 11,344

Daily Frame side:

- EXPECTED_SIDE: 15,838
- CROSSED_SIDE: 6,691

Exact-completion alignment count:

- 1 TF: 18,109
- 2 TF: 3,946
- 3 TF: 462
- 4 TF: 12

This is another reason not to manufacture an all-four-TF entry gate.

## Integrity checks

Discovery audit returned:

- duplicate day rows = 0
- duplicate day+origin rows = 0
- duplicate event IDs = 0
- negative origin age = 0
- non-positive retained remaining run = 0
- confirmation at/before cutoff = 0
- future point-check timestamp leak = 0
- Daily Frame snap ties in this discovery period = 0

The first dataset day has no completed prior H1/H4/D1 snapshot because the raw source begins at that boundary. This is preserved as left-censoring rather than backfilled from unavailable data.

## Generated artifact hashes

`0700_day_state.csv`
- bytes: 147,146
- SHA256: `3C82F15A6D1157A55C0CDDEBBF6A5E9B5B1BE46950E1A72AF521E87192781120`

`0700_origin_candidates.csv`
- bytes: 6,308,573
- SHA256: `464D8F24885EFD8E81D0239D740CD496228751900D9D05210D6B44308750B6BC`

`0700_confirmation_events.csv`
- bytes: 35,118,373
- SHA256: `0895ED3C5033263EA6906078490B7598F0AE9034D0E8EA9BBDCAEC0F716D81CF`

`REPORT.json`
- bytes: 1,707
- SHA256: `473D203A04D893C4161FC6CB0FEFA4B295BA8012343D7E9F0A88A159C66B75B7`

## Tests

Targeted V1 tests:

`11 passed`

They cover:

- closed-bar knowledge time;
- no pattern construction across data gaps;
- H4 1,500 preservation;
- unresolved D1 target preservation;
- no use of an open H4 bar;
- consumed path excludes the cutoff bar;
- Daily Frame tie ambiguity;
- exact/recent alignment kept as separate variants;
- literal point-check contact;
- future-touch hiding;
- past-touch visibility.

Ruff targeted check: PASS.

Full repository validation:

- pytest with repository-local basetemp: 153 passed;
- Ruff `src tests`: PASS;
- research preflight: PASS.

The first full-suite invocation against the Windows user temp directory hit an environment `WinError 5 / Access denied` in pytest temp cleanup. Re-running the identical suite with `--basetemp=results/pytest_tmp/0700_full_20260912` passed all 153 tests, separating the temp-permission issue from code correctness.

## What this checkpoint establishes

The project now has a reproducible feature-only 07:00 dataset that can study missing relationships without forcing a full trading formula.

It also identifies an important bounded next question:

> Among the source-partial surviving H1/H4 origin contexts at 07:00, how do origin timeframe/direction conflicts, Daily Frame side, MTF confirmation sequence, origin age, consumed ratio, and remaining run relate to later completion behavior?

This question can now be measured without choosing an origin winner first.

## What remains unresolved

- canonical autonomous PA/PAT/SIG detection;
- PAT2 exact 50% denominator;
- exact D run distance;
- canonical priority among simultaneous H1/H4/D origins;
- exact M1/M5 brake numeric gates;
- exact retest/standing quantitative geometry;
- universal SL;
- complete broker execution/fill model;
- trade/system Win/Loss.

Historical outcome analysis may rank or weaken research representations, but it cannot convert an unsupported historical winner into instructor intent.
