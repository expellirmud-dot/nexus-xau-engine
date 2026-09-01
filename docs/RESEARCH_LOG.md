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
