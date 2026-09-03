# Research Log

## 2026-09-01 — Consolidation checkpoint

### Project direction

The project is explicitly research-first. The aim is to reproduce the system rules as deterministic research logic before any live MT5 automation.

Proposed architecture recorded:

1. `NEXUS XAU Research` — data / frame / PAT / SIG / cycle / multi-TF / statistics / backtest / replay
2. `NEXUS XAU Analyst` — current-market interpretation and explanation
3. `NEXUS XAU Execution` — later-stage MT5 order handling only after validation

### Data plan

Preferred source is XAUUSD historical data from the same Exness/MT5 environment used by the relative if possible.

Store raw ticks or at least M1 with:

- Bid
- Ask
- spread
- broker/server timestamp
- symbol specification

Derive M5/M15/M30/H1/H4/D1/W1 from lower-level data where possible.

Replay should hide future candles, apply state/rule logic, then reveal outcome.

### Public source discovery

Main public channel identified as `UNLOCK TRADER` / `@Unlocktrader007`.

Visible / referenced teaching topics include:

- graph cycle and timeframe relationship,
- Sideway frame trading,
- Por Chon frame,
- half retrace / swing retrace,
- order entry,
- recap orders,
- PA/PAT/SIG fundamentals.

### Direct rule findings accumulated before this checkpoint

- Core cycle: Sideway → SIG → TP → rest/retrace → Sideway.
- Relative confirmed primary SIG TFs: H1/H4/D/W.
- H1 run: 1,000 points.
- H4 references: 1,500 points at 100%, sometimes continuation toward 3,000.
- Day: 5,000 points, references toward 10,000.
- Week: 15,000–30,000.
- run counted from `ไส้หลัง SIG`.
- PA Buy at support.
- PA Sell at resistance or TP-complete frame/area.
- PA pattern alone is insufficient; body collection occurs afterward.
- in shown PA BUY PAT2, candle #3 is the post-SIG-wick anchor candle.
- post-SIG wick is used to start run count and as a check / SL reference.
- half retrace: post-SIG wick → extreme → midpoint; opposite PA present.
- swing retrace: qualifying candle wick → extreme → midpoint; opposite PA absent.
- 50% does not have to be touched exactly.

### Body-collection transcript review

A user-provided transcript materially improved understanding of body collection:

- historical candle zones described using `ซอก + ไส้ + คู่`,
- H4 is emphasized, then H1 / sometimes M30 if needed,
- lower-TF PA may be used at the zone for entry confirmation,
- body collection is not simply a round-number / 0-or-5 rule,
- zones should not be reused after the body collection is completed,
- one teaching section described looking 2–4 candles back,
- body collection is not to be applied blindly in Sideway.

### Deep-research sessions

Multiple deep-research attempts were used to search for public clarification. Important conclusion:

- public search can support terminology and locate teaching topics,
- but generic market articles and learner summaries often introduce unsupported fixed rules,
- those claims must not be merged into the primary rulebook unless verified by the relative / primary teaching material.

Examples retained only as warnings, not system facts:

- Sideway = exactly 2–3 swings,
- universal SL 200–300 points,
- false breakout exactly 300 points,
- pyramiding every 100–200 points,
- generic RR 1:1 / 1:2,
- simplistic father-frame hierarchy.

### Current research focus

Priority order:

1. exact PA/PAT1-2-3 definitions,
2. exact half/swing anchor/classification rules,
3. exact Sideway state rules,
4. exact Entry/SL/TP rules,
5. Por Chon/Mae Pla frame exceptions,
6. labeled positive and negative historical cases.

### Repository status

The GitHub repository was initially empty. This checkpoint created the durable project documentation so future work can update rather than overwrite prior learning.

---

## 2026-09-01 — Full EP.5 transcript analyst review

Source reviewed end-to-end: user-supplied EP.5 body-collection transcript, `0:00–2:02:38`.

Detailed timestamp extraction saved at:

`docs/transcripts/EP5_BODY_COLLECTION_FULL_ANALYSIS.md`

### Material changes to the research model

