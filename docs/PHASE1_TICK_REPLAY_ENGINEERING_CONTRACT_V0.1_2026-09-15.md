# Phase 1 Tick Replay Engineering Contract V0.1 — 2026-09-15

Status: FROZEN_PRE_OUTCOME_REFERENCE_REPLAY / HOLDOUT_UNSCORED / ORDER_SEND_DISABLED

Contract ID: `PHASE1_TICK_REPLAY_ENGINEERING_V0.1`

## Purpose

Freeze deterministic engineering behavior for tick-level Phase 1 replay before any new historical outcome scoring is opened.

This contract does not change `0700_MINIMAL_V2.0` signal semantics. It only defines how the newly acquired Exness-branded Bid/Ask archive may be transformed into a deterministic replay input and, where explicitly allowed, a reference-execution diagnostic.

Governing evidence/checkpoints:
- `docs/0700_MINIMAL_V2_FROZEN_SPEC_2026-09-13.md`
- `docs/0700_MINIMAL_V2_PRE_OUTCOME_IMPLEMENTATION_FREEZE_2026-09-13.md`
- `docs/0700_HISTORICAL_DATA_READINESS_AND_TEST_STRATEGY_2026-09-13.md`
- `docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md`
- `docs/PHASE1_MT5_CAPABILITY_REPORT_2026-09-14.md`
- `docs/PHASE1_EXNESS_ARCHIVE_ACQUISITION_RECONCILIATION_2015_2026_2026-09-15.md`

## 1. Claim boundary

Allowed:
- deterministic replay mechanics;
- data-quality exclusion behavior;
- signal/run geometry replay;
- reference Bid/Ask quote diagnostics;
- spread observations from recorded Bid/Ask;
- failure/unknown-state discovery.

Not allowed under this contract:
- exact broker fill claims;
- historical slippage claims;
- commission/swap/fee assumptions not evidenced for the replayed event;
- trade/system Win Rate;
- expectancy/profitability;
- automatic order sending;
- holdout outcome scoring.

## 2. Raw archive layer

Classification: OBSERVATION / IMMUTABLE ACQUISITION EVIDENCE.

Rules:
1. Raw ZIP/CSV rows are not rewritten or silently deduplicated.
2. Original timestamp, Bid, Ask, file/month provenance and raw row position remain auditable.
3. No missing tick may be fabricated.
4. No interpolation is allowed across an observed or suspected acquisition gap.
5. The current archive is a separate source identity from the current Exness Demo MT5 route. Exact feed/server equivalence is not established.

## 3. Replay geometry layer

### Geometry quote

Engineering convention:

`REFERENCE_GEOMETRY_QUOTE = BID`

Reason:
- existing Dukascopy historical development data is BID-based;
- the existing Phase 1 bar/state machinery was developed against bar geometry rather than broker fills;
- choosing one deterministic quote is required to reproduce chart/path state without mixing execution spread into source geometry.

This is an engineering representation, not an instructor rule and not a claim that every broker chart/runtime uses an identical feed.

Ask remains retained alongside Bid for spread and reference-execution diagnostics.

### Signal semantics

All origin, PAT2, Daily Frame, PATH_REMAINING, point-check and target semantics remain those of the frozen `0700_MINIMAL_V2.0` specification. This contract does not create new PAT, threshold, location, origin-winner, SL or TP geometry.

## 4. Timestamp ordering and duplicate handling

Observed archive facts:
- current Validator V0.2 records have zero timestamp regressions across all 134 AVAILABLE months;
- equal timestamps and exact consecutive duplicate rows do exist and vary materially by period.

Frozen replay rules:
1. Preserve source row order and a stable raw-row ordinal.
2. Do not drop exact duplicates from raw acquisition.
3. Exact identical rows must be replay-idempotent: once a state transition/fill trigger has fired for a logical event, repeated identical rows cannot create a second independent event merely because the row is duplicated.
4. Equal-timestamp rows with different quotes may be traversed in stable source order for deterministic state updates that do not depend on micro-order.
5. If target-vs-invalidation, stop-vs-target, or another first-touch classification changes depending on the order of distinct rows sharing the same timestamp, return `AMBIGUOUS_SAME_TIMESTAMP`.
6. Source file row order must not be promoted to proof of physical market micro-order inside an equal timestamp.

