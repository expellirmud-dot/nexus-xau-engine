# Phase 1 Pilot Operations Scaffold Implementation V0.1 — 2026-09-17

Status: IMPLEMENTED / NON-EXECUTING / THREE P1-13 DERIVABLE-NONBLOCKING GAPS CLOSED / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract: `docs/PHASE1_PILOT_OPERATIONS_SCAFFOLD_CONTRACT_V0.1_2026-09-17.md`
Core: `src/nexus_xau/reporting/pilot_operations.py`
CLI: `scripts/pilot_operations_snapshot.py`
Tests: `tests/test_pilot_operations.py`

## Implemented scope

The scaffold composes existing project authorities into a deterministic operations snapshot. It does not create a parallel canonical state store and does not execute trades.

Implemented P1-13 dependencies:

- pilot-facing reason/audit output;
- data/feed health behavior;
- rollback/version identity workflow.

Still intentionally unresolved:

- final frozen decision version;
- trade/risk conventions if executing;
- all P1-08/P1-10/P1-11/P1-12 blockers and required-later evidence.

## Operations snapshot

The snapshot includes:

- Git/current-state/checkpoint/version identity;
- governance preflight status and fixed execution/holdout guards;
- current PARTIAL/BLOCKING readiness components;
- all OPEN unknown-registry dependencies with separate epistemic and blocking axes;
- explicit data-health checks and aggregate health state;
- deterministic reason codes/evidence references;
- reference-only rollback identity.

Automatic order send, protected holdout scoring, and economic scoring remain disabled.
## Health semantics

No new spread, latency, freshness, price-distance, or gap threshold was introduced.

Required health checks are aggregated as:

- any explicit FAIL → `FAIL_CLOSED`;
- no FAIL but required UNKNOWN → `UNKNOWN`;
- every required check PASS → `PASS`;
- no required data check → `NOT_APPLICABLE`.

MT5 collector translation uses existing status only:

- `ERROR` / `BLOCKED` or non-empty `last_error` → FAIL;
- `RUNNING` / `BACKFILLING` → PASS;
- other live-required states such as `STOPPED` → UNKNOWN.

Current real collector status observed during implementation was `STOPPED` with `last_error=null`; therefore live health is correctly UNKNOWN rather than guessed stale/healthy.

## Version and rollback

Version identity records project version, Git HEAD/branch/origin-main, working-tree cleanliness, latest progress checkpoint, and SHA-256 of Current State and unknown registry.

Dirty working tree or HEAD/origin-main mismatch fails identity. Missing identity remains explicitly UNKNOWN.

Rollback is metadata only. The scaffold does not emit or run destructive Git/filesystem commands.

## Validation

- contract tests: 10/10 PASS;
- combined P1-09 + P1-13 governance regression: 28/28 PASS;
- targeted Ruff: PASS;
- full repository durable pytest `XAU-PILOT-OPS-FULLPYTEST-20260917`: DONE, one attempt, exit code 0, persisted progress = 400/400 tests;
- broad Ruff durable job `XAU-PILOT-OPS-RUFF-20260917`: DONE, one attempt, exit code 0, `All checks passed!`.

A pre-commit CLI smoke test intentionally observed the dirty working tree and returned identity FAIL / operational `FAIL_CLOSED`, demonstrating the version guard rather than bypassing it.

Full-suite warnings remain non-fatal and outside this scaffold; no warning-driven market semantic change is made here.