1. Body collection should be modeled as its own setup family rather than as a vague generic retest.
2. The demonstrated H4 method requires the historical zone concept `ซอก + ไส้ + คู่`.
3. Same-timeframe structure is preferred; fallback hierarchy appears as H4 -> H1 -> M30 when the required structure is missing.
4. The teaching gives a first search window of roughly 2–4 historical candles.
5. Current method favors two projected body-collection zones.
6. At the zone, M1/M5 PA aligned with H4 is used before entry; M5 is the safer confirmation path.
7. The video repeatedly requires waiting for the analyzed candle to close.
8. Body collection is not based on 0/5 price endings.
9. Used body-collection zones are retired; untouched zones may persist across days.
10. Body collection should not be blindly applied inside Sideway. A separate Sideway setup exists and must be modeled separately.
11. In the demonstrated H4 sequence, the retrace/body collection helps form the post-SIG wick before the run toward TP.
12. A direct PAT3 Sell example states that the third candle body engulfs/closes through the prior wick; however, this does not close the full PAT3 algorithm.
13. The video explicitly says the next lesson covers half-retrace, swing-retrace, and Fibonacci retracement/extension, confirming that those rules should be sourced from the next transcript rather than inferred from EP.5.

### Analyst decision after review

The project's biggest blocker shifted slightly.

Before full EP.5 review, “body collection” was mostly conceptual. After the review, the workflow/state model is strong enough to scaffold in code, but the exact geometry is still missing.

Current blocker order:

1. exact PAT1/PAT2/PAT3 candle rules and invalidations;
2. exact OHLC/tolerance formula for `ซอก + ไส้ + คู่` and exact M5 break rule;
3. full Sideway state machine / separate Sideway setup;
4. half/swing + Fibonacci next lesson;
5. Por Chon/Mae Pla frame algorithms;
6. labeled truth-set examples.

### Coding implication

Safe to begin now:

- closed-bar evaluation framework;
- body-collection state/schema;
- H4 -> H1 -> M30 search pipeline shell;
- two-zone candidate storage;
- zone lifecycle state tracking;
- replay logging for zone arrival and M1/M5 PA events.

Still unsafe:

- automatic PAT classification;
- automatic `ซอกไส้คู่` geometry detector;
- automatic M5 break detector;
- automatic Sideway detector;
- live entry/SL execution.

---

## 2026-09-03 — Persistent checkpoint workflow activated

Reason: the research PC may sleep or the MCP bridge may disconnect during long analysis. From this checkpoint onward, research is intentionally split into restart-safe atomic steps.

### Checkpoint rule

Every completed research point must be persisted before starting the next point. A completed checkpoint records:

1. question being tested;
2. source/evidence inspected;
3. facts established;
4. assumptions or parameter variants used;
5. calculations/results produced;
6. conflicts or unresolved gaps;
7. code/files created or changed;
8. tests/validation status;
9. exact next resume step.

Historical findings must be appended or superseded with an explicit reason; they must not be silently removed.

### Current completed checkpoints

- MT5 M1 dataset export and multi-timeframe resample validation completed for 2026-08-03 through 2026-09-01: 30,308 M1 bars; M5/H1/H4/D1 validation against MT5 native bars produced zero mismatches on the closed-boundary dataset.
- PAT2/PAT3 color-topology month scan completed: 37,153 topology hits, explicitly NOT valid signals.
- >50% geometry sensitivity completed under BODY and FULL_RANGE midpoint variants. BODY pass = 24,240 / 37,153 (65.24%); FULL_RANGE pass = 24,001 / 37,153 (64.60%); basis disagreement = 3,603 (9.70%). These are research variants, not system-rule selections.
- PAT3 small-body and SELL equal-wick sensitivity sweep completed and preserved.
- PA location semantics confirmed: BUY requires support; SELL requires resistance.
- S/R evidence families separated rather than collapsed into one generic line: MAE_PLA_STAT_FRAME, WICK_CONTACT_FRAME, BODY_COLLECTION_ZONE, POR_CHON_ATH_FRAME, SIDEWAY_FRAME, MANUAL_SUPPORT_RESISTANCE, UNKNOWN.
- 7–14 points is retained as H4/H1 wick-contact-strength evidence, not universal PAT location tolerance.
- <=200 points is retained as setup-specific frame proximity/entry evidence, not universal PAT location tolerance.
- Location fail-closed engine shell implemented in `src/nexus_xau/engine/location.py`.
- Current test suite after location work: 26/26 passed; Ruff passed.

### Current blocker / resume point

The next research question is:

`What exact interaction qualifies a PAT as being at support/resistance for each relevant S/R source family?`

Need to recover source-backed distinctions for:

- exact touch vs allowed distance;
- wick penetration;
- body overlap;
- close relative to line/zone;
- line vs band/zone semantics;
- higher-timeframe S/R priority when lower-timeframe PAT appears opposite;
- whether qualification differs between statistical frame, wick-contact frame, and body-collection zone.

Until this is closed, do not convert the 37,153 topology candidates into claimed valid PAT statistics or Win/Loss statistics.

### Resume contract

