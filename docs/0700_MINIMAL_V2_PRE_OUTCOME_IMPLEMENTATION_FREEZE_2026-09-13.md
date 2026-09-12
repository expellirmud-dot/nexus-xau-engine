# 07:00 MINIMAL V2 — Pre-Outcome Implementation Freeze — 2026-09-13

Status: IMPLEMENTATION FROZEN / SYNTHETIC CONTRACT PASSED / REAL V2 OUTCOMES NOT YET OPENED

Version:

`0700_MINIMAL_V2.0`

Frozen semantic specification:

`docs/0700_MINIMAL_V2_FROZEN_SPEC_2026-09-13.md`

Implementation:

`src/nexus_xau/research/minimal_v2_0700.py`

Synthetic contract suite:

`tests/test_minimal_v2_0700.py`

## Purpose

Record the exact implementation checkpoint that exists before any new V2 historical discovery outcome is opened or interpreted.

This checkpoint separates:

```text
spec freeze
-> implementation
-> synthetic logic proof
-> real historical replay
```

and prevents later discovery outcomes from silently changing the same V2.0 semantics.

## Frozen implementation properties

### Origin lane

- H4 only.
- PAT2 FULL-RANGE detector.
- adjacent post-SIG H4 research anchor retained as explicit research representation.
- nominal H4 run = 1,500 project points.
- no H1/D1 origin.
- no consumed-ratio threshold.

### PAT2 detector

Midpoint:

```text
(prior.high + prior.low) / 2
```

Strict directional close pass:

- BUY: previous bearish, current bullish, current.close > midpoint.
- SELL: previous bullish, current bearish, current.close < midpoint.
- equality does not pass.

### Point-check / terminal ordering

Origin lifecycle uses first-hit ordering between:

- nominal H4 target;
- literal M1 point-check contact.

Same-M1-bar target + point-check remains:

`AMBIGUOUS_TERMINAL_SAME_BAR`

No OHLC guess is used to resolve ordering inside one M1 bar.

### 07:00 state

- 07:00 Asia/Bangkok = 00:00 UTC.
- existing Daily Frame candidate builder retained.
- exact 0/5 tie remains ambiguous.
- tie -> fail closed.

### Confirmation

- M5 only for V2.0 scope.
- PAT2 FULL-RANGE.
- strictly after 07:00 and before next 07:00.
- same side as H4 origin.

### Location

Research metadata retains coarse expected/crossed-side representation.

Action lane remains fail-closed because exact universal PAT-to-frame location geometry is not source-closed:

`PASS_SOURCE_GEOMETRY_UNRESOLVED`

Multiple materially active H4 origins / opposite-side actionable conflict:

`PASS_CONFLICT_UNRESOLVED`

### Target

Research target uses:

`PATH_REMAINING_AT_CONFIRMATION`

with M5 PAT2 close as the explicit research reference.

This is not a broker fill claim.

## Synthetic contract results

Targeted suite:

`16 passed`

Covered:

1. PAT2 BUY strict FULL-RANGE midpoint pass.
2. midpoint equality fails.
3. PAT2 SELL strict FULL-RANGE midpoint pass.
4. BODY midpoint may pass while FULL-RANGE correctly fails.
5. exact point-check touch destroys.
6. one-project-point near miss survives.
7. target-first origin lifecycle marks run complete.
8. point-check-first lifecycle marks destroyed.
9. run completion before confirmation is terminal.
10. point-check destruction before confirmation is terminal.
11. exact Daily Frame half-step produces ambiguous two-candidate tie.
12. bar beginning at 07:00 does not leak into pre-07 state.
13. same-bar target + point-check is ambiguous.
14. multiple/opposite H4 origins fail closed in action lane.
15. single research candidate still fails closed on unresolved location geometry.
16. first M5 confirmation is strictly after cutoff and before next cutoff.

Targeted Ruff:

`PASS`

Full repository pytest:

`EXIT CODE 0`

Warnings are existing/deprecation-class warnings and do not change the V2 contract result.

## Real-outcome lock

At this checkpoint:

`NEW V2 DISCOVERY OUTCOMES OPENED = NO`

Next permitted action:

run the frozen code unchanged on:

`2022-09-01 -> 2023-03-31`

Expected scaffold:

`150 07:00 days`

The first analysis must be a failure/unknown-state map and descriptive signal/run report.

It must not introduce or optimize:

- consumed threshold;
- location tolerance;
- origin winner;
- MTF minimum;
- PAT variant;
- target distance;
- outcome-selected exclusion.

## Version rule after opening discovery

Once the first V2.0 discovery report is opened:

- semantic changes require V2.1 or later;
- bug fixes require an explicit checkpoint explaining the defect and whether outcomes could have influenced the fix;
- V2.0 results remain preserved.

## Claim boundary

Passing the synthetic contract proves implementation behavior against the frozen contract.

It does not prove:

- market edge;
- market frequency;
- trade/system Win Rate;
- profitability;
- real-money readiness.
