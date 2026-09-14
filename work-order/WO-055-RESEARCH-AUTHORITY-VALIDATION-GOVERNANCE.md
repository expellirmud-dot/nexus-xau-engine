# WO-055 — Research Authority and Validation Governance Hardening

STATUS: PLAN_COMPLETE_NOT_IMPLEMENTED
TYPE: CROSS_PROJECT_GOVERNANCE_HARDENING
DATE: 2026-09-14
REPOSITORY: `D:\nexus-xau-engine-repo`
OWNER_SOURCE: Owner-provided governance design/PDF, 2026-09-14
ACTIVATION: EXPLICIT_OWNER_OR_CONTROLLER_CHECKPOINT

## 1. Purpose

Harden the existing NEXUS XAU evidence-first research control plane so current research truth, Research Question admission, validation meaning, canonical claims, and authority transitions become machine-checkable without creating a second project-state framework.

This Work Order is a **delta on top of the existing XAU governance system**. It must reuse the repository's current authority stores and preflight rather than replacing them.

Primary outcome:

`Evidence -> RQ -> Validation -> Canonical Claim -> Authority -> Current State`

must have one deterministic, inspectable path, with contradictions failing closed and historical evidence unable to regain current authority accidentally.

## 2. Non-goals

- Do not change trading/research semantics.
- Do not change 07:00 decision logic.
- Do not open or score holdout outcomes.
- Do not activate RQ-014 or any new decision-critical RQ.
- Do not re-research source material.
- Do not create a second continuity/state engine.
- Do not rewrite historical checkpoints to fit the new governance model.
## 3. Verified existing baseline

Repository inspection on 2026-09-14 established the following existing controls:

