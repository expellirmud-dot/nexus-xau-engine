# RQ-009 — Body-Collection Source Audit — 2026-09-09

Status: ACTIVE SOURCE TARGET / CURRENT LOCAL VISUAL SOURCE MISSING

## Why this audit exists

RQ-009 recovered two explicit SIG-entry modes from the local PAT lesson. Both modes rely on `เก็บบอดี้` / body-collection semantics. Before inventing an exact entry-price formula, the project must check whether the dedicated body-collection lesson already contains the missing visual geometry.

## Existing project evidence

The repo already contains a full user-supplied transcript extraction:

`docs/transcripts/EP5_BODY_COLLECTION_FULL_ANALYSIS.md`

Source lesson recorded by the project:

```text
EP.5 วิชาเก็บบอดี้ #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว
video_id = oCcG3dUjrgw
```

The public source was re-located on 2026-09-09. This availability check is navigation/provenance only; source rules below remain grounded in the user-supplied transcript extraction until the actual video frames are visually reviewed.

A filesystem search under the approved D: drive found no local file named by `oCcG3dUjrgw` or `EP.5`. Therefore the actual EP.5 video is **not currently in the local five-video visual-evidence batch**.

## What the EP.5 transcript already closes

### Body-collection zone is structural, not one arbitrary price

The lesson uses historical left-side candle structure and explicitly combines:

```text
ซอก + ไส้ + คู่
```

The source says all three are used together in the demonstrated H4 zone method. Same-timeframe search is preferred, with H4 -> H1 -> M30 fallback when structure is insufficient.

### Entry uses projected zones, not one universal exact quote

The lesson favors two projected zones in the demonstrated method. Price may react at zone 1, zone 2, or between them. The transcript therefore does **not** support replacing the method with one universal exact entry price.

### Lower-timeframe confirmation is part of the body-collection entry workflow

The transcript repeatedly supports:

```text
Higher-TF PA / idea
-> projected body-collection zone
-> price reaches zone
-> M1/M5 PA aligned with higher-TF direction
-> frame brake/confirmation
-> entry consideration
```

It also states that if price is in the body-collection zone but there is no M5 PA, do not enter under this setup.

### Body collection and Sideway must remain separate

The instructor warns not to blindly use ordinary body collection inside Sideway. A separate Sideway setup exists.

## What the transcript still cannot close deterministically

Even after the full EP.5 transcript review, the following remain unresolved:

- exact OHLC formula/tolerance for `ซอก`;
- exact OHLC formula/tolerance for `คู่`;
- exact geometric relation among `ซอก + ไส้ + คู่` inside a valid zone;
- exact zone-1 vs zone-2 ranking when many candidates exist;
- exact hard boundaries of a projection zone;
- exact `เบรกกรอบ` geometry: wick vs body vs close;
- exact market-order trigger/price inside the projected zone;
- exact invalidation before/after entry.

The point-distance examples in the lesson are context guidance, not evidence for universal hard thresholds.

## Highest-value visual windows to inspect from EP.5

If/when the actual EP.5 video is available locally, create synchronized evidence windows at these first:

1. `20:33–32:40` — visual construction of `ซอก`, `ไส้`, `คู่` and their combination into a zone.
2. `40:42–44:19` — two projected entry distances, same-TF logic, M1/M5 PA, and frame confirmation.
3. `46:40–51:27` — why two zones are used and how price reacts at zone 1 / zone 2 / between them.
4. `56:35–59:43` — actual M5 entry example inside the projected zone.
5. `1:19:13–1:20:01` — H4 -> H1 -> M30 fallback and the explicit no-M5-PA/no-entry example.

These windows are preferred over broad full-video processing because each directly targets a remaining deterministic blocker.

## Relationship to RQ-009 SIG entry modes

### Mode 1

The PAT lesson says to predict how far body collection can reach and enter during that forming post-SIG move. EP.5 provides the dedicated structural method for constructing those projected areas. Therefore Mode 1 should not be reduced to an analyst-selected percentage retrace.

### Mode 2

The PAT lesson says to wait for a confirmed post-SIG point-check and enter on the following body-collection move near that reference. The dedicated EP.5 zone method may add the source-defined structural area used to decide *where* within the retrace to act, but current transcript evidence still does not prove one universal exact entry-price equation.

## Direct point-check / SL clarification from the PAT source

A later Q&A in `1E_PYPor1qQ` directly asks whether the point-check and post-SIG wick are the same SL location/reference. The instructor answers that they are the same.

Safe structural relation for the discussed SIG-entry setup:

```text
confirmed post-SIG wick
= point-check
= structural SL reference
```

This does not make any 100/200/300-point buffer universal; buffers/frame routing remain context-specific.

## Current conclusion

The project has enough source evidence to reject the old assumption that SIG entry should be represented as one arbitrary exact price or one fitted retracement percentage.

Current source-backed representation is:

```text
SIG entry mode
-> source-defined structural body-collection area
-> context/PA/frame confirmation
-> entry event
-> structural SL reference
```

But exact fully automatic body-collection geometry is still **not closed from transcript alone**.

## Next action

Keep this work inside the single `RQ-009` worksheet. Do not create separate queue IDs.

Priority:

1. visually inspect the five EP.5 windows above when the actual EP.5 video becomes locally available;
2. until then, continue extracting any remaining source-visible location / Sideway semantics from the current five local videos;
3. do not fit the missing zone geometry from Win/Loss outcomes.
