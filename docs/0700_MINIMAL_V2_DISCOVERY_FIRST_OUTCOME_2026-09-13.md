# 07:00 MINIMAL V2.0 — First Discovery Outcome Map — 2026-09-13

Status: DISCOVERY OUTCOME OPENED ONCE / FROZEN V2.0 / NO SEMANTIC TUNING

## Guard

This checkpoint is the first interpretation of the already-completed 150-day discovery replay.

No V2.0 code, detector semantics, thresholds, target definitions, location rules, or conflict rules were changed while reading the result.

The result is a signal/run research result, not trade P&L and not system Win Rate.

Historical Q1-Q4 remain frozen history under the PAT2 BODY-midpoint research proxy. This checkpoint does not rewrite them.

## Pre-open durable receipt

Job: `XAU-0700-MINIMAL-V2-DISCOVERY-20260913`

Durable job state: `DONE`, one attempt, no recorded error.

Input:
`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2022-09-01_2023-03-31.csv`

Input SHA256:
`d6247b3d671e051e93876dcf8612f83f14d6dd49b08ba58a243a58049e2eeb55`

Persisted output hashes before first outcome read:

- `REPORT.json` — 2,092 bytes — SHA256 `4e69eeba95e1a333fb0dd25f0f3f1f53d74fcd0b8a8e2d9b38e6b53413d5df23`
- `0700_v2_day_state.csv` — 27,314 bytes — SHA256 `b10fc24dfe1f2fc4bcbf69cc2eb86b9ce81d05e6dcc6f4264a8ebe6f5dcfe762`
- `0700_v2_origin_context.csv` — 21,635 bytes — SHA256 `aca76600261c8e1fcc9505b05a6f63365151f7275114afed2464ba0b70d1cb0a`
- `0700_v2_research_events.csv` — 49,318 bytes — SHA256 `7c421c0e27a55f065f4f422b207cbd037910770be59c0e7b9189ddefaef4b3a8`

## Frozen V2.0 population

- days: 150
- eligible H4 origin rows: 98
- research event rows: 98
- research-candidate rows: 84
- candidate days: 67

Day-level research state:

- `PASS_NO_H4_ORIGIN`: 74 / 150 = 49.33%
- `RESEARCH_CANDIDATE`: 67 / 150 = 44.67%
- `PASS_ORIGIN_DESTROYED_BEFORE_CONFIRMATION`: 9 / 150 = 6.00%

Day-level action state:

- `PASS_NO_H4_ORIGIN`: 74
- `PASS_SOURCE_GEOMETRY_UNRESOLVED`: 48
- `PASS_CONFLICT_UNRESOLVED`: 19
- `PASS_ORIGIN_DESTROYED_BEFORE_CONFIRMATION`: 9

There are zero action entries by design. This is not a failure of the replay. V2.0 intentionally fails closed because exact location qualification and origin-conflict resolution are not source-complete.

## Primary finding 1 — PATH_REMAINING first-hit map

Among 84 research-candidate rows:

- `TARGET_FIRST`: 44
- `POINT_CHECK_FIRST`: 38
- `NEITHER_BY_NEXT_0700`: 2
- `AMBIGUOUS_SAME_BAR`: 0

Among resolved target-vs-point-check rows:

`44 / (44 + 38) = 53.66%`

This number is a first-hit signal/run relationship statistic under the frozen V2.0 representation. It is not a trade/system Win Rate.

## Primary finding 2 — H4 consumed/run-progress relation survives V2 source correction

For the 82 resolved V2 rows:

- Spearman-style rank correlation of `consumed_ratio_at_0700` with TARGET_FIRST indicator: `+0.5131`
- same relation using consumed state at confirmation: `+0.5791`

Historical Q4 discovery H4 under the BODY-midpoint proxy:

- resolved rows: 90
- TARGET_FIRST indicator mean: 51.11%
- consumed-ratio rank correlation: `+0.5138`

V2 FULL-RANGE discovery:

- resolved rows: 82
- TARGET_FIRST indicator mean: 53.66%
- consumed-ratio rank correlation: `+0.5131`

The broad H4 consumed/run-progress relationship therefore remains visible after moving the current source authority to PAT2 FULL-RANGE.

Important boundary:

This is not an independent replication. The two populations come from the same historical period and overlap heavily.

Unique-origin comparison:

- V2 resolved unique origins: 81
- historical Q4 H4 unique origins: 89
- unique origins present in both: 78
- V2-only: 3
- historical-Q4-only: 11

Therefore the safe claim is:

`BROAD H4 CONSUMED RELATION SURVIVES THE SOURCE-CORRECTED V2 REPRESENTATION`

not:

`FULL-RANGE independently proves the relationship`.

The stronger correlation at confirmation must also not be promoted as an independent edge because the V2 target is mechanically constructed from remaining run at confirmation.

## Primary finding 3 — shape remains broad positive but not strictly monotonic

Descriptive V2 consumed-ratio quartiles over the 82 resolved rows:

| empirical quartile | N | TARGET_FIRST | POINT_CHECK_FIRST | target-first proportion |
| --- | ---: | ---: | ---: | ---: |
| Q1 | 21 | 7 | 14 | 33.33% |
| Q2 | 20 | 4 | 16 | 20.00% |
| Q3 | 20 | 14 | 6 | 70.00% |
| Q4 | 21 | 19 | 2 | 90.48% |

The lower two bins are not monotonic, while the upper half rises strongly.

After retaining the central 80% of consumed values, the rank relationship remains positive at approximately `+0.4234`.

Safe interpretation:

`BROAD POSITIVE / NONLINEAR-OR-IRREGULAR / NO THRESHOLD`

