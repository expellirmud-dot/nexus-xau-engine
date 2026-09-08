# RQ-008 — Full-system replay and out-of-sample Win/Loss proof

Status: QUEUED_LAST

## Why this matters

This is the final validation layer, not the discovery tool for unresolved rules. Starting it too early would turn research proxies into hidden assumptions and produce a misleading system-level win rate.

## Dependencies

Requires sufficiently frozen setup/state/location/entry/SL/invalidation semantics from upstream research items.

## Primary method when activated

Freeze the complete rule set before inspecting final held-out outcomes. Use replay/backtest with explicit data provenance, costs where relevant, positive/negative controls, and untouched out-of-sample periods.

## Done when

A reproducible full-system outcome report exists with clearly defined trade construction, Win/Loss/expectancy methodology, limitations, and no unresolved upstream proxy masquerading as canonical logic.
