# Phase 1 Exness Archive Window Adapter Contract V0.1 — 2026-09-15

Status: FROZEN_PRE_IMPLEMENTATION / NO STRATEGY OUTCOME OPENED

Contract ID: `PHASE1_EXNESS_ARCHIVE_WINDOW_ADAPTER_V0.1`

Depends on:
- `docs/PHASE1_TICK_REPLAY_ENGINEERING_CONTRACT_V0.1_2026-09-15.md`
- `docs/PHASE1_EXNESS_ARCHIVE_ACQUISITION_RECONCILIATION_2015_2026_2026-09-15.md`

## Purpose

Define a reusable, bounded adapter from validated monthly Exness archive ZIP files to the frozen tick replay primitives without loading or mutating more data than the requested window requires.

This contract is data engineering only. It does not select signals or score outcomes.

## Window semantics

Frozen request interval:

`[start_utc, end_utc)`

- start is inclusive;
- end is exclusive;
- both must be timezone-aware;
- both are normalized to UTC;
- end must be strictly greater than start.

Reason:
half-open windows compose without double-counting a boundary tick and do not require an invented equality tolerance.

## Month selection

The adapter selects every calendar month intersecting the requested half-open interval.

Every selected month must have a latest manifest record satisfying:
- symbol matches request;
- `status = VALIDATED`;
- `validator_version = EXNESS_ARCHIVE_VALIDATOR_V0.2`;
- local ZIP exists;
- local ZIP byte size matches the validated manifest record.

If any required month fails this gate, the window is excluded. No network download is triggered by the replay adapter.

## ZIP/CSV reading

- stream directly from the ZIP;
- do not extract a temporary CSV;
- require exactly one CSV member;
- require normalized header:
  `Exness, Symbol, Timestamp, Bid, Ask`;
- stop scanning a month once timestamps reach the requested exclusive end;
- provider/symbol/finite/Ask>=Bid invariants are rechecked for rows actually admitted to the window.

The adapter trusts the persisted month SHA from the validated manifest and carries it as provenance. It does not re-hash an entire ZIP on every bounded read.

## Raw-row identity

Each admitted tick carries:
- source year/month;
- source ZIP SHA-256;
- zero-based raw data-row ordinal within that month's CSV after the header;
- Bid;
- Ask;
- UTC timestamp.

Raw ordinal is an engineering audit coordinate only.

## Duplicate and timestamp behavior

- no deduplication;
- equal timestamps are preserved;
- exact duplicate rows are preserved;
- source order is preserved;
- timestamp regression inside admitted rows is a hard error;
- replay-level ambiguity/idempotence remains governed by the frozen tick replay contract.

## Known-gap mask

Machine-readable gap evidence:
`docs/PHASE1_EXNESS_ARCHIVE_GAP_LEDGER_V0.1.json`

A boundary-gap candidate is represented by:
- `last_observed_before_gap`;
- `first_observed_after_gap`;
- open interval semantics between those observed endpoints.

The adapter excludes a requested window if it intersects the open interval between the two observed endpoints.

No microsecond offset or fabricated gap boundary is introduced.

Current ledger initially contains the unresolved 2016 March/April boundary candidate only.

Absence from the known-gap ledger is NOT proof of full tick continuity.

Adapter output must carry:

`continuity_status = KNOWN_GAPS_ENFORCED_FULL_CONTINUITY_NOT_PROVEN`

## Coverage boundaries

The current acquisition snapshot has:
- earliest observed tick: `2015-08-10T00:00:00Z`;
- latest observed tick: `2026-09-13T23:59:59.824Z`.

A request before the earliest observed tick is excluded as insufficient warmup/coverage.
A request whose required horizon extends beyond the latest observed tick is excluded as incomplete horizon.

This does not turn ordinary market-closed intervals inside the covered span into gaps.

## Empty windows

If a structurally eligible requested window contains zero archived ticks:

- return an empty replay frame;
- report `NO_TICKS_OBSERVED_IN_WINDOW`;
- do not infer whether the cause was market closure or missing source data.

A caller requiring a tick must fail closed separately.

## Output boundary

The adapter returns raw replay input/provenance only.

It must not output:
- signal decisions;
- target/stop outcomes;
- P&L;
- Win Rate;
- broker fill claims.

## Synthetic tests required before archive smoke

At minimum:
1. half-open boundary inclusion/exclusion;
2. multi-month selection;
3. missing/non-current manifest month exclusion;
4. raw ordinal preservation;
5. duplicate preservation;
6. equal-timestamp preservation;
7. known boundary-gap intersection exclusion;
8. request ending exactly at left observed gap endpoint remains eligible;
9. request starting exactly at right observed gap endpoint remains eligible;
10. request outside current earliest/latest acquisition boundary is excluded;
11. empty eligible window returns explicit no-ticks status;
12. manifest SHA/month provenance survives output.

Freeze declaration:

`PHASE1_EXNESS_ARCHIVE_WINDOW_ADAPTER_V0.1 = FROZEN_PRE_IMPLEMENTATION`
