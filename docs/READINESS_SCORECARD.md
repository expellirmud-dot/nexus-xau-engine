# NEXUS XAU Research Readiness Scorecard — Canonical

Last reviewed: 2026-09-01

This scorecard now separates two different measures that had previously been mixed together:

1. **Workflow / conceptual coverage** — how well the project understands the sequence and role of the system components.
2. **Deterministic coding readiness** — how much can be encoded into exact research/backtest rules without guessing missing OHLC/state mechanics.

These are NOT win rates, profit probabilities, or live-EA readiness scores.

## Canonical headline

- **Workflow / conceptual coverage: ~70%**
- **Deterministic coding readiness: ~59%**
- **Remaining deterministic gap: ~41%**

The former ~55% score is retained in historical update files, but the canonical score now uses the dual-metric interpretation because recent direct relative chat + primary images materially improved workflow understanding while exact PAT/PA detector rules remain unresolved.

## Deterministic coding coverage

| Module | Weight | Current coverage | Weighted contribution | Status |
|---|---:|---:|---:|---|
| Broker / symbol / data metadata | 5% | 95% | 4.75 | XAUUSD reference spec strong; server/account metadata must remain runtime-configurable |
| Core cycle / state names | 5% | 90% | 4.50 | SIDEWAY→SIG→TP→พักตัว definitions directly supported; exact transitions still partial |
| SIG anchor / run-distance logic | 10% | 90% | 9.00 | Run table direct; PAT2 Buy candle #3 post-SIG anchor directly clarified; other PAT anchors incomplete |
| PA / PAT1-PAT5 definitions | 15% | 20% | 3.00 | Largest dependency blocker; exact candle geometry still missing |
| Body collection | 10% | 65% | 6.50 | Workflow/lifecycle strong; pair geometry and completion event unresolved |
| Sideway state machine | 10% | 45% | 4.50 | Frame-complete + two-side confirmation + Over-round handling stronger; exact construction/break rules missing |
| Half / swing retrace + Fibonacci | 10% | 75% | 7.50 | Classification + midpoint semantics strong; swing-anchor/extreme/entry/Fib details open |
| Entry / M5 break execution | 10% | 65% | 6.50 | <=200 proximity + M5/M15/M30/H1 workflow strong; exact break geometry unresolved |
| Multi-timeframe relationship | 7% | 50% | 3.50 | TF roles clearer; full conflict matrix and M15/M30 metric incomplete |
| Por Chon / Mae Pla frame algorithms | 7% | 75% | 5.25 | Daily frame + ATH prerequisites materially supported; snapping/timezone/tie-breaks open |
| SL / TP / risk-management mechanics | 5% | 55% | 2.75 | TP ranges direct; 300-point SL example-specific; universal risk logic unresolved |
| Ground-truth labeled examples | 6% | 15% | 0.90 | More direct examples exist, but dataset remains too small for robust validation |

Weighted total = **58.65%**

Rounded deterministic coding readiness = **59%**

## Workflow / conceptual coverage

Analyst estimate = **~70%**.

This higher score reflects that the system-level sequence is now relatively clear:

- XAUUSD environment and runtime symbol metadata;
- frame preparation;
- Daily / Por Chon ATH roles;
- PA location context;
- body-collection workflow;
- SIG / post-SIG anchor / run counting;
- M5/M15/M30/H1 entry relationship;
- Sideway as a distinct setup family;
- TP / Over-round handling;
- Half vs Swing retrace conceptual classification.

The difference between 70% workflow understanding and 59% coding readiness is intentional. Missing PA/PAT definitions affect several downstream modules simultaneously.

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
- Run measured from post-SIG wick.
- PA Buy at support; PA Sell at resistance or TP-complete area.
- Shown PA Buy PAT2: candle #3 post-SIG wick is run/check/SL reference.
- Entry workflow includes <=~200-point frame proximity, M5 break first, M15/M30 same direction, H1 follow-through.
- Half retrace: overrun + opposite PA; post-SIG wick→extreme midpoint.
- Swing retrace: overrun + no opposite PA; qualifying same-direction candle wick→extreme midpoint.
- 50% is reference, not mandatory touch.
- Daily frame: 07:00 H4 context, nearby statistical 0/5 reference, +/-500 points.
- Por Chon ATH: require 1,000-point run from old ATH; H4 highest-price candidate in stated 19:00–19:00 window; no new frame if prerequisites fail; created frame remains in use.
- Sideway: wait frame complete; two-side PA/post-SIG confirmation; nominal TP completion is not automatic reversal because Over-round may continue.

## Conflict / quarantine notes

Do not hard-code until primary evidence resolves them:

- PAT1 single-bar <=50% formula;
- PAT2 fixed generic 2-bar/3-bar formula;
- PAT3 generic move-consolidation-confirm formula;
- generic M5 `close beyond frame` definition;
- generic fixed RR 1:1/1:2;
- universal 10–30 point SL buffer;
- universal 300-point SL;
- Fib 38.2/61.8 as mandatory entry rules;
- prior mixed-source ATH cutoff around `12:00 UTC` — now **UNVERIFIED/CONFLICTING** against stronger primary 19:00–19:00 wording.

## P0 blockers

1. Exact `PA` qualification and `PAT1–PAT5` candle geometry/invalidation/anchors.
2. Exact `M5 break` rule: edge, wick/body/close, buffer and same-candle sequencing.
3. Exact Sideway frame construction/completion and false-break rules.
4. Swing-retrace starting-candle selection and extreme-finalization rule.
5. Exact Daily statistical 0/5 snapping/tie algorithm.
6. Exact ATH 19:00 boundary timezone/day-window semantics.
7. Exact `คู่` geometry and `body_collection_completed()` event.
8. Enough positive + negative labeled historical ground truth.

## Safe to prototype now

- runtime broker/symbol metadata and point conversion;
- replay/data event model;
- cycle/state objects;
- run-distance config;
- source-confirmed SIG anchor storage;
- Daily-frame first-pass calculator with unresolved flags;
- Por Chon ATH candidate-state logic with unresolved time-window flag;
- Half/Swing midpoint calculators and candidate classifier with detector inputs supplied externally;
- Body Collection / Sideway / Entry state-machine shells;
- evidence-tagged replay logging.

## Placeholder-only interfaces

- `detect_PA()`
- `detect_PAT1()` ... `detect_PAT5()`
- `confirm_m5_break()`
- `sideway_frame_complete()`
- `sideway_false_break()`
- `select_swing_retrace_anchor()`
- `detect_pair()`
- `body_collection_completed()`
- universal execution / risk engine

Current engineering stage: **workflow mostly mapped; detector prototype/replay preparation underway; full strategy and live EA still premature.**