- `scripts/research_preflight.py` already validates project-current state agreement and returns `NEXUS_RESEARCH_PREFLIGHT=PASS` on the current repository.
- `docs/STATE_AUTHORITY_CONTRACT_2026-09-13.md` already separates `PROJECT_CURRENT`, `WORKSTREAM_CURRENT`, `HISTORICAL_SNAPSHOT`, and `KNOWLEDGE_AUTHORITY` scopes.
- `docs/CURRENT_RESEARCH_STATE.json` is the project-current workflow state.
- `research_queue/QUEUE.json` is the operational active-RQ/worksheet authority.
- `docs/0700_WORKSTREAM_STATE.json` is the 07:00 lane-local state and must not override project-current state.
- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json` is the machine-readable current claim index.
- `docs/SOURCE_COVERAGE_LEDGER.json` preserves durable source-review coverage and reopen triggers.
- `tests/test_research_preflight_state_drift.py` already freezes several state-drift failures.
- skill freeze integrity is already checked by preflight.

Current repository state at preflight:

- active decision-critical RQ: none;
- last closed RQ: `RQ-012`;
- holdout identity: reserved;
- holdout outcomes: unopened / unscored;
- outcome scoring: disabled;
- canonical claim register: 45 active claims / 45 total;
- source coverage ledger: 28 entries.

Therefore WO-055 must extend these controls, not duplicate them.## 4. Gap statement

The existing system is strong on workflow-state drift and provenance, but the inspected implementation does not yet expose all governance concepts from the Owner design as explicit machine-checkable contracts.

### Gap G1 — RQ admission is not globally schema-enforced

RQ records contain useful fields such as type, status, dependencies, preferred method, and closure references, but there is no single machine gate requiring every newly admitted decision-critical RQ to answer all four questions:

1. What is new?
2. What exactly are we testing?
3. What would falsify or materially weaken the hypothesis?
4. What project decision/state is allowed to change after the result?

### Gap G2 — Canonical claim authority mode is implicit

The claim register contains stable `claim_id`, status, source references, engine permission, risk flags, and some supersession metadata. The inspected structure does not expose a general `authority_mode` contract equivalent to `EXCLUSIVE` versus `COMPOSITE` ownership.

### Gap G3 — Validation dimensions are distributed

Source support, representation status, implementation proof, historical evidence, replication, controls, and holdout state exist in the project, but they are distributed across status strings, risk flags, checkpoints, tests, and holdout tooling rather than represented by one normalized validation contract.

### Gap G4 — Authority reporting is not a normalized generated view

Preflight summarizes current state well, but there is no dedicated generated authority report that resolves claim -> current authority -> validation dimensions -> unresolved conflicts without becoming a new source of truth.## 5. Design principles

1. **Extend, do not replace.** Keep `CURRENT_RESEARCH_STATE`, `QUEUE`, workstream state, claim register, source coverage ledger, and existing preflight as canonical stores.
2. **Fail closed.** Missing authority, unresolved conflict, malformed lifecycle, or incomplete admission must block promotion rather than being guessed.
3. **History is immutable evidence.** Historical checkpoints remain chronology and are never rewritten merely to satisfy a new schema.
4. **Unknown is first-class.** `UNKNOWN`, `INCONCLUSIVE`, `UNRESOLVED`, and `NOT_APPLICABLE` are valid states.
5. **Outcome isolation.** Governance changes must not inspect or use reserved holdout outcomes.
6. **No semantic contamination.** This work must not select trading rules, thresholds, or variants from outcome performance.
7. **Generated reports are views.** Editing a report never changes authority.
8. **Smallest sufficient implementation.** Prefer extensions to `research_preflight.py` and existing stores before adding new frameworks.

## 6. Canonical State Invariant extension

Retain all current state-drift checks and add generic invariants only where the existing preflight lacks coverage.

Required additional invariant families:

- duplicate canonical `claim_id` detection;
- missing claim source/authority reference detection;
- invalid claim lifecycle/supersession detection;
- active claim that is simultaneously marked superseded;
- supersession cycles;
- authority-cardinality violation;
- malformed RQ admission record;
- generated authority view mismatch against canonical stores.

Every invariant must have a stable machine-readable reason code and a deterministic regression fixture.## 7. RQ Admission Gate

Add a reusable validator for a candidate RQ before it can become the active decision-critical worksheet.

Minimum normalized admission payload:

- `rq_id`;
- `rq_type`;
- `newness_statement`;
- `question`;
- `boundary` / what is explicitly outside the test;
- `expected_evidence`;
- `falsification_condition`;
- `decision_consequence` for positive / negative / unresolved result;
- `dependencies`;
- `stop_condition`;
- `holdout_or_leakage_guard` when outcomes are involved.

Admission result:

- `ADMISSIBLE`;
- `BLOCKED_INCOMPLETE`;
- `BLOCKED_DUPLICATE_OR_ALREADY_CLOSED`;
- `BLOCKED_AUTHORITY_CONFLICT`;
- `BLOCKED_EVIDENCE_OR_HOLDOUT_GUARD`.

An RQ record existing on disk is not sufficient for activation. Activation must also satisfy the current `ONE_DECISION_CRITICAL_ACTIVE_WORKSHEET` queue policy.

Historical RQs are not required to be rewritten. The validator applies prospectively; legacy records may be adapted only when needed for a focused regression fixture.## 8. Authority Map and Canonical Claim contract

Keep `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json` as the current claim store. Do not create a competing claim database.

Extend claim governance only as needed to express:

- stable claim key (`claim_id` remains the default key);
- normalized claim statement;
- lifecycle status;
- authority mode;
- current authority reference(s);
- supersedes / superseded-by links where relevant;
- source/evidence references;
- validation references;
- unresolved/risk flags.

Authority modes:

- `EXCLUSIVE`: exactly one current authority controls the claim.
- `COMPOSITE`: more than one explicitly compatible authority jointly defines the current claim.

For `EXCLUSIVE`, promotion of a replacement must close/supersede the prior current authority in the same coherent checkpoint.

For `COMPOSITE`, every member must be explicitly named; coexistence may not be inferred merely because multiple documents mention the claim.

Do not backfill speculative authority metadata into historical documents. The current register owns current authority; historical documents remain references.## 9. Validation contract

Introduce a normalized validation object that separates **dimension**, **outcome**, and **evidence reference**.

Required dimensions:

- `SOURCE_VALIDATION` — source/user evidence supports the represented claim.
- `REPRESENTATION_VALIDATION` — the project representation faithfully encodes the supported claim and preserves unresolved boundaries.
- `IMPLEMENTATION_VALIDATION` — code/system behavior implements the frozen representation.
- `HISTORICAL_EVIDENCE` — chronology retained for context but not current promotion authority.
- `REPLICATION` — independent/repeated execution reproduces the intended result.
- `CONTROL` — baseline/control evidence used to interpret the test.
- `HOLDOUT` — outcome evidence intentionally isolated from design/tuning.

Required outcomes must include at least:

- `PASS`;
- `FAIL`;
- `MIXED`;
- `UNKNOWN`;
- `NOT_APPLICABLE`.

A PASS in one dimension must never imply PASS in another.

Examples:

- source-backed wording may have `SOURCE_VALIDATION=PASS` while implementation remains `UNKNOWN`;
- an implementation test may PASS while source authority remains unresolved;
- historical backtest evidence must not silently become current holdout or source validation.## 10. Generated Authority Report

Add one read-only generated report path that derives its output from current canonical stores.

Minimum report columns/fields:

- claim ID;
- canonical statement hash/summary;
- lifecycle status;
- authority mode;
- current authority reference(s);
- engine permission;
- validation dimension summary;
- source references;
- risk/unresolved flags;
- supersession state;
- conflict status.

Requirements:

- deterministic ordering;
- stable machine-readable JSON output;
- optional human-readable Markdown/text rendering;
- generated output must be reproducible from source records;
- generated output must never be read as the mutation source for authority state.

Prefer a small reporting script over a new service/process.

Candidate command name:

`scripts/report_research_authority.py`

Exact filename may change during implementation if an existing script is a better reuse seam.## 11. Minimal implementation surfaces

Implementation is expected to touch the smallest feasible subset of:

- `scripts/research_preflight.py` — extend generic governance validation;
- `tests/test_research_preflight_state_drift.py` — preserve and extend invariant coverage;
- one focused governance module under `src/nexus_xau/` only if preflight would otherwise become monolithic;
- focused governance tests;
- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json` only for a minimal current-schema extension;
- `research_queue/QUEUE.json` only when prospective RQ admission metadata is actually needed;
- an optional new machine-readable validation/authority sidecar only if extending the existing claim register would create an ambiguous or lossy schema;
- one generated-report script.

