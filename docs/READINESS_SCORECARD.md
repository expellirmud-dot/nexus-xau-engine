# NEXUS XAU Research Readiness Scorecard

Last reviewed: 2026-09-01

Purpose: give a transparent percentage estimate of how much of the system is currently understood well enough for deterministic research/backtest coding. These percentages are **analyst coverage estimates**, not trading win rates, probabilities of profit, or claims from the instructor.

Historical checkpoints are preserved in dated scorecards. Current canonical score incorporates:

- full EP.5 body-collection transcript review;
- primary teaching images/book pages;
- direct relative chat clarifications on XAUUSD scope, primary SIG TFs, half/swing retrace and PAT2 post-SIG anchor.

## Scoring method

Each module has a weight based on importance to a full detector/replay strategy. Coverage means: how much of that module is supported by direct/primary evidence and can be specified without guessing.

| Module | Weight | Current coverage | Weighted contribution | Status |
|---|---:|---:|---:|---|
| Broker / symbol / data metadata | 5% | 90% | 4.50 | XAUUSD-only scope strong; exact Real36 live symbol specification still needs verification |
| Core cycle / state names | 5% | 85% | 4.25 | Direct slide defines SIDEWAY/SIG/TP/พักตัว; exact transitions incomplete |
| SIG anchor / run-distance logic | 10% | 90% | 9.00 | Direct TP table + PAT2 Buy candle #3 post-SIG anchor clarification |
| PA / PAT1-PAT5 definitions | 15% | 20% | 3.00 | Largest blocker; exact OHLC definitions and PA detector missing |
| Body collection | 10% | 65% | 6.50 | Workflow/lifecycle strong; pair/zone/completion geometry missing |
| Sideway state machine | 10% | 35% | 3.50 | Frame-complete prerequisite and Over-round caution supported; exact detector missing |
| Half / swing retrace + Fibonacci | 10% | 70% | 7.00 | Direct relative classification + midpoint logic strong; entry/extreme/Fib details still open |
| Entry / M5 break execution | 10% | 60% | 6.00 | <=200 frame proximity + M5-first + M15/M30 relationship direct; exact break geometry unresolved |
| Multi-timeframe relationship | 7% | 45% | 3.15 | H1/H4/D/W primary SIG set + small-TF confirmation roles clearer; conflict matrix open |
| Por Chon / Mae Pla frame algorithms | 7% | 65% | 4.55 | ATH prerequisites + daily-frame method materially supported; timezone/confluence details open |
| SL / TP / risk-management mechanics | 5% | 50% | 2.50 | TP table direct; PAT2/PAT3 wick as SL reference/examples, but universal buffer/re-entry unresolved |
| Ground-truth labeled examples | 6% | 15% | 0.90 | Several labeled examples now exist, but dataset still far below validation target |

## Overall weighted readiness

Weighted total = **54.85%**

Rounded project score: **55% understood/codable for deterministic research logic**

Remaining unresolved weighted gap: **45%**

This 55% is readiness for the **research/backtest rule engine**, not readiness for live automated trading.

## What is substantially closed already

- XAUUSD-only target scope and broker/server metadata abstraction.
- Core lifecycle terminology: `SIDEWAY → SIG → TP → พักตัว → SIDEWAY`.
- Primary SIG TF set from direct relative statement: H1/H4/D/W.
- Candle-close requirement: whichever TF is being evaluated, wait for that candle to close before confirming.
- Direct run-distance table: H1 1,000; H4 1,500 at 100% toward 3,000; Day 5,000–10,000; Week 15,000–30,000; Month 30,000–50,000.
- `SIG_RUN_ANCHOR` concept is strong for the shown PA BUY PAT2: candle #3 post-SIG wick, used for run counting/check/SL reference.
- Half retrace classification: post-SIG wick -> extreme -> midpoint, with opposite PA driving the pullback in the supplied example.
- Swing retrace classification: qualifying same-direction candle wick -> extreme -> midpoint, without opposite PA driving the pullback.
- 50% is a calculated/reference level and does not need to be touched exactly.
- Body-collection workflow: H4 PA -> historical `ซอก+ไส้+คู่` -> H1 fallback when needed -> zone touch -> closed M1/M5 PA aligned with H4 -> frame-break candidate -> entry candidate.
- Body-collection zone lifecycle concept: `ACTIVE → CONSUMED`; consumed zone is not reused in the same context.
- Daily-frame first-pass construction: 07:00 H4 context -> nearby statistical reference ending 0/5 -> upper +500 / lower -500, with remaining rounding/timezone details tagged.
- Por Chon ATH prerequisites: previous ATH frame + 1,000-point run + qualifying H4 high in the stated 19:00–19:00 window; persistent once created.
- Entry workflow around frame proximity <=200 points, M5-first break, M15/M30 same-direction relationship, H1 follow-through.
- Sideway is a separate setup family; nominal TP completion alone is not a reversal signal because `Over รอบ` can occur.
- Research/replay architecture and evidence tagging.

