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
