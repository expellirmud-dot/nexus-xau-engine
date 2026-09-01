# Direct PAT Geometry Rules — 2026-09-01

Source class: **USER-DIRECT PROJECT EVIDENCE**.

This record preserves the PAT rules stated directly by the project owner in chat. The statement materially narrows PAT geometry but does not independently resolve every numeric tolerance. It should supersede weaker generic summaries when they conflict, while unresolved measurement bases remain parameterized.

## Global PA location rule — DIRECT

- **BUY-side PA/PAT is valid only at support.**
- **SELL-side PA/PAT is valid only at resistance.**

This is a hard qualification rule for the pattern family, not merely a confidence boost.

Engineering consequence:

```pseudo
valid_PA_BUY  = shape_match_buy  AND at_support
valid_PA_SELL = shape_match_sell AND at_resistance
```

A correct-looking BUY pattern away from support must not be promoted to valid PA Buy. Likewise, a correct-looking SELL pattern away from resistance must not be promoted to valid PA Sell.

The exact numeric tolerance for `at_support` / `at_resistance` is still unresolved and must remain configurable/unknown until a stronger source defines it.

## Direct rules stated

### PAT1

- Visual form: **long wick / small candle body**.
- BUY PAT1 must occur at support.
- SELL PAT1 must occur at resistance.
- This statement does not provide an exact wick/body ratio.

Engineering status: **SUPPORTED TOPOLOGY + HARD LOCATION RULE; NUMERIC THRESHOLD OPEN**.

Open parameter:

```text
min_directional_wick_to_body_ratio = UNKNOWN
max_body_fraction_of_range = UNKNOWN
location_tolerance_points = UNKNOWN
```

### PAT2 BUY

- Must occur at **support**.
- Candle #1 = red.
- Candle #2 = green.
- Green candle must close **more than 50% of the preceding red candle**.

Candidate logic:

```pseudo
PAT2_BUY:
  at_support
  c1.bearish
  c2.bullish
  c2.close > midpoint_reference(c1)
```

The exact denominator/reference used for “50% of candle #1” remains unresolved unless separately verified as full High–Low range versus real body.

### PAT2 SELL

- Must occur at **resistance**.
- Candle #1 = green.
- Candle #2 = red.
- Red candle must close **more than 50% of the preceding green candle**.

Candidate logic:

```pseudo
PAT2_SELL:
  at_resistance
  c1.bullish
  c2.bearish
  c2.close < midpoint_reference(c1)
```

Exact 50% measurement basis remains open.

### PAT3 BUY

- Must occur at **support**.
- Candle #1 = red.
- Candle #2 = green or red.
- Candle #2 has a **small body**.
- Candle #3 = green.
- Candle #3 must close **more than 50% of both preceding candles**.

Candidate logic:

```pseudo
PAT3_BUY:
  at_support
  c1.bearish
  c2.color in {bullish, bearish}
  small_body(c2)
  c3.bullish
  c3.close > midpoint_reference(c1)
  c3.close > midpoint_reference(c2)
```

This direct statement substantially explains the previously observed PAT3 visual variants as alternative candle-2 forms rather than separate PAT numbers.

### PAT3 SELL

- Must occur at **resistance**.
- Candle #1 = green.
- Candle #2 = green or red.
- Candle #2 has a **small body**.
- Candle #2 has upper/lower wicks described as approximately equal.
- Candle #3 = red.
- Candle #3 must close **more than 50% of both preceding candles** in the Sell direction.

Candidate logic:

```pseudo
PAT3_SELL:
  at_resistance
  c1.bullish
  c2.color in {bullish, bearish}
  small_body(c2)
  approximately_equal_upper_lower_wicks(c2)
  c3.bearish
  c3.close < midpoint_reference(c1)
  c3.close < midpoint_reference(c2)
```

Important: the equal-upper/lower-wick detail was stated explicitly for the SELL description in this chat message. Do **not** silently mirror it to BUY unless another direct source confirms symmetry.

## What this closes

This evidence materially closes the prior open questions about:

- BUY PAT/PAs must occur at support only;
- SELL PAT/PAs must occur at resistance only;
- PAT2 required color order;
- PAT2 directional >50% close relationship;
- PAT3 candle-1 direction;
- PAT3 candle-2 color flexibility;
- PAT3 candle-2 small-body role;
- PAT3 candle-3 direction;
- PAT3 candle-3 >50% relationship to both previous candles;
- PAT3 SELL candle-2 approximate equal-wick characteristic.

## What remains unresolved

Do not invent numeric values for:

1. PAT1 exact wick/body ratio.
2. PAT1 maximum body fraction.
3. PAT2/PAT3 exact 50% denominator: real body vs High–Low range.
4. PAT2/PAT3 tolerance around the 50% threshold and equality handling.
5. Numeric definition of `small_body(c2)` in PAT3.
6. Numeric tolerance for “upper/lower wicks approximately equal” in PAT3 SELL.
7. Exact support/resistance distance tolerance used by `at_support` / `at_resistance`.

## Engineering consequence

PAT candidate detection can now move from visual-topology-only to a constrained qualification chain:

```text
CANDLE COLORS / BODY / >50% GEOMETRY
→ HARD LOCATION FILTER (BUY=SUPPORT / SELL=RESISTANCE)
→ CLOSED-CANDLE REQUIREMENT
→ POST-SIG VALIDATION
```

Exact production detection should still expose unresolved thresholds as configuration/evidence fields instead of silently choosing values.
