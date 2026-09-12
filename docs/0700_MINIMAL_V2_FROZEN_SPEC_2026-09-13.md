# 07:00 MINIMAL V2 — Frozen Research Specification — 2026-09-13

Status: FROZEN_BEFORE_NEW_V2_OUTCOMES / SIGNAL-RUN RESEARCH / FAIL-CLOSED ACTION LANE

Version:

`0700_MINIMAL_V2.0`

## 1. Purpose

Build the narrowest useful 07:00 representation from evidence already in the repository, without reopening broad source research and without selecting rules from new V2 outcomes.

This version is designed to answer:

- how much of the 07:00 state can already be classified deterministically;
- which days become research candidates;
- which days must PASS because source/action geometry is unresolved;
- which failure/novelty families remain;
- whether the previously observed H4 consumed/run-progress relationship survives after replacing the historical PAT2 BODY proxy with the source-closed PAT2 FULL-RANGE geometry.

This is not yet a trade-P&L system.

## 2. Governing authority

Read with:

- `docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md`
- `docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md`
- `docs/0700_HISTORICAL_DATA_READINESS_AND_TEST_STRATEGY_2026-09-13.md`
- `docs/0700_PAT50_DENOMINATOR_SOURCE_CLOSURE_2026-09-13.md`
- `docs/RQ003_DAILY_FRAME_LOCATION_SOURCE_CLOSURE_2026-09-08.md`
- `docs/DIRECT_RELATIVE_REMAINING_SIG_RUN_DAILY_FRAME_2026-09-03.md`

## 3. Frozen scope

### Origin timeframe

`H4 only`

Reason:

- H4 nominal primary run = 1,500 project points is source-backed;
- H4 consumed/run-progress relation replicated in Q2-Q4;
- H1 consumed-state relation did not replicate;
- D1 exact stage transition remains open.

No H1/D1 origin is eligible in V2.0.

### H4 origin research representation

V2.0 keeps the existing adjacent post-SIG research-anchor topology but replaces the PA/PAT detector geometry.

Origin detector label:

`H4_PAT2_FULL_RANGE_POST_SIG_PROXY_V2`

Sequence:

```text
completed H4 prior candle
-> completed H4 confirming candle satisfies PAT2 FULL-RANGE rule
-> adjacent post-SIG H4 candle
-> BUY anchor = adjacent post-SIG low
-> SELL anchor = adjacent post-SIG high
```

This remains a **research representation**.

It is not promoted to a universal canonical SIG detector.

### PAT2 FULL-RANGE rule

Previous candle midpoint:

```text
midpoint = (previous.high + previous.low) / 2
```

BUY:

```text
previous candle bearish
current candle bullish
current.close > midpoint
```

SELL:

```text
previous candle bullish
current candle bearish
current.close < midpoint
```

Equality does not pass.

Full engulfing is not required.

### Nominal run

`H4 = 1,500 project points`

### Pre-07:00 origin eligibility

At 07:00 Asia/Bangkok = 00:00 UTC, an H4 origin research row is context-eligible only if:

- origin is known strictly before or at the cutoff under completed-bar semantics;
- nominal H4 run is not already completed before cutoff;
- literal M1 range contact has not touched the origin point-check before cutoff;
- input history is sufficient and not crossed by a known data defect.

Consumed ratio is retained continuously.

No consumed-ratio threshold is allowed.

### Point-check semantics

Literal M1 price-range contact with the research anchor destroys that research origin.

One-tick near miss survives.

This is the source-backed contact concept applied to the explicit research-proxy anchor.

### 07:00 Daily Frame construction

Retain the existing source-backed frame arithmetic:

```text
nearby statistical/minor 0-or-5 reference
upper = reference + 500 project points
lower = reference - 500 project points
```

If frame selector produces a tie/ambiguous candidate set:

`PASS_FRAME_TIE`

No outcome-selected tie break is permitted.

## 4. Critical location boundary

Source evidence does **not** yet close one universal deterministic PAT-to-frame qualification geometry.

Open possibilities include:

