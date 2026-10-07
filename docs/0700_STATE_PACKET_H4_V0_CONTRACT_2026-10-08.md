# 07:00 State Packet H4 V0 Contract — 2026-10-08

Status: FROZEN PRE-IMPLEMENTATION / STATE-ONLY / NO NEW OUTCOME SCORING / HOLDOUT UNSCORED / ORDER SEND DISABLED

Version: `0700_STATE_PACKET_H4_V0`

## Purpose

Build a deterministic, inspectable snapshot for the 07:00 Asia/Bangkok checkpoint
(`00:00 UTC`) without forcing a trade and without using information that becomes
known after the checkpoint.

This contract is state-calculation infrastructure. It does not establish Win Rate,
expectancy, profitability, exact broker execution, or a universal trading rule.

## Scope

V0 is deliberately H4-only because the currently frozen and implemented origin
lane is H4/PAT2/post-SIG. H1 and D1 origin universes are not silently promoted into
this packet.

The packet may expose Daily Frame context as the existing research
representation, but exact universal Frame action qualification remains unknown.

## Temporal boundary

The snapshot may use:

- observations strictly before the checkpoint for origin lifecycle/progress;
- a boundary price observed at the checkpoint for Daily Frame construction,
  explicitly labeled as a runtime boundary observation.

The snapshot must not use later M1/M5 confirmation, later target hit, later
point-check touch, later fill, or later outcome information.

Post-07:00 confirmation is represented only as a requirement/state transition to
wait for future runtime evidence.

## Target semantics

V0 uses the source-reanchored V2.1 H4 fixed-origin target:

- BUY: `origin_anchor + 1500 * PROJECT_POINT_SIZE`
- SELL: `origin_anchor - 1500 * PROJECT_POINT_SIZE`

Remaining nominal run progress and distance from a later confirmation to the fixed
target are distinct quantities. This packet only needs the state known at 07:00.

## Origin lifecycle

For every observed H4 origin in the declared initialization universe, expose:

- origin ID;
- side;
- pattern/origin known time;
- post-SIG anchor;
- fixed-origin target;
- lifecycle at 07:00;
- consumed points at 07:00;
- remaining nominal points;
- first target time if terminal before checkpoint;
- first literal point-check contact time if terminal before checkpoint;
- terminal ordering when known.

Lifecycle values are:

- `ACTIVE`
- `RUN_COMPLETE`
- `POINT_CHECK_DESTROYED`
- `AMBIGUOUS_TERMINAL_SAME_BAR`

Literal observed contact remains the point-check semantic. No age expiry is
introduced.

## Initialization modes

### SOURCE_PURE

Authority: source-faithful research lane.

For current real Exness data, origin history before the proven archive boundary is
not complete. Therefore:

- `origin_set_completeness = UNKNOWN_PREHISTORY`
- `canonical_state_eligibility = FAIL_CLOSED`
- `state_0700 = UNKNOWN`
- reason includes `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`

Observed origins may still be reported for inspection, but they must not be
represented as the complete historical origin universe.

### OPERATIONAL_EXPLICIT_EPOCH

Authority: OWNER-DIRECT PROJECT ENGINEERING CONVENTION.

The operational origin universe begins at an explicitly recorded epoch on one
declared feed identity. Only origins observed from that epoch forward belong to
this operational universe.

This convention:

- does not assert that earlier historical origins did not exist;
- does not change origin expiry/lifecycle semantics;
- does not become instructor/source truth;
- must record the epoch and input data boundary in every packet;
- must fail closed if the supplied data does not cover the declared epoch through
  the checkpoint sufficiently for the implemented calculation.

Completeness wording is:

`COMPLETE_WITHIN_DECLARED_OPERATIONAL_EPOCH`

It is not equivalent to source-pure historical completeness.

## Required packet fields

Top-level:

- `packet_version`
- `checkpoint_utc`
- `checkpoint_thailand`
- `generated_at_utc`
- `scope`
- `source_identity`
- `data_health`
- `initialization`
- `daily_frame`
- `origin_summary`
- `observed_h4_origins`
- `conflict`
- `state_0700`
- `post_0700_requirement`
- `unknowns`
- `guards`

Every material field group must expose an authority/classification such as
`SOURCE_BACKED`, `RUNTIME_OBSERVATION`, `DERIVED_CALCULATION`,
`RESEARCH_REPRESENTATION`, `PROJECT_ENGINEERING_CONVENTION`, or `UNKNOWN`.

No numeric confidence percentage is invented. Confidence is categorical and tied
to the evidence boundary.

## Deterministic state summary

For an operational packet whose data/initialization checks pass:

- active BUY origins only -> `BULLISH_CONTEXT`
- active SELL origins only -> `BEARISH_CONTEXT`
- active BUY and SELL origins -> `MIXED`
- no active origins -> `NO_ACTIVE_ORIGIN`

For SOURCE_PURE with incomplete prehistory -> `UNKNOWN`.

These labels summarize the observed H4 origin state. They are not predictions of
future market direction.

## Conflict semantics

The action lane is unresolved when:

- more than one same-side active origin can materially change action/target; or
- opposite-side active origins coexist.

Expose `PASS_CONFLICT_UNRESOLVED`; do not select the historically best origin.

## Post-07:00 requirement

Minimum terminal/transition states:

- `WAIT_POST_0700_CONFIRMATION`
- `PASS_NO_ACTIVE_ORIGIN`
- `PASS_CONFLICT_UNRESOLVED`
- `PASS_FRAME_TIE`
- `PASS_DATA_UNKNOWN`
- `PASS_INITIALIZATION_UNKNOWN`

Exact universal M1-vs-M5 source routing is not invented in V0. The existing M5
research lane remains separate.

## State-calculation blockers vs downstream blockers

Blocks canonical source-pure state:

- complete origin initialization / prehistory.

Does not block calculation of an operational 07:00 snapshot:

- exact stop price/buffer;
- fills/slippage;
- commission/fee/swap history;
- cross-server execution equivalence;
- position sizing;
- risk cap;
- trade-level P&L;
- expectancy/profitability;
- protected holdout confirmation.

Those remain downstream execution/economic/pilot concerns.

## Guards

- no historical outcome distribution opened for version selection;
- no protected holdout scoring;
- no economic scoring;
- no broker fill inference;
- no automatic order send;
- no PAT3 expansion;
- no H1/D1 origin promotion in V0;
- no invented origin expiry;
- no feed merge without explicit identity/provenance.

## Acceptance

Implementation is accepted only when synthetic tests prove:

1. no post-checkpoint data can alter a packet for that checkpoint;
2. exact point-check touch destroys and near-miss survives;
3. fixed-origin target is V2.1 geometry;
4. target-first / point-check-first / same-bar ambiguity map correctly;
5. source-pure incomplete prehistory fails closed;
6. operational explicit epoch is clearly labeled and deterministic;
7. multiple-origin conflict fails closed for action;
8. Daily Frame context is separated from action qualification;
9. no P&L/Win Rate/expectancy/order-send field appears;
10. a validated real MT5 engineering dataset can produce a 07:00 packet without inspecting later outcomes.
