# 07:00 Q2 — Continuous Origin State and Graded MTF Freshness Test Plan — 2026-09-12

Status: FROZEN BEFORE Q2 ASSOCIATION CALCULATION / EXPLORATORY RELATIONSHIP PLAN

## Motivation from Q1

Q1 produced two periods with the same frozen scorer.

Cross-period findings:

1. PATH_REMAINING_AT_CONFIRMATION ranked ahead of ORIGIN_TARGET_LEVEL in both periods.
2. Simple H1/H4 priority did not replicate cleanly.
3. H1+H4 context did not remain clearly superior to H1-only.
4. Opposite-direction origin conflict did not justify a veto.
5. Exact same-close-time H1/M30/M15/M5 alignment above one timeframe was too sparse in both periods.
6. The source-backed idea is graded confluence, not a proven minimum timeframe count.

Q2 therefore does **not** search for a new threshold.

It asks whether retaining more state information produces relationships that are more stable across periods.

## Research question

Among Q1 origins that remain active until the selected confirmation:

> How are origin age, run-consumption state, and graded recent multi-timeframe PA agreement related to PATH_REMAINING target-vs-point-check ordering?

This is a relationship study.

It is not a rule-selection or optimization task.

## Periods

### Discovery

`2022-09-01 -> 2023-03-31`

### Replication

`2023-09-01 -> 2023-11-23`

The same Q2 code and feature definitions must be used on both periods.

No Q2 feature, formula, grouping rule, or association statistic may be changed after discovery Q2 output is opened and before replication Q2 is calculated.

## Base Q1 population

Primary Q2 population uses:

```text
variant == FIRST_EXPECTED_SIDE_PA_PROXY
candidate_state == SCORED
```

Reason:

- this variant is the source-closer representation because the post-07:00 PA is on the frozen Daily Frame expected side;
- Q1 showed FIRST_ANY and FIRST_EXPECTED were almost identical in both periods;
- the choice is frozen before Q2 association output is calculated.

FIRST_ANY_PA_PROXY remains available as a sensitivity population but may not be substituted after seeing Q2 results.

## Primary outcome

Use the Q1 PATH_REMAINING_AT_CONFIRMATION first-hit state.

Resolved outcome rows:

```text
TARGET_FIRST       -> target_first_indicator = 1
POINT_CHECK_FIRST  -> target_first_indicator = 0
```

Retain and report, but exclude from binary rank association:

```text
NEITHER_BEFORE_NEXT_0700
AMBIGUOUS_SAME_BAR
```

Excluding these rows from the binary association is an accounting choice, not evidence that they are unimportant.

Counts must always be reported.

## Secondary outcome sensitivity

Repeat the same association table for:

`ORIGIN_TARGET_LEVEL`

This remains a sensitivity representation only because Q1 ranked it behind PATH_REMAINING in both periods.

Q2 may not promote one target representation based on Q2 performance.

## Continuous origin-state features

No cutoff is allowed.

### Primary normalized / directly comparable features

1. `origin_age_hours_at_0700`
2. `consumed_ratio_at_0700`
3. `remaining_ratio_at_confirmation`

where:

```text
remaining_ratio_at_confirmation
    = remaining_points_at_confirmation / nominal_run_points
```

These remain continuous.

### Secondary absolute features

1. `remaining_points_at_0700`
2. `remaining_points_at_confirmation`

Because nominal H1 and H4 run distances differ, absolute-point features must also be summarized separately by origin timeframe.

No absolute-point threshold may be selected.

## Graded MTF freshness features

Join each Q1 selected confirmation back to the frozen V1 confirmation-event table using:

`confirmation_event_id == event_id`

Use the three already-frozen research representations:

1. `alignment_count_exact`
2. `alignment_count_recent_1_tf_bar`
3. `alignment_count_recent_2_tf_bars`

Definitions were frozen in V1 before Q1 outcomes:

