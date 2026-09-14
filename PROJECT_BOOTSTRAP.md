# NEXUS XAU Engine — Deep Project Bootstrap

Purpose: this is the evidence-loading path used **after** the global compact continuity capsule when substantive research or semantic work is required.

Default reconnect entry point:

`py -3 D:\tools\nexus-project-continuity\continuity.py resume --project xau`

Shortcut:

`D:\tools\NEXUS-START\RESUME_WORK.cmd --project xau`

For simple reconnect/status/resume work, use the compact capsule and stop there if it already identifies the live job state, current version, checkpoint, and next action.

Do not bulk-load Project evidence merely because a chat/session restarted.

## When deep bootstrap is required

Escalate to this file before:

- changing/interpreting a research rule or representation;
- opening/reopening source research;
- changing semantic research code;
- interpreting outcomes into a research conclusion;
- modifying canonical claims;
- designing a new experiment/version;
- reconciling contradictory evidence.

## Mandatory deep entry sequence

1. Read `AGENTS.md`.
2. Read `docs/PHASE1_CURRENT_OBJECTIVE_2026-09-14.md`.
3. Read `docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md`.
4. Read `skills/nexus-xau-research/SKILL.md`.
5. Run the repository preflight:

   `.venv\Scripts\python.exe scripts\research_preflight.py`

6. Read only the structured pointers material to the active question:
   - `docs/CURRENT_RESEARCH_STATE.json`
   - active workstream dashboard;
   - relevant canonical claims;
   - relevant source-coverage entries;
   - `research_queue/QUEUE.json`;
   - active worksheet/latest checkpoint.

7. Load only the specific supporting checkpoint/source documents reached through those pointers.

Do not read the entire `docs/` tree on every session.

## Required pre-work comprehension check

Before opening a new source or running a new test, the agent must be able to state from repository evidence:

- governing 07:00 project objective;
- meaning of PASS / unknown-state handling;
- current active workstream;
- current workstream purpose/success criteria and the valid PASS/UNKNOWN behavior;
- current active RQ ID and worksheet;
- latest completed checkpoint;
- current canonical facts relevant to that RQ;
- currently unresolved blockers;
- which source windows have already been reviewed for the question;
- whether any prior finding was superseded, narrowed, reopened, or reconciled;
- whether full-system Win/Loss is currently permitted to be claimed.

If the agent cannot answer these from the repository, context loading is incomplete and work must not proceed.

## Memory model

Use these files for different kinds of project memory:

- `docs/PHASE1_CURRENT_OBJECTIVE_2026-09-14.md` = current owner-directed Phase 1 scope authority. Phase 1 is the bounded project stage; 07:00 Asia/Bangkok is a checkpoint inside it, not the method name or a run-distance label.
- `docs/DOCUMENT_SCOPE_AUDIT_2026-09-14.md` = document-age/scope reconciliation preventing older broad roadmaps from silently re-expanding current scope.
- `research_findings/FINDINGS.json` = non-canonical anti-forgetting index for observations, relation identity, contradictions, and reconciliations. Search it before reopening a materially similar relationship; it never overrides the canonical claim register.
- `docs/PHASE1_READINESS_MATRIX.json` = machine-readable Phase 1 readiness map separating research-core readiness from multi-year, economic-proof, and pilot blockers.
- `docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md` = owner-direct definition of what the 07:00 system is, what success means, how unknown states are handled, and how real versus synthetic data may be used.

- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json` = what the project currently knows/accepts. WO-055 governance metadata in this existing store protects legacy claim fingerprints and explicit authority transitions.
- `docs/WO055_MINIMAL_GOVERNANCE_SCHEMA_FREEZE_2026-09-14.md` = prospective contract for RQ admission, EXCLUSIVE/COMPOSITE claim authority, separated validation dimensions, and derived authority reporting. Read it before admitting a decision-critical RQ or changing canonical claim authority.
- `docs/SOURCE_COVERAGE_LEDGER.json` = which source windows/checks have already been reviewed, what they established, and when they may be reopened.
- `docs/STATE_AUTHORITY_CONTRACT_2026-09-13.md` = scope contract separating project-current workflow state, workstream-current state, and historical snapshots.
- `docs/CURRENT_RESEARCH_STATE.json` = project-current workflow state: where the project is now and what should happen next.
- active workstream dashboard = scoped authority for that workstream only; it may preserve an older lane checkpoint than the project-current checkpoint and must not override `CURRENT_RESEARCH_STATE`/`QUEUE` for global workflow status.
- `research_queue/QUEUE.json` = which research worksheet is operationally active. After WO-055, any non-null decision-critical active RQ must also have a valid admission record in this same Queue store.
- `results/governance/research_authority.json` = optional generated/derived authority view. It is reproducible and disposable; it is not project memory or an authority mutation source.
- RQ/checkpoint documents = detailed evidence chronology and reasoning trail.
- `TOOLS.md` = reusable tools and evidence-access paths.

Do not merge these responsibilities into one giant document. The active workstream dashboard exists to prevent a zero-context agent from missing recent work that has not yet been reflected elsewhere.

## Core anti-forgetting rule

`UNRESOLVED`, `INCONCLUSIVE`, `NOT_SUPPORTED`, and `NOT_TESTABLE` are durable knowledge states.

Before reopening a materially similar relation or experiment, check `research_findings/FINDINGS.json` as well as canonical/current state. Do not repeat an identical source check or experiment just because the prior result was not positive. Reopen only for a documented reason such as new primary evidence, clearer synchronized audio/visual evidence, a direct clarification, a contradiction, or a discovered source-mapping error.

## Core anti-invention rule

Never fill an unresolved rule from outcome performance or convenience. In particular, do not invent or backfit:

- thresholds or equality tolerances;
- candidate priority;
- PAT denominator/arithmetic;
- SL/TP geometry;
- cross-timeframe alignment tolerance;
- reference-selection formulas;
- touch/expiry rules;
- system win rate.

If the source does not establish it, keep it unresolved.

## Checkpoint invariant

A coherent project checkpoint is not complete until the intended durable files are updated, structured files validate, `git diff --check` passes, unintended media/secrets/temp files are excluded, and the checkpoint is committed/pushed to the existing branch when available.

## Current-state warning

State documents have different scopes. Never infer a contradiction solely because a dated historical checkpoint names an old active RQ. First classify the source as `PROJECT_CURRENT`, `WORKSTREAM_CURRENT`, or `HISTORICAL_SNAPSHOT` using `docs/STATE_AUTHORITY_CONTRACT_2026-09-13.md`. A real drift exists when project-current pointers disagree with each other.

This bootstrap intentionally does not hardcode the active RQ, latest commit, or open blockers. Those change over time. Read the machine-readable current state and queue every session.
