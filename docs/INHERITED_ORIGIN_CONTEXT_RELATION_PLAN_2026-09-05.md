# Inherited Origin Context × Daily Frame Side — Relation Plan — 2026-09-05

Status: FROZEN BEFORE NEW ORIGIN-CONTEXT OUTCOME EVALUATION

## Why this round exists

The prior graded-MTF interaction closed `INCONCLUSIVE` across all three frozen freshness variants. The next declared research path is therefore to study the state of the inherited origin itself instead of continuing to mine MTF freshness or aligned-timeframe thresholds.

## Exact question

Within `INHERITED_REMAINING_RUN` events, especially those on Daily Frame `EXPECTED_SIDE`, does forward behavior vary systematically with:

1. origin age;
2. how much of the nominal H1 run has already been consumed at candidate entry;
3. whether the origin belongs to the immediately preceding 24-hour preparation cycle or is older?

This is a relation test. Unknown values are preserved as continuous measurements first rather than converted into guessed production thresholds.

## Source tables

Join the already-produced research tables by:

```text
candidate_known_at + side
```

Required Remaining-Run source fields:

- `state`
- `cutoff_utc`
- `candidate_known_at`
- `side`
- `origin_anchor_known_at`
- `remaining_at_entry_points`
- `fresh_target_reached_anywhere`
- `fresh_first_hit`
- `fresh_mfe_points`
- `fresh_mae_points`
- `path_remaining_reached`
- `path_remaining_first_hit`
- `origin_level_reached`
- `origin_level_first_hit`

Required Daily-Frame interaction fields:

- `candidate_known_at`
- `side`
- `signed_valid_side_distance_points`

No raw-price recomputation is needed for this round because the necessary origin and outcome fields already exist in the prior deterministic event tables.

## Frozen derived features

For inherited events only:

```text
frame_side = EXPECTED_SIDE if signed_valid_side_distance_points >= 0 else CROSSED_SIDE

origin_age_hours = candidate_known_at - origin_anchor_known_at

consumed_run_ratio_at_entry =
    (1000 - remaining_at_entry_points) / 1000

origin_cycle_group =
    PREVIOUS_24H_CYCLE if origin_anchor_known_at > cutoff_utc - 24h
    OLDER_THAN_PREVIOUS_24H otherwise
```

The H1 nominal 1,000 project-point run is already part of the active Remaining-Run research representation. The 24-hour cycle boundary is tied to the daily preparation cutoff; it is not proposed as a production expiry rule.

## Primary outcomes — fixed-target control

Use the existing fresh H1 1,000-point control as the primary outcome lane:

- resolved target-first binary from `fresh_first_hit`;
- fresh-1000 reach from `fresh_target_reached_anywhere`;
- fresh MFE;
- fresh MAE.

Reason: `PATH_REMAINING` target size shrinks mechanically as more run is consumed. Using the fixed fresh-1000 control prevents that target-size mechanic from being mistaken for evidence that a larger consumed ratio is intrinsically better.

## Secondary descriptive outcomes

Retain, but do not use to define the primary origin-context direction:

- `PATH_REMAINING` reach / first hit;
- `ORIGIN_TARGET_LEVEL` reach / first hit.

These remain useful comparators and may show whether a relationship is specific to one target representation.

## Continuous relation measurements

For `origin_age_hours` and `consumed_run_ratio_at_entry`, calculate Spearman relation with each primary fixed-control outcome separately for:

- `EXPECTED_SIDE` — primary;
- `CROSSED_SIDE` — secondary interaction comparator.

Minimum side-group events: 10, inherited from the parent Daily-Frame-side checkpoint.

At least two distinct observed feature values are required. No per-bin minimum and no magnitude cutoff such as `|rho| > X` is invented.

## Direction labels

### Origin age

`YOUNGER_ORIGIN_FAVORED` when all primary relations move in the direction expected if increasing age is worse:

- age vs target-first < 0;
- age vs reach <= 0;
- age vs MFE <= 0;
- age vs MAE >= 0.

`OLDER_ORIGIN_FAVORED` when all four reverse.

Otherwise `MIXED`, `INSUFFICIENT`, or `INDISTINGUISHABLE`.

These labels describe the measured direction; neither direction is asserted in advance as instructor intent.

### Consumed-run ratio

`MORE_CONSUMED_FAVORED` when:

- consumed ratio vs fixed target-first > 0;
- consumed ratio vs fixed reach >= 0;
- consumed ratio vs fresh MFE >= 0;
- consumed ratio vs fresh MAE <= 0.

`LESS_CONSUMED_FAVORED` when all four reverse.

Otherwise `MIXED`, `INSUFFICIENT`, or `INDISTINGUISHABLE`.

Because the primary outcomes use the fixed fresh-1000 control, these labels are not mechanically caused by a smaller `PATH_REMAINING` target.

## 24-hour cycle comparison

Compare `PREVIOUS_24H_CYCLE` versus `OLDER_THAN_PREVIOUS_24H` on the same four primary fixed-control metrics inside `EXPECTED_SIDE` first.

Minimum 10 events per compared group.

- all four favor previous-24h origin -> `PREVIOUS_24H_FAVORED`
- all four favor older origin -> `OLDER_CYCLE_FAVORED`
- otherwise -> `MIXED` / `INSUFFICIENT`

This is a bounded research representation of origin recency, not a canonical expiry rule.

## Cross-period closure

Use the same existing periods:

- 2022-09-01 through 2023-03-31;
- 2024-09-01 through 2024-11-30;
- 2025-09-01 through 2025-11-30.

For each feature, a directional relation may be called `REPLICATED_RESEARCH_RELATION` only when the same non-mixed direction appears in at least two usable periods and no usable period shows the opposite direction.

Opposite directions across usable periods -> `NOT_STABLE_ACROSS_PERIODS`.

Otherwise -> `INCONCLUSIVE`.

## Guardrails

- Do not convert age or consumed ratio into a production threshold from this round.
- Do not use historical outcome to identify instructor intent.
- Do not call fresh target-first rate a strategy win rate.
- Do not discard `ORIGIN_TARGET_LEVEL`; retain it as a comparator.
- Do not infer an expiry rule merely because younger origins look better.
- Do not change the prior MTF closure based on origin-context results.

## Follow-up only if needed

If origin age/cycle results are stable enough to justify a narrower question, then freeze a small bounded family of explicit expiry/invalidation variants and test them separately. Do not invent expiry variants before this lower-assumption relation round is measured.
