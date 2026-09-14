# WO-055 Phase E — Derived Research Authority Report Checkpoint

Status: IMPLEMENTED / DETERMINISTIC / DERIVED_ONLY
Date: 2026-09-14 Asia/Bangkok

## Implemented

Generator/validator logic:

`src/nexus_xau/governance/research_governance.py`

CLI:

`scripts/report_research_authority.py`

Default local derived output:

`results/governance/research_authority.json`

The output path is under the repository's existing ignored `results/*` policy.

## Report schema

`WO055_AUTHORITY_REPORT_V0.1`

Each deterministic claim row includes:

- claim ID;
- canonical statement SHA256;
- canonical statement summary;
- lifecycle status;
- authority mode;
- current authority refs;
- engine permission;
- validation summary;
- source refs;
- risk flags;
- supersession state;
- conflict status.

Rows are sorted by `claim_id`.

Unchanged pre-WO055 claims are displayed as:

`LEGACY_UNCLASSIFIED`

The report does not infer EXCLUSIVE or COMPOSITE authority for legacy claims.

## Derived-only invariant

The report is generated only from the canonical claim register.

It is not read as a source of truth for claim mutation.

Deleting the report does not change authority and does not make preflight fail.

When a local report exists, preflight validates it against a freshly regenerated normalized view. A mismatch fails with the frozen reason code:

`GENERATED_AUTHORITY_VIEW_MISMATCH`

When no local report exists, preflight reports:

`NOT_GENERATED_DERIVED_VIEW_OPTIONAL`

and remains PASS.

## Frozen fixture completion

The Phase-A explicit governance harness is now fully GREEN:

`16/16 PASS`

This includes KF20:

`GENERATED_AUTHORITY_VIEW_MISMATCH`

The normal production governance/report focused run with the frozen fixtures:

`40 tests PASS`

## Real report evidence

Generated claim count:

`45`

Report validation against canonical store:

`PASS`

Report SHA256 on first generation:

`f93837b89e144156713a8494d4b19f5c92a47d8cbf62d1df03cd19e1a217d31f`

The local report was then deleted.

Preflight while report was absent:

`PASS / authority_report_status=NOT_GENERATED_DERIVED_VIEW_OPTIONAL`

The report was regenerated from the same canonical store.

Regenerated SHA256:

`f93837b89e144156713a8494d4b19f5c92a47d8cbf62d1df03cd19e1a217d31f`

Hashes are identical.

Preflight with regenerated report:

`PASS / authority_report_status=PASS`

## Mutation safety

Tests confirm generation/delete/regeneration does not modify the canonical claim-store bytes.

No Queue, claim authority, RQ status, research outcome, or holdout state is derived back from the generated report.

## Holdout safety

No holdout outcome was opened, inspected, or scored in Phase E.

The generated report contains claim governance metadata only.

## Next bounded step

Phase F reconciliation:

1. update bootstrap/agent governance instructions;
2. extend State Authority Contract with WO-055 claim/RQ governance separation;
3. mark WO-055 implementation complete in Current State and Work Order history;
4. reconcile time-relative holdout instructions without opening outcomes;
5. final preflight + all frozen fixtures + full pytest + Ruff + diff validation;
6. final commit/push and verify clean `HEAD == origin/main`.
