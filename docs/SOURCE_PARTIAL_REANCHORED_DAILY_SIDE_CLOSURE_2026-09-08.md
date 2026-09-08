# Source-Partial Re-Anchored Remaining Run + Daily-Side Retest — Closure — 2026-09-08

Status: CLOSED / `INCONCLUSIVE_AFTER_SOURCE_PARTIAL_REANCHOR`

## Question

After replacing the legacy inherited-origin selection with the already-frozen source-partial invalidation-aware re-anchor, does the existing threshold-free Daily Frame directional-side × `PATH_REMAINING` relation still satisfy the frozen cross-period support rule?

## Frozen representation used

No scientific rule was changed after seeing the output.

Re-anchor selection remained:

1. same-direction H1 PAT2-BODY origins only;
2. inspect newest to oldest;
3. `anchor_known_at <= cutoff_utc`;
4. nominal H1 1,000-project-point run incomplete at cutoff;
5. nominal H1 1,000-project-point run incomplete at candidate;
6. no strict structural destruction before candidate;
7. if the latest origin is destroyed, search older surviving origins;
8. if none survives, classify `NO_ACTIVE_INHERITED_RUN`.

Frozen destruction representation:

```text
BUY  destroyed if later M1 Low  < origin_anchor_price
SELL destroyed if later M1 High > origin_anchor_price
interval = [origin_anchor_known_at, candidate_known_at)
equality = not destroyed
buffer = none
```

The approximately 200-point transcript example was not used as a destruction threshold.

The downstream Daily Frame side rule remained:

```text
EXPECTED_SIDE = signed directional frame distance >= 0
CROSSED_SIDE  = signed directional frame distance < 0
minimum group = 10
```

Frozen cross-period decision remained:

- >=2 `SUPPORT` and no `OPPOSE` -> `SUPPORTED_AFTER_SOURCE_PARTIAL_REANCHOR`
- >=2 `OPPOSE` -> `NOT_SUPPORTED_AFTER_SOURCE_PARTIAL_REANCHOR`
- at least one `SUPPORT` and at least one `OPPOSE` -> `NOT_STABLE_AFTER_SOURCE_PARTIAL_REANCHOR`
- otherwise -> `INCONCLUSIVE_AFTER_SOURCE_PARTIAL_REANCHOR`

## Runtime validation

Local Windows project-owner runtime on branch `build/python-replay-engine` completed:

```text
126 passed, 116 warnings
Ruff: All checks passed!
[3/3] source-partial re-anchored remaining-run + Daily-side retest
Completed.
```

During the first rerun, the 2025 period exposed an engineering-only zero-event bug: after re-anchor produced zero inherited events, the Daily interaction writer created a zero-column DataFrame and downstream access to `location_group` raised `KeyError`.

This was fixed without changing research semantics by writing the existing interaction-event schema even when there are zero rows. A regression test verifies that a zero-inherited period writes a readable empty CSV and closes both interaction and Daily-side states as `INSUFFICIENT`.

Engineering fix checkpoint:

```text
806ae05 fix: handle zero reanchored daily interaction events
```

## Empirical re-anchor impact

### 2022-09-01 to 2023-03-31

```text
candidate_events = 300
legacy_inherited_events = 285
reanchored_inherited_events = 34
```

Impact counts:

- `DROPPED_NO_VALID_ORIGIN` = 251
- `SAME_ORIGIN_STILL_VALID` = 26
- `REANCHORED_TO_OLDER_VALID_ORIGIN` = 8
- `REMAINS_NO_ACTIVE_ORIGIN` = 15

Daily-side groups after re-anchor:

- EXPECTED_SIDE: 31 events, 31 resolved, target-first 0.7096774193548387, reach 0.8064516129032258
- CROSSED_SIDE: 3 events, 3 resolved, target-first 1.0, reach 1.0

Period state: `INSUFFICIENT`

### 2024-09-01 to 2024-11-30

