# Phase 1 Unknown-Classification Enforcement Implementation V0.1 — 2026-09-17

Status: IMPLEMENTED / MACHINE-ENFORCED / P1-09 READY_RESEARCH_LEVEL / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract: `docs/PHASE1_UNKNOWN_CLASSIFICATION_ENFORCEMENT_CONTRACT_V0.1_2026-09-17.md`
Registry: `docs/PHASE1_UNKNOWN_CLASSIFICATION_REGISTRY_V0.1.json`
Validator: `scripts/research_preflight.py`
Tests: `tests/test_unknown_classification_registry.py`

## Implemented behavior

Every current `PARTIAL` or `BLOCKING` Phase 1 readiness dependency with an explicit `missing` item is now required to map exactly once to an `OPEN` registry entry.

Each open entry carries:

- one allowed epistemic class;
- one orthogonal blocking axis;
- a non-empty resolution basis;
- evidence references that must exist;
- class-specific acquisition/reopen metadata.

Generic `UNKNOWN` is rejected.

Current allowed epistemic classes:

- `KNOWN_NOW`;
- `DERIVABLE`;
- `RUNTIME_OBSERVABLE`;
- `STRUCTURAL_UNKNOWN`;
- `IRREDUCIBLE_OR_NOT_YET_REDUCIBLE`.

Current allowed blocking axes:

- `BLOCKING`;
- `NON_BLOCKING`;
- `REQUIRED_LATER`;
- `IRRELEVANT`.
## Current coverage

Real preflight reports:

`unknown_classification=PASS | 14 open | 14 readiness gaps covered`

The registry currently covers unresolved dependencies in:

- P1-08 broader replay/origin-history readiness;
- P1-10 execution economics;
- P1-11 position sizing/risk cap;
- P1-12 pristine/future confirmation;
- P1-13 supervised-pilot operations.

P1-09 itself is no longer an unresolved readiness gap because this enforcement is active.

## Fail-closed checks

Preflight rejects:

- registry schema/scope/enum drift;
- generic or invalid epistemic classes;
- invalid blocking axes;
- `OPEN / KNOWN_NOW` contradictions;
- missing class-specific method/reopen metadata;
- missing evidence references;
- duplicate open mappings;
- dangling component or `missing` mappings;
- readiness gaps with no registry coverage;
- `PARTIAL`/`BLOCKING` readiness components with no explicit `missing` array;
- open registry entries attached to ready components.

## Validation evidence

- targeted registry validator: 11/11 PASS;
- targeted registry + state-drift governance regression: 18/18 PASS;
- targeted Ruff: PASS;
- research preflight: PASS with 14/14 current readiness gaps covered;
- full repository durable pytest `XAU-UNKNOWN-CLASS-FULLPYTEST-20260917`: DONE, one attempt, exit code 0, persisted progress = 390/390 tests;
- broad Ruff durable job `XAU-UNKNOWN-CLASS-RUFF-20260917`: DONE, one attempt, exit code 0, `All checks passed!`.

Full-suite warning output remains non-fatal and is outside this governance implementation; no warning-driven semantic change is made here.