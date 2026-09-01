# NEXUS XAU Research Readiness — Direct Relative Chat Update

Date: 2026-09-01

Purpose: update analyst coverage after ingesting direct relative chat evidence about XAUUSD scope, half/swing retrace classification, primary SIG timeframes, and PAT2 post-SIG anchor.

This is NOT a win rate, profit probability, or live-EA readiness score.

Previous primary-image score: ~53%.

## Updated weighted coverage

| Module | Weight | Previous | Updated | Weighted contribution | Analyst note |
|---|---:|---:|---:|---:|---|
| Broker / symbol / data metadata | 5% | 90% | 90% | 4.50 | XAUUSD-only scope strengthened; Real36 exact live symbol spec still missing |
| Core cycle / state names | 5% | 85% | 85% | 4.25 | No major new transition evidence |
| SIG anchor / run-distance logic | 10% | 85% | 90% | 9.00 | PAT2 Buy candle #3 anchor, run/check/SL role directly clarified |
| PA / PAT1-PAT5 definitions | 15% | 20% | 20% | 3.00 | Location rule strengthened, but exact OHLC patterns still missing |
| Body collection | 10% | 65% | 65% | 6.50 | Direct chat confirms body collection follows PA, but geometry unchanged |
| Sideway state machine | 10% | 35% | 35% | 3.50 | SW remains named as core setup; exact detector still missing |
| Half / swing retrace + Fibonacci | 10% | 55% | 70% | 7.00 | Direct classification and midpoint logic materially strengthened; entry/extreme selection/Fib details still open |
| Entry / M5 break execution | 10% | 60% | 60% | 6.00 | No new exact break geometry |
| Multi-timeframe relationship | 7% | 45% | 45% | 3.15 | Primary SIG TF set H1/H4/D/W reaffirmed; conflict matrix still open |
| Por Chon / Mae Pla frame algorithms | 7% | 65% | 65% | 4.55 | No new formula-level detail beyond previous evidence |
| SL / TP / risk-management mechanics | 5% | 50% | 50% | 2.50 | PAT2 wick is SL reference; exact buffer/universal rule still unresolved |
| Ground-truth labeled examples | 6% | 12% | 15% | 0.90 | One more directly labeled PAT2 anchor example and retrace classification examples |

Weighted total = **54.85%**

Rounded updated readiness = **55%**

Remaining weighted gap = **45%**

## Why the score moved only ~2 points

Most of the supplied material reinforces evidence already in the project rather than opening entirely new modules. The meaningful improvement is concentrated in:

1. half vs swing classification;
2. midpoint/reference semantics;
3. PAT2 post-SIG anchor role;
4. primary SIG TF scope;
5. XAUUSD-only target clarification.

The largest blockers still remain unaltered:

- exact PA detector;
- exact PAT1–PAT5 OHLC definitions;
- exact M5/frame-break geometry;
- Sideway frame-complete / false-break logic;
- body-collection pair geometry and completion event;
- retrace entry/invalidation/extreme-finalization;
- higher-TF conflict resolution;
- universal SL/position-management rules;
- sufficient labeled historical ground truth.

## Current stage

**55% — detector prototype / meaningful replay preparation stage.**

Safe to prototype:

- broker/symbol metadata layer;
- daily/ATH frame candidate logic with unresolved tags;
- run-distance configuration;
- SIG anchor storage for source-confirmed cases;
- half/swing midpoint calculators;
- retrace candidate classifier using `opposite_pa_present` as an input supplied by a placeholder detector;
- body-collection and entry state-machine shells;
- replay event logging and evidence tagging.

Still placeholder-only:

- `detect_PA()`;
- `detect_PAT1()` ... `detect_PAT5()`;
- `confirm_m5_break()`;
- `sideway_frame_complete()`;
- `sideway_false_break()`;
- `detect_pair()`;
- `body_collection_completed()`;
- exact retrace entry/invalidation logic;
- full live-execution risk engine.
