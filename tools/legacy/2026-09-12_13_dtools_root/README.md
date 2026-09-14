# Archived XAU one-off helpers from D:\tools root

This directory preserves Project-specific helper scripts that were found at the shared infrastructure root `D:\tools` and moved back into the Nexus-XAU-Engine repository on 2026-09-14.

## Status

HISTORICAL / LEGACY / NOT CURRENT AUTHORITY

These files were created during earlier 07:00 / Phase 1 audit, patch, reanchor, replay, and state-maintenance work. Many contain hard-coded timestamps, checkpoint names, paths, or assumptions that were correct only at the time they were written.

## Safety rule

Do not run these scripts against current Project state without first reviewing the file and comparing it with:

- `docs/CURRENT_RESEARCH_STATE.json`
- `research_queue/QUEUE.json`
- `docs/PHASE1_CURRENT_OBJECTIVE_2026-09-14.md`
- current governance/preflight rules

Several scripts directly modify state files, claim registers, queue/workstream files, or research code. Running them blindly could regress current state to an older checkpoint.

## Why preserved

They are retained for:

- chronology and forensic traceability;
- understanding how earlier checkpoints were produced;
- recovering useful audit logic if needed;
- preventing Project-specific one-off scripts from remaining mixed with shared `D:\tools` infrastructure.

## Manifest

`MANIFEST.json` records the source root, destination, date, and the 39 files moved in this cleanup.

Shared infrastructure such as `nexus-durable-work`, `nexus-project-continuity`, Bridge patches, browser/video/voice tools, and persisted durable jobs remains in `D:\tools`.
