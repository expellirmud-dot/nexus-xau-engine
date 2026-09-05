# Inherited Origin Context Relation — Implementation Checkpoint — 2026-09-05

Status: IMPLEMENTED / READY FOR LOCAL RUNTIME VALIDATION

## Closed immediately before this checkpoint

`PATH_REMAINING × Daily Frame Side × Graded MTF V2` closed `INCONCLUSIVE` for all three frozen freshness variants across the existing comparison periods.

Repository closure:

- `docs/PATH_REMAINING_DAILY_SIDE_MTF_V2_EMPIRICAL_CLOSURE_2026-09-05.md`

## New frozen question

Study inherited-origin context rather than continuing MTF freshness/threshold mining:

- origin age;
- consumed-run ratio at entry;
- previous-24h preparation-cycle origin versus older origin.

Frozen plan:

- `docs/INHERITED_ORIGIN_CONTEXT_RELATION_PLAN_2026-09-05.md`

## Important confound control

Primary outcomes use the existing fixed fresh H1 1,000-point control.

This is deliberate: using `PATH_REMAINING` completion as the primary consumed-run outcome would mechanically make a more-consumed origin easier to complete because the remaining target is shorter.

`PATH_REMAINING` and `ORIGIN_TARGET_LEVEL` are preserved as secondary descriptive comparators.

## Implementation added

- `src/nexus_xau/research/inherited_origin_context_relation.py`
- `src/nexus_xau/research/inherited_origin_context_batch.py`
- `tests/test_inherited_origin_context_relation.py`
- `tests/test_inherited_origin_context_batch.py`
- `scripts/run_inherited_origin_context_relation.ps1`

The batch discovers existing local parent research event tables under `results/`, runs the same frozen measurement independently on:

- 2022-09-01 through 2023-03-31;
- 2024-09-01 through 2024-11-30;
- 2025-09-01 through 2025-11-30;

and writes:

```text
results/INHERITED_ORIGIN_CONTEXT_RELATION/CROSS_PERIOD_SUMMARY.json
```

## Runtime validation status

The previous MTF V2 runner was runtime-validated on the project PC with 108 tests passing before these new origin-context modules/tests were added.

Therefore the new origin-context code is **not yet claimed runtime-passing**.

Required local gate:

```powershell
cd D:\nexus-xau-engine-repo
git pull
.\scripts\run_inherited_origin_context_relation.ps1
```

The script performs:

```text
pytest with repository-local basetemp
-> Ruff
-> three-period origin-context batch
-> cross-period summary
```

## Frozen interpretation rule

A directional relation is replicated only when the same direction appears in at least two periods and no usable period shows the opposite direction.

Opposite directions across periods -> `NOT_STABLE_ACROSS_PERIODS`.

Otherwise -> `INCONCLUSIVE`.

No age threshold, consumed-run threshold, or canonical expiry rule may be selected from this result.

## Next checkpoint

After local output is available:

1. record exact test/Ruff status;
2. preserve exact per-period states;
3. apply the already-frozen cross-period rule;
4. close the origin-context round;
5. only if origin recency/age is materially informative, freeze bounded expiry/invalidation variants next.
