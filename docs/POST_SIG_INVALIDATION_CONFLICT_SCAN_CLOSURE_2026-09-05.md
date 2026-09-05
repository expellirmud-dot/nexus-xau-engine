# Post-SIG Source-Partial Invalidation Conflict Scan — Closure — 2026-09-05

Status: CLOSED — `REPLICATED_SOURCE_PARTIAL_CONFLICT_OBSERVED`

## Runtime validation

Project-owner Windows runtime completed the frozen scanner successfully:

- pytest: `118 passed, 116 warnings in 3.62s`;
- Ruff: `All checks passed!`;
- three-period source-partial conflict batch: completed;
- local summary: `results/POST_SIG_INVALIDATION_CONFLICT_SCAN/CROSS_PERIOD_SUMMARY.json`.

The local `results/` directory remains gitignored. This repository closure preserves the terminal output supplied by the project owner.

## Frozen question

For H1 candidates previously classified by the research engine as `INHERITED_REMAINING_RUN`, had the selected inherited origin already been structurally destroyed before the candidate according to the narrow source-partial strict-beyond representation?

Frozen representation:

```text
BUY  destroyed if any later observed M1 Low  < selected origin_anchor_price
SELL destroyed if any later observed M1 High > selected origin_anchor_price
interval = [origin_anchor_known_at, candidate_known_at)
equality = not destroyed
buffer = none
```

The transcript's approximately 200-point example remains example-specific and was not promoted into a universal threshold.

## Results

### DISCOVERY_2022_09_TO_2023_03

- inherited events: 285
- evaluable: 285
- destroyed before candidate: 259
- intact: 26
- destroyed fraction: 0.9087719298245615 (90.88%)
- period state: `CONFLICT_OBSERVED`

### LATER_2024_09_TO_2024_11

- inherited events: 47
- evaluable: 47
- destroyed before candidate: 46
- intact: 1
- destroyed fraction: 0.9787234042553191 (97.87%)
- period state: `CONFLICT_OBSERVED`

### LATER_2025_09_TO_2025_11

- inherited events: 29
- evaluable: 29
- destroyed before candidate: 29
- intact: 0
- destroyed fraction: 1.0 (100.00%)
- period state: `CONFLICT_OBSERVED`

## Frozen cross-period decision

```text
REPLICATED_SOURCE_PARTIAL_CONFLICT_OBSERVED
['CONFLICT_OBSERVED', 'CONFLICT_OBSERVED', 'CONFLICT_OBSERVED']
```

The conflict replicated in all three comparison periods.

## Interpretation

This is a structural consistency result, not a profitability result.

The current inherited-origin selector chooses the latest same-direction origin whose nominal 1,000-point run remains incomplete, but it does not apply the source-partial post-SIG destruction condition. The scan shows that this omission is material: most origins carried forward as active by the old research representation had already crossed the strict structural invalidation boundary before the later candidate.

Therefore prior downstream analyses that depend on those selected inherited origins remain preserved as historical research, but their inherited-origin state is now known to be materially confounded by missing source-partial invalidation handling. They must not be treated as final evidence until the origin state is rebuilt with deterministic invalidation/re-anchoring.

This specifically affects interpretation of:

- `REMAINING_RUN_STATE_ROUND_01`;
- Daily Frame side × `PATH_REMAINING`;
- graded MTF interaction conditional on inherited `PATH_REMAINING`;
- inherited-origin age / consumed-run / cycle analyses.

The results are not deleted or rewritten; their chronology remains preserved.

## What this does NOT prove

- It does not prove the complete instructor invalidation geometry.
- SELL remains a directional-mirror research representation under the partial source rule.
- It does not establish a 200-point destruction threshold.
- It does not establish equality behavior as canonical; equality was only frozen as non-destruction for this strict-beyond scan.
- It does not prove how to choose among multiple surviving older origins.
- It does not produce a strategy win rate.

## Decision / next bounded step

The conflict is large and replicated, so the next engineering/research step is justified:

`build a source-partial invalidation-aware re-anchoring variant`

For each candidate, evaluate same-direction origins from newest to oldest and select the latest origin that:

1. was known before the 07:00 cutoff;
2. remains below nominal H1 completion at cutoff and candidate time;
3. is not structurally destroyed before the candidate under the same frozen strict-beyond representation.

If the formerly selected origin is destroyed, continue backward to an older still-valid origin; if none survives, classify the candidate as `NO_ACTIVE_INHERITED_RUN`.

After that deterministic reconstruction, rerun the previously supported Daily Frame directional-side × `PATH_REMAINING` relation using the same minimum-group and comparison rule. This tests whether the earlier Daily Frame result survives the now-required source-partial origin correction without changing the Daily Frame rule post-outcome.

## Provenance guard

Historical outcome behavior did not create the invalidation rule. The next re-anchoring variant is motivated by source-partial evidence plus the replicated structural conflict observed here. Exact canonical post-SIG invalidation remains unresolved beyond the safely represented strict-beyond condition.
