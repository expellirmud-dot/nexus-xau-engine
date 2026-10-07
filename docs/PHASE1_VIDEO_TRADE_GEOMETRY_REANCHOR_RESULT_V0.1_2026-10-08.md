# Phase 1 Video Trade-Geometry Re-anchor Result V0.1 — 2026-10-08

Status: SOURCE RECONCILIATION CLOSED / PRE-NEW-OUTCOME / V2.0 HISTORICAL / NEW VERSION REQUIRED FOR IMPLEMENTATION / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract:
`docs/PHASE1_VIDEO_TRADE_GEOMETRY_REANCHOR_CONTRACT_V0.1_2026-10-08.md`

New first-party evidence:
`docs/VIDEO_SOURCE_EVIDENCE_SL_TP_WICK_REANCHOR_2026-10-08.md`

Prior source closures used in reconciliation:

- `docs/RQ007_ENTRY_SL_INVALIDATION_SOURCE_CLOSURE_2026-09-08.md`
- `docs/RQ009_SIG_ENTRY_SOURCE_VISUAL_CHECKPOINT_2026-09-09.md`
- `docs/DIRECT_RELATIVE_REMAINING_SIG_RUN_DAILY_FRAME_2026-09-03.md`
- `docs/REMAINING_RUN_STATE_TEST_PLAN_2026-09-04.md`

No new historical or protected-holdout outcome was inspected to choose the source interpretation.

## 1. Confirmed wick/check maps to the existing Mode-2 post-SIG object

The new long video sequence is materially the same state machine already closed in RQ-009:

`PA confirmed -> post-SIG candle closes -> its wick becomes point-check -> next candle retraces/body-collects -> M1/M5 reversal before check touch -> entry`.

Therefore the video does **not** require a new anchor object.

Current mapping:

`CONFIRMED_CHECK_WICK = EXISTING SIG_ENTRY_MODE_2 POST_SIG POINT_CHECK STRUCTURAL OBJECT`

For the discussed Mode-2 family, the confirmed post-SIG wick/point-check remains the structural SL reference, subject to the already documented nearby-frame routing where applicable.

## 2. Target anchor is fixed at the post-SIG/origin reference

RQ-007 already recorded that:

- post-SIG reference is the run-count anchor;
- timeframe run/TP is measured from the post-SIG reference.

The new videos directly reinforce that relation by stating that the target distance is counted from the wick reference:

- H1 = 1,000 project points;
- H4 = 1,500 project points;
- Day = 5,000 project points in the shown example.

The source-faithful target representation is therefore an **absolute target level fixed from the origin/post-SIG reference**, not a target re-anchored to a later confirmation/entry price.

For direction sign `s` (+1 BUY, -1 SELL) and a source-backed nominal run `N`:

`fixed_target_level = post_sig_reference + s * N * PROJECT_POINT_SIZE`

This formula expresses the already source-closed anchor relation. It is not an outcome-fitted threshold.

The Day 5,000 statement strengthens one directly taught Day target example. It does not erase the separately evidenced Day/D1 5,000–10,000 family or close the exact stage/set transition.

## 3. Remaining run is state, not a target re-anchoring formula

Direct owner/relative guidance remains valid:

a later 07:00 Daily-Frame entry participates in an inherited unfinished H1/H4/D run and must not automatically reset a fresh full run from the later entry.

However, the old ambiguity in `REMAINING_RUN_STATE_TEST_PLAN_2026-09-04.md` is now source-reconciled:

- `ORIGIN_TARGET_LEVEL` matches the source-backed run anchor;
- `PATH_REMAINING_AT_CONFIRMATION` remains a historical research representation, not teacher-intent authority.

Two quantities must remain distinct:

1. `remaining_nominal_progress_points` — how much of the nominal run has not yet been achieved under the versioned run-progress representation;
2. `entry_to_fixed_target_points` — the directional price distance from a later entry/confirmation price to the fixed origin target level.

After a retracement these values can differ.

Therefore a new source-faithful version must **not** compute a new absolute target as:

`later_entry_or_confirmation +/- remaining_nominal_progress_points`.

V2.0 used that representation under a frozen pre-outcome research contract. Those historical results remain valid for V2.0 and must not be rewritten.

## 4. Stop geometry is materially narrowed but not fully deterministic for trade P&L

The source evidence now establishes for SIG Entry Mode 2:

`STRUCTURAL_STOP_REFERENCE = confirmed post-SIG point-check wick`

with already documented nearby source-defined frame routing where applicable.

The new short Buy example additionally says to place SL below the local low/check area by 100 points.

The new long example describes the confirmed wick as the check/SL placement reference.

Together with RQ-007/RQ-009, the safe conclusion is:

- structural stop reference: source-backed;
- one 100-point Buy buffer example: source-backed as an example;
- universal numeric buffer: not established;
- deterministic buffer/frame routing for every target trade family: not yet closed;
- exact broker fill/stop execution: not established.

Therefore the old broad unknown `U-P1-10-STOP-GEOMETRY` should be superseded by a narrower residual covering deterministic stop-price/buffer/context routing sufficient for trade-level P&L.

No 100/200/300-point value may be selected from favorable outcomes.

## 5. Historical PATH_REMAINING result is preserved

Historical Q1/related work found `PATH_REMAINING_AT_CONFIRMATION` operationally stronger than `ORIGIN_TARGET_LEVEL` under the then-frozen scoring representation.

That finding is preserved.

It cannot decide instructor/source intent.

The source reconciliation changes **semantic authority**, not the historical result.

Current interpretation:

`historical scoring usefulness of PATH_REMAINING != source proof that PATH_REMAINING is the intended TP anchor`.

## 6. V2.0 boundary

`0700_MINIMAL_V2.0` remains immutable historical evidence.

Do not patch its target formula in place.

Any source-faithful implementation of the fixed origin target must use a new version and must be frozen before inspecting its new outcome distribution.

Synthetic/invariant tests may be used before real outcomes.

## 7. Registry/readiness consequence

The following authority changes are justified:

- add an active canonical claim for fixed post-SIG/origin target level;
- demote `0700_PATH_REMAINING_RESEARCH_RELATION` to historical/versioned research representation only;
- preserve the historical PATH_REMAINING observation in the Finding Ledger;
- supersede broad `U-P1-10-STOP-GEOMETRY`;
- add a narrower blocking residual for deterministic stop-price/buffer/context routing;
- source-trigger actionability for the old stop-geometry item is consumed; the narrower residual requires new source evidence or an explicit owner-frozen project stop convention.

## 8. Next bounded engineering action

Freeze and implement a **new pre-outcome research version** that changes only the target-anchor representation from V2.0 PATH_REMAINING re-anchoring to fixed post-SIG/origin target level, while preserving:

- existing point-check lifecycle semantics;
- multiple-origin independence;
- fail-closed data/provenance guards;
- no trade P&L;
- no Win Rate/expectancy/profitability claim;
- holdout scoring disabled;
- automatic order sending disabled.

The new version must retain V2.0 reproducibility unchanged.
