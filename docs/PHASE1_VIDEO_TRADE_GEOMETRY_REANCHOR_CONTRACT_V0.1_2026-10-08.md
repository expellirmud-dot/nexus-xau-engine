# Phase 1 Video Trade-Geometry Re-anchor Contract V0.1 — 2026-10-08

Status: FROZEN PRE-IMPLEMENTATION / PRE-NEW-OUTCOME / SOURCE RE-ANCHOR / ORDER SEND DISABLED / HOLDOUT UNSCORED

Contract ID: `PHASE1_VIDEO_TRADE_GEOMETRY_REANCHOR_V0.1`

Source evidence:

`docs/VIDEO_SOURCE_EVIDENCE_SL_TP_WICK_REANCHOR_2026-10-08.md`

## Trigger

New first-party teaching evidence supplied by the project owner satisfies the actionability trigger for `U-P1-10-STOP-GEOMETRY` and also introduces a decision-critical source correction to target anchoring.

## Questions frozen before implementation/outcome

1. What exact Buy-side SL reference is supported by the two videos?
2. Is the explicit `100`-point statement a universal buffer or an example-specific placement?
3. Does the confirmed wick/check correspond exactly to an existing PAT/post-SIG origin anchor representation, or is a new source anchor mapping required?
4. Does target intent use a fixed wick/origin target level rather than V2.0 `PATH_REMAINING_AT_CONFIRMATION`?
5. Which H1/H4/Day distance statements are directly source-backed and which broader stage rules remain open?
6. What remains unresolved for SELL-side geometry and other setup families?

These questions must be answered from source/geometry first. Historical outcomes must not choose among interpretations.
## Frozen provisional source representation

### Parent-timeframe wick state

- while the parent candle is open, its wick is provisional and may move;
- after the parent candle closes with the shown directional >50% body-close condition, the final wick becomes the confirmed check reference for the shown Buy example;
- code/research semantics use neutral labels rather than relying on uncertain jargon spelling.

### Buy-side entry/check relation

For the shown H1 Buy example:

`confirmed check wick survives -> next H1 opens -> lower-TF M1/M5 reversal occurs before check touch -> Buy candidate`.

A touch of the check before entry invalidates that candidate relation in the shown teaching example.

### Buy-side stop relation

Freeze the source evidence as two layers, not one invented scalar:

`STOP_REFERENCE = CONFIRMED_CHECK_WICK / LOCAL LOW STRUCTURE`

`EXPLICIT_100_POINT_BUFFER = OBSERVED_IN_ONE_BUY_SUPPORT_EXAMPLE`

No universal `SL = wick - 100` rule is authorized until source reconciliation closes whether the 100 points is mandatory, maximum, typical, or example-specific.

SELL symmetry is not inferred.

### Target relation

For the shown Buy direction, the target reference is fixed from the wick/origin reference:

`H1_TARGET_LEVEL = confirmed_wick + 1000 project points`

`H4_TARGET_LEVEL = confirmed_wick + 1500 project points`

`DAY_5000_TARGET_EXAMPLE = confirmed_wick + 5000 project points`

For a late entry, remaining distance is the directional distance from the later entry to the pre-existing fixed target level. The source does not support resetting a fresh full run from the later entry.

The Day statement does not close the broader 5,000–10,000 stage/set family.
## Historical representation boundary

`0700_MINIMAL_V2.0` and prior Q1/Q2/Q3/Q4 results remain historical evidence exactly as run.

`PATH_REMAINING_AT_CONFIRMATION` remains valid as a versioned research/scoring representation that was frozen before those outcomes.

It is NOT allowed to remain labeled as teacher-intent authority if this re-anchor closes in favor of fixed wick/origin target levels.

Any executable/source-faithful target semantic change requires a new version after this contract.

## Required source-geometry closure before code change

1. Map the confirmed wick/check in the videos against existing PAT/post-SIG anchor definitions.
2. Determine whether existing Point #1 / point-check evidence is the same structural object or only a related concept.
3. Preserve the explicit 100-point Buy example without universalizing it.
4. Preserve Buy-only directionality unless independent Sell evidence exists.
5. Preserve Day 5,000 as a bounded target example without erasing the separately evidenced 5,000–10,000 Day family.
6. Update canonical claims/state only from source reconciliation, not from historical performance.

## Implementation tests required for any new version

- provisional wick cannot become a final check before parent-bar close;
- confirmed check wick is immutable after the parent bar is closed;
- lower-TF reversal after the parent close cannot qualify if the check was touched first;
- fixed origin target remains invariant when a later entry occurs after retracement;
- remaining entry-to-target distance is derived from the fixed target level, not `nominal - historical MFE`;
- V2.0 historical outputs remain reproducible and unchanged;
- no Sell mirror rule appears without a Sell source contract;
- no universal 100-point buffer appears unless separately source-closed;
- holdout scoring remains disabled;
- automatic order sending remains disabled.

## Prohibited shortcuts

- do not rewrite V2.0 in place;
- do not use prior TARGET_FIRST results to justify fixed-origin or PATH_REMAINING target intent;
- do not turn the 100-point statement into a universal SL constant from a single Buy example;
- do not infer SELL geometry by symmetry;
- do not reinterpret current broker point/tick size as instructor point semantics;
- do not score profitability/Win Rate/expectancy from this source re-anchor.

## Expected registry consequence

`U-P1-10-STOP-GEOMETRY` is now `ACTIONABLE_NOW` because its source-evidence trigger has arrived.

It remains OPEN until the source reconciliation identifies what is fully resolved versus what must be split into residual stop-reference/buffer/direction dependencies.