# NEXUS XAU Research Readiness Scorecard — Canonical

Last reviewed: 2026-09-01

This scorecard separates:

1. **Workflow / conceptual coverage** — how well the project understands the sequence and role of system components.
2. **Deterministic coding readiness** — how much can be encoded into research/backtest rules without inventing missing OHLC/state mechanics.

These are NOT win rates, profit probabilities, or live-EA readiness scores.

## Canonical headline

- **Workflow / conceptual coverage: ~88%**
- **Deterministic coding readiness: ~78%**
- **Remaining deterministic gap: ~22%**

The increase from 82% / 71% comes from the primary timestamp transcript associated with video `16KoS7d-koI`, which materially closes the discovery-level gaps around M1/M5 brake workflow, five-step candle-force reading, preferred retest entry, frame-standing observation, structure confirmation, overlap/false first brake, and the distinction between frame-brake entry and SIG entry.

The remaining gap is concentrated in **numeric candle geometry, exact Sideway frame boundaries, parameter tolerances, and labeled validation data**.

## Deterministic coding coverage

| Module | Weight | Current coverage | Weighted contribution | Status |
|---|---:|---:|---:|---|
| Broker / symbol / data metadata | 5% | 95% | 4.75 | XAUUSD reference spec strong; server/account remain runtime metadata |
| Core cycle / state names | 5% | 96% | 4.80 | Lifecycle and reevaluation paths strong; Sideway formal boundaries still partial |
| SIG anchor / run-distance logic | 10% | 98% | 9.80 | PAT1→2, PAT2→3, PAT3→4; no-wick fallback supported |
| PA / PAT definitions | 15% | 72% | 10.80 | Family map/count/location/invalidation strong; PAT1/PAT2/PAT3 numeric geometry still open |
| Body collection | 10% | 70% | 7.00 | Workflow strong; new source supports ซอก+ไส้+คู่ strength and nearest-zone preference; exact pair/completion open |
| Sideway state machine | 10% | 72% | 7.20 | Equal/repeated high-low examples, limited frame interactions, PA/standing execution now stronger; canonical frame-complete algorithm still open |
| Half / swing retrace + Fibonacci | 10% | 78% | 7.80 | Classification/midpoint strong; exact swing anchor/extreme/entry remains open |
| Entry / M5 brake execution | 10% | 88% | 8.80 | Zone→force steps→retest→confirmation state model now primary-source-backed; exact numeric force/standing thresholds remain |
| Multi-timeframe relationship | 7% | 72% | 5.04 | M1/M5 same concept, M5 safer, M1 structure/trendline refinement; full H1/H4/D/W conflict matrix still open |
| Por Chon / Mae Pla frame algorithms | 7% | 77% | 5.39 | Daily/ATH strong; snapping/timezone/tie-breaks remain |
| SL / TP / risk-management mechanics | 5% | 72% | 3.60 | Multiple source-backed context-specific SL/BE/TP examples; no universal risk formula |
| Ground-truth labeled examples | 6% | 50% | 3.00 | Several explicit positive/negative M5/PA examples now exist; dataset still too small |

Weighted total = **77.98%**

Rounded deterministic coding readiness = **78%**

## Workflow / conceptual coverage

Analyst estimate = **~88%**.

The project now has a strong system-level map for:

- XAUUSD/MT5 runtime context;
- Daily / ATH / support-resistance zones;
- PA/PAT family and location qualification;
- post-SIG anchor and run counting;
- body-collection workflow;
- M1/M5 brake workflow;
- first reaction versus preferred phase-2/retest entry;
- five logical candle-force stages: `ใหญ่ยาว → อ่อนแรง → Reject → เปลี่ยนสี → Retest`;
- frame-standing confirmation over a 4–10 candle observation window starting from first frame touch;
- local structure confirmation via higher-low/lower-high and local high/low destruction;
- overlap / false first brake / reevaluation;
- Sideway execution examples;
- SIG-entry versus frame-brake entry accounting;
- TP / over-round / half-swing retracement concepts.