Do **not** create:

- a second `CURRENT_RESEARCH_STATE`;
- a second queue;
- a second claim register;
- a second source coverage ledger;
- a second continuity engine;
- a parallel status/roadmap document family.

If the existing stores can express the contract cleanly, prefer schema extension over new files.## 12. Known-failure regression matrix

Freeze governance failures before implementation changes are considered complete.

Minimum required regression cases:

1. project-current queue/state drift;
2. workstream project-pointer drift;
3. reserved holdout identity drift;
4. holdout scoring enabled while reserved/unscored;
5. stale implementation instruction after closure;
6. duplicate canonical claim ID;
7. missing canonical authority/source reference;
8. active claim also marked superseded;
9. supersession cycle;
10. duplicate current authority for an `EXCLUSIVE` claim;
11. valid explicit `COMPOSITE` authority;
12. RQ missing newness statement;
13. RQ missing bounded question/test boundary;
14. RQ missing falsification condition;
15. RQ missing decision consequence;
16. outcome-bearing RQ missing holdout/leakage guard;
17. validation dimensions collapsed into one generic PASS;
18. historical evidence incorrectly treated as current authority;
19. holdout evidence incorrectly treated as design/tuning evidence;
20. generated authority report diverges from canonical stores.

Existing passing state-drift tests must remain green throughout.

## 13. Implementation order

Implementation must proceed in this dependency order:

### Phase A — Freeze schemas and fixtures

- define the minimal admission/authority/validation fields;
- create known-failure fixtures first;
- confirm existing repository current state still preflights PASS.

### Phase B — Extend preflight invariants

- add generic claim/RQ/authority validation;
- preserve all current RQ-012 holdout checks;
- return stable reason codes.

### Phase C — Add prospective RQ admission

- validate candidate RQ records before activation;
- integrate with the existing queue policy;
- do not rewrite closed historical RQs.

### Phase D — Add authority/validation normalization

