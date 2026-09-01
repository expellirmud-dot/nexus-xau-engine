# NEXUS XAU Research Readiness Scorecard — Canonical

Last reviewed: 2026-09-01

This scorecard separates two measures:

1. **Workflow / conceptual coverage** — how well the project understands the sequence and role of the system components.
2. **Deterministic coding readiness** — how much can be encoded into exact research/backtest rules without guessing missing OHLC/state mechanics.

These are NOT win rates, profit probabilities, or live-EA readiness scores.

## Canonical headline

- **Workflow / conceptual coverage: ~75%**
- **Deterministic coding readiness: ~63%**
- **Remaining deterministic gap: ~37%**

The increase from the prior 59% canonical coding score comes from new primary training-slide evidence that materially resolves the PAT family map, BUY/SELL topology, and post-SIG reference-candle index. Exact body/wick/close geometry remains unresolved, so PAT is not yet production-deterministic.

## Deterministic coding coverage

| Module | Weight | Current coverage | Weighted contribution | Status |
|---|---:|---:|---:|---|
| Broker / symbol / data metadata | 5% | 95% | 4.75 | XAUUSD reference spec strong; server/account metadata must remain runtime-configurable |
| Core cycle / state names | 5% | 90% | 4.50 | SIDEWAY→SIG→TP→พักตัว definitions directly supported; exact transitions still partial |
| SIG anchor / run-distance logic | 10% | 95% | 9.50 | Run table direct; primary slide now states PAT1→candle2, PAT2→candle3, PAT3→candle4 post-SIG reference counting |
| PA / PAT definitions | 15% | 45% | 6.75 | Primary slide identifies PAT1, PAT2, PAT3 variants 1–3 and mirrored BUY/SELL topology; exact OHLC ratios/invalidation still missing |
| Body collection | 10% | 65% | 6.50 | Workflow/lifecycle strong; pair geometry and completion event unresolved |
| Sideway state machine | 10% | 45% | 4.50 | Frame-complete + two-side confirmation + Over-round handling stronger; exact construction/break rules missing |
| Half / swing retrace + Fibonacci | 10% | 75% | 7.50 | Classification + midpoint semantics strong; swing-anchor/extreme/entry/Fib details open |
| Entry / M5 break execution | 10% | 65% | 6.50 | <=200 proximity + M5/M15/M30/H1 workflow strong; exact break geometry unresolved |
| Multi-timeframe relationship | 7% | 50% | 3.50 | TF roles clearer; full conflict matrix and M15/M30 metric incomplete |
| Por Chon / Mae Pla frame algorithms | 7% | 75% | 5.25 | Daily frame + ATH prerequisites materially supported; snapping/timezone/tie-breaks open |
| SL / TP / risk-management mechanics | 5% | 55% | 2.75 | TP ranges direct; 300-point SL example-specific; universal risk logic unresolved |
| Ground-truth labeled examples | 6% | 20% | 1.20 | Primary schematic positives now exist for five PA shapes, but historical positive/negative chart dataset remains too small |

Weighted total = **63.20%**

Rounded deterministic coding readiness = **63%**

## Workflow / conceptual coverage

Analyst estimate = **~75%**.

The system-level sequence is now relatively clear, and the PAT family map is no longer fully unknown:

- target XAUUSD environment and runtime metadata;
- frame preparation;
- Daily / Por Chon ATH roles;
- PA location context;
- visible PA pattern families: PAT1, PAT2, PAT3 variant 1/2/3;
- body-collection workflow;
- SIG / post-SIG reference / run counting;
- M5/M15/M30/H1 entry relationship;
- Sideway setup family;
- TP / Over-round handling;
- Half vs Swing retrace classification.

The gap between workflow understanding and coding readiness remains because visual topology is not the same as an exact OHLC detector.

## Strongly supported rules now

