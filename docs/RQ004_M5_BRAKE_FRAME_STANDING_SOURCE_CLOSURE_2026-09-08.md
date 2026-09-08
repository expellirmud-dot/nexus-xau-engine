# RQ-004 — M5 Brake / Frame-Standing Source Closure — 2026-09-08

Status: CLOSED / `SOURCE_BACKED_STATE_MACHINE_PARAMETERIZED`

## Question

Can the M1/M5 brake / frame-standing concept be represented as a replayable source-backed state machine without inventing numeric force or tolerance thresholds?

## Primary source basis

Timestamped primary transcript review already consolidated in:

- `docs/M5_BRAKE_TRANSCRIPT_FORENSICS_2026-09-01.md`
- source video `16KoS7d-koI` (EP.6 M1/M5 entry detail)
- current local EP.4/EP.6 source batch for contextual cross-check

## Source-backed state sequence

The source directly supports a zone-first stopping/reversal process rather than a generic one-candle breakout rule.

Safe state shell:

```text
IDLE
-> ZONE_ARMED
-> FORCE_IMPULSE          # ใหญ่ยาว / strong force
-> FORCE_WEAKENING        # อ่อนแรง
-> REJECTION              # reject / ถอดไส้
-> COLOR_SHIFT            # opposite color enters
-> BRAKE_1                # first reaction; optional/scout, higher risk
-> MOVE_AWAY
-> RETEST_PENDING
-> RETEST_AT_SWITCHED_LEVEL
-> PA_CONFIRM             # when present
-> FRAME_STAND_CONFIRM    # when used
-> STRUCTURE_CONFIRM      # HL/reclaim or LH/lose support/local break
-> ENTRY_2_READY
```

Logical stages may occur in the same candle. The source does not require one candle per state.

## Zone-first rule

Source semantics are explicit:

```text
prepared zone/frame first
-> price reaches/interacts with zone
-> only then search for brake behavior
```

A brake pattern away from an active/prepared zone is not the same setup.

Exact zone construction remains source-family dependent and is not solved by RQ-004.

## First brake vs preferred retest entry

The source distinguishes:

- `ENTRY_1_SCOUT`: first brake/reaction, higher-risk and optional;
- `ENTRY_2_RETEST`: preferred confirmation entry after the market demonstrates the stop/reversal and returns to retest.

Do not make Entry #1 mandatory.

## Retest semantics

A full structural retest is stronger than candles merely sitting on a line.

Supported concept:

```text
BRAKE_1
-> move away / through structure
-> meet opposite support/resistance
-> return to the switched level
-> retest candidate
-> confirmation
```

The source explicitly warns against treating every line-standing sequence as a complete structural retest.

## Frame-standing semantics

Source-backed findings:

- counting begins from the first candle touching/interacting with the frame;
- teacher observes approximately `4–10 closed candles` on M1/M5 in the frame-standing discussion;
- candle-body relation/finishing on the valid side is primary evidence;
- wick-on-line can contribute as secondary evidence;
- examples show bodies completing on the support side for BUY and under resistance/frame for SELL.

Safe representation:

```text
standing_observation_window = approximately 4..10 closed candles
count_start = first frame-touch candle
body_standing = primary feature
wick_on_line = secondary feature
```

The source does **not** close:

- exact point tolerance;
- all-candles vs majority/ordered-sequence requirement;
- treatment of straddling bodies;
- whether 10 is a hard maximum or practical observation guideline.

Therefore `4–10` must not become a fabricated hard pass/fail formula.

## Structure confirmation

Source supports additional local structure features:

```text
BUY: higher low / raised low + reclaim or break local high
SELL: lower high + lose support / break local low
```

Exact pivot-window parameters remain unresolved.

## Failure/overlap branch

A first brake can fail or become overlap/liquidity-sweep behavior:

```text
BRAKE_1
-> OVERLAP / LIQUIDITY_SWEEP
-> REEVALUATE
-> NEW BRAKE / RETEST
```

Example values around 300 points and volatility extensions toward 500 points occur in teaching, but are not universal thresholds.

## M1 vs M5

The source teaches the same abstract brake concept on M1 and M5.

- M1 is finer/noisier/more aggressive;
- M5 is the safer teaching path;
- M1 may use trendline/structure assistance.

Literal screen angle such as ~45 degrees is heuristic and chart-scale dependent; it must not be encoded as a market invariant.

## Entry accounting separation

Source evidence requires separate accounting:

```text
FRAME_BRAKE_ENTRY != SIG_ENTRY
```

Frame-brake entry does not automatically have a native SIG run anchor at entry. SIG entry uses post-SIG anchor and timeframe run rules.

## What remains parameterized

- large-force quantitative threshold;
- weakening ratio;
- rejection wick threshold;
- color-shift minimum body threshold;
- frame-standing point tolerance and all-vs-majority logic;
- local pivot-window definition;
- zone-family exact geometry;
- universal SL/TP values.

## Closure decision

```text
SOURCE_BACKED_STATE_MACHINE_PARAMETERIZED
```

The transition/state representation is source-backed enough to replay as features and states. Exact quantitative gates remain intentionally parameterized/unknown.

## Next queue item

Promote `RQ-005 — Sideway construction, completion, and transition to new SIG`.
