# 07:00 MINIMAL V2.0 — Unchanged-Code Replication + Geometry Control — 2026-09-13

Status: REPLICATION COMPLETE / V2.0 UNCHANGED / INTERPRETATION CORRECTED

## Guard

This checkpoint compares the frozen V2.0 Discovery period with the unchanged-code Replication period.

No V2.0 detector, target, location rule, conflict rule, threshold, or source semantics were changed between periods.

This remains signal/run research only. No trade P&L or system Win Rate is computed or claimed.

## Replication durable receipt

Job:

`XAU-0700-MINIMAL-V2-REPLICATION-20260913`

Input:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2023-09-01_2023-11-23.csv`

Input SHA256:

`f5749ffc8dc55f095fd9b1519f54a3b1fe3902a96124adf9f330e48db9d83341`

Job state:

- status: DONE
- attempts: 1
- no recorded error

Replication artifact SHA256:

- `REPORT.json`: `8f44111e27157f9050f40d6f8160f55f11b887451b4d72cd1f668bf672c745ef`
- `0700_v2_day_state.csv`: `3a19ae4f5732c5ff08647584fa6421576f5037d0f8e2306f5bf6824c09ca4f31`
- `0700_v2_origin_context.csv`: `f8124efb0b0b3ef45abdb1566d814b3e3385cbe3ae434067c01c16227fe4e0df`
- `0700_v2_research_events.csv`: `7f607066bcf694bea3ec16e3c37f0cf09ec9375a6d0c4eb164c60f1d39026e48`

Implementation SHA256 at interpretation:

`25ccd02567e065230b7757dab73c80471c077f6419da65f3cd4c78db4d43cca7`

Git diff for:

- `src/nexus_xau/research/minimal_v2_0700.py`
- `tests/test_minimal_v2_0700.py`

was empty before replication interpretation.

## Replication population

60 complete 07:00 days.

Rows:

- eligible H4 origin rows: 46
- research-candidate rows: 42
- candidate days: 33

Day-level research states:

- `RESEARCH_CANDIDATE`: 33
- `PASS_NO_H4_ORIGIN`: 25
- `PASS_RUN_COMPLETED_BEFORE_CONFIRMATION`: 1
- `PASS_ORIGIN_DESTROYED_BEFORE_CONFIRMATION`: 1

Action states:

- `PASS_NO_H4_ORIGIN`: 25
- `PASS_SOURCE_GEOMETRY_UNRESOLVED`: 25
- `PASS_CONFLICT_UNRESOLVED`: 8
- `PASS_RUN_COMPLETED_BEFORE_CONFIRMATION`: 1
- `PASS_ORIGIN_DESTROYED_BEFORE_CONFIRMATION`: 1

Daily Frame tie remains absent in this period.

## PATH_REMAINING outcome comparison

Discovery candidate rows:

- TARGET_FIRST: 44
- POINT_CHECK_FIRST: 38
- NEITHER: 2
- AMBIGUOUS: 0
- resolved TARGET_FIRST proportion: 44 / 82 = 53.66%

Replication candidate rows:

- TARGET_FIRST: 16
- POINT_CHECK_FIRST: 23
- NEITHER: 2
- AMBIGUOUS_SAME_BAR: 1
- resolved TARGET_FIRST proportion: 16 / 39 = 41.03%

Therefore the unconditional target-first proportion does not replicate at the same level.

It remains a signal/run ordering statistic, not Win Rate.

## H4 consumed association does replicate descriptively

Spearman-style rank relation of `consumed_ratio_at_0700` with TARGET_FIRST indicator:

- Discovery: +0.5131
- Replication: +0.5033

Central-80% sensitivity:

- Discovery: +0.4234
- Replication: +0.3727

Replication empirical consumed quartiles:

| quartile | N | TARGET_FIRST | POINT_CHECK_FIRST | target-first proportion |
| --- | ---: | ---: | ---: | ---: |
| Q1 | 10 | 2 | 8 | 20.0% |
| Q2 | 10 | 2 | 8 | 20.0% |
| Q3 | 9 | 3 | 6 | 33.3% |
| Q4 | 10 | 9 | 1 | 90.0% |

This preserves a broad positive shape, especially at the upper end.

However, this finding is narrowed by the geometry control below.

## Falsification control — target / point-check geometry

### Why this control is required

V2.0 defines:

`remaining_points_at_confirmation = 1500 - consumed_points_at_confirmation`

and then constructs the PATH_REMAINING target from that remaining distance.

Therefore a larger consumed state mechanically makes the remaining target closer.

At the same time, as price moves away from the protected origin, the point-check distance can become larger.

A positive consumed-vs-TARGET_FIRST relation can therefore arise from the geometry of the scoring problem itself, even without independent market-state information.

### Geometry diagnostic

For resolved rows define a scale-free diagnostic:

`geometry_target_advantage = point_check_distance / (point_check_distance + target_distance)`

where:

- `target_distance = remaining_points_at_confirmation`
- `point_check_distance = absolute distance from confirmation close to origin anchor`

This is a geometry diagnostic only.

It is not promoted as a canonical probability model, because the actual process has a finite next-07:00 horizon, market drift/volatility, OHLC ordering ambiguity, and non-Brownian behavior.

### Results

Consumed at 07:00 vs geometry diagnostic:

- Discovery: +0.8668
- Replication: +0.8282

Geometry diagnostic vs TARGET_FIRST indicator:

- Discovery: +0.6148
- Replication: +0.6855

Consumed at confirmation vs target distance:

- Discovery: -1.0000
- Replication: -1.0000

This exact inverse relation is expected from the V2.0 remaining-run construction.

Consumed at 07:00 vs target distance at confirmation:

- Discovery: -0.9459
- Replication: -0.8933

Consumed at confirmation vs point-check distance:

- Discovery: +0.7891
- Replication: +0.8552

### Partial-rank diagnostic

After residualizing rank(consumed) and rank(outcome) against rank(geometry_target_advantage):

Consumed at 07:00 vs outcome, conditional on geometry diagnostic:

- Discovery: -0.0502
- Replication: -0.1578

Consumed at confirmation vs outcome, conditional on geometry diagnostic:

- Discovery: -0.0032
- Replication: -0.1122

Because consumed and geometry are highly collinear, these partial estimates must not be treated as precise causal coefficients.

But the previously positive consumed association does not retain a positive residual relationship after this geometry control in either period.

## Corrected interpretation

The earlier Q3/Q4 result remains valid as historical evidence that:

`H4 consumed state is associated with PATH_REMAINING target-first ordering`

and that the association reproduced across the historical periods under those representations.

What is no longer supported is the stronger interpretation that:

`consumed state has established independent market-predictive information beyond the geometry created by the PATH_REMAINING target and point-check distances`.

Current safe state:

`REPLICATED ASSOCIATION / STRONGLY GEOMETRY-CONFOUNDED / INDEPENDENT EFFECT NOT ESTABLISHED / NO THRESHOLD`

This does not prove consumed has no independent information.

The strong collinearity means the independent effect is currently not identifiable from the existing analysis.

Q3's earlier "distinct information" result controlled age and recent MTF, but did not control this target/point-check geometry variable. Therefore that historical result is preserved but narrowed.

## Exploratory findings checked across periods

### BUY / SELL asymmetry does not replicate

Discovery resolved:

- BUY: 22/35 TARGET_FIRST = 62.86%
- SELL: 22/47 = 46.81%

Replication resolved:

- BUY: 5/15 = 33.33%
- SELL: 11/24 = 45.83%

The Discovery BUY advantage does not replicate and must not be promoted.

Consumed association remains positive within both Replication sides:

- BUY rho approximately +0.367
- SELL rho approximately +0.569

These remain geometry-confounded.

### Opposite-origin presence still does not support a veto

Replication resolved:

- zero opposite origins: 8/22 TARGET_FIRST = 36.36%
- one opposite origin: 7/16 = 43.75%
- two opposite origins: 1/1

No veto is established.

### Conflict state still does not support a veto

Replication resolved:

- non-conflict: 8/22 TARGET_FIRST = 36.36%
- conflict: 8/17 = 47.06%

Dependent origin/context rows and small N prohibit a positive conflict rule as well.

## Newly observed failure states

### RUN completed before confirmation

One Replication origin:

- day: 2023-10-10
- side: BUY
- consumed ratio at 07:00: approximately 0.97087
- pre-confirmation state: `RUN_COMPLETE`
- candidate state: `PASS_RUN_COMPLETED_BEFORE_CONFIRMATION`

This state was absent in Discovery but was already part of the frozen taxonomy.

### Same-bar ambiguity

One Replication candidate:

- day: 2023-11-14
- side: BUY
- consumed ratio at 07:00: approximately 0.57487
- remaining points at confirmation: approximately 589
- target and point-check were both first touched in the same M1 bar at 13:30 UTC

Frozen V2.0 correctly records:

`AMBIGUOUS_SAME_BAR`

No tick-order inference is added.

## What changed in project knowledge

Previous safe claim:

`H4 consumed/run-progress is a replicated broad relation and strongest distinct-information research lead among age/MTF variables.`

New narrower claim:

`H4 consumed/run-progress is a replicated broad association with PATH_REMAINING ordering, but it is strongly entangled with target/point-check geometry. Its independent market information is not established.`

The old Q3/Q4 documents are not rewritten.

This checkpoint records why the current interpretation changed.

## Next bounded research question

Before PAT3 expansion, thresholds, or trade-level scoring, test the geometry-null question explicitly:

`Does consumed/run-progress retain stable information after a frozen, predeclared target-vs-point-check geometry baseline is accounted for?`

Required constraints:

1. no consumed threshold optimization;
2. no outcome-selected geometry formula;
3. freeze the geometry control representation before further scoring;
4. use both Discovery and Replication;
5. preserve NEITHER and AMBIGUOUS instead of silently dropping them in any full-horizon model;
6. distinguish association caused by scoring geometry from market behavior;
7. do not call any residual a trade edge without execution/cost/holdout evidence.