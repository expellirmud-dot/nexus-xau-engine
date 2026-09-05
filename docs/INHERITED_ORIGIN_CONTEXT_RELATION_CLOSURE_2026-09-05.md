# Inherited Origin Context Relation — Empirical Closure — 2026-09-05

Status: CLOSED / `INCONCLUSIVE`

## Runtime evidence

Project-owner supplied Windows research-PC output after the origin-context runner completed:

- pytest gate had already passed with `114 passed` before the lint-only import correction;
- Ruff passed after the import-format correction;
- three-period batch completed and wrote `results/INHERITED_ORIGIN_CONTEXT_RELATION/CROSS_PERIOD_SUMMARY.json` locally.

The `results/` directory remains gitignored; this document preserves the terminal states without copying local research data into Git.

## Frozen question

Within inherited-run events on the Daily Frame `EXPECTED_SIDE`, do any of the following show a stable relation to the fixed fresh H1 1,000-point control outcome?

1. origin age;
2. consumed-run ratio at entry;
3. origin from the previous 24-hour preparation cycle versus an older inherited origin.

`PATH_REMAINING` and `ORIGIN_TARGET_LEVEL` remain secondary comparators. They are not used to choose the consumed-run relation because `PATH_REMAINING` becomes mechanically shorter as more of the inherited run is consumed.

## Period states

### DISCOVERY_2022_09_TO_2023_03

- `origin_age` -> `MIXED`
- `consumed_run_ratio_at_entry` -> `MIXED`
- `origin_cycle_group` -> `MIXED`

### LATER_2024_09_TO_2024_11

- `origin_age` -> `MIXED`
- `consumed_run_ratio_at_entry` -> `LESS_CONSUMED_FAVORED`
- `origin_cycle_group` -> `INSUFFICIENT`

### LATER_2025_09_TO_2025_11

- `origin_age` -> `INSUFFICIENT`
- `consumed_run_ratio_at_entry` -> `INSUFFICIENT`
- `origin_cycle_group` -> `INSUFFICIENT`

## Frozen cross-period decisions

- `origin_age` -> `INCONCLUSIVE`
- `consumed_run_ratio_at_entry` -> `INCONCLUSIVE`
- `origin_cycle_group` -> `INCONCLUSIVE`

## Primary closure

No inherited-origin context feature replicated a stable directional relation across at least two periods under the pre-frozen rule.

The 2024 `LESS_CONSUMED_FAVORED` observation is a single-period result and is not replicated. It must not be converted into a consumed-run threshold or production filter.

The 2025 period is insufficient for all three origin-context questions and cannot be used to lower the already-frozen minimum after seeing the outcome.

## What changed in our understanding

The prior MTF interaction round was already inconclusive. This round adds another negative constraint:

`Simple origin age, simple consumed-run ratio, and a previous-24h-versus-older grouping do not currently explain the inherited-run outcome robustly across periods.`

Therefore:

- do not mine an age threshold;
- do not mine a consumed-run threshold;
- do not promote 24 hours into a canonical expiry rule;
- do not claim that older origins are invalid merely because of age.

## Important remaining model limitation

The current inherited-origin reconstruction explicitly does not apply the instructor's exact post-SIG destruction/invalidation rule. That limitation existed before this round and remains material.

Because age/recency did not replicate, the next step should **not** be time-expiry threshold mining. The higher-value unresolved question is whether the active inherited origin should be invalidated by a deterministic structural event supported by source evidence.

This is a source-rule-identification problem first, not an outcome-optimization problem.

## Decision

Close the age / consumed-run / 24-hour grouping family as `INCONCLUSIVE`.

Next research lane:

1. search existing first-party transcript / annotated-chart evidence for explicit old-SIG / old-run destruction, cancellation, replacement, or invalidation semantics;
2. represent only source-grounded candidate invalidation rules;
3. if multiple measurable variants remain, test them as bounded variants while keeping source consistency separate from historical outcome usefulness;
4. do not introduce a time-based expiry threshold unless source evidence independently supports one.

## Provenance guard

Historical outcomes cannot identify what the instructor meant. A future invalidation candidate may be evaluated for outcome usefulness, but performance cannot upgrade that candidate into the canonical teaching rule.
