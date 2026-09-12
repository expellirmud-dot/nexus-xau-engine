# 07:00 Daily Frame / Support-Resistance Selector Source Closure — EP.3 — 2026-09-13

Status: PARTIAL SOURCE CLOSURE / SELECTOR PRINCIPLES STRENGTHENED / EXACT 0-5 SNAP STILL OPEN

## Source

YouTube:

https://youtu.be/jBEM-vWYj_o

Title:

`EP.3 แนวรับ - แนวต้าน #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว`

Acquisition:

- NEXUS Remote Chrome;
- `agent-browser --cdp 9222`;
- YouTube modern transcript panel `PAmodern_transcript_view`;
- targeted timestamp review.

This source was not required to be downloaded locally.

## Bounded questions reviewed

1. How to choose among nearby S/R candidates?
2. Is exact 0/5 snap/tie handling taught here?
3. Is qualification wick/body/close/penetration based?
4. Is there H4/H1 priority?
5. Is 7–14 points a universal tolerance?
6. When is a level retired/replaced?

---

## 1. Support/resistance is a zone, not a dead price — SOURCE-BACKED

Around ~20:00 the instructor explicitly states that support/resistance is a **zone**, not a fixed/dead price, even if a displayed price looks precise.

Engineering consequence:

```text
S/R representation = price area / zone
not universal exact-price equality
```

This argues against converting every demonstrated line into a hard one-tick gate.

---

## 2. Important S/R requires multi-timeframe price overlap — SOURCE-BACKED SEMANTIC

Around ~1:38:17–1:39:47:

- instructor separates S/R strength classes;
- “important” S/R is described using price overlap across **at least two timeframes**;
- construction can use candle **body or wick** from larger timeframes;
- larger-timeframe grouping is discussed separately from H1/H4;
- a round-price example around 4,000 is shown in the lesson.

Safe abstraction:

```text
IMPORTANT_SR_CANDIDATE
  requires cross-timeframe overlap/confluence
  using body/wick structural references
```

Do **not** infer from the single 4,000 example that every valid S/R must be a round-number price.

---

## 3. Large-TF wick/body can map into lower-TF body/wick — SOURCE-BACKED

Around ~1:42:37–1:46:13:

- instructor demonstrates drawing from a larger-TF wick;
- after moving to a smaller timeframe, that same structural price can appear as a body region;
- source explicitly emphasizes that a large-TF wick can carry significance because it may correspond to lower-TF body structure;
- overlapping structures can create meaningful future S/R zones.

Therefore:

```text
wick vs body is not a universal either/or selector
```

The source supports structural cross-timeframe mapping.

It does **not** support one universal rule such as:

`always wick`

or

`always body`.

---

## 4. Fresh / unused zones are preferred — SOURCE-BACKED

Around ~1:25:35–1:25:42:

- instructor states that support/resistance already used has reduced effectiveness;
- emphasizes using S/R that has not yet been used / fresh levels.

Around ~2:17:03–2:19:38:

- an untouched zone is discussed as still able to have an effect;
- a future resistance can become a new support after price moves through it;
- the new zone should be represented as an area, with nearby historical candle structures used as reference.

Safe state feature:

```text
zone_freshness:
  FRESH / UNTOUCHED
  USED
  BROKEN / SWITCHED
```

Important nuance:

`USED` does not automatically mean unusable.

---

## 5. Zone can remain usable until structural break — SOURCE-BACKED SEMANTIC

Around ~2:22:35 the instructor answers the question “how many times can the zone be used?” conceptually as:

`use it until it breaks`

This must be combined with the previous freshness statement:

- repeated use can reduce effectiveness;
- but the level is not automatically deleted after one contact;
- structural break is the stronger retirement/switch event.

Safe state shell:

```text
FRESH
-> TOUCHED / USED
-> may remain active with reduced strength
-> BROKEN
-> retired or role-switched according to context
```

Exact numeric break tolerance remains unresolved.

---

## 6. H4-first, H1-fallback for the reviewed strong-zone workflow — SOURCE-BACKED FAMILY ROUTING

Around ~2:25:11–2:25:28:

- instructor states that if the relevant H4 structure cannot be found, drop one timeframe and inspect H1;
- H1 can then provide the zone.

Around ~2:30:40 and ~2:35:16:

