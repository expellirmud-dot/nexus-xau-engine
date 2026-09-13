# NEXUS XAU Engine — Agent Operating Instructions

Scope: this file applies to the entire repository.

This repository is a durable evidence-first research record. Agents must preserve research history, provenance, unresolved questions, and checkpoint continuity. Do not treat each session as a fresh start.

## 1. Session bootstrap: compact first, deep only when needed

### Tier 0 — reconnect / resume / status

On every reconnect, new chat, refresh, or Bridge recovery, **do not bulk-load project documents first**.

Run the global continuity capsule:

`py -3 D:\tools\nexus-project-continuity\continuity.py resume --project xau`

or:

`D:\tools\NEXUS-START\RESUME_WORK.cmd --project xau`

The Tier-0 capsule is the default reconnect entry point. It should be enough to recover:

- repo / branch / head / dirty state;
- current workstream and active RQ;
- latest checkpoint and current frozen version;
- next action;
- global NEXUS capabilities already available;
- live durable-job state versus the Project pointer.

If the capsule reports `STALE_PROJECT_POINTER`, reconcile the live machine job/result **before retrying or loading broad context**.

Tier 0 is sufficient for:

- checking whether a durable job is still running or already done;
- resuming an already-frozen deterministic machine task;
- locating the exact checkpoint/output that should be inspected next;
- answering simple status questions.

### Tier 1 — substantive research / semantic change

Only enter the deep bootstrap when the next action requires changing or interpreting research meaning, for example:

- designing or changing a rule/representation;
- opening/reopening source research;
- changing research code semantics;
- interpreting outcomes into a research conclusion;
- modifying canonical claims;
- creating a new version or experiment;
- reconciling contradictory evidence.

Then use the zero-context evidence path:

1. `PROJECT_BOOTSTRAP.md`
2. `docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md`
3. `skills/nexus-xau-research/SKILL.md`
4. run `.venv\Scripts\python.exe scripts\research_preflight.py` and require `NEXUS_RESEARCH_PREFLIGHT=PASS`;
5. read only the Current State / Workstream / Claim / Coverage / Queue pointers that are material to the active question;
6. load the specific supporting checkpoint/source documents reached through those pointers.

Do **not** read the entire `docs/` tree on every session.

Before substantive work, the agent must still be able to answer:

- What is the governing 07:00 project objective and what does PASS mean?
- What is the active workstream/question/version?
- What is already source-backed?
- What remains unresolved?
- What was superseded or narrowed?
- What source/test has already been done?
- What claim is currently prohibited?

If the compact capsule cannot answer enough to locate the correct evidence, escalate to Tier 1 rather than guessing.

## 2. Current authority hierarchy

Use the following authority order when documents disagree:

1. direct user clarification / owner-confirmed project rule;
2. current ACTIVE entries in `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`;
3. latest source-backed reconciliation/closure checkpoint;
4. active research worksheet;
5. older historical research documents;
6. analyst inference.

Historical documents are evidence chronology, not automatically current truth.

Never erase old findings merely because newer evidence narrows or supersedes them. Preserve the old checkpoint and add an explicit reconciliation/supersession trail.

## 3. Knowledge-state rule: do not re-research from zero

Before re-opening a video, transcript, timestamp window, formula, or historical test:

1. check `CURRENT_RESEARCH_STATE` and the active workstream dashboard;
2. check the current workstream philosophy/success-criteria document when one exists;
3. check the canonical claim register;
4. check the active RQ worksheet and its checkpoint references;
5. check `SOURCE_COVERAGE_LEDGER`.

If a question/window is already source-closed, reuse that finding unless a valid reopen trigger exists.

Valid reopen triggers include:

- new primary/source evidence;
- clearer synchronized audio/visual evidence that resolves a material ambiguity;
- direct user/instructor clarification;
- a genuine contradiction with the current canonical claim;
- discovery that the prior source mapping/timestamp was wrong.

A result of `UNRESOLVED`, `INCONCLUSIVE`, or `NOT_TESTABLE` is still knowledge. Do not repeat the identical check merely because it did not produce a positive answer.

## 4. Evidence discipline

Always separate:

- Source Fact
- User-direct rule
- Management/instructor/source statement
- Visual Observation
- Derived Calculation
- Research Representation
- Analyst Assumption
- Outcome Observation

Do not use favorable backtest outcomes to manufacture or select a teaching rule.

Do not invent:

- thresholds;
- equality tolerances;
- candidate priority;
- PAT denominator/arithmetic;
- SL/TP geometry;
- Win/Loss or win rate;
- expiry/touch-count rules;
- cross-timeframe alignment tolerance;
- reference-selection formulas.

If source evidence does not establish a value or rule, keep it explicitly unresolved.

Examples are not universal laws unless the source establishes universality.

YouTube Show transcript is primary attributable source material with ASR risk. Material ambiguity in numbers, candle terminology, timeframe, equality, wick/body/close, or strict-vs-approximate wording requires visual/audio cross-check where available.

## 5. Research method

Default order:

