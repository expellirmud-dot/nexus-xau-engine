# 07:00 Minimal V2.1 Fixed-Origin Target Implementation — 2026-10-08

Status: IMPLEMENTED / SYNTHETIC + REGRESSION VALIDATED / PRE-NEW-HISTORICAL-OUTCOME / HOLDOUT UNSCORED / ECONOMIC SCORING DISABLED / ORDER SEND DISABLED

Version: `0700_MINIMAL_V2.1_FIXED_ORIGIN_TARGET`

Contract:
`docs/0700_MINIMAL_V2_1_FIXED_ORIGIN_TARGET_CONTRACT_2026-10-08.md`

Requirement matrix:
`docs/0700_MINIMAL_V2_1_FIXED_ORIGIN_TARGET_REQUIREMENT_MATRIX_2026-10-08.md`

Source authority:
- `docs/PHASE1_VIDEO_TRADE_GEOMETRY_REANCHOR_RESULT_V0.1_2026-10-08.md`
- canonical claim `SIG_RUN_FIXED_ORIGIN_TARGET_LEVEL`

Implementation:
- shared frozen-default core: `src/nexus_xau/research/minimal_v2_0700.py`
- V2.1 public entry points: `src/nexus_xau/research/minimal_v21_0700.py`
- V2.1 synthetic tests: `tests/test_minimal_v21_0700.py`

## Result

V2.1 implements the source-reanchored candidate target as a fixed post-SIG/origin H4 target:

BUY:
`anchor + 1500 * PROJECT_POINT_SIZE`

SELL:
`anchor - 1500 * PROJECT_POINT_SIZE`

The candidate target no longer moves with M5 confirmation close in V2.1.

The implementation preserves two distinct quantities:
- remaining nominal run progress;
- directional distance from confirmation close to the fixed origin target.

A synthetic retracement fixture proves these can differ.

## V2.0 compatibility

`0700_MINIMAL_V2.0` remains the default behavior of the shared core and preserves the historical `PATH_REMAINING_AT_CONFIRMATION` candidate-target representation.

V2 state carry and Archive→V2 integration continue to select V2.0 semantics because neither integration was silently upgraded.

No V2.0 historical result was rewritten.

## Output schema

V2.1 research-candidate rows expose:
- `target_representation = FIXED_ORIGIN_TARGET_V2_1`;
- `fixed_origin_target_price`;
- `confirmation_to_fixed_target_points`;
- `fixed_origin_first_hit`;
- `fixed_origin_target_at`;
- `fixed_origin_point_check_at`.

V2.1 does not label its candidate target as `path_remaining_target_price`.

## Frozen requirement closure

All 13 contract requirements have explicit requirement-to-test mapping in the requirement matrix.

Targeted V2.1 synthetic suite:
- 13/13 PASS.

Combined regression:
- V2.1: 13 cases;
- V2.0: 16 cases;
- V2 state carry: 29 cases;
- Archive→V2 integration: 14 cases;
- total: 72/72 PASS.

Targeted Ruff:
- PASS.

## Full repository validation

Durable full pytest:
- job `XAU-V21-FULLPYTEST-20261008-R2`;
- status DONE;
- attempts 1;
- exit code 0;
- 424 test cases observed from pytest progress output;
- warnings are existing pandas/NumPy deprecation warnings, not V2.1 semantic failures.

Durable broad Ruff:
- job `XAU-V21-RUFF-20261008-R2`;
- status DONE;
- attempts 1;
- exit code 0;
- `ruff check src tests scripts` = `All checks passed!`.

## Preserved failure history

The first durable submissions are intentionally preserved as failed operational history:

- `XAU-V21-FULLPYTEST-20261008`
- `XAU-V21-RUFF-20261008`

Both failed with `TOOL_FAIL` / `FileNotFoundError` because the submitted command array incorrectly contained a literal leading `--`.

This was an orchestration syntax error, not a pytest/Ruff failure.

The jobs were not overwritten. Corrected R2 job IDs were submitted without the literal `--` and completed successfully.

## Evidence boundary

This implementation establishes logic/invariant correctness only.

It does not establish:
- historical V2.1 market performance;
- system or trade Win Rate;
- expectancy/profitability;
- universal stop buffer;
- exact broker fills/slippage;
- canonical real Exness replay eligibility.

No new historical or protected-holdout V2.1 outcome distribution was inspected during implementation or validation.

Real Exness canonical replay remains blocked by incomplete origin-history seed evidence.

`U-P1-10-STOP-PRICE-ROUTING` remains open.

## Implementation-loop closure condition

The engineering loop is eligible to close after:
- Current State/load-order reconciliation;
- structured JSON validation;
- research preflight PASS;
- `git diff --check` PASS;
- commit/push;
- `main == origin/main`;
- clean tree;
- post-commit RESUME verifying this implementation checkpoint is the latest progress pointer.

Any later real-data V2.1 replay requires a separately authorized evidence/data step and must preserve the existing holdout/economic/order-send guards.

## Final acceptance

After Current State/workstream/readiness reconciliation:

- structured JSON validation: PASS;
- research preflight: PASS;
- canonical governance: PASS;
- finding ledger: PASS;
- readiness/unknown-classification consistency: PASS;
- `git diff --check`: PASS.

Pre-commit inspection confirms the shared core default remains
`PATH_REMAINING_AT_CONFIRMATION_V2_0`; V2.1 fixed-origin fields/report identity are emitted only when the explicit V2.1 target mode is selected.
