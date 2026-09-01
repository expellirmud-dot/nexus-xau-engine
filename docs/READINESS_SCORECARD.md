# NEXUS XAU Research Readiness Scorecard

Last reviewed: 2026-09-01

Purpose: give a transparent percentage estimate of how much of the system is currently understood well enough for deterministic research/backtest coding. These percentages are **analyst coverage estimates**, not trading win rates, probabilities of profit, or claims from the instructor.

## Scoring method

Each module has a weight based on how important it is to a full detector/replay strategy. Coverage means: how much of that module is supported by direct/primary evidence and can be specified without guessing.

| Module | Weight | Current coverage | Weighted contribution | Status |
|---|---:|---:|---:|---|
| Broker / symbol / data metadata | 5% | 85% | 4.25 | Mostly closed; live Real36 symbol spec still needs verification |
| Core cycle / state names | 5% | 70% | 3.50 | Cycle known; exact transition rules incomplete |
| SIG anchor / run-distance logic | 10% | 70% | 7.00 | Strong for PAT2 example and run measurements; PAT-specific anchors incomplete |
| PA / PAT1-PAT5 definitions | 15% | 20% | 3.00 | Largest blocker; exact OHLC rules and PA detector missing |
| Body collection | 10% | 65% | 6.50 | Workflow and zone lifecycle mostly understood; pair/zone/completion geometry missing |
| Sideway state machine | 10% | 20% | 2.00 | High-level concept known; deterministic rules mostly missing |
| Half / swing retrace + Fibonacci | 10% | 55% | 5.50 | Midpoint logic strong; dedicated lesson still required for anchor/trigger/Fib rules |
| Entry / M5 break execution | 10% | 45% | 4.50 | Candle-close rule is closed; exact frame-break and order trigger still incomplete |
| Multi-timeframe relationship | 7% | 35% | 2.45 | H4→H1 fallback and M1/M5 confirmation clearer; full conflict matrix missing |
| Por Chon / Mae Pla frame algorithms | 7% | 35% | 2.45 | Concepts known; exact construction/update logic incomplete |
| SL / TP / risk-management mechanics | 5% | 40% | 2.00 | Run TP partly known; SL/partial/re-entry not deterministic |
| Ground-truth labeled examples | 6% | 10% | 0.60 | Too few labeled positive/negative examples for validation |

## Overall weighted readiness

Weighted total = **43.75%**

Rounded project score: **44% understood/codable for deterministic research logic**

Remaining unresolved weighted gap: **56%**

The overall score stays roughly unchanged after the full transcript analyst review because several workflow-level gaps closed, while the review also correctly downgraded unsupported PAT/PA assumptions that had previously looked more mature than the evidence justified.

This 44% should be interpreted as readiness for the research/backtest rule engine, not readiness for live automated trading.

## What is substantially closed already

- Broker/demo point conversion and metadata model.
- Core lifecycle terminology: SIDEWAY → SIG → TP → RETRACE/PULLBACK → SIDEWAY.
- Primary SIG TF set from relative: H1/H4/D/W.
- Candle-close requirement: whichever TF is being evaluated, wait for that candle to close before confirming.
- Run-distance configuration is materially established, especially H1 = 1,000 points and H4 = 1,500 at 100% references.
- `SIG_RUN_ANCHOR` concept is strong for the shown PA BUY PAT2: candle #3 post-SIG wick.
- Half-retrace midpoint mathematics.
- Swing-retrace midpoint mathematics once its start candle is supplied.
- Body-collection workflow: H4 PA → historical `ซอก+ไส้+คู่` zone → H1 fallback when needed → price reaches zone → closed M1/M5 PA in H4 direction → frame-break confirmation → entry candidate.
- One H4 candle contains four H1 candles; the effect does not have to occur on the first H1 candle.
- Body-collection zone lifecycle concept: `ACTIVE → CONSUMED`, and a consumed zone is not reused in the same context.
- Research/replay architecture and evidence tagging.

## What remains most open

1. Exact PA plus PAT1/PAT2/PAT3/PAT4/PAT5 OHLC definitions, invalidation and anchor candle rules.
2. Exact `คู่` construction, zone bounds/tolerance, candidate ranking, and body-collection completion event.
3. Exact Sideway start/frame-complete/breakout/false-break/state-transition rules.
4. Exact M5/frame-break rule: close vs wick, edge used, penetration/buffer, and whether retest is required.
5. Half/swing dynamic anchor/extreme/entry/invalidation rules and formal Fibonacci-level use from the dedicated lesson.
6. Multi-TF conflict resolution H1/H4/D/W plus M15/M30 confirmation metric.
7. Por Chon/Mae Pla exact construction/update/timezone algorithms.
8. SL offset, universal-vs-example 300-point behavior, add-position, partial-exit and re-entry rules.
9. 20–50 labeled positive/negative historical cases for ground-truth testing.
10. Transcript for `1E_PYPor1qQ` (owner-mapped P1/PAT1) and `UV5NijhjfJ8` (entry/M5 break) remains high-value source material.

## Current implementable skeleton

```text
WAIT_H4_PA
→ FIND_REFERENCE_ZONE
→ WAIT_ZONE_TOUCH
→ WAIT_SMALL_TF_PA
→ WAIT_FRAME_BREAK
→ ENTRY_CANDIDATE
→ ZONE_CONSUMED
```

These interfaces must remain placeholders until evidence closes them:

- `detect_PA()`
- `detect_PAT1()` ... `detect_PAT5()`
- `detect_pair()`
- `confirm_frame_break()`
- `body_collection_completed()`
- exact entry/SL/TP execution

## Milestone interpretation

- 0–25%: terminology / exploratory stage
- 25–50%: architecture and partial rule extraction
- 50–70%: detector prototypes and meaningful replay become practical
- 70–85%: robust historical backtest with fewer assumptions
- 85–95%: demo-forward validation candidate
- 95%+: only then consider whether live execution research is justified; percentage alone is not sufficient

Current position: **44% — late rule-extraction / early detector-prototype stage**.
