# RQ-015 — 07:00 PATH_REMAINING Geometry Control

Status: ACTIVE — GEOMETRY-CONFOUND FALSIFICATION

## Why this is active now

Frozen V2.0 Discovery and unchanged-code Replication both reproduced a broad positive association between H4 consumed/run-progress and PATH_REMAINING target-first ordering.

However, the first explicit geometry control found:

- consumed at 07:00 is strongly correlated with target-vs-point-check geometry in both periods;
- the geometry diagnostic is more strongly associated with TARGET_FIRST than consumed alone;
- the positive consumed association does not retain a positive partial-rank residual after controlling for the geometry diagnostic;
- consumed at confirmation is exactly inversely tied to remaining target distance by construction.

Therefore the independent market-information interpretation is not established.

Authority:

`docs/0700_MINIMAL_V2_REPLICATION_GEOMETRY_CONTROL_2026-09-13.md`

Historical Q3/Q4 remain preserved and are not rewritten.

## Research question

Does H4 consumed/run-progress retain stable information after a frozen, predeclared target-vs-point-check geometry baseline is accounted for?

## Null / alternative framing

Geometry-null interpretation:

`The observed consumed association can be explained by the relative distances to PATH_REMAINING target and point-check under the frozen scoring construction.`

Residual-information interpretation:

`After accounting for frozen geometry, consumed/run-progress retains stable cross-period information about target-vs-point-check ordering.`

Do not assume either interpretation is correct before the control is frozen and evaluated.

## Required pre-outcome freeze

Before any further scoring or model comparison, freeze:

1. exact geometry variables;
2. handling of TARGET_FIRST / POINT_CHECK_FIRST / NEITHER / AMBIGUOUS;
3. cross-period comparison method;
4. any residualization or stratification method;
5. reporting rules;
6. no threshold optimization.

## Candidate geometry variables

These are research candidates, not yet frozen canonical predictors:

- target distance at confirmation;
- point-check distance at confirmation;
- scale-free relative-distance diagnostic:
  `point_distance / (point_distance + target_distance)`;
- finite-horizon status and time remaining to next 07:00.

No formula may be selected because it produces a preferred outcome.

## Guardrails

- No consumed threshold.
- No geometry threshold.
- No trade-level Win Rate.
- No broker fill/cost/P&L inference.
- Preserve same-bar ambiguity.
- Preserve NEITHER; do not silently condition it away in a full-horizon model.
- Discovery/Replication may be used for falsification and representation testing, not pristine final confirmation.
- PAT3 remains queued and excluded from this RQ.
- Exact location geometry remains unresolved and must not be inferred from outcomes.

## Success criteria

This RQ is complete when one of the following evidence-backed states is reached:

1. `CONSUMED_RESIDUAL_RELATION_SURVIVES_GEOMETRY_CONTROL`;
2. `CONSUMED_ASSOCIATION_EXPLAINED_OR_DOMINATED_BY_GEOMETRY`;
3. `INDEPENDENT_EFFECT_NOT_IDENTIFIABLE_WITH_CURRENT_DATA`.

Any result must be reported separately for Discovery and Replication and preserve contradictions.

## Immediate next action

Freeze a geometry-null analysis specification before running additional outcome summaries.