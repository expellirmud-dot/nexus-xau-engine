# Source-Partial Re-Anchored Remaining Run — Implementation Checkpoint — 2026-09-05

Status: IMPLEMENTED / READY FOR LOCAL RUNTIME VALIDATION

## Closed immediately before this checkpoint

`POST_SIG_INVALIDATION_CONFLICT_SCAN` closed:

```text
REPLICATED_SOURCE_PARTIAL_CONFLICT_OBSERVED
```

Observed destroyed-before-candidate fractions under the frozen strict-beyond representation:

- 2022-09 to 2023-03: 259 / 285 = 90.88%
- 2024-09 to 2024-11: 46 / 47 = 97.87%
- 2025-09 to 2025-11: 29 / 29 = 100.00%

This makes the old inherited-origin selection materially confounded by missing invalidation handling.

## Frozen plan

`docs/SOURCE_PARTIAL_REANCHORED_REMAINING_RUN_PLAN_2026-09-05.md`

The representation was frozen before empirical re-anchor output review.

## Implementation added

- `src/nexus_xau/research/source_partial_reanchored_remaining_run.py`
- `src/nexus_xau/research/source_partial_reanchored_daily_side_batch.py`
- `tests/test_source_partial_reanchored_remaining_run.py`
- `tests/test_source_partial_reanchored_daily_side_batch.py`
- `scripts/run_source_partial_reanchored_daily_side.ps1`

## Re-anchoring logic

For each existing parent candidate, same-direction H1 PAT2-BODY origins are checked newest to oldest.

A source-partial origin is selected only when:

1. `anchor_known_at <= cutoff_utc`;
2. nominal H1 1,000-point run remains incomplete at cutoff;
3. nominal H1 1,000-point run remains incomplete at candidate;
4. no strict structural destruction occurs before candidate:
   - BUY: later Low < anchor -> destroyed;
   - SELL: later High > anchor -> destroyed.

No 200-point buffer, time expiry, age threshold, or consumed-run threshold is added.

If the latest legacy origin is destroyed, the selector continues backward to an older valid origin. If no origin survives, the event becomes `NO_ACTIVE_INHERITED_RUN`.

## Downstream retest

The batch then runs the existing Daily Frame interaction and threshold-free Daily Frame side relation on the rebuilt inherited state without changing the Daily Frame rule.

Frozen cross-period states:

- >=2 SUPPORT and no OPPOSE -> `SUPPORTED_AFTER_SOURCE_PARTIAL_REANCHOR`
- >=2 OPPOSE -> `NOT_SUPPORTED_AFTER_SOURCE_PARTIAL_REANCHOR`
- SUPPORT and OPPOSE both observed -> `NOT_STABLE_AFTER_SOURCE_PARTIAL_REANCHOR`
- otherwise -> `INCONCLUSIVE_AFTER_SOURCE_PARTIAL_REANCHOR`

## Runtime validation status

The preceding scanner runtime was validated locally with:

```text
118 passed, 116 warnings
Ruff: All checks passed
```

Those results occurred before the new re-anchoring modules/tests were added. Therefore this new implementation is **not yet claimed runtime-passing**.

Run locally:

```powershell
cd D:\nexus-xau-engine-repo
git pull
.\scripts\run_source_partial_reanchored_daily_side.ps1
```

The runner uses a UUID-based repo-local pytest basetemp to avoid the Windows stale-temp ACL/lock failure encountered in prior runs.

## Expected output

```text
results/SOURCE_PARTIAL_REANCHORED_REMAINING_RUN/CROSS_PERIOD_SUMMARY.json
```

Terminal output prints, per period:

- re-anchor impact summary;
- Daily Frame EXPECTED/CROSSED group summaries;
- Daily-side period state;
- frozen cross-period decision.

## Interpretation boundary

This implementation is a source-partial research reconstruction, not the complete instructor state machine. H1 PAT2 BODY, SELL mirror invalidation, PATH_REMAINING, and equality handling remain research representations or partial-source choices as documented.
