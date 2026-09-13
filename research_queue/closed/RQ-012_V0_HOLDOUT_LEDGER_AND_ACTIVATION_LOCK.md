# RQ-012 — V0.1 Holdout Append-Only Ledger + Activation Lock

Status: CLOSED — tooling implemented; activation reserved; UNSCORED

## Resume note

This worksheet was paused while the owner-prioritized 07:00 bounded workstream was completed.

RQ-015 is now closed with `CONSUMED_ASSOCIATION_EXPLAINED_OR_DOMINATED_BY_GEOMETRY`.

RQ-012 is promoted back to ACTIVE. The frozen RQ-010/RQ-011 identities remain unchanged.

## Objective

Implement the audit tooling required by frozen RQ-011 before the V0.1 prospective holdout is considered live.

## Dependency

- V0.1 engine freeze: `75866d2`
- RQ-011 protocol: `docs/RQ011_PRISTINE_V0_HOLDOUT_PROTOCOL_2026-09-09.md`
- RQ-011 protocol freeze commit: `43c29be`

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

## Implementation contract freeze

`docs/RQ012_HOLDOUT_LEDGER_ACTIVATION_LOCK_IMPLEMENTATION_CONTRACT_FREEZE_2026-09-13.md`

Exact frozen identities:

- engine: `75866d2`
- protocol: `43c29be`

## Implementation closure

- implementation contract commit: `ed04b20`
- implementation commit: `1d35ab3`
- implementation checkpoint: `docs/RQ012_HOLDOUT_LEDGER_ACTIVATION_LOCK_IMPLEMENTATION_2026-09-13.md`
- activation lock: `docs/RQ012_V0_HOLDOUT_ACTIVATION_LOCK_2026-09-13.json`
- prospective boundary: `2026-09-14T07:00:00+07:00`
- holdout outcomes: unopened
- outcome scoring: disabled

RQ-012 tooling scope is complete. Future collection must follow frozen RQ-011 chronologically and remain UNSCORED until its stopping/sealing conditions are satisfied.
