# Phase 1 Research Flow Dry Run — 2026-09-14

Status: COMPLETED GOVERNANCE / ANTI-FORGETTING DRY RUN

Purpose: test how one real research result should move from observation to durable record without reopening holdout outcomes or changing trading semantics.

## Dry-run case

Case: H4 consumed/run-progress state versus PATH_REMAINING target-first ordering.

This case was selected because it contains an apparent contradiction:

1. Q3/Q4 reported a replicated broad positive association.
2. Later frozen geometry control found the primary consumed residual non-positive in both Discovery and Replication.

## Step 1 — identify whether the observations are actually the same claim

They are related but not identical statements.

Observation A asks whether consumed state and outcome ordering move together under the historical representation.

Observation B asks whether consumed still carries independent information after conditioning on target/point-check geometry.

Therefore A and B can both be true.

Classification:

`APPARENT_CONTRADICTION -> CONDITIONING_VARIABLE_RECONCILIATION`

## Step 2 — preserve chronology

Historical evidence remains in:

- `docs/0700_Q3_DISTINCT_INFORMATION_CROSS_PERIOD_2026-09-12.md`
- `docs/0700_Q4_H4_CONSUMED_SHAPE_CROSS_PERIOD_2026-09-12.md`

Later control evidence remains in:

- `docs/0700_MINIMAL_V2_REPLICATION_GEOMETRY_CONTROL_2026-09-13.md`
- `docs/0700_RQ015_GEOMETRY_NULL_RESULT_2026-09-13.md`

The old documents are not deleted or rewritten to pretend that the later result was known earlier.

## Step 3 — current authority

Canonical current interpretation:

`H4_0700_CONSUMED_STATE_RELATION`

Current conclusion:

- broad historical association remains a valid observation;
- independent market-predictive information from consumed is not established after geometry control;
- consumed must not be used as an independent predictor or threshold from current evidence.

## Step 4 — anti-forgetting index

The relation family is now indexed as:

`FIND-0001 / H4_0700_CONSUMED_STATE__PATH_REMAINING_ORDERING`

in `research_findings/FINDINGS.json`.

The finding ledger is explicitly NON-CANONICAL. It points to evidence and current canonical authority but cannot override them.

## Step 5 — stale-document hazard discovered by the dry run

`docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md` was written before RQ-015 and still described H4 consumed as the strongest lead at that time.

A worker reading only that historical snapshot could incorrectly restore the old independent-lead interpretation.

Mitigation applied:

- a later-authority correction banner now points to RQ-015 and the current canonical claim;
- history remains intact below the banner.

## Failure paths tested conceptually

### F1 — rediscovering the same relation under a new filename

Risk: duplicate work and later disagreement.

Mitigation: one unique `relation_key` in the finding ledger; preflight rejects duplicate relation keys.

### F2 — two observations look contradictory

Risk: pick the newer one blindly or discard the older one.

Mitigation: preserve representation + conditions for every observation; use an explicit reconciliation record.

### F3 — finding is mistaken for canonical truth

Risk: a research lead silently becomes a trading rule.

Mitigation: finding ledger role is fixed to `NON_CANONICAL_RESEARCH_FINDING_INDEX`; canonical claim register remains authority.

### F4 — evidence file disappears or path is wrong

Risk: finding survives without auditable support.

Mitigation: preflight validates every finding evidence reference exists.

### F5 — finding claims it was promoted but canonical claim is missing

Risk: phantom authority.

Mitigation: preflight checks `canonical_claim_ref` against the actual canonical claim register.

### F6 — historical positive result is read as system win rate

Risk: Q4 top-bin descriptive result becomes a performance claim.

Mitigation: forbidden uses explicitly include consumed threshold, system win rate, and profitability claim.

### F7 — later conditioning changes interpretation

Risk: old finding is deleted, or new finding overwrites history.

Mitigation: retain both observations inside the same relation family and change only the current reconciliation.

## Dry-run verdict

The canonical/governance layer already handled this real contradiction correctly.

The main missing layer was a prospective anti-forgetting index for pre-canonical findings. The pilot finding ledger closes that gap without creating a new truth authority.

## What this dry run does not prove

- that all future contradictions will be resolvable;
- that relation-key identity can always be assigned automatically;
- that Phase 1 is profitable;
- that a final trade-level system is complete;
- that holdout scoring is authorized.

## True contradiction branch

The dry-run case above is an apparent contradiction resolved by conditioning.

If a future pair of observations instead represents the same material claim under the same representation and conditions and the observations cannot both be true:

`status = CONTRADICTED`

`blocking = true`

The affected decision branch must not promote or choose a winner until the contradiction is resolved. Preflight rejects a contradicted finding that is marked non-blocking.

This blocks only the affected dependency/branch; unrelated Phase 1 work may continue.
