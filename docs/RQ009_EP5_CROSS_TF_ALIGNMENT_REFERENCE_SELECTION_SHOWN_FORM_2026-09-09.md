# RQ-009 — EP.5 Cross-TF Alignment + Two-Reference Shown-Form Closure

Date: 2026-09-09 Asia/Bangkok
Source: original YouTube EP.5 `oCcG3dUjrgw` rendered Show transcript + synchronized original-video screenshots
Status: `SOURCE+VISUAL_REPEATED_SHOWN_FORM_CLOSURE / UNIVERSAL PERMUTATIONS STILL OPEN`

## Research target

Close only what EP.5 actually demonstrates about two linked blockers:

1. what `ตรงกัน` means in the shown cross-timeframe Body Collection fallback; and
2. how the two forecast references behave when a higher/reference timeframe already supplies `ซอก + ไส้` and the missing `คู่` is found on the next lower timeframe.

No outcome data, Win/Loss result, profitability statistic, or fitted tolerance is used in this closure.

## Prior state

The preceding checkpoint established:

```text
H4 incomplete
-> H1 supplies ซอก + ไส้
-> M30 supplies คู่
-> instructor says the M30 pair "ตรงกัน"
-> completed โซนซอกไส้คู่
```

What remained open was whether the lower-timeframe `คู่` introduces a new third price/reference or instead aligns to one of the already identified higher-timeframe references.

## Source + visual evidence

### A. Worked H1 -> M30 example — ~1:02:17–1:02:53

Direct transcript sequence:

- ~1:02:17: on H1, instructor identifies `ซอก` and `ไส้`.
- ~1:02:35: instructor says the `คู่` exists in M30.
- ~1:02:45: instructor says `มันจะตรงกัน` and points to the M30 pair.
- ~1:02:53: instructor says this gives the previously drawn `โซนซอกไส้คู่`.

Synchronized visual evidence:

- `youtube/_evidence/oCcG3dUjrgw/visual_ep5/assembly_compare/1-02-28.png`
- `youtube/_evidence/oCcG3dUjrgw/visual_ep5/candidate_priority/1-02-53.png`

At the H1 view, **two horizontal reference lines are already present** while the source is identifying the H1 `ซอก + ไส้` structure.

At the M30 view, those **same two horizontal reference lines remain overlaid**. The instructor points to the opposite-color pair and says the pair is `ตรงกัน`. No third forecast line is introduced after the pair is found.

Safe visual/source interpretation for this shown form:

```text
parent/reference TF:
    ซอก + ไส้ -> two existing forecast/reference levels

next lower TF:
    คู่ equilibrium/reference aligns with one existing parent level
    -> completes the required ซอก + ไส้ + คู่ structural set
    -> no third forecast line is added
```

The visual supports level co-location/alignment at chart precision. It does **not** establish the exact broker-tick equality or an allowed numeric tolerance.

### B. Independent PA Sell example — ~1:12:57–1:13:16

Direct transcript sequence:

- source identifies the PA Sell PAT2 example and two forecast points;
- ~1:13:08: instructor says one reference is `ไส้` and one is `ซอก`;
- immediately after, instructor says the missing structure also exists in H1 (`แล้วก็ใน H1 ก็จะมี`).

Synchronized visual evidence:

- `youtube/_evidence/oCcG3dUjrgw/visual_ep5/mirror_lifecycle/1-13-05.png`
- `youtube/_evidence/oCcG3dUjrgw/visual_ep5/mirror_lifecycle/1-13-16.png`

The chart already carries two forecast/reference lines on the higher-timeframe structure while `ไส้` and `ซอก` are annotated. The lower-timeframe component is discussed as completing the structure, not as adding a third visible forecast line.

This independently repeats the same topology family: **two parent/reference-TF levels first, lower-TF component as completion/alignment evidence**.

### C. Later recap — ~1:56:13–1:56:28

The instructor again describes a fallback from H4 to H1 and then points out the `คู่` in M30. This is transcript-level repetition of the H1-partial / M30-pair completion pattern.

Because this recap is ASR-sensitive and no new synchronized screenshot was required for the present closure, it is supporting repetition rather than the primary geometry evidence.

## What is now source+visual closed

For the repeatedly shown fallback topology where the parent/reference timeframe already supplies `ซอก + ไส้`:

1. The two forecast/reference levels can already exist from the parent/reference timeframe before the lower-timeframe `คู่` is identified.
2. The lower-timeframe `คู่` is required to be `ตรงกัน` / aligned with the existing candidate structure.
3. In the reviewed M30 visual, the pair is associated with an already drawn parent reference level rather than creating a third forecast line.
4. Therefore a missing lower-TF component can act as **structural completion/validation at an existing forecast/reference level**, not necessarily as a new independent forecast price.
5. Component timeframe provenance must remain explicit.

Safe shown-form representation:

```text
parent_components = [SOK, WICK]
parent_reference_levels = [R1, R2]

lower_component = PAIR
lower_pair_equilibrium = ALIGNED_TO_EXISTING_PARENT_REFERENCE

result:
  components_complete = true
  forecast_reference_count = 2
  third_reference_added = false
```

## What `ตรงกัน` does NOT yet establish

The source/visuals support co-location/alignment at the charted reference in the shown example, but they do not define machine precision.

Still unresolved:

```text
exact equality?
normalized same broker tick?
within spread?
within one point?
within another tolerance?
```

No numeric tolerance may be chosen from historical outcomes.

Machine implementation must therefore keep two concepts separate:

```text
SOURCE_SEMANTIC: aligned / same structural reference
MACHINE_EQUALITY_NORMALIZATION: UNRESOLVED
```

## What remains NOT universal

This checkpoint does **not** prove a generic algorithm for every component permutation.

Still open examples include:

- parent TF supplies only `ซอก`; lower TF must supply `ไส้ + คู่`;
- parent TF supplies only `ไส้`; lower TF supplies `ซอก + คู่`;
- parent TF supplies only `คู่`; lower TF supplies the other two components;
- all three valid component references remain distinct;
- multiple lower-TF pairs align with the same parent candidate;
- multiple parent candidates coexist;
- universal wick selection;
- exact mapping of labels `1` versus `2` to near/far, upper/lower, or component type.

The visible numbering `1/2` varies by example orientation and must not be converted into an unsourced universal ordering rule.

## Research implication for two-reference selection

The prior broad question `how do three component prices reduce to two?` is narrowed further.

In the repeated shown form, there is no three-to-two reduction step at all:

```text
parent TF already provides two forecast/reference levels
+
lower-TF pair validates/completes one existing level
=
complete ซอก + ไส้ + คู่ structure with the same two references
```

This explains at least one major source-shown family without inventing min/max, averaging, nearest/farthest, or ranking arithmetic.

For unseen configurations that do not naturally follow this topology, retain `UNRESOLVED_REFERENCE_SELECTION`.

## Decision

Result:

`SOURCE+VISUAL_REPEATED_SHOWN_FORM_CLOSURE`

Source-backed now for the reviewed topology:

```text
PARENT SOK+WICK -> TWO REFERENCES
LOWER-TF PAIR -> ALIGNS/COLOCATES WITH EXISTING PARENT REFERENCE
NO THIRD FORECAST LINE
-> STRUCTURE COMPLETE
```

Universal cross-TF alignment for other component permutations and exact broker/feed equality remain unresolved.

This closure must not be generalized beyond the demonstrated topology without new primary evidence.
