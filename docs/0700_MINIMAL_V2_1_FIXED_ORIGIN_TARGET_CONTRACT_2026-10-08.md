# 07:00 Minimal V2.1 Fixed-Origin Target Contract — 2026-10-08

Status: FROZEN PRE-IMPLEMENTATION / PRE-NEW-OUTCOME / SOURCE-REANCHORED TARGET ONLY / HOLDOUT UNSCORED / ORDER SEND DISABLED

Version ID: `0700_MINIMAL_V2.1_FIXED_ORIGIN_TARGET`

Supersedes no historical implementation. `0700_MINIMAL_V2.0` remains immutable historical evidence.

Source authority:
- `docs/PHASE1_VIDEO_TRADE_GEOMETRY_REANCHOR_RESULT_V0.1_2026-10-08.md`
- canonical claim `SIG_RUN_FIXED_ORIGIN_TARGET_LEVEL`

## 1. Purpose

V2.1 changes exactly one decision-relevant research representation from V2.0:

`candidate target anchoring after M5 confirmation`.

V2.0 historical representation:

`confirmation_close +/- remaining_nominal_progress_points`

V2.1 source-reanchored representation:

`origin/post-SIG anchor +/- full nominal H4 run`

No new historical/holdout outcome may be inspected to choose or tune this representation.

## 2. Frozen target formula

Constants remain:

- `PROJECT_POINT_SIZE = 0.01`
- H4 nominal primary run = `1500 project points`

For H4 origin anchor `A` and side `S`:

BUY:

`fixed_origin_target_price = A + 1500 * PROJECT_POINT_SIZE`

SELL:

`fixed_origin_target_price = A - 1500 * PROJECT_POINT_SIZE`

The fixed target is determined by the origin and does not move when the later M5 confirmation close changes.

## 3. Distinct state quantities

V2.1 must preserve these as different quantities:

1. `consumed_points_at_confirmation`
   - versioned favorable-progress state from the origin anchor;
2. `remaining_points_at_confirmation`
   - `max(0, 1500 - consumed_points_at_confirmation)`;
3. `fixed_origin_target_price`
   - absolute target from the origin anchor;
4. `confirmation_to_fixed_target_points`
   - directional distance from confirmation close to the fixed target.

After retracement, (2) and (4) may differ.

No code may force them equal.

## 4. Lifecycle semantics unchanged

Before confirmation, V2.1 uses the same existing H4 origin lifecycle as V2.0:

- target-first before confirmation => run complete;
- literal M1 point-check/anchor contact first => origin destroyed;
- target and point-check in the same M1 bar => ambiguous terminal same bar;
- active origins remain independent;
- consumed state remains continuous/versioned metadata;
- no arbitrary origin expiry is introduced.

The source re-anchor does not alter point-check semantics.

## 5. Candidate outcome semantics

After a valid M5 confirmation, V2.1 measures the first observed relation between:

- `fixed_origin_target_price`;
- `origin_anchor_price` as point-check.

Using the existing literal M1 boundary-hit semantics:

- target first => `TARGET_FIRST`;
- point-check first => `POINT_CHECK_FIRST`;
- same M1 bar => `AMBIGUOUS_SAME_BAR`;
- neither before next 07:00 => `NEITHER_BY_NEXT_0700`.

This remains signal/run research, not trade P&L.

## 6. Scope that must remain unchanged from V2.0

V2.1 must preserve:

- PAT2 FULL-RANGE detector;
- H4 origin construction and adjacent post-SIG anchor mapping;
- M5-only confirmation lane used by Minimal V2;
- 07:00 Asia/Bangkok = 00:00 UTC cutoff;
- Daily Frame research proxy behavior;
- multiple-origin independence;
- action conflict fail-closed behavior;
- source/data/provenance guards;
- archive/carry V2.0 behavior unless a separately versioned V2.1 integration explicitly selects the new target mode.

No universal SL buffer is added.

## 7. Implementation architecture freeze

To preserve V2.0 reproducibility:

1. retain the existing V2.0 public entry points and defaults;
2. parameterize only the internal candidate-target representation with an explicit mode;
3. V2.0 public entry points must explicitly or by frozen default select:
   `PATH_REMAINING_AT_CONFIRMATION_V2_0`;
4. add new V2.1 public entry point(s) selecting:
   `FIXED_ORIGIN_TARGET_V2_1`;
5. carry/archive code remains on V2.0 default unless explicitly upgraded by a later bounded contract.

No existing V2.0 output column may silently change meaning.

## 8. V2.1 output fields

For research-candidate rows, V2.1 must expose explicit names:

- `target_representation = FIXED_ORIGIN_TARGET_V2_1`;
- `fixed_origin_target_price`;
- `confirmation_to_fixed_target_points`;
- `fixed_origin_first_hit`;
- `fixed_origin_target_at`;
- `fixed_origin_point_check_at`.

It may retain consumed/remaining metadata for state context.

It must not label the V2.1 target as `path_remaining_target_price`.

## 9. Synthetic falsification requirements

Before any new historical outcome inspection:

1. BUY fixed target equals anchor + 1500 points.
2. SELL fixed target equals anchor - 1500 points.
3. Changing confirmation close while keeping the same origin does not change fixed target.
4. A retracement fixture proves `remaining_points_at_confirmation != confirmation_to_fixed_target_points` can occur.
5. V2.1 does not reset a fresh 1500-point target from confirmation close.
6. Target-first after confirmation remains target-first.
7. Point-check-first after confirmation remains point-check-first.
8. Same-bar target + point-check remains ambiguous.
9. Multiple origins retain independent fixed targets.
10. V2.0 output regression remains unchanged under its default mode.
11. V2 state-carry V0.1 regression remains unchanged because it continues selecting V2.0 semantics.
12. Archive V2 integration regression remains unchanged because it continues selecting V2.0 semantics.
13. No P&L, Win Rate, expectancy, profitability, exact broker-fill, slippage or order-send field is introduced.

Test count is not a substitute for requirement-to-test traceability.

## 10. Prohibited inference

V2.1 implementation must not:

- use historical V2.0 results to tune the target formula;
- convert the one 100-point Buy SL example into a universal stop;
- infer SELL stop buffer by symmetry;
- modify D1 stage semantics;
- open protected holdout outcomes;
- claim trade/system Win Rate;
- claim expectancy/profitability;
- enable order sending.

## 11. Stop condition for this engineering loop

The V2.1 implementation loop is closed only when:

- the fixed target representation is implemented under a new version;
- all frozen synthetic requirements have explicit tests;
- V2.0/carry/archive regressions pass unchanged;
- governance/preflight/structured files pass;
- implementation checkpoint is committed and pushed;
- no new historical/holdout outcome distribution has been inspected.

After that, any real replay using V2.1 requires a separately authorized evidence/data step and remains subject to the existing real Exness origin-history blocker.
