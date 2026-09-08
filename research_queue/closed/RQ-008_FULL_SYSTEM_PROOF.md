# RQ-008 — Full-system replay and out-of-sample Win/Loss proof

Status: CLOSED / NOT_TESTABLE_WITH_CURRENT_EVIDENCE

## Why this matters

This is the final validation layer, not the discovery tool for unresolved rules. Starting it too early would turn research proxies into hidden assumptions and produce a misleading system-level win rate.

## Dependencies

Requires sufficiently frozen setup/state/location/entry/SL/invalidation semantics from upstream research items.

## Primary method when activated

Freeze the complete rule set before inspecting final held-out outcomes. Use replay/backtest with explicit data provenance, costs where relevant, positive/negative controls, and untouched out-of-sample periods.

## Done when

A reproducible full-system outcome report exists with clearly defined trade construction, Win/Loss/expectancy methodology, limitations, and no unresolved upstream proxy masquerading as canonical logic.

## Current first action

Perform a readiness audit before any outcome run. Verify complete setup->entry->SL->invalidation->exit construction, frozen rule provenance, data/cost requirements, and a genuinely untouched out-of-sample period. If any material prerequisite fails, close `NOT_TESTABLE_WITH_CURRENT_EVIDENCE` rather than using research proxies as hidden production rules.

## Closure — 2026-09-08

Readiness gate failed before any full-system outcome run. See `docs/RQ008_FULL_SYSTEM_PROOF_READINESS_CLOSURE_2026-09-08.md`. Complete trade construction remains unresolved and prior DEV/VAL/TEST periods are not a pristine final holdout for a newly frozen full-system rule set. Current system Win rate remains `NOT_ESTABLISHED` / `ยังสรุปไม่ได้`.
