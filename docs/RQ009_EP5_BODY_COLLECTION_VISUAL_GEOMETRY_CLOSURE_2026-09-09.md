# RQ-009 — EP.5 Body Collection Visual Geometry Closure

Status: `SOURCE+VISUAL_PARTIAL_GEOMETRY_CLOSURE / UNIVERSAL_ZONE_ASSEMBLY_STILL_OPEN`

Date: 2026-09-09 Asia/Bangkok

## Source and access path

Primary source:

- YouTube Video ID: `oCcG3dUjrgw`
- Lesson: `EP.5 วิชาเก็บบอดี้ #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว`
- Original YouTube player, not a re-upload or analyst recreation
- YouTube Show transcript remains auto-caption / ASR evidence with normal ASR risk

Visual access path validated in this checkpoint:

```text
separate headed Chrome profile
-> Chrome remote debugging / CDP 9223
-> agent-browser --cdp 9223
-> seek original YouTube <video> by source timestamp
-> capture the rendered video element
-> IE Coder image bridge
-> NEXUS visual review
```

This uses a separate NEXUS Chrome profile and does not use the owner's normal Chrome profile.

Local ignored evidence bundle:

- `youtube/_evidence/oCcG3dUjrgw/visual_ep5/`
- `youtube/_evidence/oCcG3dUjrgw/visual_ep5/detail_49_50/`

These image files remain local under the gitignored `youtube/` evidence vault. They are not Git artifacts.

## Method guard

This checkpoint is source-first and visual-first. No Win/Loss, replay performance, or outcome-fit threshold was used to decide the geometry.

Three evidence layers are kept separate:

1. `SOURCE WORDING` — instructor speech / transcript.
2. `SOURCE VISUAL` — what the instructor actually draws or labels on-screen.
3. `ANALYST REPRESENTATION` — the minimum machine geometry that can be justified from 1+2.

A geometry is not promoted beyond the cases actually shown.

---

## 1. `ซอก` — visual form is now materially closed

### Source wording

Around `20:33-22:43`, the instructor defines `ซอก` as a corner/joint between candle prices and describes the prior close / next open as the same price in the shown same-color relation.

### Source visual

At the whiteboard sequence around `23:49` and in the worked chart around `49:56-50:12`, the instructor points to the body junction between adjacent candles of the same color.

In the worked PA Sell example, the handwritten `ซอก` arrow points to the common horizontal body-junction level of two adjacent red candles, on the line labelled approximately `3563.59`.

### Safe machine representation for the shown form

For the source-shown same-color form:

```text
same candle color
AND normalized prior close ~= next open
=> shared body-junction price is a `ซอก` reference
```

This closes the structural meaning substantially more than transcript-only evidence.

### Still open

- broker-feed equality normalization / allowable tick difference;
- whether every valid `ซอก` orientation is exhausted by the currently shown same-color cases;
- candidate priority when several valid joints exist nearby.

Do not add a positive point tolerance from outcome data.

---

## 2. `คู่` — support/resistance reversal-pair geometry is now visually closed for the shown forms

### Source wording

Around `26:47-30:08`, the instructor teaches `คู่` as an alternating-color paired-candle relation at support/resistance and calls the paired open/close relation an equilibrium price (`ราคาดุลยภาพ`). The source also says the visible body sizes/overlap do not have to match perfectly while the relevant open/close price at support/resistance is the material shared level.

### Source visual

The whiteboard at approximately `28:03-29:44` draws both sides:

- resistance form: green candle followed by red candle, sharing the body reversal level at resistance;
- support form: red candle followed by green candle, sharing the body reversal level at support.

The two bodies are visibly allowed to have different heights; generic full-range overlap is therefore not the definition.

In the worked PA Sell example around `50:08-50:12`, the handwritten `คู่` arrow points to the shared reversal level of the green candle and following red candle on the same approximate `3563.59` line.

### Safe machine representation for the shown forms

```text
RESISTANCE PAIR:
  green -> red
  normalized C_green ~= O_red
  shared level is at resistance

SUPPORT PAIR:
  red -> green
  normalized C_red ~= O_green
  shared level is at support
```

The body heights themselves are not required by this source example to be equal.

### Still open

- broker-feed equality normalization;
- whether there are additional valid pair orientations not shown here;
- exact location detector used to certify the shared level as support/resistance in every setup family.

---

## 3. `ไส้` — closed-bar wick remains the second structural ingredient

Transcript evidence already closed that the wick is final only after the relevant timeframe candle closes.

The worked PA Sell visual around `50:04-50:24` adds an important geometric relation: the instructor marks the wick/reference inside the same local PA cluster as a second price level distinct from the shared `คู่/ซอก` level.

In this example:

- shared `คู่/ซอก` level is shown around `3563.59`;
- the second forecast line is shown around `3560.31`;
- the instructor labels all three ingredients (`คู่`, `ซอก`, `ไส้`) as present in the cluster before calling the projected area complete.

Safe conclusion:

