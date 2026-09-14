# Phase 1 Research Finding Ledger

Role: NON-CANONICAL RESEARCH FINDING INDEX

Purpose: prevent a result from being discovered, saved in an isolated checkpoint, forgotten, and later rediscovered or misread as current authority.

## Authority boundary

`research_findings/FINDINGS.json` is an index of observations and reconciliations. It is NOT a source of canonical truth.

Current truth/authority remains in:
- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json` for accepted claims;
- `research_queue/QUEUE.json` for active decision-critical research;
- `docs/CURRENT_RESEARCH_STATE.json` for project-current workflow state;
- source/closure checkpoints for evidence chronology.

A finding may be useful without being canonical.

## Why one finding can contain apparently conflicting observations

An observation must preserve its representation and conditions. Two observations under the same relation family may both be true if a conditioning variable, timeframe, regime, or representation differs.

Do not collapse:
- marginal association into independent effect;
- one timeframe into another;
- one historical representation into a later corrected representation;
- historical evidence into holdout confirmation.

## Required finding fields

- `finding_id`
- `relation_key`
- `title`
- `status`
- `scope`
- `current_interpretation`
- `observations`
- `reconciliation` when status is `RECONCILED`
- `canonical_claim_ref` when a current canonical claim represents the reconciled conclusion
- `allowed_uses`
- `forbidden_uses`
- `blocking`

Each observation must preserve:
- `observation_id`
- `statement`
- `representation`
- `conditions`
- `evidence_refs`

## Status values

- `OPEN`
- `RECONCILED`
- `CONTRADICTED`
- `SUPERSEDED`
- `PROMOTED`
- `REJECTED`

## Anti-forgetting rule

Before opening a materially similar experiment, search this ledger by `relation_key`, title, involved variables, and canonical claim reference.

`INCONCLUSIVE`, negative controls, and reconciled contradictions remain durable findings.

## True contradiction rule

If two credible observations are the same material claim under the same representation and conditions and cannot both be true:

- set finding status to `CONTRADICTED`;
- set `blocking=true` for the affected branch;
- do not choose a winner from recency, confidence, or favorable outcome;
- open/route a bounded research question when resolution is decision-critical;
- independent unrelated work may continue;
- after resolution, preserve both observations and record the reconciliation/supersession path.

Preflight rejects a `CONTRADICTED` finding that is marked non-blocking.

A `PROMOTED` finding must point to an existing canonical claim.
