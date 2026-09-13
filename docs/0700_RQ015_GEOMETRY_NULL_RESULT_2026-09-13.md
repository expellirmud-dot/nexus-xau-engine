# RQ-015 Geometry-Null Result - 2026-09-13

Status: CLOSED / CONSUMED_ASSOCIATION_EXPLAINED_OR_DOMINATED_BY_GEOMETRY

Frozen analysis and implementation were executed unchanged on the checkpointed V2.0 Discovery and Replication event artifacts.

Analyzer: `src/nexus_xau/research/geometry_null_rq015.py`

Implementation SHA256: `8f0579b922d31bb762f13d38d8ac0f067b37c7d97868ce3556426e641d81cb81`

Result artifact: `results/0700_RQ015_GEOMETRY_NULL/REPORT.json`

## Inputs and validation

Discovery input SHA256: `7c421c0e27a55f065f4f422b207cbd037910770be59c0e7b9189ddefaef4b3a8`

Replication input SHA256: `7f607066bcf694bea3ec16e3c37f0cf09ec9375a6d0c4eb164c60f1d39026e48`

Geometry validation passed: target distance matches the frozen remaining-points construction, all geometry denominators are positive, and all confirmation-to-next-07:00 horizons are positive.

## Lane A - all outcome states preserved

Discovery candidate rows: 84 — TARGET_FIRST 44, POINT_CHECK_FIRST 38, NEITHER 2, AMBIGUOUS 0.

Replication candidate rows: 42 — TARGET_FIRST 16, POINT_CHECK_FIRST 23, NEITHER 2, AMBIGUOUS 1.

NEITHER and AMBIGUOUS were not recoded as losses and were not silently removed from the full-state output.

## Lane B - resolved ordering diagnostic

Discovery resolved rows: 82.
- consumed 07:00 vs TARGET_FIRST: +0.5131
- geometry vs TARGET_FIRST: +0.6148
- consumed 07:00 vs geometry: +0.8668
- primary partial-rank residual: -0.0181
- secondary confirmation-consumed residual: +0.0848

Replication resolved rows: 39.
- consumed 07:00 vs TARGET_FIRST: +0.5033
- geometry vs TARGET_FIRST: +0.6855
- consumed 07:00 vs geometry: +0.8282
- primary partial-rank residual: -0.1009
- secondary confirmation-consumed residual: -0.1353

Frozen classification: `CONSUMED_ASSOCIATION_EXPLAINED_OR_DOMINATED_BY_GEOMETRY`.

## Interpretation

Historical Q3/Q4 and V2.0 remain valid evidence that consumed/run-progress is associated with PATH_REMAINING target-first ordering.

RQ-015 narrows that interpretation: the positive consumed relation is not established as independent market information. Under the frozen geometry-null analysis, the primary consumed residual is non-positive in both periods while geometry is more strongly related to outcome.

This does not prove that consumed contains zero information in every possible representation. It shows that the current PATH_REMAINING scoring construction does not identify a stable independent consumed effect beyond target/point-check geometry.

The secondary confirmation-consumed residual changes sign across periods and cannot override the frozen primary result.

## Guards

This was not a pristine blind holdout. No consumed/geometry threshold or alternate model was selected after result inspection. No trade Win Rate, PnL, fill, cost, expectancy, or profitability claim follows.

RQ-015 is complete. Without new source evidence, already exhausted Daily Frame/D1/PAT source gaps should not be reopened merely to seek a positive result.
