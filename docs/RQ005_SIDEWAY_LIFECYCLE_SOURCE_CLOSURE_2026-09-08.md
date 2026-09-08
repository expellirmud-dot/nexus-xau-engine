# RQ-005 — Sideway Lifecycle Source Closure — 2026-09-08

Status: CLOSED / `SOURCE_BACKED_LIFECYCLE_GEOMETRY_UNRESOLVED`

## Question

Can Sideway begin/persist/end and its handoff to a new SIG be represented from source evidence without inventing an exact upper/lower frame detector?

## Evidence basis

- `docs/PA_PAT_TRANSCRIPT_FORENSICS_2026-09-01.md`
- `docs/M5_BRAKE_TRANSCRIPT_FORENSICS_2026-09-01.md`
- `docs/PRIMARY_IMAGE_EVIDENCE_2026-09-01.md`
- system-summary / EP.2 local source visual evidence, including the reviewed slide showing `SIG ... SIG` / `SIG ชน SIG = SW`
- RQ-001 post-SIG lifecycle source review

## Source-backed lifecycle meaning

The high-level system cycle remains source-backed:

```text
SIG -> TP/RUN -> RETRACE/REST -> SIDEWAY -> next SIG
```

Equivalent teaching view:

```text
SIDEWAY -> SIG -> TP -> REST -> SIDEWAY
```

Exact duration is not fixed.

## How Sideway can begin

Source evidence supports multiple contextual paths into Sideway rather than one universal candle-count trigger:

1. post-SIG reference/PA is disturbed or destroyed, causing the old SIG interpretation to stop and the market to be re-evaluated as Sideway/new setup context;
2. after a completed run and retrace/rest, price can construct Sideway as part of the graph lifecycle;
3. in demonstrated examples, competing/opposite PA/SIG behavior can produce `SIG ชน SIG` inside the same frame/range.

These are lifecycle/context facts, not an exact OHLC Sideway detector.

## Persistence inside Sideway

Source-backed characteristics include:

- price oscillates/trades within a frame while waiting for a new SIG to leave the frame;
- SIG/PA can occur on both sides inside the Sideway frame (`SIG ชน SIG`);
- a SIG occurring inside Sideway does not automatically have normal full run space;
- examples use support/resistance frame interactions, repeated/equal lows or highs, M1/M5 brake behavior, frame-standing, PA and local structure confirmation;
- limited repeated frame entries are discussed in teaching examples.

Do not reduce Sideway to a generic textbook `no trend`, `2 swing highs`, or `2 swing lows` rule.

## Sideway completion / exit

The source supports the semantic exit condition:

```text
Sideway persists
-> a new valid SIG/set develops in relation to the frame
-> price leaves/escapes the Sideway frame with that new directional state
-> new SIG/run lifecycle takes authority
```

This is sufficient as a state-transition shell but not as a numeric `sideway_frame_complete()` detector.

## What remains unresolved

The current evidence does not uniquely establish:

- exact Sideway upper-frame construction;
- exact Sideway lower-frame construction;
- exact minimum/maximum candle count;
- exact `กรอบ SW เกิดครบ` completion event;
- equality/tolerance for repeated highs/lows;
- formal wick/body/close requirements for frame standing inside SW;
- exact false-break / `เจิด` distinction at the SW edge;
- exact rule for which new SIG is considered to have escaped the frame when multiple TFs conflict;
- exact number/frequency of allowable repeated frame entries as a universal rule.

## Safe research state machine

```text
NOT_SIDEWAY
-> SIDEWAY_CANDIDATE        # post-run/rest, destroyed SIG, or competing SIG context
-> SIDEWAY_ACTIVE           # frame context externally/source-family identified
-> FRAME_INTERACTION
-> PA/BRAKE/STANDING/STRUCTURE_FEATURES
-> INTERNAL_SIG             # may remain inside frame
-> EXIT_CANDIDATE
-> NEW_SIG_OUTSIDE_FRAME
-> SIDEWAY_EXITED
```

`SIDEWAY_ACTIVE` must remain `HUMAN_CONFIRM` or source-family-parameterized until exact frame bounds are established.

## Important guard

Historical W6 oscillation-strength work is only a research proxy and failed fresh confirmation as a standalone Sideway proxy. It must not become canonical Sideway semantics.

No threshold should be retuned from historical outcomes to fill the missing Sideway geometry.

## Closure decision

```text
SOURCE_BACKED_LIFECYCLE_GEOMETRY_UNRESOLVED
```

The lifecycle/transition shell is source-backed enough to represent state. Exact frame construction and deterministic completion remain unresolved and must fail closed / require human confirmation.

## Next queue item

Promote `RQ-006 — Por Chon remaining boundary and old-frame lifecycle details`.
