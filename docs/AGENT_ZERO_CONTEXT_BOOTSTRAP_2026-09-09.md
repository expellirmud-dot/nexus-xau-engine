# Agent Zero-Context Bootstrap Checkpoint — 2026-09-09

Status: VALIDATED / RESTART-SAFE INFRASTRUCTURE

## Objective

Make the repository sufficient for a new AI/agent with no chat memory to discover the current project state, avoid repeating already-reviewed source work, follow the evidence discipline, and continue the active research question without inventing missing rules.

## Added

- `PROJECT_BOOTSTRAP.md` — short zero-context entry route and comprehension gate.
- `skills/nexus-xau-research/SKILL.md` — repeatable evidence-first research workflow from bootstrap through checkpoint.
- `docs/SOURCE_COVERAGE_LEDGER.json` — durable memory of reviewed source windows, findings, residual unknowns, checkpoint links, and reopen triggers.
- `scripts/research_preflight.py` — deterministic preflight that validates core files, resolves the active RQ and latest checkpoint, summarizes canonical/coverage state, and emits a required-read manifest with SHA-256 prefixes.

## Integrated

- `AGENTS.md` now requires zero-context bootstrap, skill load, preflight PASS, source-coverage check, and comprehension gate before new substantive work.
- `README.md` points new agents to the entry path.
- `docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md` resume rule includes the bootstrap/preflight/coverage workflow.
- `TOOLS.md` registers the repository-local research preflight.
- `docs/CURRENT_RESEARCH_STATE.json` records the bootstrap architecture and mandatory resume order.

## Coverage ledger seed policy

The initial ledger is a **partial seed**, primarily covering the RQ-009 source windows already reviewed in the current research sequence. It is not a claim that every historical source window from RQ-001 through RQ-008 has been backfilled.

Backfill rule:

- preserve existing historical RQ/checkpoint documents;
- add older coverage entries when that topic/source is next touched or when a bounded backfill task is explicitly performed;
- do not fabricate timestamps, review modality, or closure state merely to make the ledger look complete.

## Runtime validation

Command:

`.venv\Scripts\python.exe scripts\research_preflight.py`

Validated result:

`NEXUS_RESEARCH_PREFLIGHT=PASS`

The runtime correctly resolved:

- active RQ: `RQ-009`;
- active worksheet: `research_queue/active/RQ-009_SOURCE_GAP_CLOSURE.md`;
- latest checkpoint: `docs/RQ009_EP5_CROSS_TF_COMPONENT_COMPLETION_2026-09-09.md`;
- source coverage ledger: 14 seeded entries at validation time;
- current blocked performance claims remain visible, including strategy Win/Loss/expectancy.

## Important limitation

Preflight proves that the required repository state can be discovered and validated; it does **not** prove that an agent has cognitively read or understood every file. `AGENTS.md` and `PROJECT_BOOTSTRAP.md` therefore retain an explicit comprehension gate before substantive work.

## Decision

The project now has four distinct restart-safe memory layers:

1. `CANONICAL_CLAIM_REGISTER` — what is currently accepted;
2. `SOURCE_COVERAGE_LEDGER` — what source material has already been checked;
3. `CURRENT_RESEARCH_STATE` + `QUEUE` — where work stands and what is next;
4. `AGENTS.md` + `PROJECT_BOOTSTRAP.md` + research Skill + preflight — how a zero-context agent must load and use those memories.

This checkpoint changes research infrastructure only. It does not upgrade any unresolved trading rule or establish any system Win/Loss result.