- exact: latest same-direction PA proxy known at the same event knowledge time;
- recent-1: latest same-direction PA proxy within one bar of each respective timeframe;
- recent-2: latest same-direction PA proxy within two bars of each respective timeframe.

The one-bar and two-bar windows are research representations.

They are **not** instructor thresholds.

All three are reported in parallel.

Q2 is prohibited from choosing the best window and calling it canonical.

## Association method — origin-row level

For every Q2 feature, calculate Spearman rank correlation:

```text
feature
vs
target_first_indicator
```

on resolved rows only.

Report:

- N resolved rows
- feature unique-value count
- Spearman rho
- TARGET_FIRST feature median
- POINT_CHECK_FIRST feature median
- TARGET_FIRST feature IQR
- POINT_CHECK_FIRST feature IQR

No p-value threshold is used for rule selection.

No rho magnitude threshold is defined.

## Association method — context level

Rows sharing `day_id + side` are not independent.

Therefore a second table must aggregate by `context_id`.

For every context with at least one resolved origin row:

```text
context_target_first_fraction
    = TARGET_FIRST resolved origin count / resolved origin count

context_feature
    = median feature across resolved origins in that context
```

Then calculate Spearman rank correlation:

```text
context_feature
vs
context_target_first_fraction
```

Report:

- N contexts
- rho
- median resolved origins per context

This context-level result is required before interpreting any origin-row relation.

## MTF count distributions

For each of the three alignment representations, also report each observed count value:

```text
alignment_count = 1 / 2 / 3 / 4
origin rows
contexts
TARGET_FIRST
POINT_CHECK_FIRST
NEITHER
AMBIGUOUS
resolved target-first fraction
```

This is descriptive.

No minimum count is selected.

## Timeframe-stratified origin-state sensitivity

For the continuous origin-state features, repeat origin-row rank associations separately for:

- H1
- H4

This tests whether a combined relation is merely a nominal-run/timeframe mixture.

A relation that changes sign between H1 and H4 must be labeled heterogeneous rather than converted into one universal rule.

## Cross-period comparison

For every feature and analysis level, compare discovery versus replication.

Possible descriptive labels:

- `SAME_SIGN`
- `SIGN_FLIP`
- `ZERO_OR_UNDEFINED`

No minimum rho is required for these labels.

Same sign alone does not establish a useful trading effect.

The magnitude and sample structure must still be reported.

## What counts as a useful Q2 result

A result may be carried forward as a research lead only when:

1. its feature definition was frozen before outcome association;
2. origin-row and context-level results do not materially contradict each other;
3. discovery and replication do not show a sign flip;
4. sample support is not a tiny exceptional subgroup;
5. the result is described as a relationship, not a threshold/rule.

This is a research discipline criterion, not a trading gate.

## What Q2 may falsify

Q2 is specifically capable of weakening the following ideas:

- older surviving origin is automatically better or worse;
- more consumed run is automatically better or worse;
- more remaining run is automatically better or worse;
- more recent aligned timeframes necessarily improves target-first ordering;
- exact simultaneous alignment is the right confluence representation.

A null or unstable relationship is a valid result.

## Claims prohibited by Q2

Q2 may not claim:

- system or trade Win rate;
- expectancy;
- profitability;
- canonical MTF minimum;
- canonical freshness window;
- H1/H4 priority;
- origin-age expiry threshold;
- consumed-ratio threshold;
- remaining-run threshold;
- exact instructor PA/PAT/SIG geometry;
- exact 50% denominator;
- D1 run distance;
- universal SL.

## Required output

For each period:

1. `Q2_FEATURE_EVENTS.csv`
2. `Q2_ASSOCIATIONS.csv`
3. `Q2_MTF_COUNT_GROUPS.csv`
4. `REPORT.json`

Then produce one cross-period checkpoint that distinguishes:

- directionally replicated relationships;
- sign flips;
- undefined/sparse relationships;
- remaining unresolved questions.

No production rule is created by Q2.
