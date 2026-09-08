# RQ-009 — EP.5 Body Collection ↔ Sideway Routing Reconciliation

Date: 2026-09-09 Asia/Bangkok
Source: original YouTube EP.5 `oCcG3dUjrgw` rendered Show transcript
Status: `SOURCE_BACKED_ROUTE_SEPARATION / SIDEWAY_ENTRY_GEOMETRY_STILL_OPEN`

## Question

EP.5 contains two statements that can look contradictory if `Body Collection zone` and `Body Collection entry workflow` are treated as the same thing:

1. the instructor says not to Body Collect in Sideway; and
2. later says the zone condition can also be used for Sideway entry.

The research question is whether these are actually contradictory or whether the source is routing the same structural zone information into different workflows.

No outcome data is used.

---

## 1. Normal Body Collection workflow stops when the setup becomes Sideway

### ~44:12–44:19

In the Body Collection condition recap, after describing the H4 setup, forecast-zone construction, lower-TF PA confirmation and brake requirement, the instructor explains what to do if price runs beyond the planned frame/zone instead of producing the expected brake.

Source sequence:

```text
~44:12
price runs beyond the frame / goes too far
-> it may become Sideway

~44:19
"เราจะไม่เก็บบอดี้ในไซด์เวย์"
```

Safe source interpretation:

```text
if the normal Body Collection setup transitions into Sideway:
    STOP normal Body Collection entry workflow
    ROUTE to Sideway state/workflow
```

This is a workflow/state rule, not a claim that old structural zone prices cease to exist.

---

## 2. The zone can still be used as a Sideway location/reference

### ~1:19:37–1:20:01

Later Q&A repeats that being inside a Body Collection zone is not enough by itself; M5 PA/confirmation is still required.

Then the instructor adds:

```text
~1:19:44
if it is in the Sideway cycle, the zone condition...

~1:19:53
can be used for a Sideway-style entry too

~1:20:01
but first focus on whether this is genuine PA / genuine SIG
```

Safe source interpretation:

```text
Body Collection-derived / S-R zone information may remain useful as location context
inside a separate Sideway workflow.
```

The source does **not** say that the normal Body Collection entry algorithm continues unchanged inside Sideway.

---

## 3. Reconciliation

The two statements are compatible when the project separates:

```text
STRUCTURAL ZONE / LOCATION REFERENCE
from
ENTRY WORKFLOW / MARKET-STATE ROUTING
```

Source-backed routing:

```text
NORMAL BODY COLLECTION STATE
  -> PA/SIG + forecast zone + lower-TF confirmation

if expected brake/confirmation fails and structure becomes SIDEWAY
  -> normal Body Collection workflow is no longer used
  -> route to SIDEWAY workflow
  -> zone may still be retained as location/reference context
  -> Sideway-specific PA/SIG validity must be assessed
```

Therefore:

```text
"do not Body Collect in Sideway"
!=
"all Body Collection/S-R zone information becomes invalid in Sideway"
```

The first statement is about the **entry method/state machine**. The second is about **reuse of zone context in a separate Sideway entry mode**.

---

## 4. What this closes

Source-backed now:

1. Normal Body Collection and Sideway are distinct workflows/states.
2. When the Body Collection setup has transitioned into Sideway, do not keep applying the normal Body Collection entry workflow as if nothing changed.
3. A structural/forecast zone may still be relevant as location/reference information for a separate Sideway entry workflow.
4. In that Sideway workflow, genuine PA/SIG state remains important; zone presence alone is not enough.

---

## 5. What remains unresolved

This checkpoint does **not** define a deterministic Sideway entry algorithm.

Still open:

- exact event that proves the Body Collection setup has transitioned to Sideway;
- exact Sideway frame-complete geometry;
- exact false-break/JERID boundary;
- exact Sideway PA/SIG eligibility;
- whether/how the reused zone changes role after multiple touches;
- exact cross-timeframe Sideway priority;
- exact Body Collection-to-Sideway handoff timestamp when the source visuals are ambiguous;
- broker/feed tolerance for zone contact.

Do not fill those gaps with backtest-selected thresholds.

---

## Decision

```text
BODY_COLLECTION_NORMAL_WORKFLOW_IN_SIDEWAY = ROUTE_OUT
BODY_COLLECTION/SR_ZONE_AS_SIDEWAY_LOCATION_CONTEXT = SOURCE_SUPPORTED
SIDEWAY_ENTRY_ALGORITHM = STILL UNRESOLVED
```

Classification:

`SOURCE_BACKED_ROUTE_SEPARATION / SIDEWAY_ENTRY_GEOMETRY_STILL_OPEN`
