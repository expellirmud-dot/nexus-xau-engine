# RQ-012 — V0.1 Holdout Append-Only Ledger + Activation Lock

Status: ACTIVE — tooling/activation preparation; holdout outcome scoring prohibited

## Objective

Implement the audit tooling required by frozen RQ-011 before the V0.1 prospective holdout is considered live.

## Dependency

- V0.1 engine freeze: `75866d2`
- frozen RQ-011 protocol commit: record after RQ-011 is pushed
- protocol: `docs/RQ011_PRISTINE_V0_HOLDOUT_PROTOCOL_2026-09-09.md`

## Required tooling

1. Canonical JSON record serialization for checkpoint/event records.
2. SHA256 hash chain:
   - `previous_record_sha256`
   - `record_sha256`
3. Append-only writer that rejects mutation/duplicate record index.
4. Verification command that replays the full chain and fails closed on any mismatch.
5. Activation lock containing:
   - V0 engine commit;
   - RQ-011 protocol freeze commit;
   - prospective start boundary;
   - schema version;
   - dataset/environment fields still required before collection;
   - `holdout_outcome_scoring_authorized=false`.
6. Tests for valid append, tamper detection, duplicate/reorder detection, and lock validation.

## Activation boundary rule

After the RQ-011 freeze commit is pushed, record:

```text
prospective boundary = first 07:00 Asia/Bangkok boundary strictly after protocol freeze/push
```

The activation lock may reserve that future boundary, but RQ-012 must not inspect/score any post-boundary outcome.

## Guardrails

- no outcome scoring;
- no future-bar label creation;
- no code changes to V0.1 semantics;
- no force overwrite of historical label records;
- no silent target/horizon/location changes;
- no system/trade Win-rate claim.

## Done when

- ledger + verifier tests pass;
- activation lock is generated with exact commits/boundary;
- preflight/full suite/Ruff pass;
- checkpoint committed/pushed;
- holdout status is explicitly `RESERVED_OR_COLLECTION_READY / UNSCORED` only, never scored by RQ-012.