- wick touch;
- body intersection;
- close;
- penetration;
- family-specific distance/tolerance.

Therefore V2.0 has two separate lanes.

### A. Research candidate lane

For continuity with V1 and for exploratory failure-map comparison, record the frozen coarse relation:

BUY:

```text
EXPECTED_SIDE_RESEARCH_PROXY if PAT pattern low >= Daily Frame lower
CROSSED_SIDE_RESEARCH_PROXY otherwise
```

SELL:

```text
EXPECTED_SIDE_RESEARCH_PROXY if PAT pattern high <= Daily Frame upper
CROSSED_SIDE_RESEARCH_PROXY otherwise
```

This coarse relation is **not canonical location qualification**.

It may be used as metadata/grouping in V2 research.

It must not be called a source-closed entry location.

### B. Action eligibility lane

Automated action eligibility requires:

`location_qualification_state = TRUE`

Under current V2.0 historical automation, exact family-specific qualification is not source-closed.

Therefore when no external/manual source-compatible location label is available:

`location_qualification_state = UNKNOWN`

and terminal action state must be:

`PASS_SOURCE_GEOMETRY_UNRESOLVED`

This fail-closed lane prevents exploratory location proxies from silently becoming trading rules.

## 5. Post-07:00 confirmation lane

First V2.0 confirmation timeframe:

`M5 only`

This is a project research scope choice, not an instructor-exclusive rule.

Confirmation detector:

`PAT2_FULL_RANGE_SOURCE_CLOSED`

Requirements:

- event known strictly after 07:00;
- event known before next 07:00 boundary;
- same side as the H4 origin;
- PAT2 FULL-RANGE rule passes;
- Daily Frame is not tied/ambiguous.

Recent MTF alignment is recorded only as metadata if available.

No MTF count/minimum gate is allowed.

PAT3 is excluded.

## 6. Pre-confirmation recheck

Before a research candidate can be scored from an M5 confirmation:

- origin point-check must still be untouched before confirmation;
- H4 nominal run must still be incomplete before confirmation.

If point-check was touched first:

`PASS_ORIGIN_DESTROYED_BEFORE_CONFIRMATION`

If H4 nominal target was already completed first:

`PASS_RUN_COMPLETED_BEFORE_CONFIRMATION`

No later confirmation may revive that origin.

## 7. Remaining-run target representation

At confirmation time:

```text
consumed_points_at_confirmation
    = maximum favorable excursion from origin anchor up to confirmation knowledge time

remaining_points_at_confirmation
    = 1500 - consumed_points_at_confirmation
```

Research target price:

BUY:

```text
confirmation_reference_price + remaining_points_at_confirmation * point_size
```

SELL:

```text
confirmation_reference_price - remaining_points_at_confirmation * point_size
```

The exact confirmation reference used in the scorer must be explicitly recorded.

Preferred V2.0 research representation:

`confirmation close`

This is a **project research convention**, not a broker fill claim.

Do not reset a fresh 1,500-point target from confirmation.

## 8. Multiple-origin handling

No origin winner rule is source-closed.

Therefore:

### Research lane

Retain and score each surviving H4 origin separately.

Rows that share day/side are dependent context rows and must not be counted as independent trades.

### Action lane

If more than one surviving H4 origin can materially change the action/target and no source-backed winner exists:

`PASS_CONFLICT_UNRESOLVED`

Do not choose the best historical origin.

## 9. Opposite-direction context

Opposite-direction surviving H4 context is retained as metadata.

It is not a mandatory veto because Q1 did not support that rule.

If the action lane produces simultaneously conflicting actionable states without a source-backed resolver:

`PASS_CONFLICT_UNRESOLVED`

## 10. Research scoring horizon

For V2.0 development replay:

`confirmation known_at -> next 07:00 Asia/Bangkok boundary`

This is a project research convention for daily failure-map accounting.

It is not a source claim that the underlying run expires at the next 07:00.

Possible result categories:

- `TARGET_FIRST`
- `POINT_CHECK_FIRST`
- `AMBIGUOUS_SAME_BAR`
- `NEITHER_BY_NEXT_0700`

