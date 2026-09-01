# NEXUS XAU Research Readiness Scorecard — Canonical

Last reviewed: 2026-09-01

This scorecard separates two measures:

1. **Workflow / conceptual coverage** — how well the project understands the sequence and role of the system components.
2. **Deterministic coding readiness** — how much can be encoded into exact research/backtest rules without guessing missing OHLC/state mechanics.

These are NOT win rates, profit probabilities, or live-EA readiness scores.

## Canonical headline

- **Workflow / conceptual coverage: ~82%**
- **Deterministic coding readiness: ~71%**
- **Remaining deterministic gap: ~29%**

The increase from the prior 75% / 63% score comes from primary timestamp-transcript evidence that closes or materially narrows: PAT candle-count semantics, PAT2 non-engulf behavior and ~50% close concept, PAT1/PAT2/PAT3 post-SIG reference indexes, no-wick anchor fallback, PA location qualification, overlapping PAT parsing, post-SIG invalidation/replacement behavior, explicit positive/negative ground truth, and the critical semantic distinction between system `เบรก` (brake/stop at frame in this lesson) and generic English `breakout`.

Exact PAT3 geometry, PAT2 50% denominator/tolerance, PAT1 quantitative wick/body geometry, M5 brake geometry, sideway construction, `ยืนกรอบ`, and several frame/MTF edge rules remain unresolved, so the engine is still not production-deterministic.

## Deterministic coding coverage

| Module | Weight | Current coverage | Weighted contribution | Status |
|---|---:|---:|---:|---|
| Broker / symbol / data metadata | 5% | 95% | 4.75 | XAUUSD reference spec strong; server/account metadata must remain runtime-configurable |
| Core cycle / state names | 5% | 95% | 4.75 | SIG→TP→พัก→Sideway lifecycle and replacement/re-evaluation behavior materially stronger; exact Sideway transitions still partial |
| SIG anchor / run-distance logic | 10% | 98% | 9.80 | PAT1→2, PAT2→3, PAT3→4 directly supported; no-wick fallback Buy=low / Sell=high now primary transcript evidence |
| PA / PAT definitions | 15% | 70% | 10.50 | Family map, candle counts, location, PAT2 non-engulf + ~50% close, overlapping labels and invalidation now direct; exact OHLC geometry still open |
| Body collection | 10% | 65% | 6.50 | Workflow/lifecycle strong; `คู่` geometry and exact completion event unresolved |
| Sideway state machine | 10% | 60% | 6.00 | SIG-in-sideway, post-SIG destruction, invalid PA→Sideway and no fixed duration now supported; exact frame construction/completion remains open |
| Half / swing retrace + Fibonacci | 10% | 78% | 7.80 | 50% reference strong; 61.8 now directly mentioned as optional watched zone; exact swing anchor/extreme/entry still open |
| Entry / M5 brake execution | 10% | 55% | 5.50 | Major semantic correction: `เบรก` cannot be assumed breakout; live M5 stand-on-line example exists, but exact brake/stop detector still missing |
| Multi-timeframe relationship | 7% | 65% | 4.55 | PA every TF, SIG H1+, H4/H1 relationship and larger-TF strength clearer; full conflict matrix incomplete |
| Por Chon / Mae Pla frame algorithms | 7% | 75% | 5.25 | Daily frame + ATH prerequisites materially supported; snapping/timezone/tie-breaks open |
| SL / TP / risk-management mechanics | 5% | 60% | 3.00 | TF run distances, H4+ TP2/tight-round concept and example SL anchors stronger; universal risk rules unresolved |
| Ground-truth labeled examples | 6% | 40% | 2.40 | Primary schematic positives plus explicit transcript invalid→replace five-candle case; historical dataset still too small |

Weighted total = **70.80%**

Rounded deterministic coding readiness = **71%**

## Workflow / conceptual coverage

Analyst estimate = **~82%**.

The system-level sequence is now relatively clear and PA/PAT is no longer a mostly unknown subsystem:

