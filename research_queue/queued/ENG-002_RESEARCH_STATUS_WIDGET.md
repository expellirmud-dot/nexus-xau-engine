# ENG-002 — Compact research status widget

Status: QUEUED_NON_BLOCKING
Type: INFRASTRUCTURE / OBSERVABILITY

## Purpose

Give the project owner a small translucent top-right status panel showing what NEXUS is doing without requiring terminal/JSON inspection.

Minimum fields:

- active worksheet ID/title;
- current phase;
- current source/period being reviewed;
- last meaningful result;
- blocker if any;
- latest checkpoint/commit.

## Activate when

Observability becomes a practical blocker, or there is a natural engineering window that does not interrupt a decision-critical research closure.

## Guard

Do not invent a fake overall project completion percentage. Show only real task/phase states from the operational queue and checkpoint data.
