# Direct Relative PA Location Clarification — 2026-09-01

Date: 2026-09-01
Evidence class: **DIRECT RELATIVE / PROJECT OWNER-SUPPLIED RULE**

## Direct rule

The project owner supplied the following clarification from the relative who learned/uses the system:

- **BUY PA must occur at support only.**
- **SELL PA must occur at resistance only.**

This is a stronger wording than merely saying that support/resistance is a preferred context. For the system rule, side/location is a required qualification condition.

## Engineering consequence

At the semantic level:

```text
PA_BUY_VALID  => location == SUPPORT
PA_SELL_VALID => location == RESISTANCE
```

A visually matching PAT at the wrong side must not be promoted to a valid PA of that direction.

Suggested qualification shell:

```pseudo
if pat.direction == BUY and not at_support(candidate, context):
    reject_as_valid_PA_buy()

if pat.direction == SELL and not at_resistance(candidate, context):
    reject_as_valid_PA_sell()
```

## What this closes

- Direction/location mapping is now **CLOSED at rule semantics**:
  - BUY = support only
  - SELL = resistance only

## What remains unresolved

This does **not** yet make `at_support()` / `at_resistance()` deterministic. Still required:

- exact support/resistance construction source;
- point-distance tolerance from the line/zone;
- treatment of wick penetration versus body close;
- overlapping multi-timeframe support/resistance priority;
- whether the valid object is a line, band/zone, or nearest `ซอก/ไส้/คู่` structure in each setup family.

Therefore this evidence strengthens PA qualification confidence but does not remove the location-tolerance blocker for `detect_PA_exact()`.
