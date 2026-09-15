# Phase 1 V2 Origin-State Carry Contract V0.1 — 2026-09-15

Status: FROZEN_PRE_IMPLEMENTATION / PRE-OUTCOME / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract ID: `PHASE1_V2_ORIGIN_STATE_CARRY_V0.1`

## Purpose

Define a restart-safe continuation state for frozen `0700_MINIMAL_V2.0` without inventing a warmup, changing origin lifecycle semantics, or allowing an incomplete historical seed to become complete merely because replay advances.

This contract addresses sequential replay after a seed state exists. It does not by itself solve unknown prehistory.

## Governing inputs

- `docs/0700_MINIMAL_V2_FROZEN_SPEC_2026-09-13.md`
- `docs/PHASE1_ARCHIVE_V2_INTEGRATION_CONTRACT_V0.2_2026-09-15.md`
- `docs/PHASE1_ORIGIN_HISTORY_INITIALIZATION_AUDIT_2026-09-15.md`
- `src/nexus_xau/research/minimal_v2_0700.py`
- `src/nexus_xau/replay/v2_integration.py`

## Derived sufficiency result

Current V2 Daily Frame construction is local to the cutoff price and does not require unbounded historical state.

V2 origin continuation can therefore be finite once a complete seed exists, provided active-origin state and detector-boundary context are both preserved.
## Seed-completeness invariant

Every carry checkpoint MUST declare one of:

- `COMPLETE`: all active origins at the checkpoint are proven represented;
- `SYNTHETIC_COMPLETE`: completeness is known by controlled fixture construction only;
- `UNKNOWN_PREHISTORY`: at least one pre-boundary origin may be missing.

Completeness is monotonic under ordinary forward continuation:

`UNKNOWN_PREHISTORY -> UNKNOWN_PREHISTORY`

A checkpoint created from `UNKNOWN_PREHISTORY` MUST NOT become `COMPLETE` solely because additional future M1 data were observed or because another checkpoint was written.

Promotion to `COMPLETE` requires independent evidence that closes the missing prehistory and recomputation/verification of the state from that evidence.

This invariant falsifies the idea that checkpointing alone can cure the current `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED` blocker.

## Active-origin carry state

For each origin that is `ACTIVE` at checkpoint time, preserve at minimum:

- `origin_id`;
- `side`;
- `pattern_known_at`;
- `origin_known_at`;
- `anchor_price`;
- `consumed_points_at_checkpoint`.
`consumed_points_at_checkpoint` is the historical maximum favorable excursion already observed for that origin under frozen V2 semantics.

Forward continuation updates it as:

`max(prior_consumed_points, favorable_excursion_observed_after_checkpoint)`

Only active origins are required for future eligibility. Terminal origins are historical audit evidence but do not need to be reactivated or carried as eligible state.

An active-origin record implies that, before the checkpoint, neither target completion nor literal point-check contact occurred first and no same-bar terminal ambiguity remains unresolved for that origin.

## Detector-boundary bridge

Origin state alone is insufficient because PAT detection can straddle the checkpoint boundary.

The checkpoint therefore preserves the exact observed M1 bridge:

`[checkpoint_at - 8 hours, checkpoint_at)`

with no synthetic bars, interpolation, or feed relabeling.

Eight hours is an engineering derivation from the frozen detector topology, not a market warmup:

- two completed H4 bars are sufficient to detect an H4 PAT whose event becomes known at the checkpoint and whose post-SIG bar completes after it;
- the same bridge contains the immediately preceding M5 bar required for an M5 PAT confirmation whose event becomes known just after the checkpoint.

This bridge is detector context only. It does not assert that eight hours is enough to reconstruct older active origins.
## Checkpoint boundary

`checkpoint_at` MUST be an exact 4-hour UTC boundary.

The bridge ends exactly at `checkpoint_at`; continuation M1 begins at or after `checkpoint_at`. Overlap outside the declared bridge or silent holes at the handoff are not allowed.

Known archive gaps retain their existing fail-closed authority. The carry layer MUST NOT fill or fabricate missing minutes.

## Provenance envelope

Every checkpoint MUST preserve:

- carry contract/version;
- frozen V2 version;
- archive/integration representation version;
- checkpoint UTC timestamp;
- seed-completeness state;
- source family and symbol;
- M1 representation;
- bridge source provenance and digest;
- active-origin rows;
- prior checkpoint digest/reference when continuation is chained.

A deterministic checkpoint digest MUST cover the semantic payload so a later restart can detect mutation or version mismatch.

## Cross-feed guard

A checkpoint MUST NOT silently change source family.

`DUKASCOPY -> EXNESS_BRANDED_ARCHIVE` or any other feed transition requires a separately frozen transition/sensitivity contract.

Cross-feed availability does not establish feed identity. Until transition sensitivity is closed, a Dukascopy-derived state cannot be relabeled as Exness-derived canonical state.
## Runtime eligibility

A `CONTINUATION_CHECKPOINT` may enter canonical V2 continuation only when:

- checkpoint semantic/version validation passes;
- source/provenance compatibility passes;
- checkpoint digest validation passes;
- `seed_completeness == COMPLETE`.

`SYNTHETIC_COMPLETE` remains limited to controlled logic fixtures.

`UNKNOWN_PREHISTORY` MUST fail closed as `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`; carrying that state forward is allowed for engineering inspection but does not authorize canonical day/candidate state.

Therefore the current earliest Exness archive boundary cannot be converted into a complete checkpoint under this contract.

## Required pre-implementation tests

Before real continuation is enabled:

1. full synthetic replay and split replay from a complete checkpoint produce identical post-checkpoint V2 state;
2. consumed progress before the checkpoint is preserved and future favorable excursion updates by maximum, not reset;
3. multiple same-side and opposite-side active origins survive the checkpoint independently;
4. exact point-check contact after restart terminates the carried origin;
5. target completion after restart terminates the carried origin;
6. same-bar target/point-check remains ambiguous;
7. H4 PAT/origin creation straddling the checkpoint matches unsplit replay;
8. earliest post-checkpoint M5 PAT confirmation matches unsplit replay;9. `UNKNOWN_PREHISTORY` cannot promote itself to `COMPLETE` through forward continuation;
10. checkpoint digest mutation is rejected;
11. V2/carry semantic-version mismatch is rejected;
12. bridge provenance mismatch is rejected;
13. source-family transition is rejected unless separately authorized;
14. no P&L, Win Rate, expectancy, broker-fill, or order-send field is introduced.

## Falsification target

This contract is invalid if synthetic split replay cannot reproduce unsplit V2 state using only:

- active-origin carry state;
- the declared eight-hour detector bridge;
- post-checkpoint M1 data;
- current cutoff price data already present in post-checkpoint M1.

If parity fails, inspect the exact missing historical dependency and revise the contract before any real replay.

## Non-goals

- proving the current Exness initial state complete;
- choosing an origin winner;
- adding origin expiry;
- creating a finite market warmup;
- treating Dukascopy and Exness as the same feed;
- revealing protected holdout outcomes.

## Next implementation step

Implement the minimal serialized carry object and synthetic split-parity harness only. Keep real Exness continuation blocked until an independently defensible complete seed or separately authorized feed-transition route exists.