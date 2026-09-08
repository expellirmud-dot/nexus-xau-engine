# RQ-009 — SIG Entry / Post-SIG Source + Visual Checkpoint — 2026-09-09

Status: ACTIVE CHECKPOINT / SOURCE-BACKED MATERIAL CLOSURE

## Research question

Can the current five-video batch close enough of the remaining PAT / post-SIG / SIG-entry uncertainty to make a bounded source-faithful trade-family proof materially closer, without inventing thresholds from outcomes?

## Sources reviewed in this checkpoint

Primary local instructor sources:

- `1E_PYPor1qQ` — PA/PAT lesson (`2. PAT1  P1 — 1E_PYPor1qQ.txt` + synchronized local MP4)
- `vcdN51_OrPE` — system summary (`1. สรุประบบทั้งหมด — vcdN51_OrPE.txt` + synchronized local MP4)

Visual evidence windows were extracted with the registered local tool `D:/tools/nexus-video-evidence` and inspected through the registered image bridge. Media remains local under gitignored `youtube/_evidence`.

Key synchronized windows:

- `1E_PYPor1qQ` ~14:05–17:56 — PAT2/PAT3 >half explanation
- `1E_PYPor1qQ` ~53:01–58:15 — SIG entry method 1
- `1E_PYPor1qQ` ~58:15–1:06:40 — SIG entry method 2 / point-check / SL
- `1E_PYPor1qQ` ~1:09:23–1:09:54 — valid post-SIG example: reference does not exceed PA and later candle does not touch reference
- `vcdN51_OrPE` ~1:27:33–1:30:03 and ~1:44:15–1:48:56 — post-SIG must not disturb/exceed SIG body
- `vcdN51_OrPE` ~1:32:53–1:33:09 — active post-SIG point-check destruction by contact
- `vcdN51_OrPE` ~1:35:36–1:35:43 — near-miss example remains not destroyed

## 1. PAT2/PAT3 50% — stronger body semantics, exact machine denominator still open

### FACT — transcript

`1E_PYPor1qQ` repeatedly uses body-specific wording:

- ~14:22–14:29: the green **body** exceeds half / 50% of the red candle and can qualify as PAT2;
- ~15:46–15:52: PAT3 variant 1 uses the same >half language;
- ~16:53–17:02: PAT3 variant 2 explicitly refers to the green body exceeding half of two red candles combined;
- ~17:25–17:56: if the first green does not exceed half, PAT2 is not yet valid; a third candle may complete PAT3; full engulfing is presented as stronger/prettier but >half is still accepted.

### VISUAL

The synchronized PAT slides show the same PAT2/PAT3 schematic families while these statements are made. No visual measurement line was found in the inspected frames that uniquely distinguishes a real-body midpoint formula from a full High-Low midpoint formula for every pattern.

### Safe closure

Source language now **strongly supports a candle-body / body-volume relation**, rather than an outcome-selected BODY proxy. However, an exact universal OHLC denominator/arithmetic remains partially open, especially for multi-candle PAT3 variants.

Do not use historical performance to choose the remaining arithmetic.

## 2. Post-SIG candidate validity — source-backed body guard

### FACT — transcript

Across the system-summary source, the instructor repeatedly states in substance that a good post-SIG wick/reference must not reach into, exceed, or disturb the SIG/PA body:

- ~1:27:33: if the post-SIG wick goes beyond the SIG body, expect Sideway first;
- ~1:29:48–1:30:03: post-SIG should not destroy the signal candle body;
- ~1:44:15–1:45:42: post-SIG should not go beyond the SIG body under the discussed valid-SIG semantics;
- ~1:48:56: recap again says the post-SIG wick should not exceed the SIG body.

`1E_PYPor1qQ` ~1:09:23–1:09:54 shows the complementary positive case: the candidate post-SIG candle does not exceed the PA set, and the following candle does not touch the active post-SIG wick.

### Safe closure

At semantic level:

```text
VALID_POST_SIG_CANDIDATE requires the post-SIG reference not to disturb/contact the protected PA/SIG body region.
```

Still open:

- exact protected-body boundary for every multi-candle PAT2/PAT3 variant;
- feed/tick normalization at an exact equality boundary.

Therefore this is stronger than the former generic `~200-point destruction` representation, but it is not permission to invent a numerical body buffer.

## 3. Active post-SIG point-check destruction — contact semantics materially closed

### FACT — transcript

`vcdN51_OrPE` ~1:32:53–1:33:09 states that destruction of the active post-SIG reference requires only touching/nicking the wick: the wording explicitly says a small contact is enough for it to be destroyed.

The same source ~1:35:36–1:35:43 gives a contrasting near-miss: price comes very close but the post-SIG wick is **not** destroyed.

`1E_PYPor1qQ` ~59:39–1:00:50 independently says that for the confirmed point-check entry, if price comes back and **does not touch** the point-check/post-SIG wick, the reference remains active and the run can still be counted; it repeats that continuation behavior should not touch the post-SIG reference.

