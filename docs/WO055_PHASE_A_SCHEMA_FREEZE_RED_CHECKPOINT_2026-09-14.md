# WO-055 Phase A — Schema Freeze + RED Governance Fixture Checkpoint

Status: FROZEN / RED_CONFIRMED / CANONICAL_STORES_UNTOUCHED
Date: 2026-09-14 Asia/Bangkok

## Inputs

- Work Order: `work-order/WO-055-RESEARCH-AUTHORITY-VALIDATION-GOVERNANCE.md`
- Schema freeze: `docs/WO055_MINIMAL_GOVERNANCE_SCHEMA_FREEZE_2026-09-14.md`
- Fixture matrix: `tests/fixtures/wo055/governance_matrix.json`
- Explicit RED harness: `tests/red_wo055_governance.py`

The owner-provided Work Order was preserved without semantic edits.

## Read-only baseline audit

Before Phase A writes:

- canonical claims: 45;
- every existing claim has `claim_id`, `canonical_statement`, `status`, `engine_permission`, `source_refs`, and `risk_flags`;
- authority mode is not currently explicit;
- queue RQs: 15;
- legacy RQs do not contain the new admission payload;
- no decision-critical RQ is active.

This justified a prospective/additive schema rather than speculative historical backfill.

## Frozen migration decision

Existing 45 claims are grandfathered by deterministic authority-sensitive fingerprints at migration time.

WO-055 must not guess EXCLUSIVE/COMPOSITE authority for those records.

Any future authority-sensitive change to a grandfathered claim requires explicit governed-claim metadata in the same coherent checkpoint.

Prospective/new RQ admission is gated without rewriting historical RQs.

## RED execution evidence

Fixture JSON parse:

`WO055_FIXTURE_JSON_OK`

Existing repository preflight:

`NEXUS_RESEARCH_PREFLIGHT=PASS`

Existing state-drift focused tests:

`6 passed`

Explicit RED command:

```text
python -m pytest -q tests/red_wo055_governance.py --basetemp=.pytest-tmp-wo055-red
```

Observed:

- 16/16 WO-055 fixture tests FAILED;
- failure cause: `ModuleNotFoundError: No module named 'nexus_xau.governance'`;
- this is the intended pre-implementation RED state;
- no production governance validator existed at this checkpoint.

The 16 RED cases cover WO-055 new failures KF06-KF10, KF12-KF20 plus the valid COMPOSITE and valid admission targets. Existing KF01-KF05 remain covered by the already-green state-drift suite.

## Canonical-store mutation lock verification

Phase A did not modify:

- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`;
- `research_queue/QUEUE.json`;
- `docs/CURRENT_RESEARCH_STATE.json`;
- `docs/SOURCE_COVERAGE_LEDGER.json`;
- `docs/0700_WORKSTREAM_STATE.json`.

No holdout outcome was inspected or scored.

## Next bounded step

Phase B:

1. implement `nexus_xau.governance.research_governance`;
2. make KF06-KF19 and valid governance/admission fixtures green with frozen reason codes;
3. extend existing preflight to call generic claim-governance validation while preserving current state PASS;
4. do not mutate canonical stores until the validator contract is proven.
