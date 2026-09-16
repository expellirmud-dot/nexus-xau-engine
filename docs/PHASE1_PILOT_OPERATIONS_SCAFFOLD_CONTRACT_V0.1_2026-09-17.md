# Phase 1 Pilot Operations Scaffold Contract V0.1 — 2026-09-17

Status: FROZEN PRE-IMPLEMENTATION / NON-EXECUTING / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract ID: `PHASE1_PILOT_OPERATIONS_SCAFFOLD_V0.1`

## Scope

This contract addresses only the P1-13 dependencies currently classified `DERIVABLE / NON_BLOCKING`:

1. pilot-facing reason/audit output;
2. data/feed health behavior;
3. rollback/version identity workflow.

It does not resolve:

- final frozen decision version;
- position sizing;
- risk cap;
- trade/stop conventions;
- execution economics;
- protected holdout confirmation.

Those dependencies remain governed by their existing registry classifications.

## Reuse-first architecture

The scaffold MUST compose existing authorities rather than create a parallel state system:

- `docs/CURRENT_RESEARCH_STATE.json` for project-current workflow state;
- `docs/PHASE1_READINESS_MATRIX.json` for current readiness status;
- `docs/PHASE1_UNKNOWN_CLASSIFICATION_REGISTRY_V0.1.json` for unresolved-dependency classification;
- `scripts/research_preflight.py` for fail-closed governance validation;
- MT5 collector status/state/gap information from existing collector surfaces;
- Exness archive manifest/gap-ledger guards where archive health is relevant;
- Git `HEAD` and current-state checkpoint identity for version/rollback identity.

No new market-data downloader, strategy detector, execution engine, or canonical claim store is authorized.
## Output model

The scaffold emits an auditable operations snapshot. It is not a trading signal.

Required top-level sections:

- `identity`: project/version/checkpoint/Git identity;
- `governance`: preflight and holdout/order-send guards;
- `readiness`: current blocking/partial components;
- `unknowns`: unresolved dependencies with epistemic class and blocking axis;
- `data_health`: explicit observed collector/archive/provenance checks;
- `reasons`: deterministic reason codes and evidence references;
- `rollback_reference`: non-destructive reference identity only.

Required fixed guards:

- `order_send = DISABLED`;
- `holdout_scoring = DISABLED`;
- `economic_scoring = DISABLED` unless separately authorized by future governance;
- no Win Rate, expectancy, profitability, or exact broker-fill claim.

## Reason/audit behavior

Reasons MUST be derived from current structured state. They MUST NOT be reconstructed from market outcomes.

At minimum, reason generation must surface:

- any `BLOCKING` readiness component;
- every `OPEN / BLOCKING` unknown-registry entry;
- any preflight failure;
- any explicit data-source/provenance/gap failure supplied to the scaffold;
- the current fail-closed real-Exness origin-seed state when present.

The snapshot may distinguish `BLOCKING`, `REQUIRED_LATER`, and `NON_BLOCKING` reasons. It must not collapse them into one generic warning bucket.

## Data/feed health behavior

The scaffold MUST NOT invent a price, spread, latency, freshness, or gap tolerance.

Health checks use only explicit existing observations/guards supplied by current systems.

Each health check status is one of:

- `PASS`;
- `FAIL`;
- `UNKNOWN`;
- `NOT_APPLICABLE`.

Overall operational health is:

- `FAIL_CLOSED` if any required check is `FAIL`;
- `UNKNOWN` if no required check fails but at least one required check is `UNKNOWN`;
- `PASS` only when every required check is explicitly `PASS`;
- `NOT_APPLICABLE` only when the snapshot has no required live/archive data check for its declared mode.

Examples of explicit existing FAIL evidence include collector `ERROR`/`BLOCKED`, source-identity mismatch, rejected archive month/window, known-gap rejection, or governance preflight failure.

Raw timestamps and collector states are reported. The scaffold does not invent a staleness-duration threshold.
## Version and rollback identity

The snapshot records immutable identity; it does not perform rollback.

Required identity fields:

- current project version;
- Git `HEAD` commit;
- branch name;
- current-state `latest_progress_checkpoint`;
- SHA-256 of `CURRENT_RESEARCH_STATE.json`;
- SHA-256 of the unknown-classification registry;
- working-tree cleanliness when observed.

`rollback_reference` is reference-only metadata pointing to a prior verified checkpoint/commit when supplied.

The scaffold MUST NOT run `reset --hard`, force-push, history rewrite, file deletion, or any other destructive rollback action.

If Git/state identity cannot be read or is internally inconsistent, the version-identity check is `UNKNOWN` or `FAIL`; it is never guessed.

## Determinism and provenance

For identical structured inputs, the core snapshot builder must produce identical semantic content except an explicitly injected observation timestamp.

Every reason and health check must identify its source section or evidence reference.

No field may silently merge Dukascopy and Exness provenance.

## Required tests before implementation completion

1. deterministic snapshot from identical structured inputs;
2. preflight FAIL yields overall `FAIL_CLOSED` and an explicit governance reason;
3. structural/blocking origin-seed dependency remains distinct from runtime-observable/required-later dependencies;
4. collector `ERROR` or `BLOCKED` yields data-health FAIL without a new threshold;
5. unknown collector state remains `UNKNOWN`, not PASS;
6. all required PASS checks produce overall PASS;
7. Git/state identity missing or inconsistent fails closed or remains explicitly UNKNOWN;
8. rollback output is reference-only and contains no destructive action;
9. snapshot always reports holdout scoring and order send disabled;
10. output contains no Win Rate, expectancy, profitability, P&L, broker-fill, or market-entry recommendation fields.

## Completion boundary

Implementation of this scaffold may resolve only these current P1-13 gaps:

- pilot-facing reason/audit output;
- data/feed health behavior;
- rollback/version identity workflow.

P1-13 remains `PARTIAL` while its other dependencies remain open.

No completion of this scaffold can promote P1-08, P1-10, P1-11, or P1-12 readiness.