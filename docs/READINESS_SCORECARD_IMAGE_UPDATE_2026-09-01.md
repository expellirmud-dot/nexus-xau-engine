# NEXUS XAU Research Readiness — Primary Image Update

Date: 2026-09-01

This scorecard is an analyst coverage estimate for deterministic research/backtest coding. It is NOT win rate, profit probability, or live-EA readiness.

Previous scorecard: ~44% after full EP.5 transcript review.

New evidence added in this update:

- direct teaching image for the core cycle;
- direct Por Chon ATH rules;
- book pages for the daily 1,000-point frame;
- direct run-distance / TP table;
- direct daily-preparation slide;
- direct entry-condition slide;
- direct February 2569 Sideway/Over-round slide;
- Exness Real36 Standard Cent screenshot;
- direct UNLOCK TRADER channel screenshot.

## Updated weighted coverage

| Module | Weight | Previous | Updated | Weighted contribution | Analyst note |
|---|---:|---:|---:|---:|---|
| Broker / symbol / data metadata | 5% | 85% | 90% | 4.50 | Real36 Standard Cent attribution strengthened; live symbol spec still missing |
| Core cycle / state names | 5% | 70% | 85% | 4.25 | Direct slide defines SIDEWAY/SIG/TP/พักตัว; exact transitions still incomplete |
| SIG anchor / run-distance logic | 10% | 70% | 85% | 8.50 | Direct TP table and post-SIG-wick run anchor strengthen this module |
| PA / PAT1-PAT5 definitions | 15% | 20% | 20% | 3.00 | No deterministic OHLC definitions yet; remains largest blocker |
| Body collection | 10% | 65% | 65% | 6.50 | No new geometry evidence in this image batch |
| Sideway state machine | 10% | 20% | 35% | 3.50 | Direct slide confirms SW frame-complete prerequisite, two-side PA/post-SIG confirmation, Over-round caution; exact detector still missing |
| Half / swing retrace + Fibonacci | 10% | 55% | 55% | 5.50 | No new dedicated lesson in this image batch |
| Entry / M5 break execution | 10% | 45% | 60% | 6.00 | <=200-point proximity, M5-first break, M15/M30 direction, no casual adding, H1 follow-through are direct; break geometry still unknown |
| Multi-timeframe relationship | 7% | 35% | 45% | 3.15 | M5/M15/M30/H1 relationship directly supported; higher-TF conflict matrix remains open |
| Por Chon / Mae Pla frame algorithms | 7% | 35% | 65% | 4.55 | ATH prerequisites + daily-frame method materially improved; timezone/tie-break/confluence details remain |
| SL / TP / risk-management mechanics | 5% | 40% | 50% | 2.50 | TP distances now directly supported; 300-point SL remains example-specific |
| Ground-truth labeled examples | 6% | 10% | 12% | 0.72 | PAT3 Buy image adds a labeled example, but dataset is still far too small |

Weighted total = **52.67%**

Rounded updated readiness = **53%**

Remaining weighted gap = **47%**

## Interpretation

The project has crossed from `late rule extraction` into `detector prototype / meaningful replay preparation`, but only for modules whose rules are sufficiently explicit.

The increase from ~44% to ~53% is driven mainly by primary evidence for:

1. daily-frame construction;
2. Por Chon ATH construction prerequisites;
3. direct run-distance table;
4. direct entry workflow;
5. Sideway/Over-round high-level handling;
6. core cycle definitions.

The score does NOT increase PA/PAT because the uploaded markdown summaries contain mixed-source formulas that are not yet safe as system truth.

## What is safe to prototype now

- broker metadata abstraction;
- point conversion as broker-specific metadata;
- daily-frame first-pass calculator using 07:00 H4 context + statistical reference +500/-500, with unresolved rounding/timezone tagged;
- Por Chon ATH candidate-state logic: old ATH frame -> require 1,000-point run -> H4-high candidate in 19:00–19:00 window -> persistent frame;
- run-distance configuration H1/H4/D/W/MN;
- SIG run-anchor storage from post-SIG wick where source-specific anchor is known;
- entry state skeleton using `NEAR_FRAME <= 200` -> `M5_BREAK_CANDIDATE` -> `M15/M30_DIRECTION_CHECK` -> `ENTRY_CANDIDATE`;
- Sideway state shell with `WAIT_SW_FRAME_COMPLETE` and `OVER_ROUND_NO_COUNTER` guards;
- body-collection state skeleton from prior transcript work;
- replay/backtest event logging with evidence tags.

## Still blocked / placeholder only

- `detect_PA()`;
- `detect_PAT1()` ... `detect_PAT5()`;
- `confirm_m5_break()` exact wick/body/close rule;
- `sideway_frame_complete()`;
- `sideway_false_break()`;
- `break_equals_stop()` definition;
- `body_collection_completed()`;
- exact `pair` geometry;
- half/swing retracement trigger/invalidation;
- higher-timeframe conflict resolver;
- universal SL engine;
- live EA execution.

## Evidence quarantine

The uploaded markdown summaries `backtes-replay-engine.md` and `PA-PAT-SIG.md` contain candidate formulas such as fixed PAT body percentages, generic breakout-close definitions, generic RR rules, and universal SL buffers. These remain hypothesis material only until confirmed by direct teaching transcript/image evidence.

Current stage: **53% — detector prototype / replay-preparation stage, not full strategy and not live automation.**
