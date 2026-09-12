# 07:00 Q4 — Quantile Tie Failure Checkpoint / Pre-Outcome Technical Amendment — 2026-09-12

Status: RECORDED BEFORE ANY Q4 OUTCOME ARTIFACT / TECHNICAL AMENDMENT ONLY

## What happened

Frozen Q4 scorer commit:

`238b38a — research: freeze 07:00 Q4 consumed shape scorer`

The first Discovery execution stopped before producing any Q4 result artifact.

Failure:

```text
ValueError: Bin edges must be unique
```

The consumed-ratio feature has enough repeated values at exactly zero that the first and second empirical quintile boundaries were both zero.

Observed failing bin edges:

```text
0.0
0.0
0.39964000000000244
0.5633333333333365
0.8129600000000028
0.9953333333333376
```

The intended output directory was not created.

Therefore:

- no Q4 outcome table was written;
- no Q4 target-first quintile rates were observed;
- no Q4 trim sensitivity result was observed;
- no Q4 interpretation was available when this amendment was made.

## Why not force equal-frequency bins

A deterministic rank-first workaround could force exactly five equally sized groups, but it would split observations with identical consumed ratio (especially exact zero) into different bins based only on row ordering.

That would create artificial shape.

This is rejected.

## Technical amendment

Keep the original diagnostic intent of up to five empirical quantile regions, but preserve equal feature values in the same bin.

Implementation:

```text
pd.qcut(..., q=5, duplicates="drop")
```

Consequences:

- target quantile count remains 5;
- duplicate empirical edges are collapsed;
- effective bin count may be <5;
- bin labels are generated dynamically as Q1..Qk;
- exact equal consumed values are never split merely to satisfy equal-frequency counts.

## Shape classification amendment

Adjacent-shape analysis uses the actual ordered effective bins.

If fewer than 2 effective bins exist:

`UNRESOLVED_INSUFFICIENT_BINS`

Otherwise retain the original descriptive classification:

- STRICT_NONDECREASING
- NOT_STRICT_NONDECREASING

No effective bin boundary may be promoted into a trading threshold.

## What does not change

The following frozen Q4 elements remain unchanged:

- H4 primary population;
- H1 sensitivity;
- PATH_REMAINING resolved outcome;
- full-sample Spearman;
- context-level Spearman;
- 10%-90% central trim;
- one-sided bottom/top 10% removal;
- MFE/MAE descriptive fields;
- no threshold optimization;
- no trading rule;
- same code must be used for Discovery and Replication after this amendment is frozen.

## Evidence boundary

This amendment is driven only by the feature-value distribution and a runtime failure.

It was recorded before any Q4 outcome result was produced.
