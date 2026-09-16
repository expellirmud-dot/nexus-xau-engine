# Phase 1 Unknown-Classification Enforcement Contract V0.1 — 2026-09-17

Status: FROZEN PRE-IMPLEMENTATION / GOVERNANCE ONLY / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract ID: `PHASE1_UNKNOWN_CLASSIFICATION_ENFORCEMENT_V0.1`

## Purpose

Prevent unresolved dependencies from being collapsed into a generic `UNKNOWN` bucket.

Every current Phase 1 readiness dependency that is still explicitly missing under a `PARTIAL` or `BLOCKING` component must carry two orthogonal machine-readable classifications:

1. epistemic class;
2. blocking axis.

This is governance metadata. It does not create market rules, thresholds, targets, or execution assumptions.

## Allowed epistemic classes

- `KNOWN_NOW`
- `DERIVABLE`
- `RUNTIME_OBSERVABLE`
- `STRUCTURAL_UNKNOWN`
- `IRREDUCIBLE_OR_NOT_YET_REDUCIBLE`

`UNKNOWN` by itself is forbidden.

## Allowed blocking axes

- `BLOCKING`
- `NON_BLOCKING`
- `REQUIRED_LATER`
- `IRRELEVANT`

The two axes MUST remain independent. For example, a future confirmation can be `RUNTIME_OBSERVABLE / REQUIRED_LATER` while a missing lifecycle definition can be `STRUCTURAL_UNKNOWN / BLOCKING`.
## Registry coverage rule

Introduce `docs/PHASE1_UNKNOWN_CLASSIFICATION_REGISTRY_V0.1.json`.

For every readiness component whose status is `PARTIAL` or `BLOCKING`:

- the component MUST have a non-empty `missing` array;
- every `missing` item MUST have exactly one `OPEN` registry entry matched by `(readiness_component_id, readiness_missing)`;
- every `OPEN` registry entry MUST match a current readiness `missing` item;
- duplicate open mappings are invalid;
- every evidence reference in a registry entry MUST exist.

`READY` and `READY_RESEARCH_LEVEL` components do not require open unknown entries.

Historical `RESOLVED` or `SUPERSEDED` entries may remain in the registry but do not satisfy current missing-item coverage.

## Class-specific metadata

Every `OPEN` entry requires non-empty `resolution_basis`.

Additionally:

- `DERIVABLE` requires `derivation_method`;
- `RUNTIME_OBSERVABLE` requires `observation_method`;
- `STRUCTURAL_UNKNOWN` requires `reopen_condition`;
- `IRREDUCIBLE_OR_NOT_YET_REDUCIBLE` requires `reduction_condition`.

`KNOWN_NOW` is not valid for an `OPEN` unresolved dependency.

## Preflight behavior

`scripts/research_preflight.py` MUST fail closed on:

- schema/version mismatch;
- invalid epistemic class or blocking axis;
- generic `UNKNOWN` classification;
- missing class-specific metadata;
- missing or duplicate readiness coverage;
- dangling registry mapping;
- missing evidence reference;
- a `PARTIAL`/`BLOCKING` readiness component with no explicit `missing` array.

Failure reasons must identify the offending entry/component rather than silently coercing values.

## Scope guard

This contract covers current Phase 1 readiness dependencies only.

It does not require every historical note, research observation, or future value to become a registry row.

It does not authorize opening protected holdout outcomes or automatic order execution.

## Completion criterion

P1-09 may move from `PARTIAL` to `READY_RESEARCH_LEVEL` only after:

1. the registry covers every current PARTIAL/BLOCKING readiness missing item;
2. preflight enforces the registry contract;
3. targeted validator tests pass;
4. existing project preflight and full regression remain green.