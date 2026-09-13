# RQ-015 Geometry-Null Analysis Freeze - 2026-09-13

Status: FROZEN BEFORE FURTHER SCORING / NOT PRISTINE BLIND PREREGISTRATION

## Purpose
Freeze the next RQ-015 falsification analysis before any additional outcome summaries, model comparison, or threshold work.

Research question:
Does H4 consumed/run-progress retain stable information after a fixed target-vs-point-check geometry baseline is accounted for?

## Contamination / chronology guard
V2.0 Discovery and Replication outcomes have already been opened, and the replication checkpoint already contains an exploratory one-variable geometry diagnostic.
Therefore this document is not a pristine pre-outcome preregistration.

Its role is narrower and explicit:
- freeze all further RQ-015 calculations before running them;
- prevent outcome-selected geometry formulas, thresholds, or model variants;
- preserve the already-seen exploratory result as historical evidence rather than pretending it was unseen.

No future claim from this RQ may be described as untouched holdout confirmation.

## Frozen population
Use only rows where the frozen V2.0 artifact has candidate_state == RESEARCH_CANDIDATE.

Use the already checkpointed artifacts:
- Discovery: results/0700_MINIMAL_V2/DISCOVERY_2022_09_TO_2023_03/0700_v2_research_events.csv
- Replication: results/0700_MINIMAL_V2/REPLICATION_2023_09_TO_2023_11_23/0700_v2_research_events.csv

Do not rerun or alter minimal_v2_0700.py for this analysis.

## Frozen pre-outcome geometry variables
All variables are computed from information available at M5 confirmation and the already-frozen next-07:00 accounting horizon.

1. target_distance_points
   abs(path_remaining_target_price - confirmation_close) / PROJECT_POINT_SIZE
   It must numerically agree with remaining_points_at_confirmation.

2. point_distance_points
   abs(confirmation_close - origin_anchor_price) / PROJECT_POINT_SIZE

3. geometry_target_advantage
   point_distance_points / (point_distance_points + target_distance_points)
   No threshold or binning is permitted.

4. total_boundary_distance_points
   point_distance_points + target_distance_points
   This preserves absolute scale under a finite horizon.

5. horizon_minutes
   minutes from confirmation_known_at to next_cutoff_utc
   This is retained because NEITHER probability depends on available time.

If the geometry_target_advantage denominator is non-positive, fail the analysis rather than inventing a fallback.

## Frozen outcome handling
Preserve the exact four V2.0 states:
- TARGET_FIRST
- POINT_CHECK_FIRST
- NEITHER_BY_NEXT_0700
- AMBIGUOUS_SAME_BAR

No state may be relabeled from M1 OHLC ordering.

### Lane A - full-state preservation
All candidate rows remain in the output.
Report by period:
- count and proportion of all four outcome states;
- median numeric geometry/consumed fields by outcome state;
- exact row-level derived geometry table.

This lane is descriptive so NEITHER and AMBIGUOUS are not silently discarded.

### Lane B - resolved ordering diagnostic
Only TARGET_FIRST and POINT_CHECK_FIRST enter the resolved binary diagnostic.
Encode TARGET_FIRST = 1 and POINT_CHECK_FIRST = 0.
NEITHER and AMBIGUOUS remain reported in Lane A and are not treated as losses or wins.

## Frozen rank-residual method
Compute separately within Discovery and Replication.
Use average ranks for ties.

Primary consumed variable: consumed_ratio_at_0700

Geometry controls:
- rank(geometry_target_advantage)
- rank(total_boundary_distance_points)
- rank(horizon_minutes)

Procedure:
1. rank consumed_ratio_at_0700;
2. regress that rank by OLS on an intercept plus the three frozen geometry-control ranks;
3. rank the binary TARGET_FIRST indicator;
4. regress that rank on the same intercept plus the same three geometry-control ranks;
5. report Pearson correlation of the two residual vectors as the partial-rank diagnostic.

No interaction term, polynomial, threshold, binning, feature selection, or coefficient tuning is permitted.

Secondary diagnostic:
Repeat with consumed_points_at_confirmation / 1500 in place of consumed_ratio_at_0700.
This secondary value cannot replace the primary result.

## Additional fixed diagnostics
For each period on resolved rows report ordinary Spearman correlations for:
- consumed at 07:00 vs TARGET_FIRST indicator;
- geometry_target_advantage vs TARGET_FIRST indicator;
- consumed at 07:00 vs geometry_target_advantage.

These are context diagnostics, not independent proof.

## Cross-period interpretation rule
Do not pool Discovery and Replication into one score.

### CONSUMED_RESIDUAL_RELATION_SURVIVES_GEOMETRY_CONTROL
Allowed only if the primary partial-rank residual is positive in both Discovery and Replication.
This establishes only a directionally stable residual association under this frozen control, not causality, profitability, or a trading edge.

### CONSUMED_ASSOCIATION_EXPLAINED_OR_DOMINATED_BY_GEOMETRY
Allowed if, in both periods:
- geometry_target_advantage is positively associated with TARGET_FIRST;
- consumed at 07:00 is positively associated with geometry_target_advantage; and
- the primary partial-rank consumed residual is non-positive.

### INDEPENDENT_EFFECT_NOT_IDENTIFIABLE_WITH_CURRENT_DATA
Use for every other cross-period pattern, including sign disagreement, missing or degenerate residual variance, or insufficient resolved rows.

Because target distance is mechanically connected to run consumption, strong collinearity must be reported even if the residual is positive.

## Reporting guardrails
- No consumed threshold.
- No geometry threshold.
- No parameter search.
- No alternate model search after seeing the result.
- No trade Win Rate, expectancy, fill, cost, SL/TP, or profitability claim.
- No PAT3 expansion.
- No reinterpretation of historical Q3/Q4 documents.
- Discovery and Replication remain separate.
- Any contradiction must be preserved.

## Required output
The execution checkpoint must contain:
- artifact hashes used;
- exact implementation hash;
- row counts by outcome state;
- derived geometry validation;
- Lane A summary;
- Lane B diagnostics by period;
- frozen classification result;
- explicit limitations and contamination note.

This freeze supersedes no historical result. It governs only the next RQ-015 calculation.
