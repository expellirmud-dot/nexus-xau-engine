# NEXUS XAU Project Skills

Status: FROZEN CORE SKILL SET

The project intentionally keeps the skill set small.

## Active project skill

- `nexus-xau-research/SKILL.md`

Role:

- restart-safe evidence-first research;
- source review and provenance control;
- experiment/question freezing;
- canonical-state reconciliation;
- checkpoint persistence;
- anti-duplication / anti-backfit discipline.

## Important boundary

Skills define **how NEXUS works**.

They do not store the current trading knowledge.

Current knowledge belongs in:

- `docs/CURRENT_RESEARCH_STATE.json`;
- `docs/0700_WORKSTREAM_STATE.json`;
- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`;
- `docs/SOURCE_COVERAGE_LEDGER.json`;
- `research_queue/QUEUE.json`;
- versioned checkpoint/closure documents.

This separation prevents the skill and the research record from drifting into two competing versions of truth.

## Why there is only one skill now

The current bottleneck is not lack of instructions.

It is reliable routing to the correct current knowledge.

Adding multiple overlapping skills now would:

- duplicate rules;
- make restart behavior harder to reason about;
- increase the chance that one skill becomes stale;
- make agents choose between overlapping procedures.

New skills should be created only after a workflow becomes stable, repeated, and materially distinct in toolchain or execution contract.

Potential future candidates, not yet authorized:

- replay / prospective-holdout operations;
- source-forensics/browser-video evidence operations;
- UI/explainability artifact generation.

## Freeze contract

`SKILLS_MANIFEST.json` records the currently frozen skill files and their SHA256 hashes.

Repository preflight must fail when a frozen skill file changes without an intentional manifest update.

A skill change is therefore a versioned project change, not an incidental edit.