- target XAUUSD environment and runtime metadata;
- frame preparation and 0/5 location context;
- PA can occur on any TF; SIG terminology/qualification is H1+;
- visible PA pattern families: PAT1, PAT2, PAT3 variant 1/2/3;
- PAT means candle-count family;
- PAT2 is two candles and does not require full engulfing;
- PAT2 second-candle close is assessed around 50% of candle #1, with exact denominator still unresolved;
- patterns may overlap in the same candle region rather than being mutually exclusive;
- post-SIG mapping: PAT1→2, PAT2→3, PAT3→4;
- no-wick post-SIG fallback uses Buy low / Sell high;
- invalid post-SIG that disturbs/exceeds PA can invalidate the set, push interpretation to Sideway, and allow a new PA/SIG to replace it;
- body-collection workflow;
- run/TP counting and H4+ TP2 (`ตึงรอบ`) concept;
- Sideway/SIG interaction;
- Half vs Swing retrace classification and purpose-specific Fibonacci usage;
- larger-TF context / H4-H1 relationship;
- teacher-driven requirement to backtest and record behavior rather than trust rules by assertion.

The remaining gap is now concentrated in **exact geometry, state boundaries, and edge-case arbitration**, not broad workflow discovery.

## Strongly supported rules now

- Target instrument: `XAUUSD`; do not substitute `XAUUSDc`.
- Reference MT5 spec: Digits 2, Tick size 0.01, Contract size 100, Tick value 0.1, Bid chart mode.
- Server may vary by account; do not hard-code `Exness-MT5Real36` as a strategy rule.
- PA can occur on all timeframes; the course repeatedly uses `SIG` from H1 upward.
- Primary operational SIG set from owner-relative evidence remains H1/H4/D/W; Month is still SIG-capable in the lesson's broader H1+ terminology/run table.
- Candle being evaluated must close before confirmation.
- Broad cycle: `SIG → TP → พักตัว → SIDEWAY`, while rest/Sideway ordering can vary.
- H1 run = 1,000 points.
- H4 = 1,500 (TP1 / 100%) toward 3,000 (TP2 / tight-round).
- Day = 5,000–10,000; Week = 15,000–30,000; MN = 30,000–50,000 from cleaner primary visual evidence where transcript OCR drops zeros.
- Run measured from post-SIG wick/reference.
- PA Buy belongs at support; PA Sell belongs at resistance / correct upper context. Same geometry at the wrong location can reverse the interpretation.
- Primary slide + transcript show five PA shapes total: `PAT1`, `PAT2`, `PAT3 รูปแบบที่ 1`, `PAT3 รูปแบบที่ 2`, `PAT3 รูปแบบที่ 3`.
- `PAT` denotes candle-count family: PAT1 one candle, PAT2 two candles, PAT3 three candles.
- PAT2 does not require full engulfing.
- PAT2 candle #2 should close around the 50% level of candle #1; exact denominator/tolerance remains unresolved.
- BUY/SELL pattern rows are directional mirrors around valid support/resistance context.
- Post-SIG reference counting: `PAT1=2`, `PAT2=3`, `PAT3=4`.
- If the post-SIG counting candle lacks the relevant wick, Buy uses its low and Sell uses its high as fallback reference.
- PAT parsing may overlap: a three-candle region can support PAT3 while candles 2+3 also form PAT2.
- A post-SIG wick/reference that goes beyond/disturbs the PA is invalid; the set may transition to Sideway/re-evaluation.
- Explicit five-candle teaching example shows invalid old PAT2/post-SIG followed by new PAT2 and a new valid post-SIG reference.
- A destroyed post-SIG reference requires waiting/re-evaluating for a new setup; the ~200-point destruction shown is example-specific, not a universal threshold.
- PAT family does not change the TF run distance; PAT3 and PAT2 have the same TP framework on the same TF.
- System term `เบรก` in this introductory lesson means brake/stop at a frame, judged with M1/M5; do not equate it automatically with English breakout. Continued movement is described as `เจิด`.
- Half retrace: overrun + opposite PA; post-SIG wick→extreme midpoint.
- Swing retrace: overrun + no opposite PA; qualifying same-direction candle wick→extreme midpoint.
- 50% is a reference, not mandatory touch.
- 61.8 is directly mentioned as a possible watched Fibonacci zone, but not established as a mandatory universal rule.
- Fibonacci use is purpose-specific: entry, exit or countertrade must be defined before drawing it.
- Daily frame: 07:00 H4 context, nearby statistical 0/5 reference, +/-500 points.
- Por Chon ATH: require 1,000-point run from old ATH; H4 highest-price candidate in stated 19:00–19:00 window; no new frame if prerequisites fail; created frame remains in use.
- Sideway: post-SIG destruction/invalid PA can lead to Sideway; SIGs inside Sideway (`ซิกชนซิ`) do not have ordinary full-run space; duration is not fixed.