No tolerance is invented.

## 5. Data-quality and gap handling

Frozen behavior:
- required replay windows crossing a known gap or unresolved archive-boundary gap terminate as `DATA_EXCLUDED_ARCHIVE_GAP`;
- missing pre-state history terminates as `DATA_EXCLUDED_INSUFFICIENT_WARMUP`;
- missing post-event horizon terminates as `DATA_EXCLUDED_INCOMPLETE_HORIZON`;
- unexpected timestamp regression is a hard validation failure;
- no gap is forward-filled or synthetically patched.

Preserved known boundaries:
- 2015-08 begins on 2015-08-10 despite month status AVAILABLE;
- the 2016-03 / 2016-04 archive boundary remains an unresolved gap candidate;
- 2026-09 is partial in the current snapshot and ends on 2026-09-13.

A day/window may still be eligible when all data required by that exact replay window is present; calendar-month completeness is not assumed.

## 6. Confirmation reference versus execution reference

Frozen `0700_MINIMAL_V2.0` research target continues to use:

`confirmation_reference_price = M5 PAT2 close`

That value is a research reference, not a broker fill.

For a separate reference-execution diagnostic only:

`REFERENCE_ENTRY_TICK = first archive tick strictly after confirmation known_at`

- BUY reference entry price = Ask.
- SELL reference entry price = Bid.
- if no qualifying tick exists inside the allowed replay window, return `DATA_EXCLUDED_NO_POST_CONFIRMATION_QUOTE`.

The strict-after rule prevents using the quote that helped form the already-closed confirmation bar as a post-knowledge fill.

Reference entry is not an exact broker fill claim.

## 7. Target / invalidation / stop boundary

### Signal-run lane

The existing Phase 1 signal/run lane remains based on frozen V2 target and point-check geometry.

Point-check is a research invalidation/reference lifecycle concept. It is not silently promoted to a broker stop order.

### Trade stop geometry

Exact trade SL geometry remains unresolved for this replay layer unless an independently frozen source-compatible stop level is supplied.

This contract does NOT invent:
- a fixed-point stop;
- a PAT-derived stop distance;
- a new Point #1 formula;
- any outcome-selected SL.

### Conditional execution mechanics once a stop/TP level is externally frozen

Engineering convention only:
- long stop trigger: Bid <= supplied stop level;
- short stop trigger: Ask >= supplied stop level;
- long take-profit trigger: Bid >= supplied TP level;
- short take-profit trigger: Ask <= supplied TP level;
- reference exit price = the first observed executable-side quote that satisfies the trigger;
- if price gaps beyond a supplied stop, do not fill retrospectively at the ideal stop level;
- if stop and target ordering is unresolved inside one timestamp, return `AMBIGUOUS_SAME_TIMESTAMP`.

These rules define execution mechanics only. They do not choose the stop/TP geometry.

## 8. Spread, cost and slippage treatment

### Spread

DERIVABLE from each archived Bid/Ask row:

`spread = Ask - Bid`

For reference entry/exit diagnostics, spread is already embedded by using the executable quote side. Do not subtract a second synthetic spread charge.

No universal spread constant is allowed.

### Commission / fees / swap

Current multi-year archive does not establish the exact historical account-specific commission, fee or financing schedule for every replayed event.

Status:
`STRUCTURAL_OR_RUNTIME_UNKNOWN / BLOCKING_FOR_ECONOMIC_PNL`

No zero-cost assumption is permitted.

### Slippage

Archive quotes do not reveal the exact historical fill slippage of the current Exness Demo MT5 runtime.

