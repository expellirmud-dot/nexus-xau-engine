# WO-055 Phase A — Minimal Admission / Authority / Validation Schema Freeze

Status: FROZEN_BEFORE_GOVERNANCE_IMPLEMENTATION
Date: 2026-09-14 Asia/Bangkok
Work Order: `work-order/WO-055-RESEARCH-AUTHORITY-VALIDATION-GOVERNANCE.md`

## 1. Freeze purpose

Freeze the smallest prospective governance contract before implementation changes or canonical-store migration.

This contract is additive. It does not replace:

- `docs/CURRENT_RESEARCH_STATE.json`;
- `research_queue/QUEUE.json`;
- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`;
- `docs/SOURCE_COVERAGE_LEDGER.json`;
- `docs/0700_WORKSTREAM_STATE.json`;
- `scripts/research_preflight.py`.

No trading/research semantics are changed by this freeze.

## 2. Migration rule for existing claims

The 45 claims present before WO-055 are legacy current records. Their missing authority mode must not be guessed.

At migration, the canonical claim register may add one top-level governance section containing:

```json
{
  "schema_version": "WO055_RESEARCH_GOVERNANCE_V0.1",
  "legacy_claim_fingerprints": {
    "<claim_id>": "<sha256>"
  }
}
```

The fingerprint is computed deterministically from these authority-sensitive existing fields only:

- `claim_id`;
- `canonical_statement`;
- `status`;
- `engine_permission`;
- `source_refs`;
- `supersedes` when present;
- `supersession_note` when present.

A legacy claim whose fingerprint still matches may remain without an explicit WO-055 governance block.

If an authority-sensitive legacy field changes after the migration baseline, that claim must leave legacy-only treatment and satisfy the explicit governed-claim contract in the same coherent checkpoint.

This avoids speculative backfill while preventing a legacy record from changing authority silently.

## 3. Prospective RQ admission schema

A candidate decision-critical RQ admitted after WO-055 uses:

```json
{
  "schema_version": "WO055_RQ_ADMISSION_V0.1",
  "rq_id": "RQ-XXX",
  "rq_type": "TYPE",
  "newness_statement": "What is genuinely new?",
  "question": "What exactly is being tested?",
  "boundary": {
    "in_scope": ["..."],
    "out_of_scope": ["..."]
  },
  "expected_evidence": ["..."],
  "falsification_condition": "What result would falsify or materially weaken it?",
  "decision_consequence": {
    "positive": "Allowed project decision/state change",
    "negative": "Allowed project decision/state change",
    "unresolved": "Allowed project decision/state change"
  },
  "dependencies": [],
  "stop_condition": "Bounded stopping condition",
  "outcome_bearing": false,
  "holdout_or_leakage_guard": null
}
```

Rules:

1. fields above are required;
2. `boundary.in_scope` and `boundary.out_of_scope` must both be explicit non-empty lists;
3. the three decision-consequence branches are mandatory;
4. `expected_evidence` must be non-empty;
5. `outcome_bearing=true` requires a non-empty `holdout_or_leakage_guard`;
6. `outcome_bearing=false` permits the guard to be null;
7. the candidate ID must not duplicate an active/queued/closed RQ identity unless an explicit reopen path is separately authorized;
8. admission does not activate an RQ; existing one-active-decision-critical queue policy still controls activation;
9. historical RQs are not rewritten to this schema merely to satisfy WO-055.

Admission decisions:

- `ADMISSIBLE`;
- `BLOCKED_INCOMPLETE`;
- `BLOCKED_DUPLICATE_OR_ALREADY_CLOSED`;
- `BLOCKED_AUTHORITY_CONFLICT`;
- `BLOCKED_EVIDENCE_OR_HOLDOUT_GUARD`.

## 4. Governed canonical-claim extension

Existing canonical fields remain authoritative for their existing meanings:

- `claim_id`;
- `canonical_statement`;
- `status`;
- `engine_permission`;
- `source_refs`;
- existing supersession fields;
- existing risk flags.

A claim requiring explicit WO-055 governance adds:

```json
{
  "governance": {
    "schema_version": "WO055_CLAIM_GOVERNANCE_V0.1",
    "authority_mode": "EXCLUSIVE",
    "current_authority_refs": ["docs/..."],
    "composite_compatibility_statement": null,
    "validations": []
  }
}
```

Authority rules:

### EXCLUSIVE

- exactly one `current_authority_ref`;
- replacement must close/supersede the prior controller coherently;
- multiple current controllers fail closed.

### COMPOSITE

- at least two explicitly named `current_authority_refs`;
- `composite_compatibility_statement` must be a non-empty explicit statement explaining why coexistence is compatible;
- coexistence is never inferred merely from multiple references.

General rules:

- every governed claim must retain non-empty `source_refs`;
- every `current_authority_ref` must resolve to an explicit current authority reference, not an unclassified historical-only artifact;
- an ACTIVE lifecycle may not simultaneously be marked superseded;
- supersession links must be acyclic;
- duplicate `claim_id` values are forbidden.

## 5. Validation record schema

A governed claim contains exactly one normalized record for every required validation dimension:

```json
{
  "dimension": "SOURCE_VALIDATION",
  "outcome": "PASS",
  "evidence_refs": ["docs/..."],
  "governance_role": "PROMOTION_ELIGIBLE"
}
```

Required dimensions:

1. `SOURCE_VALIDATION`;
2. `REPRESENTATION_VALIDATION`;
3. `IMPLEMENTATION_VALIDATION`;
4. `HISTORICAL_EVIDENCE`;
5. `REPLICATION`;
6. `CONTROL`;
7. `HOLDOUT`.

Allowed outcomes:

- `PASS`;
- `FAIL`;
- `MIXED`;
- `UNKNOWN`;
- `NOT_APPLICABLE`.

Allowed governance roles:

- `PROMOTION_ELIGIBLE`;
- `CONTEXT_ONLY`;
- `CONFIRMATORY_ONLY`;
- `NO_PROMOTION_AUTHORITY`.

Validation rules:

- all seven dimensions must exist exactly once for a governed claim;
- no generic unscoped validation `PASS` is accepted;
- `PASS`, `FAIL`, or `MIXED` requires at least one evidence reference;
- `UNKNOWN` and `NOT_APPLICABLE` may use an empty evidence list;
- `HISTORICAL_EVIDENCE` must use `CONTEXT_ONLY` or `NO_PROMOTION_AUTHORITY`;
- `HOLDOUT` must use `CONFIRMATORY_ONLY` or `NO_PROMOTION_AUTHORITY`;
- HOLDOUT evidence may not be labeled `PROMOTION_ELIGIBLE` for design/tuning;
- a PASS in one dimension has no implication for any other dimension.

## 6. Generated authority view contract

Generated report schema version:

`WO055_AUTHORITY_REPORT_V0.1`

Minimum deterministic claim row:

```json
{
  "claim_id": "...",
  "canonical_statement_sha256": "...",
  "canonical_statement_summary": "...",
  "lifecycle_status": "...",
  "authority_mode": "EXCLUSIVE|COMPOSITE|LEGACY_UNCLASSIFIED",
  "current_authority_refs": [],
  "engine_permission": "...",
  "validation_summary": {},
  "source_refs": [],
  "risk_flags": [],
  "supersession_state": {},
  "conflict_status": "NONE|BLOCKED|LEGACY_UNCLASSIFIED"
}
```

Rules:

- ordering is by `claim_id`;
- JSON serialization is deterministic;
- legacy unchanged claims may report `LEGACY_UNCLASSIFIED` without inventing an authority mode;
- report is derived-only;
- deleting/regenerating the report cannot mutate canonical stores;
- a stored report, if checked, must reproduce byte-equivalent normalized content from canonical inputs or fail with a mismatch reason.

## 7. Stable reason-code freeze

Existing reason codes retained:

1. `PROJECT_QUEUE_POINTER_MISMATCH`
2. `WORKSTREAM_PROJECT_POINTER_MISMATCH`
3. `HOLDOUT_ACTIVATION_IDENTITY_MISMATCH`
4. `HOLDOUT_SCORING_ENABLED`
5. `RQ012_STALE_IMPLEMENTATION_INSTRUCTION`

WO-055 reason codes frozen:

6. `DUPLICATE_CANONICAL_CLAIM_ID`
7. `CLAIM_AUTHORITY_OR_SOURCE_REF_MISSING`
8. `ACTIVE_CLAIM_MARKED_SUPERSEDED`
9. `CLAIM_SUPERSESSION_CYCLE`
10. `EXCLUSIVE_AUTHORITY_CARDINALITY_VIOLATION`
11. valid explicit COMPOSITE authority must return PASS
12. `RQ_ADMISSION_NEWNESS_MISSING`
13. `RQ_ADMISSION_BOUNDARY_MISSING`
14. `RQ_ADMISSION_FALSIFICATION_MISSING`
15. `RQ_ADMISSION_DECISION_CONSEQUENCE_MISSING`
16. `RQ_ADMISSION_HOLDOUT_GUARD_MISSING`
17. `VALIDATION_DIMENSION_COLLAPSED`
18. `HISTORICAL_EVIDENCE_USED_AS_CURRENT_AUTHORITY`
19. `HOLDOUT_EVIDENCE_USED_FOR_DESIGN_TUNING`
20. `GENERATED_AUTHORITY_VIEW_MISMATCH`

Additional implementation reason codes may be introduced only when they represent a distinct failure not covered above. Existing frozen codes must not be renamed merely for implementation convenience.

## 8. Phase-A mutation lock

Until the RED fixture checkpoint is recorded:

- do not modify canonical claim register;
- do not modify QUEUE;
- do not modify CURRENT_RESEARCH_STATE;
- do not modify SOURCE_COVERAGE_LEDGER;
- do not modify 07:00 workstream state;
- do not inspect or score holdout outcomes.

Allowed Phase-A writes:

- this freeze document;
- synthetic governance fixtures;
- RED governance tests/harness;
- an implementation checkpoint recording actual RED execution evidence.

## 9. Terminal meaning of this freeze

This checkpoint proves only that the WO-055 governance contract and expected failures were fixed before implementation.

It does not prove that WO-055 validation exists or passes.