```text
A valid worked Body Collection cluster can use a closed-candle wick reference
as a distinct boundary/reference level in addition to body-junction references.
```

Still open:

- which wick is selected when several wicks qualify;
- whether the wick must always supply the second boundary in every valid cluster;
- BUY mirror examples sufficient to prove every orientation.

---

## 4. Exact worked-example zone assembly is now visually recoverable

The chart sequence `49:48-50:24` is the strongest new visual closure.

### Source visual facts

The worked PA Sell chart labels two horizontal forecast levels:

```text
ระยะคาดการณ์ 2 ~= 3563.59
ระยะคาดการณ์ 1 ~= 3560.31
```

During the explanation the instructor annotates:

- `คู่` at the green->red reversal joint on the upper line;
- `ซอก` at the red->red same-color joint on the same upper line;
- `ไส้` as the additional wick/reference inside the same local cluster;
- then states that all three are present and identifies the two forecast distances/zone.

The later explanation around `50:49-51:18` says reaction can occur at projection 1, projection 2, or between them and that the zone is not a dead/fixed price.

### Safe example-level representation

For this specific source example:

```text
upper_reference ~= shared คู่ + ซอก body-junction level
lower_reference ~= wick-derived / second structural reference
body_collection_area = interval between the two forecast reference levels
```

### What this does NOT prove

Do not universalize from one worked example that:

- `คู่` and `ซอก` must always share exactly one price;
- the wick must always be the opposite boundary;
- every valid Body Collection zone always has exactly the same candle indexing;
- the lower reference is always the wick and upper reference always the joint;
- candidate ranking among many historical clusters is solved.

Therefore the universal zone-assembly algorithm remains `PARTIAL`, not fully canonical.

---

## 5. Lower-timeframe confirmation visual is strengthened

The M5 worked sequence around `56:51-58:47` visually shows the projected H4 levels carried into the lower timeframe.

Source visual/text together show:

- price reaches the projected area;
- a PA Sell forms below/around the upper forecast line;
- the local structure fails to make a higher high in the discussed brake sequence;
- a red candle then engulfs the left-side local candle structure and price continues down;
- the instructor summarizes the actionable relation as `Zone + PA`;
- M1 can be used earlier by a more experienced trader, while M5 is presented as the more conservative confirmation path.

This strengthens the signal-level state machine but still does not define one universal broker fill tick.

Example point distances mentioned in this sequence remain contextual metadata, not universal constants.

---

## 6. What changed versus the prior EP.5 browser-source closure

Previous checkpoint:

```text
SOURCE-BACKED STATE MACHINE: substantially closed
EXACT VISUAL OHLC/ZONE GEOMETRY: visually blocked
```

After this headed-browser visual review:

```text
SOURCE-BACKED STATE MACHINE: closed at routing level
SHOWN ซอก GEOMETRY: source+visual closed
SHOWN คู่ GEOMETRY: source+visual closed
SHOWN WORKED ZONE ASSEMBLY: source+visual closed at example level
UNIVERSAL ZONE ASSEMBLY / CANDIDATE PRIORITY: still partial
EXACT BROKER FILL PRICE: still open / execution convention required
```

The previous headless-player limitation remains historically true for that checkpoint, but it is no longer the current visual blocker because the original YouTube video plays successfully in the separate headed CDP Chrome path.

---

## 7. Canonical research consequence

It is now defensible to build **research-only candidate detectors** for the shown forms of `ซอก` and `คู่`, provided they retain:

- source-form tags;
- feed-equality normalization as an explicit parameter/guard;
- support/resistance context for `คู่`;
- manual/source validation during initial replay;
- no outcome-selected tolerance.

It is not yet defensible to claim a universal automatic Body Collection detector because candidate selection and universal assembly are still incomplete.

---

## 8. Remaining RQ-009 blockers after this checkpoint

1. PAT2/PAT3 exact `>50%` denominator/arithmetic remains unresolved.
2. Universal Body Collection candidate selection when several historical `ซอก/ไส้/คู่` clusters exist.
3. Universal zone assembly across BUY/SELL and all source variants, including whether `คู่+ซอก` must coincide.
4. Exact broker execution price/tolerance after a source-valid confirmation signal.
5. Sideway method routing / frame-complete / false-break geometry.
6. Cross-timeframe/source-frame priority when multiple valid structures coexist.
7. Final pristine holdout is still required before any newly frozen full-system Win/Loss claim.

## Decision

`PARTIAL SOURCE+VISUAL CLOSURE`.

This checkpoint materially reduces the Body Collection geometry blocker without inventing a universal formula. RQ-009 remains ACTIVE.

## Follow-up: BUY/SELL mirror and zone lifecycle

A later same-RQ checkpoint reviewed source visuals at `1:12-1:13` and direct Q&A at `2:01-2:02`.

It closes two-level BUY/SELL availability and the fresh/touched/completed-retired zone lifecycle while keeping candidate priority and exact transition geometry open.

See: `docs/RQ009_EP5_BODY_COLLECTION_MIRROR_LIFECYCLE_CLOSURE_2026-09-09.md`
