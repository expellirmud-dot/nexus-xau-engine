# NEXUS XAU Engine — Zero-Context Project Bootstrap

Purpose: this is the shortest safe entry path for an AI/agent that knows nothing about prior chats or project history.

Do not begin research, coding, backtesting, source review, or rule interpretation from conversational memory alone.

## Mandatory entry sequence

1. Read `AGENTS.md`.
2. Read `docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md`.
3. Read `skills/nexus-xau-research/SKILL.md`.
4. Run the repository preflight:

   `.venv\Scripts\python.exe scripts\research_preflight.py`

5. Read the files reported by preflight, at minimum:
   - `docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md`
   - `TOOLS.md`
   - `docs/CURRENT_RESEARCH_STATE.json`
   - the active workstream dashboard referenced by current state; currently `docs/0700_WORKSTREAM_STATE.json`
   - `docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md` for current 07:00 purpose/success criteria
   - `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`
   - `docs/SOURCE_COVERAGE_LEDGER.json`
   - `research_queue/QUEUE.json`
   - the active worksheet referenced by `research_queue/QUEUE.json -> active.worksheet`
   - the latest checkpoint referenced by the active queue/current-state checkpoint fields
6. Read any additional current checkpoint/source files named by `docs/CURRENT_RESEARCH_STATE.json -> research_loop.load_order` when they are material to the active question.

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

- `docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md` = owner-direct definition of what the 07:00 system is, what success means, how unknown states are handled, and how real versus synthetic data may be used.

- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json` = what the project currently knows/accepts.
- `docs/SOURCE_COVERAGE_LEDGER.json` = which source windows/checks have already been reviewed, what they established, and when they may be reopened.
- `docs/CURRENT_RESEARCH_STATE.json` = where the project is now and what should happen next.
- active workstream dashboard = compact current authority for the presently active research stream, including what is already closed, what was superseded, and what not to repeat.
- `research_queue/QUEUE.json` = which research worksheet is operationally active.
- RQ/checkpoint documents = detailed evidence chronology and reasoning trail.
- `TOOLS.md` = reusable tools and evidence-access paths.

Do not merge these responsibilities into one giant document. The active workstream dashboard exists to prevent a zero-context agent from missing recent work that has not yet been reflected elsewhere.

## Core anti-forgetting rule

`UNRESOLVED`, `INCONCLUSIVE`, `NOT_SUPPORTED`, and `NOT_TESTABLE` are durable knowledge states.

Do not repeat an identical source check or experiment just because the prior result was not positive. Reopen only for a documented reason such as new primary evidence, clearer synchronized audio/visual evidence, a direct clarification, a contradiction, or a discovered source-mapping error.

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

This bootstrap intentionally does not hardcode the active RQ, latest commit, or open blockers. Those change over time. Read the machine-readable current state and queue every session.
