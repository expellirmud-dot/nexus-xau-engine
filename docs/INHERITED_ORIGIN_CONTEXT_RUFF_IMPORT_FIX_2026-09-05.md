# Inherited Origin Context — Ruff Import Fix — 2026-09-05

Status: ENGINEERING CHECKPOINT / LINT-ONLY FIX

## Runtime evidence before this fix

Project-owner Windows runtime reported:

- pytest: `114 passed, 115 warnings in 4.69s`;
- Ruff stopped on a single `I001` import-formatting error in `src/nexus_xau/research/inherited_origin_context_batch.py`.

The pytest result confirms the newly-added origin-context test suite passed before this lint-only change.

## Fix

The import block for `nexus_xau.research.inherited_origin_context_relation` was formatted exactly in the structure Ruff requested by separating the aliased `run as run_period` import from the constant imports.

## Research guard

This checkpoint does not change:

- origin age definition;
- consumed-run ratio definition;
- previous-24h versus older origin grouping;
- fixed fresh H1 1000-point primary outcome lane;
- PATH_REMAINING / ORIGIN_TARGET_LEVEL comparator role;
- minimum group size;
- relation-state signs;
- cross-period replication rule;
- any production trading rule.

## Next step

Pull the branch and rerun `scripts/run_inherited_origin_context_relation.ps1`.

Expected flow:

`pytest -> Ruff -> three-period origin-context batch -> cross-period summary`.