## Strongly supported rules now

### Environment / cycle / SIG

- Target instrument `XAUUSD`; do not substitute `XAUUSDc`.
- Reference spec: Digits 2, Tick size 0.01, Contract size 100, Tick value 0.1, Bid chart mode.
- Server/account metadata must not be hard-coded as strategy rules.
- PA can occur on all TF; course terminology uses SIG from H1 upward; owner-relative operational SIG set remains H1/H4/D/W.
- Candle under evaluation must close before confirmation.
- Core lifecycle broadly: `SIG → TP → พักตัว → SIDEWAY`, with reevaluation/replacement paths.

### PAT / SIG anchor

- Five PA visual forms: PAT1 + PAT2 + PAT3 variants 1/2/3.
- PAT refers to candle-count family: PAT1=1, PAT2=2, PAT3=3 candles.
- PAT2 does not require full engulfing.
- PAT2 candle #2 closes around the 50% level of candle #1; denominator/tolerance unresolved.
- PAT labels may overlap over the same candle region.
- PA Buy belongs at support; PA Sell belongs at resistance/correct upper context.
- Post-SIG reference: PAT1=#2, PAT2=#3, PAT3=#4.
- No-wick fallback: Buy uses low; Sell uses high.
- Post-SIG reference disturbing/exceeding the PA can invalidate the setup and trigger Sideway/reevaluation.

### M1/M5 brake / entry

- M1 and M5 use the same abstract brake-entry pattern; M1 is finer/more volatile.
- Brake must be sought at a prepared zone; zone is a waiting area, not a guaranteed reversal quote.
- Core candle-force logic: `ใหญ่ยาว → อ่อนแรง → Reject/ถอดไส้ → เปลี่ยนสี → Retest`.
- Weakening/rejection/color-shift may combine in a single candle.
- Single wick rejection alone is not enough.
- First brake/reaction is higher-risk; phase 2 / retest is the preferred confirmation entry in this lesson.
- Full structural retest requires a move away / interaction with opposite structure / return to the switched support-resistance context.
- `ยืนกรอบ`: begin counting from first frame touch; roughly 4–10 candles are used as an observation/confirmation window on M1/M5.
- Frame standing primarily uses candle bodies; wick-on-line can also contribute.
- Buy structure evidence includes higher-low / reclaim / prior-high destruction; Sell mirrors with lower-high / support loss / prior-low destruction.
- `overlap` / false first brake exists; reevaluate instead of assuming every first reaction is valid.
- `เบรก` in this lesson means a stopping/braking process at zone, not a generic one-candle breakout rule.

### Entry mode separation

- `FRAME_BRAKE_ENTRY` is not the same as `SIG_ENTRY`.
- M5 brake is used mainly for frame/retracement/counter-round/TP-complete contexts.
- A frame entry does not begin with a native SIG run anchor; practical target examples use nearby frames / ~500–1,000 points and may later hold if a SIG activates.
- SIG entry uses post-SIG wick/reference and timeframe run table.

### Run / retracement

- H1 run = 1,000 points.
- H4 = 1,500 toward 3,000.
- Day = 5,000–10,000; Week = 15,000–30,000; MN = 30,000–50,000 from primary visual evidence.
- Half retrace: overrun + opposite PA; post-SIG wick→extreme midpoint.
- Swing retrace: overrun + no opposite PA; qualifying same-direction candle wick→extreme midpoint.
- 50% is a reference, not mandatory touch.
- 61.8 is a source-mentioned watched level, not a universal mandatory entry rule.

### Zone / Sideway improvements from M5 transcript

