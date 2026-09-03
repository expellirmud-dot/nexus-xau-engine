# Direct Relative Por Chon Over-Round Usage — 2026-09-03

Status: DIRECT RELATIVE / PROJECT-OWNER-SUPPLIED EVIDENCE

## Source package

Project owner supplied one relative-chat message together with an annotated M5 XAUUSD chart. The two images are the same event/evidence package and must not be double-counted as separate examples.

Direct relative wording preserved conceptually:

- `กรอบพ่อชล คือ เอาไว้สวน ตอนวิ่งเกินรอบมาเยอะ`
- `ถ้าไม่แตะเส้น เกิดสัญญาณกลับตัวก็เข้าออเดอร์`
- `วาง SL ใต้เส้น ATH`
- `ช่วงกราฟ SW จะไม่นิยมใช้`

Annotated chart context:

- timeframe shown: M5;
- a `PA Sell` is marked after a strong upward move;
- the marked ATH frame is above the PA Sell/reversal area;
- annotation says `ไม่แตะ ATH วิ่งเกินรอบ`;
- therefore this example explicitly demonstrates a reversal setup that does not require price to touch the ATH line first.

## Claims closed by this direct evidence

### 1. Por Chon ATH is used as over-round reversal context

Direct semantic rule:

```text
POR_CHON_ATH_USAGE includes counter/reversal planning after price has run substantially beyond its normal round.
```

This does NOT mean that nominal TP completion alone is enough to counter-trade. Existing source-backed rules still require reversal evidence. The new direct relative statement fits that structure: over-round context + reversal signal.

### 2. Touching the ATH line is not mandatory for this reversal use

Direct rule:

```text
ATH_LINE_TOUCH is NOT a mandatory precondition when an over-round move produces a valid reversal signal in this Por Chon usage context.
```

The chart itself is labeled `ไม่แตะ ATH` while showing `PA Sell` and the relative explicitly says that if the line is not touched but a reversal signal occurs, an order can be entered.

Engineering consequence: do not encode Por Chon reversal use as `distance_to_ath == 0` or `must_touch_ath`.

### 3. Sideway is not the preferred Por Chon usage state

Direct wording:

```text
ช่วงกราฟ SW จะไม่นิยมใช้
```

Canonical interpretation:

```text
POR_CHON_ATH reversal usage is not normally preferred during SIDEWAY.
```

Important wording discipline: `ไม่นิยมใช้` means not normally/preferentially used. It is weaker than a universal hard prohibition such as `FORBIDDEN_IN_SIDEWAY` unless a stronger source later states that.

### 4. Setup-specific Sell SL relation to ATH line

In the supplied Sell example, the ATH line is visibly above the PA Sell/entry area. Therefore the phrase `วาง SL ใต้เส้น ATH` is geometrically compatible with a Sell stop: the stop can be above the entry/current price while still remaining below the ATH line.

Evidence-supported relation for this example/context only:

```text
SELL over-round reversal example:
entry/reversal area < SL < ATH line
```

Still unresolved:

- exact SL-to-ATH distance/buffer;
- whether this is mandatory for every Por Chon reversal setup;
- BUY-side mirror logic;
- behavior when the reversal signal forms above/beyond the ATH line rather than below it.

Do not universalize or mirror without direct evidence.

## Interaction with existing project rules

This evidence does NOT replace the hard PA location semantics:

```text
BUY PA/PAT valid only at support
SELL PA/PAT valid only at resistance
```

It instead clarifies that the Por Chon ATH line itself does not have to be physically touched for the over-round reversal setup. A valid reversal PA still needs its own valid location context under the system's PA rules.

It also remains consistent with the existing rule:

```text
nominal TP/run completion alone is not a reversal signal;
additional brake/opposite-PA/reversal evidence is required.
```

## Still unresolved

- exact meaning/timezone of Por Chon `19:00-19:00` construction window;
- exact numeric definition of `วิ่งเกินรอบมาเยอะ` beyond the known timeframe/run framework;
- exact reversal-signal qualification for every Por Chon setup family;
- exact SL buffer below ATH;
- whether/when Por Chon may still be used inside a special Sideway configuration despite `ไม่นิยมใช้` wording.

## Engineering status

Safe to encode as state/context metadata:

```text
por_chon_overround_context = true|false|unknown
ath_touch_required_for_overround_reversal = false
sideway_preference = NOT_PREFERRED
ath_relative_sl_rule = EXAMPLE_SUPPORTED_NOT_UNIVERSAL
```

Do not promote unresolved numeric thresholds to canonical engine constants.
