# 07:00 Minimal V2.1 Fixed-Origin Target — Requirement/Test Matrix — 2026-10-08

Status: IMPLEMENTATION TRACEABILITY / SYNTHETIC + REGRESSION / PRE-NEW-HISTORICAL-OUTCOME

Contract:
`docs/0700_MINIMAL_V2_1_FIXED_ORIGIN_TARGET_CONTRACT_2026-10-08.md`

Implementation surfaces:
- `src/nexus_xau/research/minimal_v2_0700.py` — shared core with frozen V2.0 default target mode;
- `src/nexus_xau/research/minimal_v21_0700.py` — explicit V2.1 fixed-origin public entry points;
- `tests/test_minimal_v21_0700.py` — V2.1 synthetic/invariant suite.

Test count is not the contract. The mapping below is the requirement-level closure record.

| # | Frozen requirement | Evidence test(s) |
|---|---|---|
| 1 | BUY fixed target = anchor + 1,500 project points | `test_buy_fixed_origin_target_is_anchor_plus_1500_points` |
| 2 | SELL fixed target = anchor - 1,500 project points | `test_sell_fixed_origin_target_is_anchor_minus_1500_points` |
| 3 | Confirmation close changes must not move the fixed origin target | `test_fixed_target_is_invariant_to_confirmation_close` |
| 4 | Retracement can make remaining nominal progress differ from confirmation-to-fixed-target distance | `test_retracement_separates_remaining_progress_from_entry_to_fixed_target` |
| 5 | V2.1 must not reset a fresh 1,500-point target from confirmation close | `test_v21_does_not_reset_fresh_1500_point_target_from_confirmation` |
| 6 | Target-first after confirmation remains target-first under fixed target | `test_v21_target_first_uses_fixed_origin_boundary` |
| 7 | Literal point-check-first after confirmation remains point-check-first | `test_v21_point_check_first_uses_existing_literal_anchor_contact` |
| 8 | Same M1 bar hitting target and point-check remains ambiguous | `test_v21_same_bar_target_and_point_check_remains_ambiguous` |
| 9 | Multiple origins retain independent fixed targets | `test_multiple_origins_keep_independent_fixed_targets` |
| 10 | V2.0 default output/target representation remains unchanged | `test_v2_default_mode_remains_path_remaining_and_has_no_v21_fields`; existing `tests/test_minimal_v2_0700.py` regression |
| 11 | V2 state carry remains on V2.0 semantics and unchanged | existing `tests/test_v2_state_carry.py`, especially `test_synthetic_split_replay_matches_unsplit_post_checkpoint_state` plus target/point-check/same-bar restart tests |
| 12 | Archive→V2 integration remains on V2.0 semantics and unchanged | existing `tests/test_archive_v2_integration.py`, including file/frame parity, synthetic-complete integration and fail-closed provenance/seed guards |
| 13 | No P&L, Win Rate, expectancy, profitability, exact broker-fill, slippage or order-send field introduced | `test_v21_does_not_add_economic_or_execution_fields`; existing carry/archive no-economic-field regressions |

## Supplemental implementation guards

Additional V2.1 tests:
- `test_v21_schema_uses_fixed_origin_fields_not_path_remaining_target`
  - requires explicit V2.1 fixed-origin field names;
  - forbids the V2.0 `path_remaining_target_price` label in V2.1 candidate output.
- `test_v21_file_and_frame_entry_points_are_identical`
  - verifies deterministic parity between public file and in-memory V2.1 entry points.

## Current targeted validation

- V2.1 synthetic suite: **13/13 PASS**.
- Targeted Ruff for V2/V2.1 implementation/tests: **PASS**.
- Combined V2.1 + V2.0 + carry + archive collection:
  - V2.1: 13 cases;
  - V2.0: 16 cases;
  - V2 carry: 29 cases;
  - Archive→V2 integration: 14 cases;
  - combined = **72 cases**.
- Combined 72-case regression: **PASS**.
- Warnings observed are pre-existing pandas/NumPy deprecation warnings in older V2/archive tests; no V2.1 semantic failure.

## Evidence boundary

These tests establish implementation logic/invariants only.

They do **not** establish:
- historical market performance;
- system/trade Win Rate;
- expectancy/profitability;
- exact broker fills or slippage;
- universal SL buffer;
- canonical real Exness replay eligibility.

No new historical or protected-holdout V2.1 outcome distribution was inspected for this implementation.
