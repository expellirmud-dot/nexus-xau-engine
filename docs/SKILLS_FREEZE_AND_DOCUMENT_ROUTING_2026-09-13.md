# Skills Freeze and Document Routing Checkpoint — 2026-09-13

Status: FROZEN / VALIDATED / PRE-0700-MINIMAL-V2

## Purpose

Freeze the project skill layer before beginning the next 07:00 replay cycle, and define how a large document set is consumed without requiring every session to reread the whole repository.

## Repository observation

At this checkpoint:

- project skills: 1 core skill;
- top-level files under `docs/`: 170;
- files under `docs/` including subdirectories: 171.

Therefore “read every document every session” is not a sustainable memory model.

The project must use routed/lazy loading.

## Frozen skill set

Manifest:

`skills/SKILLS_MANIFEST.json`

Human-readable boundary:

`skills/README.md`

Frozen skill:

`skills/nexus-xau-research/SKILL.md`

Role:

- evidence-first research procedure;
- restart/bootstrap discipline;
- source coverage checks;
- question/representation freeze;
- provenance separation;
- canonical reconciliation;
- checkpoint persistence.

The skill is intentionally procedural.

It does not duplicate current trading/research facts.

## Knowledge boundary

Current project knowledge belongs in:

- `docs/CURRENT_RESEARCH_STATE.json`;
- `docs/0700_WORKSTREAM_STATE.json`;
- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`;
- `docs/SOURCE_COVERAGE_LEDGER.json`;
- `research_queue/QUEUE.json`;
- referenced versioned closure/checkpoint documents.

This prevents SKILL.md from becoming a second stale copy of the system state.

## Document routing policy

Sessions do not read all 171 documents.

Required order:

```text
AGENTS / PROJECT_BOOTSTRAP / operating philosophy
-> skill manifest + frozen core skill
-> research preflight required-read manifest
-> Current State / Workstream / Claims / Coverage / Queue
-> active worksheet/latest checkpoint
-> only then load a specific supporting/historical document when a pointer or active question requires it
```

A document existing on disk is not sufficient to make it current authority.

When a new document changes current understanding, it must be routed from the appropriate durable store.

## Skill integrity enforcement

`scripts/research_preflight.py` now:

1. loads `skills/SKILLS_MANIFEST.json`;
2. requires manifest status `FROZEN`;
3. verifies each frozen skill file exists;
4. computes SHA256;
5. fails if the current hash differs from the frozen manifest.

Validated positive state:

`skill_freeze=FROZEN | 1 skill(s) verified`

Validated negative control:

a deliberately incorrect expected hash returns:

`FROZEN_SKILL_HASH_MISMATCH`

Therefore an incidental edit to the core skill cannot silently enter a new session.

## Decision on adding more skills

Do not add another skill before the first MINIMAL_V2 replay.

Current bottleneck is not missing procedural instructions.

Add a skill later only if replay evidence shows a stable repeated workflow with a materially separate execution contract.

Potential future candidates, only after need is demonstrated:

- replay/holdout operations;
- source-forensics/browser-video evidence;
- UI/explainability generation.

Document volume by itself is not a reason to create a new skill.

## Decision on plugins/tools

Do not add integrations merely to reduce anxiety about project complexity.

The existing stack already provides:

- repository durable state;
- preflight/router;
- IE Coder/Bridge local access;
- local research code/tests;
- browser/video evidence tooling;
- Git checkpoint history.

A new tool/plugin should be added only when a concrete repeated task cannot be handled cleanly by the current stack.

## Next action

Stop infrastructure/document cleanup here.

Next project action:

```text
freeze 0700_MINIMAL_V2
-> synthetic contract/boundary tests
-> real 150-day discovery replay
-> failure/unknown-state map
-> unchanged-code 60-day cross-period replay
```

Do not begin a broad documentation reorganization before the 150-day replay.

The replay should reveal which additional skill/tool/UI capability is actually needed.
