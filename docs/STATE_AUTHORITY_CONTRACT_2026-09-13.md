# State Authority Contract — 2026-09-13

Status: ACTIVE / PROJECT-CURRENT WORKFLOW CONTRACT

## Purpose

Prevent State Drift caused by reading documents with different scopes as if they were one current state.

## Scope classes

### PROJECT_CURRENT

These files jointly describe where the project is now:

- docs/CURRENT_RESEARCH_STATE.json
- research_queue/QUEUE.json
- the project-current fields embedded in docs/0700_WORKSTREAM_STATE.json
- the current holdout activation lock when a reserved holdout identity exists

They must agree on active RQ, active worksheet, queue state, latest project checkpoint, and reserved holdout identity.

### WORKSTREAM_CURRENT

A workstream dashboard is current only for its named lane.

For the 07:00 lane:

- docs/0700_WORKSTREAM_STATE.json

Its lane-local latest checkpoint may legitimately be older than the latest project checkpoint. That is not drift if the file explicitly points back to the project-current state.

### HISTORICAL_SNAPSHOT

Dated RQ worksheets, closures, implementation checkpoints, and experiment reports preserve what was true at their recorded time.

Historical text such as "RQ-009 active" or "RQ-012 active" must remain preserved when it was true then. It must not be used as present workflow authority.

### KNOWLEDGE_AUTHORITY

Canonical claims and source-coverage state answer what the project currently accepts as evidence, not which workflow is active:

- docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json
- docs/SOURCE_COVERAGE_LEDGER.json

Workflow status and knowledge authority are separate dimensions.

## Project-current invariants

Preflight must fail when any of these are violated:

1. QUEUE.active and CURRENT_RESEARCH_STATE.operational_research_queue active fields disagree.
2. Queue state differs between QUEUE and CURRENT_RESEARCH_STATE.
3. A workstream's project-current pointers disagree with the project queue.
4. The project-current latest checkpoint disagrees with the last closure when no RQ is active.
5. The recorded last-closed RQ is not actually closed or its closure reference differs.
6. Reserved RQ-012 holdout identity differs across CURRENT_RESEARCH_STATE, QUEUE, and activation lock.
7. Holdout scoring is enabled/authorized while the state says RESERVED/UNSCORED.
8. A newer project-current structured file exists while CURRENT_RESEARCH_STATE is older.

## Current project state at this contract freeze

- active decision-critical RQ: none
- queue state: NO_ACTIVE_DECISION_CRITICAL_RQ_HOLDOUT_RESERVED_UNSCORED
- last closed RQ: RQ-012
- project-current checkpoint: docs/RQ012_HOLDOUT_LEDGER_ACTIVATION_LOCK_IMPLEMENTATION_2026-09-13.md
- RQ-012 engine freeze: 75866d2
- RQ-011 protocol freeze: 43c29be
- prospective boundary: 2026-09-14T07:00:00+07:00
- holdout outcomes: unopened
- outcome scoring: disabled
- 07:00 workstream lane: RQ-015 closed; no reopen trigger

## Reconciliation rule

When drift is found:

- do not select the most convenient document;
- identify scope and chronology;
- preserve historical wording;
- repair only project-current pointers or add explicit scope labels;
- validate JSON, preflight, tests, Ruff, and git diff;
- commit/push one coherent reconciliation checkpoint.

## WO-055 governance extension — 2026-09-14

This extension adds machine-checkable research-governance semantics without changing the original workflow/status scope model.

### RQ_ADMISSION_AUTHORITY

`research_queue/QUEUE.json` remains the single operational queue.

After WO-055 migration:

- `governance.admission_required_for_activation=true`;
- a non-null decision-critical `active` RQ requires a matching valid record under `admissions`;
- closed/queued legacy RQs are not rewritten merely to satisfy the new prospective schema;
- admission validates newness, bounded question scope, falsification, decision consequences, dependencies, stop condition, and an outcome/leakage guard when applicable;
- admission never overrides the one-active-decision-critical-RQ policy.

### CLAIM_AUTHORITY

`docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json` remains the single current claim store.

Pre-WO055 claims are grandfathered only while deterministic authority-sensitive fingerprints match the migration baseline.

A new claim or authority-sensitive change to a grandfathered claim requires explicit per-claim governance:

- `EXCLUSIVE`: exactly one current authority reference;
- `COMPOSITE`: at least two explicitly compatible current authority references plus a compatibility statement;
- source references remain mandatory;
- active+superseded contradictions and supersession cycles fail closed.

No EXCLUSIVE/COMPOSITE mode is inferred for unchanged legacy claims.

### VALIDATION_AUTHORITY

Governed claims keep validation dimensions separate:

1. `SOURCE_VALIDATION`;
2. `REPRESENTATION_VALIDATION`;
3. `IMPLEMENTATION_VALIDATION`;
4. `HISTORICAL_EVIDENCE`;
5. `REPLICATION`;
6. `CONTROL`;
7. `HOLDOUT`.

A PASS in one dimension has no authority in another dimension.

Historical evidence is context/no-promotion authority. Holdout evidence is confirmatory/no-promotion authority and cannot be used for design/tuning promotion.

`UNKNOWN` and `NOT_APPLICABLE` remain valid first-class outcomes.

### DERIVED_AUTHORITY_VIEW

`results/governance/research_authority.json` is an optional derived view with schema `WO055_AUTHORITY_REPORT_V0.1`.

It is not a canonical store and cannot mutate authority.

Rules:

- deleting it does not change project state;
- regeneration must be deterministic from the canonical claim register;
- unchanged legacy claims render as `LEGACY_UNCLASSIFIED`, not guessed authority;
- if a local generated view exists, preflight compares it with a fresh normalized derivation and fails with `GENERATED_AUTHORITY_VIEW_MISMATCH` on divergence;
- absence of the derived file is allowed.

### Additional preflight invariants

WO-055 adds fail-closed checks for:

- duplicate canonical claim IDs;
- missing claim authority/source references;
- active+superseded contradictions;
- supersession cycles;
- EXCLUSIVE/COMPOSITE authority cardinality and compatibility;
- collapsed validation dimensions;
- historical evidence promoted as current authority;
- holdout evidence used for design/tuning authority;
- migrated legacy claim fingerprint drift without explicit governance;
- active RQ without valid admission;
- generated authority-report mismatch when the local view exists.

These checks extend the original state-drift contract; they do not weaken or replace any existing project-current, workstream, or holdout invariant.
