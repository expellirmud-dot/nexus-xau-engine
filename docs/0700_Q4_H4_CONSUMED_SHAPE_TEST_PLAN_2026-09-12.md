# 07:00 Q4 — H4 Consumed-State Shape Diagnostic Plan — 2026-09-12

Status: FROZEN BEFORE Q4 CALCULATION / DESCRIPTIVE SHAPE STUDY ONLY

## Why Q4 exists

Q3 identified `consumed_ratio_at_0700` as the strongest distinct cross-period H4 relationship lead.

Q4 does **not** search for a threshold.

It asks whether the H4 consumed-state relationship:

1. changes smoothly across the observed range;
2. is approximately monotonic;
3. survives when extreme low/high consumed observations are removed; or
4. is mostly created by a small extreme region / proxy artifact.

## Primary population

Use frozen Q3 resolved feature rows:

```text
origin_tf == H4
PATH_REMAINING outcome resolved
TARGET_FIRST      -> 1
POINT_CHECK_FIRST -> 0
```

Periods:

- Discovery: 2022-09-01 -> 2023-03-31
- Replication: 2023-09-01 -> 2023-11-23

Use the same frozen Q4 code on both periods.

## Primary feature

`consumed_ratio_at_0700`

No transformation is selected after outcome.

## Diagnostic A — full-sample rank relation

For each period, calculate:

- origin-row Spearman rho;
- context-level Spearman rho.

Context aggregation:

```text
context consumed = median consumed ratio
context outcome  = mean resolved target-first indicator
```

This reproduces the Q3 lead in a Q4-specific artifact before shape diagnostics.

## Diagnostic B — fixed five-quantile shape

Use exactly five equal-frequency groups within each period.

The number five is frozen before Q4 outcome calculation.

These quantile boundaries are descriptive sample partitions only.

They are **not** candidate entry thresholds.

For each quintile report:

- quantile label Q1..Q5;
- observed consumed min/max/median;
- origin rows;
- unique contexts;
- TARGET_FIRST count;
- POINT_CHECK_FIRST count;
- resolved target-first fraction;
- median post-confirmation MFE;
- median post-confirmation MAE.

Repeat at context level:

- context rows;
- consumed min/max/median;
- mean context target-first fraction.

## Diagnostic C — adjacent shape

For Q1 -> Q5 report the four adjacent changes in resolved target-first fraction:

```text
Q2 - Q1
Q3 - Q2
Q4 - Q3
Q5 - Q4
```

Report only the signs and raw differences.

No tolerance is introduced.

Classify only:

- `STRICT_NONDECREASING` if every adjacent difference >= 0;
- `NOT_STRICT_NONDECREASING` otherwise.

This classification is descriptive and cannot become a trading rule.

## Diagnostic D — central-80% sensitivity

To test whether the relation is driven only by extremes, calculate the same Spearman relation after removing observations below the 10th percentile and above the 90th percentile of consumed ratio within each period.

This fixed 10%-90% trim is frozen before outcome.

Report:

- N rows/contexts retained;
- origin-row rho;
- context-level rho;
- sign compared with full sample.

The 10th/90th percentile values are not trading thresholds.

## Diagnostic E — one-sided extreme removal

Also calculate:

1. remove only bottom 10%;
2. remove only top 10%.

Report Spearman rho at origin-row and context level.

Purpose:

- detect whether the positive relation disappears only when one extreme tail is removed;
- distinguish a broad relation from a single-tail artifact.

No result may be used to select a cutoff.

## Diagnostic F — H1 sensitivity

Run the exact same diagnostics for H1 as a predeclared sensitivity population.

Q3 showed H1 consumed-state independence did not replicate.

Therefore H1 is not a co-primary population.

Its purpose is to detect timeframe heterogeneity and prevent accidental generalization from H4.

## Cross-period interpretation

For H4, a relationship may be described as broad-shape-supported only if:

1. full-sample rho is positive in discovery and replication;
2. central-80% rho does not flip negative in either period;
3. the five-quantile pattern is not dependent on a single extreme bin in both periods;
4. context-level direction does not materially contradict origin-row direction.

This is a research-description criterion, not a trading gate.

A failure of exact monotonicity is not evidence that the relationship is useless.

A positive full-sample relation with unstable central sensitivity must be labeled extreme-sensitive.

## Prohibited conclusions

Q4 may not create or claim:

- consumed-ratio entry threshold;
- optimal consumed range;
- minimum/maximum consumed ratio;
- trading score;
- trade/system Win rate;
- expectancy;
- profitability;
- H1/H4 priority rule;
- canonical instructor intent;
- universal SL;
- canonical MTF window.

## Required outputs

For each period:

1. `Q4_FEATURE_ROWS.csv`
2. `Q4_QUINTILES.csv`
3. `Q4_TRIM_SENSITIVITY.csv`
4. `REPORT.json`

Then record:

- Discovery checkpoint;
- Replication/cross-period checkpoint;
- artifact hashes;
- code/test validation state;
- explicit claim boundary.

No Q5 begins before the Q4 cross-period checkpoint is committed and pushed.
