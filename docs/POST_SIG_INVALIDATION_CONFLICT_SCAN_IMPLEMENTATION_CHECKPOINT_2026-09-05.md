# Post-SIG Structural Invalidation Conflict Scan — Implementation Checkpoint — 2026-09-05

Status: IMPLEMENTED / READY FOR LOCAL RUNTIME VALIDATION

## Prior closure

`Inherited Origin Context Relation` closed `INCONCLUSIVE` for:

- origin age;
- consumed-run ratio at entry;
- previous-24h versus older origin grouping.

Repository closure:

`docs/INHERITED_ORIGIN_CONTEXT_RELATION_CLOSURE_2026-09-05.md`

This means the project has no evidence basis to mine time expiry or consumed-run thresholds.

## Source evidence used next

The canonical claim register already contains:

`POST_SIG_INVALIDATION = ACTIVE_PARTIAL / SAFE_PARTIAL_REJECT_ONLY`

The primary PA/PAT/SIG transcript says an active SIG remains active while the post-SIG reference is not destroyed and contains an illustrated BUY case where a later lower wick destroys the prior post-SIG reference. The approximately 200-point difference in one example remains example-specific, not a universal threshold.

Frozen plan:

`docs/POST_SIG_INVALIDATION_CONFLICT_SCAN_PLAN_2026-09-05.md`

## Implementation added

- `src/nexus_xau/research/post_sig_invalidation_conflict_scan.py`
- `src/nexus_xau/research/post_sig_invalidation_conflict_batch.py`
- `tests/test_post_sig_invalidation_conflict_scan.py`
- `scripts/run_post_sig_invalidation_conflict_scan.ps1`

## Frozen diagnostic rule

For the **selected origin already recorded** in the parent Remaining-Run event table:

```text
BUY destroyed  := any M1 Low  < origin_anchor_price
SELL destroyed := any M1 High > origin_anchor_price
```

Interval:

```text
[origin_anchor_known_at, candidate_known_at)
```

Strict beyond only. Equality is not counted as destruction in this partial representation. No point buffer is applied.

## Why this is a diagnostic first

The scan does not yet search for a replacement origin after destruction. It only measures whether the current state reconstruction is retaining selected origins that the source-partial rule would reject.

This separates two questions:

1. **representation conflict:** is the omission actually present in historical reconstructed events?
2. **full state-machine usefulness:** if yes, does rebuilding/re-anchoring the origin state improve sequential decision quality?

Only question 1 is executed now.

## Frozen cross-period closure

- conflict in at least 2 periods -> `REPLICATED_SOURCE_PARTIAL_CONFLICT_OBSERVED`;
- conflict in exactly 1 period -> `SOURCE_PARTIAL_CONFLICT_SINGLE_PERIOD`;
- evaluable evidence but zero conflicts -> `NO_SOURCE_PARTIAL_CONFLICT_OBSERVED`;
- no evaluable events -> `NOT_TESTABLE_WITH_CURRENT_EVIDENCE`.

No minimum conflict fraction is invented.

## Runtime validation status

The project PC previously validated the origin-context modules with `114 passed` before this new invalidation scanner was added.

Therefore the new scanner/tests are **not yet claimed runtime-passing**.

Run locally:

```powershell
cd D:\nexus-xau-engine-repo
git pull
.\scripts\run_post_sig_invalidation_conflict_scan.ps1
```

The runner performs:

```text
pytest with repository-local basetemp
-> Ruff
-> three-period source-partial invalidation conflict scan
-> cross-period summary
```

Expected summary:

`results/POST_SIG_INVALIDATION_CONFLICT_SCAN/CROSS_PERIOD_SUMMARY.json`

## Next decision

If replicated conflict is observed, freeze and implement a separate full re-anchoring experiment that removes destroyed origins and searches backward for the latest still-valid same-direction origin.

If conflict is absent or not testable, do not introduce time expiry; move to the next unresolved source-geometry question.

## Provenance guard

The source-partial wick-break representation has stronger provenance than an invented age threshold, but it is still partial. Historical outcomes cannot upgrade it into a fully canonical teacher rule.