### VISUAL CROSSCHECK

- Local window `vcdN51_OrPE/01-33-03`: the instructor's arrow points to the contact region being discussed while the transcript describes the small contact as destruction.
- Local window `vcdN51_OrPE/01-35-40`: the instructor circles the candidate sequence and points to the close-but-not-contacting relation while the transcript explicitly calls it almost touched but not destroyed.

### Safe closure

```text
ACTIVE_POINT_CHECK semantic:
    touch/contact => destroyed
    near miss without contact => survives
```

This rejects use of a universal positive 200-point destruction buffer.

Engineering must still normalize comparison to the source/broker price precision; do not create a tolerance from outcome performance.

## 4. SIG entry has two directly taught source-backed modes

This materially narrows RQ-007. The source does not teach one universal SIG entry event; it explicitly teaches two entry methods.

### Mode 1 — PA confirmed, enter during forming post-SIG / body collection

`1E_PYPor1qQ` ~53:01–58:15:

```text
PA confirmed
-> next candle begins / prospective post-SIG candle is still forming
-> price retraces to collect body
-> take the directional entry during that body-collection move
```

Source-backed structural SL reference:

```text
SL = beyond the longest PA wick
or use the nearby source-defined frame as SL reference when the PA wick is close to that frame
```

Reason stated in the lesson: the post-SIG wick is not yet confirmed at the time this earlier entry is taken, so it cannot yet be the confirmed point-check SL reference.

### VISUAL — Mode 1

The synchronized slide at ~56:34 is explicitly labeled as method 1, shows a `PA sell` candle group and a separate `SL` line beyond the PA structure. This is consistent with the transcript's longest-PA-wick structural stop reference.

### Mode 2 — post-SIG confirmed, enter on next candle / point-check body collection

`1E_PYPor1qQ` ~58:15–1:06:40:

```text
PA confirmed
-> post-SIG candle closes and confirms
-> its wick becomes the point-check
-> enter on the following candle as price retraces/collects body near the point-check context
```

Source-backed structural SL reference:

```text
SL = at/beyond the confirmed post-SIG point-check wick
or use the nearby source-defined frame as the stop reference when the point-check is close to the frame
```

### VISUAL — Mode 2

The synchronized slide at ~59:56 explicitly shows:

- the post-SIG / point-check area;
- an `SL` marker at that reference side;
- an `Open Order` marker on the following candle/entry area.

This visually confirms the transcript's sequence: confirmed post-SIG point-check first, then next-candle entry.

## 5. Numerical SL distances are contextual examples, not a universal rule

The same entry lesson discusses examples such as roughly 100–200 points beyond a post-SIG wick, 200–300 points around a frame, and other setup-dependent allowances.

Crucially, ~1:06:32 states that each event is not the same and should be considered plan-by-plan.

Therefore:

```text
STRUCTURAL SL REFERENCE = source-backed
UNIVERSAL 100/200/300-POINT BUFFER = NOT source-backed
```

No historical outcome may be used to choose one of those examples as the canonical system buffer.

## 6. What changed from RQ-007

RQ-007 correctly concluded that a full universal trade tuple was not yet frozen. New RQ-009 source review materially narrows that uncertainty:

### Newly source-backed

- SIG entry is explicitly split into two modes;
- Mode 1 timing/state and PA-wick structural SL reference;
- Mode 2 timing/state and confirmed post-SIG point-check structural SL reference;
- nearby frame can supersede the wick as the practical SL reference in the shown context;
- active point-check destruction is contact/touch based rather than a universal positive point buffer;
- post-SIG candidate validity is body-sensitive and must not disturb the PA/SIG body.

### Still not deterministic enough for a final system Win/Loss claim

- exact entry **price** inside the body-collection / near-point-check area;
- exact frame-selection/zone geometry where multiple source frames exist;
- exact multi-candle protected-body boundary for every PAT variant;
- universal SL buffer does not exist in current evidence; setup/context routing must be represented instead;
- Sideway exact auto-construction and some MTF conflict handling remain partial.

## 7. Current proof-readiness consequence

A bounded `SIG_ENTRY_MODE_2` proof is now much closer than the prior RQ-007 state because the event order, point-check, structural invalidation and target anchor are source-backed.

However, **do not run a final Win/Loss proof yet**. Exact deterministic entry-price selection remains open, and previously inspected periods are not pristine final holdout periods for a newly frozen rule version.

Development-only mechanics replay may be used later to validate event construction, but it must not be reported as system performance.

## 8. Next action inside RQ-009

Continue this same worksheet rather than creating more queue IDs:

1. search the current five-video batch for an exact entry-zone/entry-price convention for Mode 2;
2. further close source-family location/body-standing semantics required by that entry;
3. map exact multi-candle protected-body region for PAT2/PAT3 if the source shows it;
4. then inspect Sideway exact frame/completion evidence;
5. only if the current source batch cannot close a material item, name the missing source explicitly instead of fitting it from outcomes.
