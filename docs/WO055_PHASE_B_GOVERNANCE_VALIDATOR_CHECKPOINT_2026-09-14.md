# WO-055 Phase B — Governance Validator + Preflight Integration Checkpoint

Status: IMPLEMENTED / VALIDATED / CANONICAL_STORES_NOT_YET_MIGRATED
Date: 2026-09-14 Asia/Bangkok
Phase-A freeze commit: `a37e86b`

## Implemented

New governance package:

- `src/nexus_xau/governance/research_governance.py`
- `src/nexus_xau/governance/__init__.py`

Default regression tests:

- `tests/test_research_governance.py`

Existing preflight now runs read-only canonical claim governance validation before declaring PASS.

## Enforced now

- duplicate canonical claim IDs fail closed;
- missing claim source/authority references fail closed;
- active+superseded contradiction fails closed;
- supersession cycles fail closed;
- EXCLUSIVE authority cardinality is enforced when an explicit governance block exists;
- COMPOSITE requires at least two named authorities plus an explicit compatibility statement;
- validation dimensions cannot collapse into one generic PASS;
- historical-only evidence cannot become current authority;
- holdout evidence cannot become design/tuning promotion authority;
- candidate RQ admission validates newness, boundary, falsification, decision consequences, holdout/leakage guard, and duplicate identity;
- legacy fingerprint helper exists for Phase D migration without guessing authority mode.

## Frozen fixture progress

Explicit Phase-A RED harness after Phase-B implementation:

- KF06-KF19: GREEN;
- VC11 explicit COMPOSITE: GREEN;
- VC_ADMISSION: GREEN;
- KF20 generated-report mismatch: still RED intentionally for Phase E.

Observed explicit RED harness result:

`15 passed / 1 failed (KF20 only)`

## Real current-state validation

Current canonical claim register, still unmigrated:

- 45 claims;
- `validate_claim_store = PASS`;
- no authority mode was invented for legacy claims.

Research preflight:

`NEXUS_RESEARCH_PREFLIGHT=PASS`

Preflight now emits:

`canonical_governance=PASS`

## Test evidence

Focused governance + existing state-drift tests:

`24 passed`

Full repository pytest after Phase-B changes:

`PASS / exit code 0`

Ruff:

`PASS`

`git diff --check`:

`PASS`

## Canonical-store safety

This phase did not modify:

- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`;
- `research_queue/QUEUE.json`;
- `docs/CURRENT_RESEARCH_STATE.json`;
- `docs/SOURCE_COVERAGE_LEDGER.json`;
- `docs/0700_WORKSTREAM_STATE.json`.

No holdout outcome was opened or scored.

## Next bounded step

Phase C/D migration:

1. add prospective admission enforcement metadata to the existing Queue store without activating an RQ;
2. add deterministic legacy claim fingerprints to the existing claim register;
3. do not assign speculative EXCLUSIVE/COMPOSITE modes to the 45 legacy claims;
4. make preflight verify both migration contracts;
5. keep RQ-014 queued and holdout semantics unchanged.
