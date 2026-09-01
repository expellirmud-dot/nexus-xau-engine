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