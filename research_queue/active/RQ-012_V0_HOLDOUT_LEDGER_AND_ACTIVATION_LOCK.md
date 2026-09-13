# RQ-012 — V0.1 Holdout Append-Only Ledger + Activation Lock

Status: ACTIVE — implementation pending

## Resume note

This worksheet was paused while the owner-prioritized 07:00 bounded workstream was completed.

RQ-015 is now closed with `CONSUMED_ASSOCIATION_EXPLAINED_OR_DOMINATED_BY_GEOMETRY`.

RQ-012 is promoted back to ACTIVE. The frozen RQ-010/RQ-011 identities remain unchanged.

## Objective

Implement the audit tooling required by frozen RQ-011 before the V0.1 prospective holdout is considered live.

## Dependency

- V0.1 engine freeze: `75866d2`
- RQ-011 protocol: `docs/RQ011_PRISTINE_V0_HOLDOUT_PROTOCOL_2026-09-09.md`
- exact protocol freeze commit must be resolved from Git history before activation

## Required tooling

1. Canonical JSON record serialization.
2. SHA256 record chain using `previous_record_sha256` and `record_sha256`.
3. Append-only writer rejecting duplicate or mutated record index.
4. Verification command that fails closed on any chain mismatch.
5. Activation lock recording engine commit, protocol commit, prospective start boundary, schema version, and required environment metadata.
6. Tests for valid append, tamper detection, duplicate/reorder detection, and lock validation.

The activation lock must explicitly keep outcome scoring disabled.

## Activation boundary rule

After the RQ-011 freeze commit is verified, record the first 07:00 Asia/Bangkok boundary strictly after the protocol freeze/push as the prospective boundary.

RQ-012 may reserve that boundary but must not inspect post-boundary outcomes.

## Guardrails

- no outcome scoring;
- no future-bar label creation;
- no change to frozen V0.1 semantics;
- no overwrite of historical ledger records;
- no silent target/horizon/location changes;
- no system or trade Win-rate claim.

## Done when

- ledger and verifier tests pass;
- activation lock is generated with exact commits and boundary;
- preflight, full suite, and Ruff pass;
- checkpoint is committed and pushed;
- holdout status is `RESERVED_OR_COLLECTION_READY / UNSCORED` only.

## Immediate next action

Resolve the exact RQ-010 engine freeze commit and RQ-011 protocol freeze commit from Git history, then freeze the ledger/activation-lock implementation contract before writing code.