If the PC sleeps, bridge disconnects, or the chat is interrupted, restart from the latest `Current blocker / resume point` in this file plus `docs/CURRENT_RESEARCH_STATE.json`. Do not recompute completed checkpoints unless validation or a new stronger source requires it.


---

## 2026-09-03 — Win/Loss proof + negative-control checkpoint

Goal: build a defensible path from validated XAUUSDm history to Win/Loss/expectancy without promoting incomplete PAT/SIG rules.

Facts:
- Current XAUUSDm MT5 spec: digits=3, broker point=0.001, tick size=0.001, tick value=0.1, contract size=100.
- Project teaching-reference point remains separately tracked as 0.01 USD; broker point and project point must not be conflated.
- Repo has validated price data/research events, but no saved deal/order-history dataset for the test month.
- New no-lookahead outcome engine measures MFE, MAE, directional return, first-hit, same-M1-bar ambiguity, and `known_at`.
- Full tests: 30/30 passed; Ruff passed on new modules.

Negative control:
- Raw topology-only target reach was very high, proving target reach alone is not Win rate.
- Matched opposite-direction control:
  - H1 PAT2 actual=0.824 vs flipped=0.841 (delta -0.017, n=233)
  - H1 PAT3 actual=0.850 vs flipped=0.807 (delta +0.043, n=233)
  - H4 PAT2 actual=0.810 vs flipped=0.897 (delta -0.086, n=58)
  - H4 PAT3 actual=0.850 vs flipped=0.883 (delta -0.033, n=60)
  - D1 sample too small.
Conclusion: color topology alone shows no consistent directional advantage over matched opposite direction. This is NOT system Win rate.

Methodological closure:
- Signal/run success is separate from realized trade Win/Loss.
- Canonical trade Win/Loss requires frozen valid setup, entry, SL/invalidation, TP/exit, execution/cost, and ambiguity handling.
- Protocol: `docs/WIN_LOSS_PROOF_PROTOCOL_2026-09-03.md`
- Negative-control record: `docs/OUTCOME_NEGATIVE_CONTROL_2026-09-03.md`

Next resume:
1. Evidence track: close PAT-to-S/R interaction, valid post-SIG, entry/invalidation/state transitions.
2. Statistics track: expand history in monthly chunks if available; add random-time/shuffled-side/non-overlap controls and out-of-sample partitions.
3. Do not use outcome to choose the source rule. Only after rules/labels freeze may the outcome harness produce claimed system Win/Loss/expectancy.


---

## 2026-09-03 — Expanded-history / OOS negative-control checkpoint

Expanded MT5 history was recovered month-by-month. Actual M1 history begins 2026-05-25 04:28 UTC. A clean-boundary consolidated set was frozen from 2026-05-26 00:00 UTC through 2026-09-01 23:59 UTC with 97,341 M1 bars.

Native MT5 validation over the consolidated range:
- M5 19,500 vs 19,500, mismatches=0
- H1 1,625 vs 1,625, mismatches=0
- H4 438 vs 438, mismatches=0
- D1 85 vs 85, mismatches=0

Expanded topology scan: 120,546 research-only color-topology hit records.

Full-period matched opposite-direction control (NOT system Win rate):
- H1 PAT2 actual=0.810 vs flipped=0.815, delta=-0.005, n=789
- H1 PAT3 actual=0.809 vs flipped=0.831, delta=-0.022, n=823
- H4 PAT2 actual=0.857 vs flipped=0.886, delta=-0.029, n=210
- H4 PAT3 actual=0.847 vs flipped=0.874, delta=-0.027, n=222

Time split:
- Development: 2026-05-26 -> 2026-06-30
- Validation: 2026-07-01 -> 2026-07-31
- Test: 2026-08-03 -> 2026-09-01

Across splits, actual-vs-flipped topology deltas change sign and H4 is mostly non-positive. Conclusion remains: color topology alone has no robust directional edge established. This does not test the full system because S/R, final geometry, post-SIG validity, cycle and entry/invalidation are omitted.

New durable records:
- docs/OUT_OF_SAMPLE_NEGATIVE_CONTROL_2026-09-03.md
- docs/STATE_RESPONSE_MATRIX_2026-09-03.md
- data/raw/XAUUSDm_M1_MT5_2026-05-26_2026-09-01.csv
- results/XAUUSDm_MT5_resample_validation_2026-05-26_2026-09-01.json

Resume priority returns to the evidence track:
1. PAT-to-S/R interaction by source family.
2. Post-SIG destruction/invalidation.
3. Entry + SL/invalidation mechanics.
4. Freeze those rules before using the expanded outcome harness.
