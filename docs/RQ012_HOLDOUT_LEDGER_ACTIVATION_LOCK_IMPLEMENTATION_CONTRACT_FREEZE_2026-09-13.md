# RQ-012 — V0.1 Holdout Ledger + Activation-Lock Implementation Contract Freeze

Date: 2026-09-13 Asia/Bangkok  
Status: `IMPLEMENTATION_CONTRACT_FROZEN_PRE_CODE`

## Frozen dependencies

- Engine freeze commit: `75866d2` — `engine: freeze deterministic Mode2 signal-run V0`
- RQ-011 protocol freeze commit: `43c29be` — `research: freeze pristine V0 holdout protocol`
- Engine/schema identity: `SIG_MODE2_SIGNAL_RUN_V0.1`
- Protocol authority: `docs/RQ011_PRISTINE_V0_HOLDOUT_PROTOCOL_2026-09-09.md`

This contract implements audit/activation tooling only. It must not alter V0.1 signal/run semantics or inspect prospective outcomes.

## 1. Canonical ledger representation

Ledger storage is newline-delimited canonical JSON: one complete JSON object per line.

Canonical serialization for hashing is UTF-8 JSON with:

- keys sorted recursively;
- separators exactly `,` and `:` with no insignificant whitespace;
- `ensure_ascii=False`;
- no NaN/Infinity values.

Each record contains exactly these chain fields plus protocol payload fields:

```text
record_index
checkpoint_time
record_created_at
record_type
visible_data_until
payload
previous_record_sha256
record_sha256
engine_version
protocol_version
```

`record_sha256` is SHA256 over the canonical JSON bytes of the record with the `record_sha256` field omitted.

For record 0, `previous_record_sha256` is 64 zeroes. Every later record must reference the immediately preceding `record_sha256`.

## 2. Append-only writer

The writer must:

- create a new ledger or append exactly one next record;
- reject a supplied/derived `record_index` that is not the next contiguous index;
- verify the complete existing chain before append;
- reject duplicate index, reordering, mutation, malformed hash, or malformed JSON;
- never rewrite prior ledger bytes as part of a normal append;
- write a final newline after each canonical record.

Corrections are new records; historical records are never replaced.

## 3. Fail-closed verifier

Verification must fail on:

- non-canonical or invalid JSON record;
- non-contiguous `record_index`;
- wrong genesis previous hash;
- broken `previous_record_sha256`;
- incorrect `record_sha256`;
- duplicate/reordered records;
- empty/missing required identity fields;
- protocol/engine version drift within one ledger identity.

A valid empty ledger may be reported as empty but cannot be treated as sealed or activation-ready.

## 4. Activation lock

Activation lock is canonical JSON and records at minimum:

```text
lock_schema_version
engine_schema_version
engine_freeze_commit
protocol_freeze_commit
activation_created_at
prospective_boundary
timezone
outcome_scoring_enabled
ledger_path
environment
```

Frozen values:

- `lock_schema_version = HOLDOUT_ACTIVATION_LOCK_V0.1`
- `engine_schema_version = SIG_MODE2_SIGNAL_RUN_V0.1`
- `engine_freeze_commit = 75866d2`
- `protocol_freeze_commit = 43c29be`
- `timezone = Asia/Bangkok`
- `outcome_scoring_enabled = false`

The prospective boundary must be exactly a 07:00 Asia/Bangkok instant and strictly after the protocol freeze commit time. RQ-012 may reserve this boundary without reading any post-boundary outcome.

The lock validator must fail closed if either commit identity changes, scoring is enabled, the boundary is not timezone-aware/07:00 Asia/Bangkok, or required environment metadata is missing.

## 5. Required environment metadata

The lock must carry a mapping containing non-empty values for:

- broker_server
- symbol
- data_side
- digits
- point
- tick_size
- source_export_method
- timezone_normalization_method

Raw-file SHA256 and first/last timestamps belong to dataset sealing/collection records when those files exist; this implementation must not fabricate them before collection.

## 6. CLI / API scope

RQ-012 implementation may expose pure Python APIs and a small command-line entry point for:

- append;
- verify;
- create/validate activation lock.

No command may score V0.1 outcomes.

## 7. Tests required before activation-ready status

At minimum:

1. valid genesis + append chain;
2. tamper detection;
3. duplicate/reordered index rejection;
4. previous-hash mismatch rejection;
5. non-canonical/malformed record rejection;
6. activation-lock valid case;
7. wrong engine/protocol commit rejection;
8. scoring-enabled rejection;
9. invalid prospective-boundary rejection;
10. missing environment metadata rejection.

## 8. Holdout status boundary

Passing these tooling tests means only:

`RESERVED_OR_COLLECTION_READY / UNSCORED`

It does not mean:

- holdout outcomes were opened;
- sample collection is complete;
- V0.1 is profitable;
- any trade/system Win Rate is established.

## Decision

This contract is frozen before RQ-012 implementation code. Any semantic change to chain hashing, activation identity, eligibility, horizon, target, tick handling, or outcome scoring requires a new explicit version/checkpoint rather than silent modification.