## What remains most open

1. Exact PA + PAT1/PAT2/PAT3/PAT4/PAT5 OHLC definitions, invalidation and anchor rules.
2. Exact `คู่` construction, zone bounds/tolerance, candidate ranking, and body-collection completion event.
3. Exact Sideway start/frame-complete/breakout/false-break/state-transition rules.
4. Exact M5/frame-break rule: wick vs body vs close, boundary used, penetration/buffer, and retest requirement.
5. Half/swing dynamic details: qualifying swing-start candle, extreme finalization, entry trigger, invalidation, SL/TP, formal Fibonacci-level use.
6. Multi-TF conflict resolution H1/H4/D/W plus exact M15/M30 same-direction metric.
7. Por Chon/Mae Pla timezone/tie-break/confluence/update details.
8. Universal-vs-setup-specific SL offset, adding/scaling, partial exits and re-entry.
9. 20–50 labeled positive/negative historical cases for ground-truth testing.
10. Dedicated transcript extraction remains high-value for `1E_PYPor1qQ` (P1/PAT1), `UV5NijhjfJ8` (entry/M5 break), Sideway, and half/swing/Fibonacci lessons.
11. Exact Real36 XAUUSD symbol specification still needs direct verification before live-equivalent point/tick calculations are locked.

## Current implementable skeleton

```text
MARKET_DATA / BROKER_METADATA
→ FRAME_CONTEXT (Daily / ATH / SW shell)
→ WAIT_H4_PA
→ FIND_REFERENCE_ZONE
→ WAIT_ZONE_TOUCH
→ WAIT_SMALL_TF_PA
→ WAIT_FRAME_BREAK
→ ENTRY_CANDIDATE
→ SIG_RUN_ANCHOR
→ RUN / TP STATE
→ RETRACE_CANDIDATE (HALF / SWING)
→ ZONE_CONSUMED / NEXT_CYCLE
```

Safe utilities / interfaces to implement now:

- broker-specific point conversion;
- closed-candle validation;
- run-distance configuration;
- evidence-tagged frame candidates;
- PAT2 source-confirmed anchor storage;
- half/swing midpoint calculators;
- retrace candidate classifier **only when `opposite_pa_present` and anchors are supplied by validated detectors**;
- replay event logging and ground-truth schema.

These interfaces must remain placeholders until evidence closes them:

- `detect_PA()`;
- `detect_PAT1()` ... `detect_PAT5()`;
- `detect_pair()`;
- `confirm_m5_break()`;
- `sideway_frame_complete()`;
- `sideway_false_break()`;
- `body_collection_completed()`;
- exact retrace entry/invalidation logic;
- exact live execution / risk engine.

## Milestone interpretation

- 0–25%: terminology / exploratory stage
- 25–50%: architecture and partial rule extraction
- 50–70%: detector prototypes and meaningful replay become practical
- 70–85%: robust historical backtest with fewer assumptions
- 85–95%: demo-forward validation candidate
- 95%+: only then consider whether live execution research is justified; percentage alone is not sufficient

Current position: **55% — detector prototype / meaningful replay-preparation stage**.

## Preserved dated checkpoints

- `docs/READINESS_SCORECARD_IMAGE_UPDATE_2026-09-01.md` — primary image update (~53%).
- `docs/READINESS_SCORECARD_CHAT_UPDATE_2026-09-01.md` — direct relative chat update (~55%).
- earlier transcript checkpoints remain preserved in research/analyst review files.
