# Post-SIG Structural Invalidation Conflict Scan — Frozen Plan — 2026-09-05

Status: FROZEN BEFORE EMPIRICAL EXECUTION

## Why this is next

The inherited-origin context round closed `INCONCLUSIVE` for origin age, consumed-run ratio, and previous-24h versus older origin grouping. Therefore no time-expiry threshold is justified.

A stronger unresolved upstream issue already has first-party transcript support: an active SIG remains active only while its post-SIG reference has not been destroyed, and the project canonical claim register marks `POST_SIG_INVALIDATION` as `ACTIVE_PARTIAL`.

The current inherited-run reconstruction explicitly does not apply the exact post-SIG destruction/invalidation rule.

## Source basis

Primary transcript evidence preserved in `docs/PA_PAT_TRANSCRIPT_FORENSICS_2026-09-01.md` states:

- a SIG remains active while its post-SIG wick/reference has not been destroyed;
- a post-SIG reference that disturbs/exceeds the PA is invalid;
- a later candle extending beyond the post-SIG wick can destroy it;
- in the illustrated BUY sequence, a later wick lower than the prior post-SIG wick is treated as destruction;
- an approximately 200-point difference appears in one illustrated example only and is **not** established as a universal threshold.

Canonical claim:

`POST_SIG_INVALIDATION = ACTIVE_PARTIAL / SAFE_PARTIAL_REJECT_ONLY`

## Exact question

Among events currently labeled `INHERITED_REMAINING_RUN`, how often had the **selected origin anchor already been destroyed before the candidate** under the narrowest source-partial wick-break representation?

This is a representation-consistency diagnostic before attempting a full re-anchoring state machine.

## Frozen source-partial representation

For the selected origin already recorded in the parent Remaining-Run event table:

```text
BUY destroyed  := any later M1 Low  < origin_anchor_price
SELL destroyed := any later M1 High > origin_anchor_price
```

Scan interval:

```text
[origin_anchor_known_at, candidate_known_at)
```

Use strict `beyond` semantics. Equality does not count as destroyed in this frozen partial representation because the source wording is farther/beyond/exceed, while exact equality behavior remains unresolved.

No 200-point buffer is used.

## Why this is not yet full canonical invalidation

This scan does not claim to solve:

- exact initial post-SIG-versus-PA disturbance geometry;
- PA/frame boundary interaction;
- equality/tolerance behavior;
- SELL-side source wording beyond the directional mirror research representation;
- replacement with an older or newer valid origin after destruction;
- complete Sideway transition logic.

It only asks whether the origin selected by the current research representation would already fail the narrow source-partial wick-break condition.

## Measurements

For each existing comparison period, report:

- inherited events;
- evaluable selected-origin events;
- destroyed-before-candidate count;
- intact-before-candidate count;
- destroyed fraction;
- first destruction timestamp per destroyed event;
- maximum anchor exceed distance in project points as descriptive metadata only.

No threshold is selected from the exceed distance.

## Frozen cross-period closure

No invented minimum fraction is used.

- conflict observed in at least 2 periods -> `REPLICATED_SOURCE_PARTIAL_CONFLICT_OBSERVED`;
- conflict observed in exactly 1 period -> `SOURCE_PARTIAL_CONFLICT_SINGLE_PERIOD`;
- evaluable events exist but zero conflicts in all periods -> `NO_SOURCE_PARTIAL_CONFLICT_OBSERVED`;
- no evaluable events -> `NOT_TESTABLE_WITH_CURRENT_EVIDENCE`.

A conflict means only that the **current selected-origin representation** retains origins that the frozen source-partial wick-break rule would reject. It does not make the partial rule fully canonical.

## Outcome discipline

Historical performance is not needed to identify this conflict and will not be used to choose the source rule.

Only after this diagnostic closes may outcome usefulness be tested for a full re-anchoring implementation, and performance still cannot upgrade provenance.

## Next branch

If replicated conflict is observed, implement a separate deterministic re-anchoring/state-machine experiment that removes destroyed origins and searches for the latest still-valid same-direction origin.

If conflict is absent or not testable, do not mine time expiry; return to the next unresolved source-geometry question.