`PRIMARY SOURCE -> TIMESTAMP MAP -> SYNCHRONIZED VISUAL -> AUDIO CROSS-CHECK IF NEEDED -> SOURCE CLOSURE/UNKNOWN -> TARGETED COMPUTATION ONLY IF STILL NECESSARY`

Do not run broad historical searches when direct source review can answer the question.

When computation is necessary:

- freeze the question and representation before looking at outcomes;
- preserve DEV/VAL/TEST contamination history;
- do not retune a failed frozen rule on its confirmation period;
- require a pristine holdout before future full-system claims.

Full-system Win/Loss is currently not established unless the canonical state explicitly changes.

## 6. Active research queue

`research_queue/QUEUE.json` is the operational source of truth for which research worksheet is active.

Do not assume the active RQ number from memory.

After each coherent closure:

1. update the closure/checkpoint document;
2. update the canonical claim register if current authority changed;
3. update `CURRENT_RESEARCH_STATE.json` and the active workstream dashboard when workstream state changed;
4. update `research_queue/QUEUE.json` and the active worksheet;
5. update `SOURCE_COVERAGE_LEDGER` whenever the source coverage changed;
6. validate structured files;
7. commit and push the coherent checkpoint.

Do not delete prior RQ/checkpoint history.

## 7. Tooling and source media

Read `TOOLS.md` before creating a new tool.

Reuse before building.

Current important tooling includes:

- Desktop Commander is the primary local filesystem plane for bulk read/write/search/edit and ordinary local commands/processes;
- if Desktop Commander is unavailable in the current session, fall back to IE Coder Connect before declaring a local-access blocker;
- a Desktop Commander remote device/workspace OFFLINE state is not proof that the local repository is unavailable; probe actual local tool availability first;
- `agent-browser` for browser/YouTube transcript, metadata, timestamps, and headed CDP visual evidence;
- `D:\tools\nexus-video-evidence` for local video/frame evidence;
- IE Coder image bridge for agent vision over local images.

Local source media under `youtube/` is research evidence and is gitignored. Do not commit MP4/video/screenshots/media unless the owner explicitly changes policy.

Never display, copy, or commit credentials/secrets from local files.


## 8. Long-task durability / UI-timeout invariant

Before starting or resuming any local long-running/urgent work, query the global NEXUS work supervisor first:

`py -3 D:\tools\nexus-durable-work\supervisor.py resume`

If it returns an ACTIVE/IN_PROGRESS/BLOCKED/WAITING job for this repository, resume from its checkpoint/state/result references before starting any new duplicate work.
The supervisor registry is the cross-session execution source of truth; the repository remains the research/evidence source of truth.

Also query the machine-side executor before re-running Terminal work:

`py -3 D:\tools\nexus-durable-work\local_work_agent.py status`

If an agent job is already RUNNING or DONE, inspect/reuse it instead of submitting a duplicate. Long deterministic/resumable commands should be handed to the Local Work Agent so they can outlive the ChatGPT/Terminal request.

For high-count, long-running, or expensive-to-repeat work, conversation context is not a valid progress store.

Read and follow `docs/LONG_TASK_RESUME_PROTOCOL_2026-09-12.md`.
Use the registered `D:\tools\nexus-durable-work` utility and persist item-level progress/result references on disk.

A browser/UI/connector timeout must not make a new session restart completed work. Resume an existing `IN_PROGRESS` item first, then the next `PENDING` item. Preserve `DONE` unless a documented reopen trigger exists.

For local processes that may outlive the connection, preserve Bridge `jobId` / idempotency identifiers and query existing job state before retrying.

Materially ambiguous STT must be marked `AMBIGUOUS`, never silently guessed or normalized into a trading/system rule. Cross-check original audio/visual or ask the owner before evidence promotion.

## 9. Terminal and Git safety

Before any terminal action through the IE Coder bridge, inspect `bridge_capabilities` and the current `activeTerminalMode`.

Only the local user can change terminal mode. Never claim to change it remotely.

Routine non-destructive Git status/stage/commit/push is authorized after a coherent validated checkpoint on the existing branch/remote.

Destructive history changes require explicit owner approval.

Before commit:

- validate JSON/structured files;
- run `git diff --check`;
- inspect staged files;
- confirm `youtube/` media is not staged;
- confirm temporary research scripts are not accidentally staged;
- preserve chronology/provenance.

## 10. Required reasoning posture

Prefer evidence over confidence.

If evidence is insufficient, state `ยังสรุปไม่ได้` / `UNRESOLVED` rather than filling the gap.

A negative or inconclusive research result is valid project knowledge and must be preserved.

The project objective is quality of sequential decisions under uncertainty, not merely profit/loss optimization.

## 11. Restart invariant

A new agent/session must continue from the repository state, not from conversational memory alone.

Minimum restart invariant:

`AGENTS.md -> PROJECT_BOOTSTRAP.md -> 07:00 Project Objective/Decision Doctrine -> nexus-xau-research SKILL -> preflight PASS -> Maintenance Policy -> TOOLS -> Current State -> Active Workstream Dashboard -> Canonical Claims -> Source Coverage -> Queue -> Active RQ -> Latest Checkpoint`

Only after this chain is loaded should new research begin.