## Conflict / quarantine notes

Do not hard-code until primary evidence resolves them:

- prior assumption that the system has separately numbered `PAT1–PAT5`; strongest primary evidence shows PAT1 + PAT2 + three PAT3 variants;
- PAT1 generic single-bar `body <=50%` formula;
- PAT2 generic `body2 >=50% of body1` formula — primary transcript instead says candle #2 **closes around the 50% level of candle #1**;
- PAT3 generic move-consolidation-confirm threshold formula;
- generic M5 `close beyond frame` / breakout definition — **semantic conflict** with primary transcript use of `เบรก = brake/stop` in this lesson;
- treating the ~300-point frame overshoot discussion as a universal break threshold;
- treating ~200-point post-SIG destruction example as a universal invalidation threshold;
- generic fixed RR 1:1/1:2;
- universal 10–30 point SL buffer;
- universal 300-point SL;
- Fib 38.2 or 61.8 as mandatory entry rules; 61.8 is now source-mentioned but optional/contextual here;
- prior mixed-source ATH cutoff around `12:00 UTC` — **UNVERIFIED/CONFLICTING** against stronger primary 19:00–19:00 wording.

## P0 blockers

1. Exact PAT3 variant 1/2/3 OHLC geometry: body relations, wick relations, close thresholds and per-variant invalidation.
2. PAT2 50% exact denominator and tolerance: prior-candle body vs full range, `>=` vs approximate zone, and equality handling.
3. PAT1 quantitative wick/body qualification and exact support/resistance touch tolerance.
4. Exact dedicated M5 `เบรก`/brake rule: what constitutes stopping, which frame edge, wick/body/close, timing and `เจิด` transition.
5. Exact `ยืนกรอบ` candle-reading predicate.
6. Exact Sideway frame construction/completion and false-break/exit rules.
7. Enough positive + negative labeled historical ground truth to validate geometry thresholds.

## P1 blockers

1. Exact `คู่` geometry and `body_collection_completed()` event.
2. Swing-retrace starting-candle selection and extreme-finalization rule.
3. Half/Swing entry and invalidation rules; classify 61.8 as contextual until dedicated lesson proves stronger use.
4. Exact Daily statistical 0/5 snapping/tie algorithm.
5. Exact ATH 19:00 boundary timezone/day-window semantics.
6. Complete timeframe conflict matrix: H1/H4/D/W plus exact M15/M30 same-direction metric.

## Safe to prototype now

- runtime broker/symbol metadata and point conversion;
- replay/data event model;
- cycle/state objects including `INVALIDATED -> REEVALUATE -> NEW_PA/NEW_SIG`;
- run-distance config;
- PAT family data model: `PAT1`, `PAT2`, `PAT3.variant={1,2,3}`;
- overlapping candidate labels over the same candle windows;
- source-backed `post_sig_reference_index`: PAT1=2, PAT2=3, PAT3=4;
- no-wick SIG-anchor fallback;
- PAT2 candidate feature `close_near_prior_50pct` with denominator explicitly unresolved/configurable;
- location qualification flags (`AT_SUPPORT`, `AT_RESISTANCE`, `WRONG_LOCATION`);
- post-SIG disturbance/invalidation state shell;
- explicit semantic enum separating `BRAKE_AT_FRAME` from `BREAKOUT`;
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
- `close_near_prior_50pct_exact()`
- `post_sig_disturbs_pa_exact()`
- `confirm_m5_brake()`
- `detect_jerid_continuation()`
- `frame_standing_exact()`
- `sideway_frame_complete()`
- `sideway_false_break()`
- `select_swing_retrace_anchor()`
- `detect_pair()`
- `body_collection_completed()`
- universal execution / risk engine

Current engineering stage: **workflow is substantially mapped and the PAT subsystem is now source-constrained enough for feature-level/replay prototypes. Exact OHLC PAT3/PAT2/PAT1 geometry, M5 brake/standing-frame semantics, Sideway boundaries and a larger labeled dataset remain the main barriers to a non-guessing detector and full historical backtest.**
