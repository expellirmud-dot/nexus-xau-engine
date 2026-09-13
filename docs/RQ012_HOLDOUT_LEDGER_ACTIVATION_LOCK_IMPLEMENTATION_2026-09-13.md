# RQ-012 — Holdout Ledger + Activation Lock Implementation Checkpoint

Date: 2026-09-13 Asia/Bangkok
Status: `IMPLEMENTED_COMMITTED_PUSHED / RESERVED_OR_COLLECTION_READY / UNSCORED`

## Frozen identities

- V0.1 engine freeze: `75866d2`
- RQ-011 protocol freeze: `43c29be`
- pre-code implementation contract freeze: `ed04b20`
- implementation commit: `1d35ab3`
- engine schema: `SIG_MODE2_SIGNAL_RUN_V0.1`

## Implemented

- canonical JSON serialization;
- SHA256 per-record hash with previous-record chain;
- append-only writer that verifies the existing ledger before append;
- fail-closed verifier for malformed/non-canonical/tampered/reordered chains;
- activation-lock creation and validation;
- write-once activation-lock file helper;
- explicit outcome-scoring disablement.

Implementation: `src/nexus_xau/research/holdout_ledger_v0.py`

Tests: `tests/test_holdout_ledger_v0.py`

## Activation reservation

Tracked activation lock:

`docs/RQ012_V0_HOLDOUT_ACTIVATION_LOCK_2026-09-13.json`

Operational ledger target:

`results/holdout/v0/checkpoints.jsonl`

Prospective boundary:

`2026-09-14T07:00:00+07:00` (`Asia/Bangkok`)

No post-boundary outcome was opened.

Environment metadata is grounded in existing broker/runtime evidence for `Exness-MT5Trial6 / XAUUSDm` and the existing MT5 M1 export method. This is environment-specific and must be re-verified if broker/server/symbol changes.

## Validation

- focused RQ-012 tests: PASS (13/13);
- full repository pytest suite: PASS / exit code 0;
- full repository Ruff: PASS;
- activation lock runtime validation: `ACTIVATION_LOCK_OK`;
- holdout outcome scoring: disabled;
- holdout outcomes opened: no.

## Interpretation boundary

Current status is only:

`RESERVED_OR_COLLECTION_READY / UNSCORED`

This checkpoint does not establish trade/system Win Rate, expectancy, profitability, or any V0.1 outcome distribution.

## Closure

Implementation commit `1d35ab3` is pushed to `origin/main`. RQ-012 tooling scope is closed. The prospective holdout remains UNSCORED; future collection must follow frozen RQ-011 and must not inspect or score post-boundary outcomes before its preregistered stopping/sealing conditions are met.