```text
candidate_events = 71
legacy_inherited_events = 47
reanchored_inherited_events = 1
```

Impact counts:

- `DROPPED_NO_VALID_ORIGIN` = 46
- `SAME_ORIGIN_STILL_VALID` = 1
- `REMAINS_NO_ACTIVE_ORIGIN` = 24

Daily-side groups after re-anchor:

- EXPECTED_SIDE: 1 event, 1 resolved, target-first 0.0, reach 1.0
- CROSSED_SIDE: 0 events

Period state: `INSUFFICIENT`

### 2025-09-01 to 2025-11-30

```text
candidate_events = 74
legacy_inherited_events = 29
reanchored_inherited_events = 0
```

Impact counts:

- `DROPPED_NO_VALID_ORIGIN` = 29
- `REMAINS_NO_ACTIVE_ORIGIN` = 45

Daily-side groups after re-anchor:

- EXPECTED_SIDE: 0 events
- CROSSED_SIDE: 0 events

Period state: `INSUFFICIENT`

## Frozen cross-period closure

Observed period states:

```text
[
  "INSUFFICIENT",
  "INSUFFICIENT",
  "INSUFFICIENT"
]
```

Therefore, by the frozen decision rule:

```text
INCONCLUSIVE_AFTER_SOURCE_PARTIAL_REANCHOR
```

## What changed from the legacy Daily-side result

The earlier threshold-free Daily Frame side study had produced `SUPPORT` in two usable periods under the legacy inherited-origin selection.

The invalidation conflict scan subsequently showed that the legacy selector was materially confounded because it retained origins already destroyed under the frozen source-partial destruction representation.

After rebuilding the same candidate universe with that invalidation-aware representation, inherited-event counts collapsed from:

- 285 -> 34 in 2022-09 to 2023-03;
- 47 -> 1 in 2024-09 to 2024-11;
- 29 -> 0 in 2025-09 to 2025-11.

As a result, the old `SUPPORTED_RESEARCH_REPRESENTATION` finding cannot be carried forward as confirmed under the corrected source-partial origin state. The corrected retest is **inconclusive due to insufficient post-re-anchor sample**, not `OPPOSE` and not proof that Daily Frame side is false.

The historical legacy result remains preserved as a prior checkpoint and is not deleted or rewritten.

## Evidence boundary

Facts from this run:

- the frozen source-partial re-anchor removes most legacy inherited origins in all three periods;
- the corrected Daily-side samples fail the minimum-group requirement in every period;
- the frozen cross-period decision is `INCONCLUSIVE_AFTER_SOURCE_PARTIAL_REANCHOR`.

Still research representations / unresolved source questions:

- H1 PAT2 BODY as the origin proxy;
- SELL destruction as directional mirror;
- exact canonical post-SIG destruction geometry;
- exact equality behavior in the instructor system;
- whether an older origin may remain active after a newer origin is destroyed;
- `PATH_REMAINING` as the inherited objective representation.

Historical outcomes cannot resolve those source-rule questions and must not be used to select a more favorable invalidation rule.

## Next bounded research step

Do not retune the invalidation rule, add an expiry timer, add a 200-point buffer, or choose an age/consumed-run threshold from this outcome.

The next defensible step is to investigate post-SIG lifecycle semantics with source evidence and/or threshold-free descriptive relationships, specifically:

- when a destroyed newer origin causes full state reset versus re-evaluation of an older origin;
- whether origin age, consumed progress, or candidate timing co-vary with survival/destruction without selecting a threshold;
- whether additional source-backed origin families materially change the active-origin population.

If source evidence remains insufficient, retain the closure as `INCONCLUSIVE` rather than manufacturing a replacement rule.

## Local result artifact

Primary local output remains intentionally gitignored:

```text
results/SOURCE_PARTIAL_REANCHORED_REMAINING_RUN/CROSS_PERIOD_SUMMARY.json
```

Legacy results remain preserved locally as historical evidence.
