# State Drift Audit — 2026-09-13

Status: RECONCILED / VALIDATED

## Trigger

The project owner identified that documents were reporting different states.

## Findings

### Real project-current drift

1. research_queue/QUEUE.json had RQ-012 status CLOSED while its current_summary still described the pre-implementation action: resolve commits, freeze contract, implement and test.
2. docs/CURRENT_RESEARCH_STATE.json and docs/0700_WORKSTREAM_STATE.json had been repaired earlier, but their scopes were not explicit enough to prevent a lane-local RQ-015 checkpoint from being mistaken for the latest project checkpoint.
3. Bootstrap/maintenance wording assumed an active worksheet even when QUEUE.active was null.

### Historical differences that are not drift

- docs/AGENT_ZERO_CONTEXT_BOOTSTRAP_2026-09-09.md correctly records RQ-009 as active at that historical checkpoint.
- docs/0700_STATE_DATASET_V1_IMPLEMENTATION_2026-09-12.md correctly records RQ-012 as operationally active at that historical checkpoint.
- RQ-015 freeze/result documents correctly preserve the 07:00 lane chronology.

These are retained. Historical state is not rewritten into current state.

## Reconciliation

- Added docs/STATE_AUTHORITY_CONTRACT_2026-09-13.md.
- Marked CURRENT_RESEARCH_STATE as PROJECT_CURRENT and added explicit state-authority pointers.
- Marked 0700_WORKSTREAM_STATE as WORKSTREAM_CURRENT_0700_ONLY and added project-current pointers.
- Reconciled RQ-012 current_summary in QUEUE.json to its closed/reserved state.
- Added historical-snapshot notice to the zero-context bootstrap checkpoint.
- Updated AGENTS / PROJECT_BOOTSTRAP / maintenance policy to separate workflow scope from evidence authority.
- Extended research preflight to detect cross-file state drift rather than only active-RQ mismatch/timestamp staleness.

## Holdout safety

No holdout outcome was opened or scored during this audit.

The activation identity remains:

- engine commit 75866d2
- protocol commit 43c29be
- prospective boundary 2026-09-14T07:00:00+07:00
- scoring disabled

## Validation

- structured JSON parse: PASS via preflight/load
- State Drift preflight: PASS
- focused State Drift tests: 5/5 PASS
- RQ-012 focused tests: 13/13 PASS
- full pytest suite: PASS / exit code 0
- Ruff: PASS
- git diff --check: PASS

Existing pandas/NumPy timedelta deprecation warnings remain unchanged and are not State Drift failures.