- H4 is repeatedly emphasized for strong-zone work / planning;
- entry timing is then refined on smaller timeframe such as M5.

Safe routing for this **support/resistance / strong-zone family**:

```text
search H4 structural zone first
if no valid H4 candidate:
    inspect H1 fallback
then use lower-TF confirmation/entry logic
```

Do not universalize this routing to every Mae Pla / ATH / Sideway / SIG family without separate source evidence.

---

## 7. Daily working preparation uses multiple H4 zones — SOURCE-BACKED EXAMPLE/METHOD

Around ~2:18:21:

- instructor says she normally draws **two zones per day**;
- those daily working zones are H4 zones;
- whether price breaks/does not break the zone must be read from candle behavior.

This is useful evidence against a hidden assumption that a day always has only one valid S/R candidate.

Research representation should preserve multiple Daily/H4 candidate zones rather than silently selecting one universal winner.

---

## 8. Daily 1,000-point frame is not simply deleted after price passes it — SOURCE-BACKED

Around ~2:21:14–2:21:21:

Question is asked whether a Daily 1,000-point frame should be deleted after price has passed it.

Instructor answers conceptually:

- do not delete it;
- after the main 1,000-point role has passed, it remains as an ordinary meaningful ~500-point frame/reference;
- the line can remain drawn.

This strengthens lifecycle representation:

```text
DAILY_1000_ACTIVE
-> primary 1000 role completed/passed
-> downgrade to ordinary 500-significance frame/reference
not immediate DELETE
```

This is a source lifecycle statement, not a reason to add a new entry by itself.

---

## 9. Break/stand qualification is candle-structural, not simply line-touch — SOURCE-BACKED SEMANTIC / NUMERIC OPEN

Around ~2:18:21–2:22:10:

- instructor repeatedly says to inspect whether the candle “breaks / does not break” the zone;
- discussion distinguishes standing/breaking the frame and whether price/candle moves through it;
- lower-timeframe M5 is used to read the reaction/entry sequence;
- later M5 brake lesson provides the detailed confirmation state machine.

Safe conclusion:

```text
S/R qualification is structural/candle-based
not merely:
distance_to_line <= fixed_tolerance
```

Still unresolved from this source:

- exact wick penetration allowance;
- exact body-close condition;
- exact number of confirming closed candles;
- universal point tolerance.

---

## 10. Exact 0/5 snap/tie rule — NOT CLOSED BY EP.3

The targeted EP.3 transcript review did **not** provide a direct universal statement defining:

- nearest statistical price ending in 0 or 5;
- how ties are resolved;
- rounding precision;
- whether 0/5 is mandatory for all S/R families.

A round-price example occurs, but it is not enough to define the 0/5 algorithm.

Current status remains:

`EXACT_0_5_SNAP_TIE = UNRESOLVED / PARAMETERIZED`

Do not derive the snap rule from whichever historical rounding produces better results.

---

## 11. 7–14 point contact tolerance — NOT CLOSED AS UNIVERSAL

This EP.3 review did not provide a clean universal statement that:

`7–14 points = mandatory S/R qualification tolerance`

Existing project material can still retain 7–14 as source-observed confluence/contact guidance where originally evidenced.

It must not be promoted into a universal pass/fail threshold from this review.

---

# Updated selector representation

The Daily/SR layer can now safely preserve more source state:

```text
candidate zone family
timeframe source
body/wick structural reference
cross-TF overlap count/set
freshness state
touch/use history
break/switch state
H4-first / H1-fallback for strong-zone workflow
multiple daily H4 candidates
```

The selector must still keep UNKNOWN/parameterized fields for:

```text
exact 0/5 snap/tie
exact wick/body/close numeric qualification
exact contact tolerance
universal priority across different frame families
```

## 07:00 implication

This source narrows the 07:00 location problem from:

> “Which one line is the correct line?”

to:

> “Which source-backed zone candidates exist, what TF/structure supports them, are they fresh/used/broken, and what cross-TF confluence do they have?”

That is a richer and safer representation than selecting one nearest price before source qualification.

## Claim boundary

This closure does not establish:

- a universal 0/5 rounding formula;
- one exact line for every day;
- a universal 7–14 point gate;
- a universal body-only or wick-only rule;
- a profitable entry strategy;
- system/trade Win Rate.

It closes/narrows selector semantics and zone lifecycle only.
