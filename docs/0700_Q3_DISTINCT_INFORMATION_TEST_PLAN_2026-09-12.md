# 07:00 Q3 — Distinct Information / Redundancy Test Plan — 2026-09-12

Status: FROZEN BEFORE Q3 CALCULATION / EXPLORATORY RELATIONSHIP PLAN

## Why Q3 exists

Q2 produced three research leads:

1. origin age at 07:00 showed the cleanest directional replication across both periods and both H1/H4;
2. H4 run-progress state retained a stable relation across both periods, while H1 did not;
3. recent graded multi-TF agreement was directionally positive across both periods, while exact simultaneous alignment was near-zero/sparse.

Q3 asks whether these relationships contain distinct information or are redundant views of the same state.

Q3 is not a model-selection, score-building, or threshold-optimization exercise.

## Primary population

Use the frozen Q2 feature-event population:

```text
variant == FIRST_EXPECTED_SIDE_PA_PROXY
candidate_state == SCORED
origin_tf == H4
PATH_REMAINING_AT_CONFIRMATION outcome
```

Resolved binary rows only for association:

```text
TARGET_FIRST      -> 1
POINT_CHECK_FIRST -> 0
```

Retain counts of NEITHER and AMBIGUOUS in the period report.

Reason for H4 primary population:

- H4 consumed/remaining state replicated strongly in Q2;
- H1 consumed/remaining relation did not replicate;
- mixing H1/H4 would reintroduce the exact heterogeneity Q2 identified.

H1 must be run as a pre-declared sensitivity population with the same code.

## Frozen primary features

### A — origin age

`origin_age_hours_at_0700`

### B — run progress

`consumed_ratio_at_0700`

This is the primary run-progress feature because it is normalized by nominal run distance.

Remaining-ratio fields are not entered simultaneously with consumed ratio in the same control set because they are strongly related by construction and would create redundant geometry.

### C1 — recent MTF agreement window 1

`alignment_count_recent_1_tf_bar`

### C2 — recent MTF agreement window 2

`alignment_count_recent_2_tf_bars`

C1 and C2 are analyzed in separate control models.

Q3 is prohibited from selecting the better window and calling it canonical.

## Analysis 1 — feature redundancy map

For each period and each origin timeframe population:

Calculate pairwise Spearman rho among:

- age;
- consumed ratio;
- recent-1 alignment;
- recent-2 alignment.

Report N and rho.

This determines whether apparently separate leads are themselves highly correlated.

No correlation threshold defines redundancy.

## Analysis 2 — partial Spearman relationship

Use rank-residual partial correlation.

For every primary feature:

1. rank-transform feature, outcome, and control variables using average ranks;
2. fit ordinary least squares of ranked feature on ranked controls;
3. fit ordinary least squares of ranked outcome on ranked controls;
4. correlate the two residual vectors with Pearson correlation.

This is equivalent to a partial Spearman-style association under the frozen rank-residual representation.

### H4 model family A

`age | consumed + recent-1`

`consumed | age + recent-1`

`recent-1 | age + consumed`

### H4 model family B

`age | consumed + recent-2`

`consumed | age + recent-2`

`recent-2 | age + consumed`

Repeat the exact same families for H1 as sensitivity.

No interaction term is fitted in Q3.

No nonlinear transform is selected after outcome.

## Analysis 3 — context-level partial relationship

Rows sharing the same `day_id + side` context are not independent.

For each timeframe population, aggregate resolved origin rows by `context_id`:

```text
context outcome
    = mean target_first_indicator

context age
    = median origin_age_hours_at_0700

context consumed
    = median consumed_ratio_at_0700

context recent-1
    = median alignment_count_recent_1_tf_bar

context recent-2
    = median alignment_count_recent_2_tf_bars
```

Run the same rank-residual partial correlations at context level.

A lead is not considered robust if origin-row direction and context-level direction materially contradict each other.

## Analysis 4 — leave-one-feature-out descriptive comparison

This is not predictive model optimization.

For each model family, calculate a fixed logistic model only to compare descriptive information contribution:

Full model:

```text
target_first ~ age_rank + consumed_rank + mtf_rank
```

Then three leave-one-feature-out models:

- remove age;
- remove consumed;
- remove MTF.

Report only:

- in-sample log loss;
- delta log loss versus full model;
- coefficient signs.

No probability threshold is applied.
No classification accuracy is reported.
No model is promoted into a trading decision rule.

Reason: partial correlation can show conditional direction, while fixed leave-one-out log loss can reveal whether a variable contributes measurable descriptive information beyond the others.

Q3 is prohibited from tuning regularization or selecting a model from outcome.

Use unregularized logistic regression implemented deterministically; if fitting fails or separates, mark the model `UNSTABLE/UNRESOLVED` rather than changing the method.

## Cross-period requirement

Run the same frozen Q3 scorer on:

### Discovery
`2022-09-01 -> 2023-03-31`

### Replication
`2023-09-01 -> 2023-11-23`

No Q3 implementation change is allowed between the two calculations.

For each feature/window/population, classify direction only as:

- `SAME_SIGN`
- `SIGN_FLIP`
- `ZERO_OR_UNDEFINED`

No partial-rho magnitude threshold promotes a rule.

## Interpretation discipline

A feature may be carried forward only as a distinct-information research lead when:

1. marginal relation had already replicated in Q2;
2. partial relation has the same sign in discovery and replication;
3. origin-row and context-level partial relations do not contradict materially;
4. the feature is not merely surviving because of one tiny count subgroup;
5. leave-one-out descriptive contribution is not obviously zero/unstable in both periods.

This remains a research-evidence criterion, not a trading gate.

## Expected falsification possibilities

Q3 may show that:

- age is merely a proxy for consumed run;
- H4 consumed ratio remains distinct after controlling for age and MTF;
- recent MTF agreement disappears after controlling for origin state;
- recent-1 and recent-2 windows disagree;
- H1 behaves differently from H4;
- all three effects weaken enough that no distinct-information claim is justified.

Any of these is a valid result.

## Claims prohibited by Q3

Q3 may not create:

- a weighted score;
- a probability-of-win model for trading;
- an age cutoff;
- consumed-ratio cutoff;
- MTF minimum;
- canonical recent-1 or recent-2 window;
- H1/H4 priority;
- entry rule;
- trade/system Win rate;
- expectancy or profitability claim;
- universal SL;
- canonical instructor intent.

## Required outputs

For each period:

1. `Q3_FEATURE_ROWS.csv`
2. `Q3_PAIRWISE_SPEARMAN.csv`
3. `Q3_PARTIAL_ASSOCIATIONS.csv`
4. `Q3_LEAVE_ONE_OUT.csv`
5. `REPORT.json`

Then one cross-period checkpoint must distinguish:

- distinct-information leads;
- redundant/unstable leads;
- timeframe heterogeneity;
- unresolved source questions.
