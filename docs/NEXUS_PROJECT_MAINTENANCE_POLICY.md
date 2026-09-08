# NEXUS Project Maintenance Policy

Status: USER-DIRECT OPERATING AUTHORIZATION
Effective: 2026-09-03
Updated: 2026-09-08

## Ownership

Repository hygiene and restart-safe project maintenance are delegated to NEXUS for this project.

After a coherent research/engineering checkpoint is complete, NEXUS should normally perform the maintenance workflow without asking the user again:

1. persist source/evidence notes and checkpoint state;
2. preserve prior history and explicitly record corrections/supersessions;
3. run relevant tests/lint/validation;
4. inspect repository status and avoid committing secrets, credentials, caches, temporary files, or clearly unintended large artifacts;
5. create a descriptive Git commit for the completed checkpoint;
6. push the commit to the already-configured remote/branch when normal authentication/network access permits;
7. if commit or push cannot be completed, preserve all local work and record/report the concrete blocker.

## Local Bridge / GitHub execution policy

The project owner authorizes NEXUS to choose the faster or more suitable execution path for each step and to mix both paths when useful.

Default operating preference:

```text
local workspace through IE Coder / Bridge
-> inspect sources / files / media
-> edit / run / test / analyze locally
-> create coherent checkpoint
-> Git commit
-> push to configured GitHub remote
-> verify local/remote synchronization
```

This is a preference, not a restriction. GitHub-side inspection or other normal repository workflows may be used when they are faster or clearer for history, diffs, remote state, review, or cross-machine continuity.

The invariant is **synchronization**, not which path performed the work:

- do not assume local and remote are synchronized merely because a command succeeded earlier;
- after each coherent checkpoint, verify repository status and branch/upstream state;
- when push succeeds, prefer ending with a clean working tree and local branch aligned with its configured upstream;
- if intentional local-only artifacts exist, keep them explicitly ignored or documented rather than leaving ambiguous untracked files;
- if local and remote cannot be synchronized, preserve the local checkpoint and report the exact blocker instead of silently continuing as if sync succeeded;
- never trade evidence integrity for speed.

For NEXUS XAU research specifically, large local datasets, video sources, extracted evidence frames, and other local evidence assets remain local unless a project policy explicitly says otherwise. GitHub stores code, manifests, research state, evidence references, and checkpoint history rather than unnecessary large media copies.

## Standing authorization

Routine non-destructive repository maintenance does not require repeated confirmation from the project owner. This includes normal `git status`, staging intended project files, commit, and push to the existing configured remote/branch after validation.

## Actions that still require explicit approval

Do not infer authorization for destructive or history-rewriting operations. Ask before actions such as:

- force push;
- deleting branches/tags/remotes;
- `reset --hard` or destructive checkout/restore;
- rewriting/rebasing published history when it can affect collaborators;
- changing repository remote destinations or credentials;
- deleting historical evidence/checkpoints;
- committing secrets or private credentials.

## Commit discipline

Prefer one coherent commit per restart-safe checkpoint. Commit messages should describe the research/engineering closure rather than only listing files.

Examples:

- `research: close Mae Pla 07:00 time mapping`
- `engine: add evidence provenance guard`
- `research: add location interaction truth-set scaffold`

## Evidence discipline remains higher priority than repository convenience

A successful commit/push does not promote uncertain evidence to CONFIRMED. Evidence status, provenance, test status, and unresolved blockers must remain explicit in the repository.

## STT ambiguity handling

The project owner commonly uses speech-to-text (STT), and STT can mis-hear or distort spoken wording.

NEXUS must not silently normalize or guess a suspicious STT phrase when that ambiguity could materially change:

- a trading/system rule;
- a number, price, point distance, percentage or threshold;
- a time, date, timezone or timeframe;
- a proper name, source name or proprietary term;
- BUY/SELL direction;
- wick/body/close/open/high/low terminology;
- an instruction to create, modify, delete, commit, push, execute or otherwise act on the project.

If the intended wording is not clear enough from context, ask the project owner to confirm the phrase before treating it as evidence or executing a materially different action.

Minor STT errors that are semantically obvious and cannot change the research/engineering conclusion may be normalized without interrupting the workflow.

When a user clarification corrects an earlier STT interpretation, preserve the correction in the relevant evidence/checkpoint rather than silently treating the earlier wording as authoritative.

## Resume rule

On a resumed or zero-context session, start from root `AGENTS.md` and `PROJECT_BOOTSTRAP.md`, read `skills/nexus-xau-research/SKILL.md`, and run `.venv\Scripts\python.exe scripts\research_preflight.py`. Require a PASS before new substantive work. Then read this policy together with `TOOLS.md`, `docs/CURRENT_RESEARCH_STATE.json`, `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`, `docs/SOURCE_COVERAGE_LEDGER.json`, `research_queue/QUEUE.json`, the active worksheet, and the latest checkpoint.

The source coverage ledger is durable memory of what has already been reviewed. A closed or unresolved source window must not be re-researched from zero without a documented reopen trigger. If validated work from the prior session is still uncommitted/unpushed, complete repository maintenance before starting a new unrelated checkpoint when practical.
