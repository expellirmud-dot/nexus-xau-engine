# RQ-009 — EP.5 Component Definition Source Reconciliation

Date: 2026-09-09 Asia/Bangkok
Source: original YouTube EP.5 `oCcG3dUjrgw` Show transcript + synchronized original-video whiteboard frames
Status: `SOURCE_DEFINITION + VISUAL RECONCILIATION / UNIVERSAL ASSEMBLY STILL OPEN`

## Why this checkpoint exists

A prior visual checkpoint inferred the shown `คู่` relation mainly from the whiteboard geometry and described the two candle bodies as not needing equal heights. A later direct re-read of the dedicated definition block at approximately `20:33-36:32` provides materially more precise instructor wording.

The old checkpoint remains preserved as research history. This document narrows/corrects the current interpretation instead of silently rewriting that history.

No historical outcome, Win/Loss, or replay performance is used here.

## Evidence layers

Keep three layers separate:

1. `SOURCE WORDING` — YouTube Show transcript attributable to the original lesson, with ASR risk.
2. `SOURCE VISUAL` — original-video whiteboard/chart frames synchronized to the teaching block.
3. `SAFE RESEARCH REPRESENTATION` — only the minimum geometry justified by 1+2.

## 1. `ซอก` — direct source definition is stronger than the prior visual inference

### Source wording

Around `20:33-22:43`, the instructor defines `ซอก` as the joint/corner between prices and repeatedly states that, in the taught same-color form, the prior candle close and the next candle open are the same price.

Key source semantics:

- `ซอก` is a price joint/corner (`รอยต่อ/ข้อต่อของราคา`).
- The taught form uses same-color candles.
- Prior close and next open are the same reference price.
- That shared price may function as support or resistance depending on context.

### Safe research representation

For the source-defined shown form:

```text
same candle color
AND normalized C[i] == normalized O[i+1]
=> shared close/open body-junction price is a `ซอก` reference
```

`==` above is semantic equality after feed/price normalization. The broker-feed tolerance/normalization rule is still unresolved and must not be fitted from outcomes.

## 2. `คู่` — source wording narrows the previous “body heights need not match” statement

### Source wording

Around `26:47-30:08`, the instructor explicitly teaches `คู่` as a support/resistance pair and gives several constraints:

- `คู่` can be a support pair or resistance pair.
- The two candles are opposite colors / alternating colors (`แดง-เขียว` or `เขียว-แดง`).
- The instructor repeatedly says the paired candle body relation is equal at support/resistance (`เนื้อเทียนเท่ากันที่แนวรับ/แนวต้าน`).
- The relevant paired open/close price is called an equilibrium price (`ราคาดุลยภาพ`).
- Around `29:52-29:59`, the instructor immediately qualifies that the residual/overhanging body portion (`เนื้อเทียนเหลื่อมล้ำกัน`) does not have to be equal, while the open/close relation at support/resistance must be equal.

### Source visual

The original whiteboard frames at approximately `26:47`, `28:03`, and `29:44` show both mirror forms:

- resistance: green followed by red at a common resistance reference;
- support: red followed by green at a common support reference.

The drawings show a common paired/equilibrium reference while one candle may extend farther away from that reference. This is consistent with the spoken distinction between the equal/aligned paired relation at support/resistance and a residual body extension that may differ.

### Reconciliation with the older visual checkpoint

The prior wording:

```text
body heights do not have to match
```

is too broad if read as saying body equality is irrelevant.

Current source-faithful wording is narrower:

```text
`คู่` requires opposite-color adjacent candles with an equal/aligned open-close equilibrium reference at support/resistance.
The residual body extension away from that paired reference may differ.
The source does not establish that the full absolute body lengths of both candles must be identical.
```

### Safe research representation

For the source-defined shown forms:

```text
RESISTANCE PAIR:
  green -> red
  normalized C_green == normalized O_red
  shared equilibrium price is at resistance

SUPPORT PAIR:
  red -> green
  normalized C_red == normalized O_green
  shared equilibrium price is at support
```

This is a source-defined shown-form representation, not yet a complete universal detector. Exact feed equality/tolerance and the universal support/resistance certification rule remain unresolved.

## 3. `ไส้` — remains a closed-candle wick structural price, not merely spacing metadata

Around `23:49-25:33`, the instructor defines `ไส้` as the candle wick and emphasizes that its final form is only known after the relevant timeframe candle closes.

A later Q&A at approximately `1:06:35-1:07:15` rejects the idea that the wick merely tells the distance between zones; the construction must be marked/considered in full.

Safe conclusion:

```text
wick reference = structural input price after the source timeframe candle is complete
```

Which wick wins when several source-compatible wicks exist remains unresolved.

## 4. All three components are required for the taught Body Collection zone

Around `31:27-32:40`, the instructor states that for H4 Body Collection the three components must occur in the zone and explicitly summarizes:

```text
ซอก + ไส้ + คู่ = โซน
```

This supports `ALL_COMPONENTS_REQUIRED` more directly than the later worked examples alone.

It does not by itself define a universal 3-component -> 2-reference reduction.

## 5. Component prices are used as forecast references, but the universal 3->2 transform is still absent

Around `36:21-36:32`, the source says, in substance, that whichever prices are found for `ซอก ไส้ คู่` are used as forecast points/references and distances are laid from them.

Around `40:42-40:58`, the current method is explicitly described as using `2 ระยะคาดการณ์` for order-entry reference, while finding `ซอก ไส้ คู่` on the same timeframe.

These two source facts create a bounded unresolved question:

```text
three required component types have meaningful source prices
AND current method uses two forecast references/distances
BUT reviewed source wording does not yet state a generic merge/min/max/rank rule when all three component prices are distinct
```

Therefore the prior `UNRESOLVED_THREE_TO_TWO` guard remains valid.

## 6. What is now closed more strongly

Source+visual evidence now supports the following current claims:

1. `ซอก` shown form: same-color close/open price joint.
2. `คู่` shown forms: opposite-color pair with equal/aligned open-close equilibrium reference at support/resistance; residual body extension may differ.
3. `ไส้`: closed-candle wick structural price.
4. `ซอก + ไส้ + คู่` are all required in the taught Body Collection zone.
5. Component reference prices are material forecast inputs.
6. Current teaching uses two forecast references/distances.

## 7. What remains unknown

- Broker/feed normalization or allowed tick difference for semantic open-close equality.
- Universal support/resistance certification geometry for every `คู่` candidate.
- Universal wick selection when several wicks qualify.
- Universal three-distinct-component -> two-reference transform.
- Same-timeframe multi-cluster winner priority.
- Exact touched/revalidated -> completed/used OHLC transition.
- Exact broker fill after lower-timeframe confirmation.

## Decision

Result: `SOURCE_DEFINITION_VISUAL_PARTIAL_ASSEMBLY`.

This checkpoint **narrows/corrects the active interpretation of `คู่`** while preserving the older visual-only document as historical evidence. The source definition is now strong enough to use the shown close/open equilibrium forms as research detectors with an explicit feed-equality guard. It is still not defensible to claim a universal automatic Body Collection assembly algorithm or to choose equality/assembly rules from historical outcomes.

Raw transcript and visual frames remain local under `youtube/_evidence/oCcG3dUjrgw/` and are not committed.
