# PATH_REMAINING × Daily Frame Side × Graded MTF V2 — Empirical Closure — 2026-09-05

Status: CLOSED / `INCONCLUSIVE` FOR ALL THREE FROZEN FRESHNESS VARIANTS

## Evidence used for this closure

Runtime output supplied directly by the project owner from the Windows research PC after:

- pytest: `108 passed`;
- Ruff gate: passed after lint-only fixes;
- deterministic V2 multiperiod batch completed;
- deterministic closure markdown was generated locally at `results/PATH_REMAINING_DAILY_SIDE_MTF_V2/EMPIRICAL_CLOSURE.md`.

The local `results/` directory remains gitignored. This repository document preserves the terminal cross-period states without copying raw/local research data into Git.

## Research question

Within inherited `PATH_REMAINING` events, after conditioning on 07:00 Daily Frame directional side, does increasing same-direction H1/M30/M15/M5 PAT2-BODY proxy alignment show a stable relationship with remaining-run behavior?

This remains a graded relation test. It does not search for or select a hard minimum aligned-timeframe count.

## Period states

### Discovery: 2022-09-01 through 2023-03-31

- `EXACT_COMPLETION` -> `INCONCLUSIVE`
- `RECENT_1_TF_BAR` -> `SIDE_CONDITIONAL_SUPPORT`
- `RECENT_2_TF_BARS` -> `GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC`

### Later period: 2024-09-01 through 2024-11-30

- `EXACT_COMPLETION` -> `INCONCLUSIVE`
- `RECENT_1_TF_BAR` -> `INCONCLUSIVE`
- `RECENT_2_TF_BARS` -> `EXPECTED_SIDE_OPPOSE`

### Later period: 2025-09-01 through 2025-11-30

- `EXACT_COMPLETION` -> `INCONCLUSIVE`
- `RECENT_1_TF_BAR` -> `INCONCLUSIVE`
- `RECENT_2_TF_BARS` -> `INCONCLUSIVE`

## Frozen cross-period decisions

- `EXACT_COMPLETION` -> `INCONCLUSIVE`
- `RECENT_1_TF_BAR` -> `INCONCLUSIVE`
- `RECENT_2_TF_BARS` -> `INCONCLUSIVE`

## Primary closure

`INCONCLUSIVE`

None of the three frozen freshness representations replicated strongly enough across the existing comparison periods to support a stable graded MTF relationship conditional on `PATH_REMAINING + Daily Frame side`.

The strongest conflict is `RECENT_2_TF_BARS`:

- 2022-09 to 2023-03: `GENERAL_MTF_SUPPORT_NOT_SIDE_SPECIFIC`;
- 2024-09 to 2024-11: `EXPECTED_SIDE_OPPOSE`;
- 2025-09 to 2025-11: `INCONCLUSIVE`.

This is direct evidence of regime/period instability for that research representation. It must not be promoted because one period looked favorable.

`RECENT_1_TF_BAR` showed `SIDE_CONDITIONAL_SUPPORT` only in the discovery period and failed to replicate in both later periods. `EXACT_COMPLETION` remained inconclusive in every period.

## What changed in our understanding

Before this test, standalone MTF alignment had already closed inconclusive, while the project-owner semantic remained that more same-direction timeframe alignment is preferable/stronger.

This interaction test adds a stronger negative constraint:

`Adding PATH_REMAINING + Daily Frame side does not currently make any of the three PAT2-BODY freshness proxies robust across periods.`

Therefore MTF alignment should remain a descriptive/confluence field in the research engine, not a production gate and not a proven outcome filter.

## What this result does NOT mean

- It does not refute the project owner's direct semantic that true multi-timeframe PA alignment is preferable/stronger.
- It does not establish that MTF alignment has no value under full PA/PAT1/PAT3/SW/location representations.
- It does not identify the instructor's canonical freshness window.
- It does not justify choosing `RECENT_1_TF_BAR` because one period was favorable.
- It does not justify rejecting `RECENT_2_TF_BARS` as the instructor rule because historical outcomes conflicted.
- It does not produce a strategy win rate.
- PAT2 BODY and `PATH_REMAINING` remain research representations.

## Decision

Do not continue threshold/freshness mining on MTF alignment in isolation or inside this same interaction.

Per the previously declared next-step sequence, move to inherited-origin context:

1. origin age;
2. consumed-run ratio;
3. current 24-hour preparation-cycle origin versus older inherited origin;
4. only after those relations are measured, bounded expiry/invalidation variants if uncertainty remains material.

Keep `ORIGIN_TARGET_LEVEL` preserved as a comparator and use a fixed fresh-1000 control for primary origin-quality outcome relationships where target-size mechanics would otherwise confound `PATH_REMAINING`.

## Provenance / interpretation guard

This closure is an outcome-research result. It cannot upgrade or downgrade source provenance and cannot be used to declare what the instructor originally meant.
