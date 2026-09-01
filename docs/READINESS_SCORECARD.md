# NEXUS XAU Research Readiness Scorecard

Last reviewed: 2026-09-01

Purpose: give a transparent percentage estimate of how much of the system is currently understood well enough for deterministic research/backtest coding. These percentages are **analyst coverage estimates**, not trading win rates, probabilities of profit, or claims from the instructor.

## Scoring method

Each module has a weight based on how important it is to a full detector/replay strategy. Coverage means: how much of that module is supported by direct/primary evidence and can be specified without guessing.

| Module | Weight | Current coverage | Weighted contribution | Status |
|---|---:|---:|---:|---|
| Broker / symbol / data metadata | 5% | 85% | 4.25 | Mostly closed; live Real36 symbol spec still needs verification |
| Core cycle / state names | 5% | 70% | 3.50 | Cycle known; exact transition rules incomplete |
| SIG anchor / run-distance logic | 10% | 75% | 7.50 | Strong for PAT2 example and run measurements; other PAT anchors incomplete |
| PA / PAT1-PAT3 definitions | 15% | 25% | 3.75 | Largest blocker; exact OHLC rules still missing |
| Body collection | 10% | 60% | 6.00 | Workflow largely understood; exact geometry still missing |
| Sideway state machine | 10% | 20% | 2.00 | High-level concept known; deterministic rules mostly missing |
| Half / swing retrace + Fibonacci | 10% | 55% | 5.50 | Midpoint logic strong; anchor-selection/trigger rules incomplete |
| Entry / M5 break execution | 10% | 45% | 4.50 | Workflow known; exact break/entry trigger incomplete |
| Multi-timeframe relationship | 7% | 30% | 2.10 | TF roles known; conflict/priority rules missing |
| Por Chon / Mae Pla frame algorithms | 7% | 35% | 2.45 | Concepts known; exact construction/update logic incomplete |
| SL / TP / risk-management mechanics | 5% | 40% | 2.00 | Run TP partly known; SL/partial/re-entry not deterministic |
| Ground-truth labeled examples | 6% | 10% | 0.60 | Too few labeled positive/negative examples for validation |

## Overall weighted readiness

Weighted total = **44.15%**

Rounded project score: **44% understood/codable for deterministic research logic**

Remaining unresolved weighted gap: **56%**

This 44% should be interpreted as readiness for the research/backtest rule engine, not readiness for live automated trading.

## What is substantially closed already

- Broker/demo point conversion and metadata model.
- Core lifecycle terminology: SIDEWAY → SIG → TP → RETRACE/PULLBACK → SIDEWAY.
- Primary SIG TF set from relative: H1/H4/D/W.
- Run-distance configuration is materially established, especially H1 = 1,000 points and H4 = 1,500 at 100% references.
- `SIG_RUN_ANCHOR` concept is strong for the shown PA BUY PAT2: candle #3 post-SIG wick.
- Half-retrace midpoint mathematics.
- Swing-retrace midpoint mathematics once its start candle is supplied.
- Body-collection workflow: H4 PA → historical `ซอก+ไส้+คู่` zone → H1/M30 fallback → M1/M5 same-direction PA/break → consider entry → post-SIG wick/run.
- Body-collection zone lifecycle: based on historical candles rather than 0/5 digits; completed zone is retired in the same context.
- Research/replay architecture and evidence tagging.

## What remains most open

1. Exact PAT1/PAT2/PAT3 OHLC definitions, invalidation and anchor candle rules.
2. Exact Sideway start/frame-complete/breakout/false-break/state-transition rules.
3. Exact M5 break and first-entry condition.
4. Exact `ซอก+ไส้+คู่` geometry and candidate-selection rules.
5. Half/swing dynamic anchor/extreme/entry/invalidation rules and formal Fibonacci-level use.
6. Multi-TF conflict resolution H1/H4/D/W plus M5/M15/M30 confirmation metric.
7. Por Chon/Mae Pla exact construction/update/timezone algorithms.
8. SL offset, universal-vs-example 300-point behavior, add-position, partial-exit and re-entry rules.
9. 20–50 labeled positive/negative historical cases for ground-truth testing.

## Milestone interpretation

- 0–25%: terminology / exploratory stage
- 25–50%: architecture and partial rule extraction
- 50–70%: detector prototypes and meaningful replay become practical
- 70–85%: robust historical backtest with fewer assumptions
- 85–95%: demo-forward validation candidate
- 95%+: only then consider whether live execution research is justified; percentage alone is not sufficient

Current position: **44% — late rule-extraction / early detector-prototype stage**.