Status:
- historical multi-year slippage: `NOT_YET_REDUCIBLE_FROM_ARCHIVE`;
- future supervised/demo slippage: `RUNTIME_OBSERVABLE`.

Reference fills therefore carry:

`slippage_status = UNMODELED_NOT_ASSUMED_ZERO`

No profitability, expectancy or broker-execution claim may treat the reference quote as a known real fill.

## 9. Replay lanes

### Lane A — signal/run research

Allowed now:
- deterministic state reconstruction;
- TARGET_FIRST / POINT_CHECK_FIRST / AMBIGUOUS / NEITHER-style signal/run ordering under frozen V2 semantics;
- PASS/UNKNOWN/DATA_EXCLUDED taxonomy;
- relation/failure analysis.

This is not trade P&L.

### Lane B — reference-execution diagnostics

Allowed after synthetic contract tests pass:
- first post-confirmation Bid/Ask reference entry;
- observed spread;
- conditional supplied-level trigger mechanics;
- source/feed sensitivity diagnostics.

Outputs must carry the archive source identity and `REFERENCE_NOT_BROKER_FILL` marker.

### Lane C — economic/trade scoring

Disabled.

Requires separate closure of:
- explicit trade stop geometry;
- commission/fee/swap treatment where material;
- slippage/residual execution treatment sufficient for the claim;
- position sizing/risk convention if P&L or supervised pilot use is requested.

## 10. Unknown classification

KNOWN NOW:
- 134/134 current AVAILABLE archive months are Validator V0.2 validated;
- recorded Bid/Ask/timestamp rows;
- archive source identity and hashes;
- symbol point grid from current MT5 capability evidence;
- frozen V2 signal/run semantics.

DERIVABLE:
- per-row spread;
- first post-confirmation reference quote;
- Bid-based geometry path under this engineering convention;
- data-window completeness against recorded boundaries/gap masks.

RUNTIME-OBSERVABLE:
- future current-MT5 spreads;
- future demo/supervised actual fill versus requested/reference quote;
- future execution/deal history.

STRUCTURAL UNKNOWN / BLOCKING FOR TRADE ECONOMICS:
- exact archive-to-current-MT5 feed identity;
- exact trade stop geometry where not independently frozen;
- historical account-specific cost schedule where not evidenced.

NOT-YET-REDUCIBLE FROM CURRENT ARCHIVE:
- historical broker fill slippage for the current target runtime.

## 11. Synthetic/invariant tests required before real tick replay

At minimum:
1. exact duplicate rows do not create duplicate logical triggers;
2. equal-timestamp distinct quotes that reverse first-touch ordering return `AMBIGUOUS_SAME_TIMESTAMP`;
3. BUY reference entry selects first Ask strictly after known_at;
4. SELL reference entry selects first Bid strictly after known_at;
5. no post-confirmation quote -> explicit exclusion;
6. long/short conditional stop trigger uses executable quote side;
7. gap-through stop uses observed executable quote, not ideal stop price;
8. spread equals Ask-Bid and no duplicate spread charge is added;
9. known gap crossing -> `DATA_EXCLUDED_ARCHIVE_GAP`;
10. incomplete horizon -> explicit exclusion;
11. raw rows remain unchanged by replay preparation;
12. archive provenance and `REFERENCE_NOT_BROKER_FILL` survive into replay outputs;
13. slippage is marked unmodeled, never silently zero;
14. no economic P&L/Win Rate field is produced by the reference replay primitive.

## 12. Freeze and version rule

This contract must be committed and pushed before implementing or opening new tick-replay outcomes.

After freeze:
- semantic changes require V0.2+ or an explicit pre-outcome defect-fix checkpoint;
- no historical outcome may be used to choose deduplication, fill, stop, cost, slippage or same-timestamp rules;
- raw acquisition evidence and earlier bar-based V2 history remain preserved.

Freeze declaration:

`PHASE1_TICK_REPLAY_ENGINEERING_V0.1 = FROZEN_PRE_OUTCOME`