Ambiguous and neither rows remain in the report.

## 11. Daily terminal decision taxonomy

Every available 07:00 day must receive explicit day/action states.

Minimum terminal states:

- `RESEARCH_CANDIDATE`
- `PASS_NO_H4_ORIGIN`
- `PASS_H4_RUN_ALREADY_COMPLETE`
- `PASS_POINT_CHECK_ALREADY_DESTROYED`
- `PASS_FRAME_TIE`
- `PASS_NO_M5_PAT2_CONFIRMATION`
- `PASS_ORIGIN_DESTROYED_BEFORE_CONFIRMATION`
- `PASS_RUN_COMPLETED_BEFORE_CONFIRMATION`
- `PASS_SOURCE_GEOMETRY_UNRESOLVED`
- `PASS_CONFLICT_UNRESOLVED`
- `PASS_DATA_QUALITY`
- `PASS_UNKNOWN_STATE`
- `RECORD_FOR_RESEARCH`

Research candidate state and action eligibility must be separate columns.

## 12. Frozen exclusions

V2.0 deliberately excludes:

- H1 origins;
- D1 origins;
- D1 5K/10K stage logic;
- PAT3;
- universal Sideway auto-routing;
- automatic Body Collection winner;
- universal S/R-family conflict resolution;
- consumed-ratio threshold;
- minimum MTF alignment threshold;
- exact M1/M5 brake-force numeric gates;
- broker fill;
- spread/slippage/cost P&L;
- position sizing;
- system/trade Win Rate.

## 13. Synthetic contract tests required before real replay

At minimum:

1. PAT2 BUY strict full-range midpoint pass.
2. PAT2 BUY equality at midpoint fails.
3. PAT2 SELL strict full-range midpoint pass.
4. BODY midpoint would pass but FULL-RANGE midpoint fails.
5. point-check exact touch destroys.
6. one-tick near miss survives.
7. origin completed before 07:00 is not eligible.
8. origin destroyed before 07:00 is not eligible.
9. origin completes before M5 confirmation -> pass.
10. point-check destroys before M5 confirmation -> pass.
11. frame tie -> pass.
12. after-07:00 information cannot enter pre-07 state.
13. same-bar target + point-check -> ambiguous.
14. multiple unresolved H4 origins -> action pass / research rows retained.
15. unknown location qualification -> action pass while research metadata remains available.

No real V2 outcome replay may be interpreted until these contract tests pass.

## 14. Real replay order

After synthetic contract suite passes:

### Discovery

`2022-09-01 -> 2023-03-31`

Expected 07:00 scaffold days:

`150`

Output must emphasize:

- terminal-state counts;
- ENTER/research-candidate coverage;
- PASS reason counts;
- unknown-state fingerprints;
- H4 consumed-state relation under V2;
- differences from historical V1 caused by PAT2 FULL-RANGE;
- target/point/ambiguous/neither ordering.

Do not optimize thresholds.

### Cross-period replication

Run unchanged V2 code on:

`2023-09-01 -> 2023-11-23`

Expected 07:00 scaffold days:

`60`

No semantic code changes between discovery and replication.

## 15. Promotion rule

V2.0 may only be changed after discovery by creating a new version.

Do not modify V2.0 in place to rescue a losing historical case.

If a new material state appears:

```text
record
-> classify UNKNOWN/PASS
-> investigate
-> create V2.1 or later
-> test new version separately
```

## 16. Claim boundary

V2.0 can establish:

- deterministic logic correctness;
- coverage/PASS/unknown taxonomy;
- source-correct PAT2 representation effects;
- research signal/run relations;
- failure/novelty families.

V2.0 cannot establish by itself:

- guaranteed future outcomes;
- trade/system Win Rate;
- profitability;
- broker execution performance;
- a universal location rule;
- a universal H4 origin winner;
- a consumed threshold.

## Freeze declaration

This specification must be committed and pushed **before** implementation opens or summarizes new V2 discovery outcomes.

After freeze:

`semantic changes require a new version or an explicit pre-outcome bug-fix checkpoint that proves no V2 outcomes were inspected.`
