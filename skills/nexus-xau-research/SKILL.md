# Skill: NEXUS XAU Evidence-First Research

Use this skill for source review, rule decoding, formula verification, replay research, hypothesis testing, checkpoint reconciliation, and any work that may change the project’s current understanding of the trading framework.

## Goal

Convert source material and bounded computation into durable, restart-safe project knowledge without inventing missing rules or repeating already-closed work.

## Inputs

At least one of:

- an active research question from `research_queue/QUEUE.json`;
- a new primary source/video/transcript/image;
- a contradiction against a current canonical claim;
- a bounded measurable hypothesis;
- a request to resume project research.

## Phase 0 — Bootstrap gate

Before doing substantive work:

1. read `AGENTS.md`;
2. read `PROJECT_BOOTSTRAP.md`;
3. read `docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md`;
4. run `.venv\Scripts\python.exe scripts\research_preflight.py`;
5. read the active/current files identified by preflight, including the active workstream dashboard and current workstream philosophy/success criteria;
6. state what the workstream already knows, what was superseded, and what must not be repeated;
7. inspect `docs/SOURCE_COVERAGE_LEDGER.json` for the source/topic/window being considered.

For 07:00 work, preserve the owner-direct doctrine that unresolved/novel states may terminate as PASS / NO TRADE / STUDY rather than being forced into a known rule.

Do not continue if preflight fails or if the active workstream/question cannot be reconstructed from repository state. A stale central state is itself a blocker; do not compensate by broad source searching.

## Phase 1 — Duplicate/coverage check

For the intended source or experiment, classify prior coverage as one of:

- `UNSEEN`
- `SCREENED`
- `REVIEWED`
- `SOURCE_CLOSED`
- `SOURCE_CLOSED_WITH_RESIDUAL_OPEN`
- `REVIEWED_UNRESOLVED`
- `REOPENED`
- `SUPERSEDED`

If already closed, reuse the finding unless a valid reopen trigger exists.

Valid reopen triggers:

- new primary evidence;
- clearer synchronized visual/audio evidence;
- direct owner/instructor clarification;
- contradiction with current canonical state;
- source/timestamp mapping error;
- a new question that the prior review did not actually test.

Do not reopen merely because the prior answer was `UNRESOLVED` or `INCONCLUSIVE`.

## Phase 2 — Freeze the question

Write the exact question before reviewing outcomes or selecting numeric variants.

For source questions, identify:

- source ID;
- topic;
- timestamp/window;
- expected evidence modality: transcript / visual / audio / user-direct;
- what would count as closure;
- what must remain unresolved if not directly evidenced.

For computational questions, additionally freeze:

- representation;
- comparison/control;
- dataset split;
- decision rule;
- leakage/holdout guard.

## Phase 3 — Evidence collection order

Default order:

`PRIMARY SOURCE -> TIMESTAMP MAP -> SYNCHRONIZED VISUAL -> AUDIO CROSS-CHECK IF MATERIAL -> SOURCE CLOSURE/UNKNOWN -> TARGETED COMPUTATION ONLY IF STILL NEEDED`

Use the smallest sufficient tool.

Preferred source tooling is registered in `TOOLS.md`.

Do not run broad backtests to answer a question that a direct source can close.

## Phase 4 — Evidence classification

Every material statement must be classified internally as one of:

- `SOURCE_FACT`
- `USER_DIRECT_RULE`
- `SOURCE_STATEMENT_OR_GUIDANCE`
- `VISUAL_OBSERVATION`
- `DERIVED_CALCULATION`
- `RESEARCH_REPRESENTATION`
- `ANALYST_ASSUMPTION`
- `OUTCOME_OBSERVATION`

Do not promote one class into another without evidence.

Examples:

- a pixel measurement is a derived calculation, not instructor wording;
- a strong backtest result is an outcome observation, not source proof;
- a source example is not automatically a universal rule;
- YouTube ASR transcript is attributable primary-source text with ASR risk, not guaranteed verbatim audio.

## Phase 5 — Decision states

Use explicit terminal/intermediate states rather than vague confidence:

- `SUPPORTED`
- `OPPOSED`
- `MIXED`
- `INCONCLUSIVE`
- `INSUFFICIENT`
- `NOT_TESTABLE_WITH_CURRENT_EVIDENCE`
- `SOURCE_CLOSED`
- `SOURCE_CLOSED_WITH_RESIDUAL_OPEN`
- `REVIEWED_UNRESOLVED`

An unresolved result is a valid result and must be persisted.

## Phase 6 — Canonical decision

Before changing canonical state, ask:

1. Is the claim directly supported by current source/user evidence?
2. Is it universal, or only demonstrated for a shown setup family?
3. Does new evidence narrow or contradict an older claim?
4. Are equality/tolerance/priority/geometry details still missing?
5. Would the proposed rule exist if no outcome data had been seen?

If an older finding changes, preserve chronology and create explicit reconciliation/supersession. Never silently rewrite history.

## Phase 7 — Persistence checklist

For each coherent research closure, update only the durable stores that actually changed:

- closure/checkpoint document;
- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json` if current authority changed;
- `docs/CURRENT_RESEARCH_STATE.json` if project state/next step changed;
- the active workstream dashboard if workstream authority, supersession, gaps, or next action changed;
- `research_queue/QUEUE.json` and active worksheet if operational research state changed;
- `docs/SOURCE_COVERAGE_LEDGER.json` whenever a source/topic/window was screened, reviewed, closed, reopened, or found unresolved.

Coverage ledger entries should record:

- source ID/title;
- exact timestamp/window where possible;
- topic;
- reviewed modalities;
- finding summary;
- residual unknowns;
- checkpoint/canonical references;
- reopen triggers;
- review date/status.

Do not store raw media in Git unless project policy explicitly changes.

## Phase 8 — Validation and checkpoint

Before committing:

1. validate JSON/structured files;
2. run relevant tests/lint when code changed;
3. run `git diff --check`;
4. inspect staged files;
5. verify `youtube/` media is not staged;
6. verify temporary scripts are not staged;
7. verify secrets/credentials are not exposed;
8. commit one coherent checkpoint;
9. push to the existing configured branch/remote;
10. verify clean/synchronized status when possible.

## Hard stop rules

Stop and mark unresolved rather than inventing when any of these occur:

- source cannot distinguish two candidate definitions;
- exact equality/tolerance is not stated;
- multiple candidate structures exist without source priority;
- ASR ambiguity could change a numeric or structural rule and no visual/audio cross-check is available;
- a shown example does not establish universality;
- a rule would be selected because it backtests better;
- a full-system trade tuple is incomplete;
- a pristine holdout does not exist for a newly frozen full-system version.

## Full-system guard

Do not report canonical system Win/Loss, win rate, loss rate, or expectancy unless the canonical/current state explicitly says the full trade construction is testable and a suitable untouched holdout exists.

## Output style for project decisions

Prefer this order:

1. finding;
2. evidence;
3. what changed from prior state;
4. counterargument/risk;
5. what remains unknown;
6. next action;
7. checkpoint/commit status.

When evidence is insufficient, state `ยังสรุปไม่ได้` / `UNRESOLVED` clearly.