- In Sideway examples, repeated/equal lows or highs combine with zone reaction, PA and frame-standing.
- Teacher limits repeated frame interactions in the example (support/resistance #1/#2 rather than unlimited re-entry).
- `ซอก + ไส้ + คู่` all present is described as stronger than only two components.
- When multiple nearby historical zone candidates exist, nearest relevant zone is preferred first.

## Conflict / quarantine notes

Do not hard-code without stronger evidence:

- PAT1 generic body<=50% rule;
- PAT2 `body2 >= 50% body1`; primary wording is close around 50% of candle #1, denominator still unknown;
- generic PAT3 formula not sourced from primary geometry;
- M5 `close beyond frame = brake`;
- treating one rejection wick as confirmed brake;
- treating 300-point overlap as universal — teacher explicitly notes volatility exceptions;
- universal 50–150 point SL;
- universal 200–300 point frame SL;
- universal 300-point SL;
- literal screen `45°` trendline as a market invariant;
- fixed RR 1:1/1:2;
- Fib 38.2/61.8 as mandatory universal entries;
- old ATH 12:00 UTC claim conflicting with stronger 19:00–19:00 evidence.

## P0 blockers

1. PAT3 variants 1/2/3 exact OHLC geometry.
2. PAT2 50% exact denominator and tolerance.
3. PAT1 quantitative wick/body and location tolerance.
4. Exact numeric thresholds for M5 force states (`ใหญ่ยาว`, `อ่อนแรง`, `Reject`, color-shift strength).
5. Canonical Sideway upper/lower frame construction and formal `frame complete`/exit rule.
6. Sufficient positive + negative labeled historical dataset for threshold validation.

## P1 blockers / open parameters

1. Exact frame-standing tolerance and all-vs-majority rule inside 4–10 candles.
2. Exact local-pivot window for higher-low/lower-high / structure break.
3. Exact `คู่` geometry and `body_collection_completed()` event.
4. Swing-retrace starting-candle selection and extreme-finalization.
5. Half/Swing exact entry/invalidation and operational Fib levels.
6. Daily 0/5 snapping tie algorithm.
7. ATH 19:00 timezone/day-boundary semantics.
8. Complete H1/H4/D/W conflict matrix and exact M15/M30 same-direction metric.
9. Universal execution/risk formula.

## Safe to prototype now

- runtime broker/symbol metadata and point conversion;
- replay/data event model;
- cycle/SIG replacement state objects;
- PAT candidate model with overlapping labels;
- post-SIG anchor mapping and no-wick fallback;
- location qualification flags;
- M1/M5 shared brake state machine;
- five candle-force feature states;
- `ENTRY_1_SCOUT` versus `ENTRY_2_RETEST` classification;
- structural retest candidate detection;
- frame-standing counter from first touch;
- 4–10 candle observation metadata;
- higher-low/lower-high and structure-break features;
- overlap / false-brake / reevaluation states;
- frame-brake versus SIG-entry accounting separation;
- M1 trendline metadata as heuristic, not literal-angle rule;
- Sideway and Body Collection state-machine shells;
- evidence-tagged SL/TP/replay logging.

## Placeholder / candidate-only interfaces

- `detect_PAT1_exact()`
- `detect_PAT2_exact()`
- `detect_PAT3_v1_exact()`
- `detect_PAT3_v2_exact()`
- `detect_PAT3_v3_exact()`
- `close_near_prior_50pct_exact()`
- `is_large_force_candle_exact()`
- `is_weakening_exact()`
- `is_rejection_exact()`
- `frame_standing_exact()`
- `local_pivot_exact()`
- `sideway_frame_complete()`
- `sideway_false_exit()`
- `select_swing_retrace_anchor()`
- `detect_pair_exact()`
- `body_collection_completed()`
- universal execution / risk engine

Current engineering stage: **workflow is close to fully mapped; Entry/M5 is now suitable for evidence-backed state-machine and replay prototypes. Remaining barriers are concentrated in exact PAT/candle thresholds, formal Sideway boundaries, parameter tolerances, and labeled validation data.**