The high-consumed top quartile is descriptive only. It must not be promoted to a fixed entry threshold or a “90% rule”.

## Primary finding 4 — failure / PASS / unknown map

Eligible H4 origin count per day:

- 0 origins: 74 days
- 1 origin: 57 days
- 2 origins: 16 days
- 3 origins: 3 days

Daily Frame construction:

- exactly one frame candidate on all 150 days
- frame-tie days: 0

No occurrence in this period of:

- `PASS_FRAME_TIE`
- `PASS_NO_M5_PAT2_CONFIRMATION`
- `PASS_RUN_COMPLETED_BEFORE_CONFIRMATION`
- `PASS_DATA_QUALITY`
- `PASS_UNKNOWN_STATE`

Absence in this one period does not prove these states cannot occur.

All 84 research-candidate rows have:

`location_qualification_state = UNKNOWN`

which is expected under frozen V2.0. The research frame-side proxy is metadata only:

- EXPECTED_SIDE_RESEARCH_PROXY: 83
- CROSSED_SIDE_RESEARCH_PROXY: 1

It must not be upgraded into canonical location qualification.

## Primary finding 5 — independent-origin lifecycle remains material

There are 14 origin rows destroyed before confirmation across 14 dates.

Only 9 dates end with the whole research day in `PASS_ORIGIN_DESTROYED_BEFORE_CONFIRMATION`.

Five dates contain both a destroyed origin and another surviving research candidate:

- 2022-09-13
- 2022-10-28
- 2022-11-08
- 2022-12-22
- 2023-03-03

This is consistent with the source-backed per-origin lifecycle: destruction of one origin does not globally erase other valid origins.

Destroyed-before-confirmation rows have low consumed state descriptively:

- median consumed ratio at 07:00: 0.000
- mean: 0.1394
- max: 0.6047

Research candidates:

- median: 0.5069
- mean: 0.4698

This difference is descriptive and may be structurally coupled to early point-check vulnerability; it is not promoted as a decision rule.

## Exploratory / incidental findings — not predeclared rules

These observations are recorded because they may motivate later bounded RQs. They do not change V2.0.

### BUY / SELL asymmetry

Resolved rows:

- BUY: 22 TARGET_FIRST / 13 POINT_CHECK_FIRST = 62.86%
- SELL: 22 TARGET_FIRST / 25 POINT_CHECK_FIRST = 46.81%

Consumed relation remains positive within both sides:

- BUY rank relation: approximately +0.3703
- SELL rank relation: approximately +0.6164

This suggests the broad consumed relation is not produced solely by mixing BUY and SELL rows. The side-level difference itself remains exploratory and may be period/context dependent.

### Conflict state does not show a discovery veto

Resolved candidate rows:

- non-conflict action state: 24 / 47 TARGET_FIRST = 51.06%
- conflict action state: 20 / 35 TARGET_FIRST = 57.14%

Opposite-origin metadata:

- zero opposite origins: 31 / 57 TARGET_FIRST = 54.39%
- one opposite origin: 13 / 24 TARGET_FIRST = 54.17%
- two opposite origins: one row only, POINT_CHECK_FIRST

This is consistent with earlier Q1 evidence that opposite-direction surviving origin presence is not a proven veto.

Conflict rows are dependent context/origin rows, not independent trades. No conflict-resolution rule is inferred.

Conflict-day fingerprints among 19 action-level conflict days:

- opposite present with no same-side multiplicity: 12
- multiple same-side only: 5
- both multiple same-side and opposite present: 2

### Simple metadata did not reveal another strong relationship

Rank relationship with TARGET_FIRST indicator on resolved rows:

- signed Daily Frame research-proxy distance: approximately -0.0356
- M5 confirmation delay from 07:00: approximately -0.0110
- additional consumed movement between 07:00 and confirmation: approximately -0.0815

These are near zero in this discovery sample and are not promoted.

### Confirmation timing

Across 84 research-candidate rows:

- median M5 confirmation delay after 07:00: 17.5 minutes
- mean: 22.38 minutes
- 34 rows changed consumed state between 07:00 and confirmation
- median consumed change: 0 points
- mean consumed change: about 110.83 project points

The two `NEITHER_BY_NEXT_0700` rows are both SELL:

- 2022-09-14 — consumed ratio at 07:00 approximately 0.4517
- 2023-03-02 — consumed ratio at 07:00 = 0.0

Two rows are insufficient to define a NEITHER fingerprint.

## Falsification / correction check

The discovery did not falsify the broad H4 consumed/run-progress lead.

It did falsify any expectation that the relationship should be strictly monotonic across empirical quartiles.

It also provides no discovery support for introducing:

- an opposite-origin veto;
- a fixed MTF/conflict rule;
- a frame-distance threshold;
- a confirmation-delay threshold;
- a consumed threshold.

## Version boundary

V2.0 remains frozen.

No source geometry was inferred from this outcome.

Any semantic change must become V2.1 or later and must be frozen before its outcome is inspected.

## Next bounded action

Run the unchanged frozen V2.0 implementation on the complete replication period:

`2023-09-01 -> 2023-11-23`

No V2.0 semantic or code change is allowed between discovery and replication.

The replication comparison should focus on:

1. day-state and action-state coverage;
2. FULL-RANGE population shift;
3. PATH_REMAINING first-hit map;
4. H4 consumed/run-progress rank relation and broad shape;
5. independent-origin destruction/conflict fingerprints;
6. whether BUY/SELL asymmetry and other exploratory observations recur.

Only after unchanged-code replication should a new source question or V2.1 semantic change be considered.