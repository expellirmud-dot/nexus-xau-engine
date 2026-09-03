# NEXUS Project Maintenance Policy

Status: USER-DIRECT OPERATING AUTHORIZATION
Effective: 2026-09-03

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

On a resumed session, read this policy together with `docs/CURRENT_RESEARCH_STATE.json` and the latest checkpoint before continuing. If validated work from the prior session is still uncommitted/unpushed, complete repository maintenance before starting a new unrelated checkpoint when practical.