- Target instrument: `XAUUSD`; do not substitute `XAUUSDc`.
- Reference MT5 spec: Digits 2, Tick size 0.01, Contract size 100, Tick value 0.1, Bid chart mode.
- Server may vary by account; do not hard-code `Exness-MT5Real36` as a strategy rule.
- Primary trading SIG TFs from relative: H1/H4/D/W.
- Candle being evaluated must close before confirmation.
- Core cycle: `SIDEWAY → SIG → TP → พักตัว → SIDEWAY`.
- H1 run = 1,000 points.
- H4 = 1,500 (100%) toward 3,000.
- Day = 5,000–10,000; Week = 15,000–30,000; MN = 30,000–50,000.
- Run measured from post-SIG wick/reference.
- PA Buy at support; PA Sell at resistance or TP-complete area.
- Primary slide shows five PA shapes total: `PAT1`, `PAT2`, `PAT3 รูปแบบที่ 1`, `PAT3 รูปแบบที่ 2`, `PAT3 รูปแบบที่ 3`.
- BUY and SELL pattern rows are directional mirrors around support/resistance context.
- Primary slide explicitly states post-SIG reference counting: `PAT1 นับแท่งที่ 2`, `PAT2 นับแท่งที่ 3`, `PAT3 นับแท่งที่ 4`.
- Entry workflow includes <=~200-point frame proximity, M5 break first, M15/M30 same direction, H1 follow-through.
- Half retrace: overrun + opposite PA; post-SIG wick→extreme midpoint.
- Swing retrace: overrun + no opposite PA; qualifying same-direction candle wick→extreme midpoint.
- 50% is reference, not mandatory touch.
- Daily frame: 07:00 H4 context, nearby statistical 0/5 reference, +/-500 points.
- Por Chon ATH: require 1,000-point run from old ATH; H4 highest-price candidate in stated 19:00–19:00 window; no new frame if prerequisites fail; created frame remains in use.
- Sideway: wait frame complete; two-side PA/post-SIG confirmation; nominal TP completion is not automatic reversal because Over-round may continue.

## Conflict / quarantine notes

Do not hard-code until primary evidence resolves them:

- prior assumption that the system has separately numbered `PAT1–PAT5`; the new primary slide instead shows five shapes as PAT1 + PAT2 + three PAT3 variants;
- PAT1 generic single-bar <=50% formula;
- PAT2 generic 50%-body rule;
- PAT3 generic move-consolidation-confirm threshold rule;
- generic M5 `close beyond frame` definition;
- generic fixed RR 1:1/1:2;
- universal 10–30 point SL buffer;
- universal 300-point SL;
- Fib 38.2/61.8 as mandatory entry rules;
- prior mixed-source ATH cutoff around `12:00 UTC` — **UNVERIFIED/CONFLICTING** against stronger primary 19:00–19:00 wording.

## P0 blockers

1. Exact PA/PAT OHLC geometry: body ratio, wick ratio, open/close relations, support/resistance tolerance and invalidation for PAT1, PAT2 and PAT3 variants 1–3.
2. Exact `M5 break` rule: edge, wick/body/close, buffer and same-candle sequencing.
3. Exact Sideway frame construction/completion and false-break rules.
4. Exact `คู่` geometry and `body_collection_completed()` event.
5. Swing-retrace starting-candle selection and extreme-finalization rule.
6. Half/Swing entry and invalidation rules plus whether any Fib levels other than 50% are operational.
7. Exact Daily statistical 0/5 snapping/tie algorithm.
8. Exact ATH 19:00 boundary timezone/day-window semantics.
9. Enough positive + negative labeled historical ground truth.

## Safe to prototype now

- runtime broker/symbol metadata and point conversion;
- replay/data event model;
- cycle/state objects;
- run-distance config;
- PAT family data model: `PAT1`, `PAT2`, `PAT3.variant={1,2,3}`;
- source-backed `post_sig_reference_index`: PAT1=2, PAT2=3, PAT3=4;
- topology-only PAT candidate labeling with `CANDIDATE_ONLY` status;
- source-confirmed SIG anchor storage;
- Daily-frame first-pass calculator with unresolved flags;
- Por Chon ATH candidate-state logic with unresolved time-window flag;
- Half/Swing midpoint calculators and candidate classifier with detector inputs supplied externally;
- Body Collection / Sideway / Entry state-machine shells;
- evidence-tagged replay logging.

## Placeholder / candidate-only interfaces

- `detect_PA_exact()`
- `detect_PAT1_exact()`
- `detect_PAT2_exact()`
- `detect_PAT3_v1_exact()`
- `detect_PAT3_v2_exact()`
- `detect_PAT3_v3_exact()`
- `confirm_m5_break()`
- `sideway_frame_complete()`
- `sideway_false_break()`
- `select_swing_retrace_anchor()`
- `detect_pair()`
- `body_collection_completed()`
- universal execution / risk engine

Current engineering stage: **workflow substantially mapped; topology-level PAT detector prototypes are now justified; exact OHLC signal detector and full historical backtest still require unresolved geometry and negative examples.**
