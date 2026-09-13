# V0.1 Holdout Progressive-Reveal Runner Implementation — 2026-09-13

Status: IMPLEMENTED_PUSHED / PRE_ACTIVATION / UNSCORED

## Freeze and implementation identity

- runner contract freeze commit: `ac8f278`
- runner implementation commit: `0556b6f`
- engine freeze commit: `75866d2`
- protocol freeze commit: `43c29be`
- activation boundary: `2026-09-14T07:00:00+07:00`

## Implemented

Library guard:

`src/nexus_xau/research/holdout_progressive_runner_v0.py`

CLI:

`scripts/holdout_progressive_runner_v0.py`

Tests:

`tests/test_holdout_progressive_runner_v0.py`

The runner:

- revalidates the tracked activation lock on every status/append operation;
- forbids ledger append before the prospective boundary;
- requires timezone-aware checkpoint and visibility times;
- requires `visible_data_until <= checkpoint_time <= now`;
- enforces chronological non-decreasing checkpoint order;
- allows same-time records for complete decision-time batches;
- permits only the four frozen RQ-011 Stage-B checkpoint classes;
- recursively rejects outcome/scoring fields and frozen V0 outcome labels;
- validates eligible event payloads with the frozen RQ-010 event schema;
- requires eligible `checkpoint_time == post_sig_closed_at`;
- requires eligible `visible_data_until == checkpoint_time`;
- requires the frozen 30-calendar-day administrative horizon;
- appends through the existing RQ-012 canonical hash-chain ledger primitive.

The runner has no scoring command.

## Existing tooling reused

Stage-A raw M1 export remains separate and continues to reuse:

`src/nexus_xau/data/mt5_export.py`

No duplicate MT5 exporter was introduced.

## Validation

Focused runner + RQ-012 ledger tests:

- 22 tests PASS

Full repository pytest:

- PASS / exit code 0

Ruff:

- PASS

Research preflight:

- PASS

Tracked activation-lock runtime status before boundary:

```text
activation_state=PRE_ACTIVATION
prospective_boundary=2026-09-14T07:00:00+07:00
outcome_scoring_enabled=false
ledger_record_count=0
```

The tracked ledger `results/holdout/v0/checkpoints.jsonl` was not created during implementation or validation.

## Safety boundary

This implementation does not activate the holdout early.

Before the boundary, only validation/status inspection is permitted. At or after the boundary, collection/label locking may begin only if intentionally resumed under frozen RQ-011.

No holdout outcome has been opened or scored.

## Current interpretation

`PRE_ACTIVATION EXECUTION GUARD READY / HOLDOUT RESERVED / UNSCORED`

This is operational readiness only. It is not an outcome, performance result, trade/system Win Rate, expectancy, or profitability claim.
