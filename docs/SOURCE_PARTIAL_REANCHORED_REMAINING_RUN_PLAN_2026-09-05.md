# Source-Partial Re-Anchored Remaining Run — Frozen Plan — 2026-09-05

Status: FROZEN BEFORE EMPIRICAL RE-ANCHOR OUTPUT REVIEW

## Motivation

The immediately prior checkpoint closed `REPLICATED_SOURCE_PARTIAL_CONFLICT_OBSERVED`: the old inherited-origin selector was carrying structurally destroyed origins in 90.88%, 97.87%, and 100.00% of its inherited events across the three comparison periods.

This round does not invent an expiry threshold. It rebuilds the inherited state with the already-frozen strict structural invalidation representation.

## Source / evidence boundary

Source-partial facts retained:

- a SIG/post-SIG reference remains meaningful only while it is not destroyed;
- source examples show later price extending beyond the post-SIG reference as destruction/re-evaluation behavior;
- the approximately 200-point example is not a universal threshold.

Research representation retained:

```text
BUY  destroyed if later observed Low  < origin anchor
SELL destroyed if later observed High > origin anchor
```

SELL is a directional mirror research representation. Exact canonical geometry and equality remain unresolved.

## Candidate universe

Use the already-generated parent Remaining-Run event rows as the candidate universe. This preserves the same first-H1-PAT2-BODY-candidate-per-side/day population and avoids silently changing candidate discovery while repairing only origin state.

H1 PAT2 BODY remains a research proxy, not canonical PA/SIG.

## Re-anchoring algorithm

At each existing candidate:

1. rebuild H1 PAT2-BODY origins from the same M1 data;
2. consider same-direction origins with `anchor_known_at <= cutoff_utc`;
3. examine origins newest to oldest;
4. require nominal H1 1,000-point run to be incomplete at both cutoff and candidate;
5. require no strict structural destruction in `[origin_anchor_known_at, candidate_known_at)`;
6. select the newest origin satisfying all requirements;
7. if none survives, classify `NO_ACTIVE_INHERITED_RUN`.

No age threshold, expiry timer, consumed-run threshold, or distance buffer is used.

## Re-anchoring impact labels

For rows previously classified as inherited:

- `SAME_ORIGIN_STILL_VALID`
- `REANCHORED_TO_OLDER_VALID_ORIGIN`
- `DROPPED_NO_VALID_ORIGIN`

Rows previously no-active remain part of the candidate universe and may only become inherited if the deterministic source-partial selector finds a valid pre-cutoff origin. This possibility must be reported rather than assumed impossible.

## Outcome reconstruction

Fresh fixed-1,000 outcomes from the parent event rows remain unchanged because the candidate itself is unchanged.

For a newly selected inherited origin, recompute:

- `remaining_at_entry_points`;
- `PATH_REMAINING` reach / first hit;
- `ORIGIN_TARGET_LEVEL` reach / first hit;

using the same 24-H1-bar research horizon and symmetric 1,000-point adverse control previously used by the parent representation.

## Primary downstream retest

Re-run the existing threshold-free Daily Frame directional-side relation on the re-anchored inherited events:

```text
EXPECTED_SIDE = signed directional frame distance >= 0
CROSSED_SIDE  = signed directional frame distance < 0
minimum group = 10
```

Per-period state remains exactly the existing rule:

- higher target-first and no-lower PATH_REMAINING reach for EXPECTED vs CROSSED -> `SUPPORT`;
- lower target-first and no-higher reach -> `OPPOSE`;
- otherwise `MIXED`;
- either group <10 -> `INSUFFICIENT`.

## Frozen cross-period closure

- >=2 `SUPPORT` and zero `OPPOSE` -> `SUPPORTED_AFTER_SOURCE_PARTIAL_REANCHOR`
- >=2 `OPPOSE` -> `NOT_SUPPORTED_AFTER_SOURCE_PARTIAL_REANCHOR`
- at least one `SUPPORT` and at least one `OPPOSE` -> `NOT_STABLE_AFTER_SOURCE_PARTIAL_REANCHOR`
- otherwise -> `INCONCLUSIVE_AFTER_SOURCE_PARTIAL_REANCHOR`

Do not change these rules after seeing output.

## Secondary diagnostics

Report, but do not use to choose the representation:

- inherited count before vs after;
- re-anchoring impact labels;
- selected-origin age and remaining points;
- PATH_REMAINING vs ORIGIN_TARGET_LEVEL descriptive behavior.

## Guardrails

- Preserve all prior results as historical checkpoints.
- Do not reinterpret this re-anchoring as the full instructor state machine.
- Do not add a 200-point buffer.
- Do not choose equality behavior from performance.
- Do not choose a production expiry or minimum age.
- Do not call target-first rate a strategy win rate.
- Historical outcomes cannot upgrade source provenance.