- minimally extend current claim records or a sidecar where justified;
- enforce EXCLUSIVE/COMPOSITE cardinality and supersession rules;
- keep UNKNOWN/NOT_APPLICABLE explicit.

### Phase E — Add generated report

- generate JSON first;
- optional human-readable rendering second;
- prove it is derived-only and reproducible.

### Phase F — Reconcile documentation

Only after code/tests prove the behavior:

- update `STATE_AUTHORITY_CONTRACT` if its contract boundary materially expands;
- update `PROJECT_BOOTSTRAP.md`/`AGENTS.md` only if bootstrap behavior changes;
- update maintenance/research skill only if operator procedure changes;
- preserve historical documents unchanged except for explicit forward references where necessary.

## 14. Holdout and active-research safety lock

WO-055 is governance work and must not contaminate the currently reserved V0.1 holdout.

During this Work Order:

- holdout outcomes remain unopened;
- outcome scoring remains disabled unless a separate authorized research action changes that state;
- holdout identity/freeze commits remain unchanged;
- no engine eligibility/target/horizon/tick semantics change;
- no current research rule is promoted because of WO-055;
- `RQ-014` remains queued and is not activated by this work;
- no new decision-critical RQ is made active solely to implement governance tooling.

If implementation requires fixture data, use synthetic governance fixtures or already-visible metadata only.

## 15. Validation gate

Before WO-055 can be declared implemented, all required validation must actually execute.

Required gate:

1. repository `research_preflight.py` returns PASS on the real current state;
2. all existing state-drift tests remain green;
3. every new known-failure fixture fails with its intended stable reason code;
4. valid admission fixture returns `ADMISSIBLE`;
5. incomplete/non-falsifiable admission fixtures fail closed;
6. EXCLUSIVE authority rejects multiple current controllers;
7. explicit compatible COMPOSITE authority passes;
8. supersession cycle and active-superseded contradictions fail;
9. validation dimensions round-trip without semantic loss;
10. generated authority report is deterministic and reproducible;
11. generated report can be deleted/regenerated without changing current authority;
12. structured files parse successfully;
13. relevant focused tests pass;
14. full applicable test suite passes;
15. Ruff/lint applicable to changed Python passes;
16. `git diff --check` passes;
17. holdout activation/scoring state is unchanged;
18. no source/media/outcome contamination occurred.

Validation evidence must be recorded only after execution. The Work Order itself is not proof.

## 16. Terminal condition

WO-055 is complete only when:

- current XAU state authority remains single and restart-safe;
- new decision-critical RQs cannot activate without the admission contract;
- canonical claims have explicit enforceable authority behavior where needed;
- source/representation/implementation/historical/replication/control/holdout validation meanings cannot silently collapse into one status;
- contradictory authority fails closed;
- generated authority reporting is derived and reproducible;
- existing research and holdout semantics remain unchanged;
- all validation in Section 15 is green.

## 17. Stop / rollback conditions

Stop implementation and report the blocker if:

- migration would require rewriting historical research evidence;
- the new model duplicates an existing canonical store instead of extending it;
- current preflight becomes weaker or starts ignoring an existing drift condition;
- holdout identity/scoring semantics would need to change;
- a schema decision would force unresolved research knowledge into a false binary state;
- implementation scope expands into trading-engine semantics.

Rollback must be possible by reverting only the WO-055 governance code/schema changes while leaving research history and evidence intact.

## 18. Delivery and repository discipline

- Preserve all unrelated dirty changes.
- Do not reset/stash/discard owner work.
- Do not add local media, datasets, caches, `.pytest-*`, `.venv`, secrets, or credentials.
- Use one coherent checkpoint if/when implementation is later completed.
- Commit/push are not part of this planning-file move and require the applicable controller/user authorization at execution time.

## 19. Current planning status

Planning file is complete.

Implementation status: `NOT_STARTED`.
Repository preflight observed during planning: `PASS`.
Serena / CodeGraph: `NOT_REQUIRED` for this documentation-only move/refinement.

Next bounded action if activated: freeze the minimal admission/authority/validation schema and RED governance fixtures before modifying current canonical stores.