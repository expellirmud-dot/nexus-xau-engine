# RQ-003 — Daily Frame and Location Source Closure — 2026-09-08

Status: CLOSED / `SOURCE_BACKED_CONSTRUCTION_PARAMETERIZED`

## Question

What Daily Frame / Location construction is directly supported by current project source evidence, and what geometry must remain parameterized rather than being inferred from historical outcome variants?

## Evidence basis

Primary source evidence reviewed through the project evidence register and source-linked teaching images/transcripts:

- `docs/PRIMARY_IMAGE_EVIDENCE_2026-09-01.md`
- `docs/PA_LOCATION_SR_EVIDENCE_SYNTHESIS_2026-09-03.md`
- current local teaching transcripts for frame/standing/support-resistance context
- direct project-owner time clarification for 07:00 Thailand local time

## Source-backed Daily Frame construction

Primary teaching images materially support this workflow:

```text
07:00 local Thailand preparation
-> inspect completed H4 context
-> use the nearby statistical/minor S/R price whose ending is 0 or 5
-> upper frame = reference + 500 project points
-> lower frame = reference - 500 project points
```

The outer-frame spacing is therefore 1,000 project points.

Project time normalization already closed separately:

```text
07:00 Asia/Bangkok = 00:00 UTC
```

This is a project-owner-confirmed local-time interpretation, not a claim that the instructor literally said the timezone name.

## Wick-contact frame evidence

Teaching evidence also supports:

- H4 wick-end references for major frame construction;
- H1 wick-end references for minor S/R context;
- approximately `7–14 project points` as a wick-contact/confluence concept for a strong frame in the demonstrated construction method.

This number is **not** a universal PAT-to-frame distance tolerance and is not a universal entry tolerance.

## Location semantics

The hard directional qualification remains:

```text
BUY PA/PAT  -> support only
SELL PA/PAT -> resistance only
```

The engine must retain `location_source_type`; support/resistance is not one universal formula. Current source families include Mae Pla statistical frame, wick-contact frame, body-collection zone, Por Chon ATH frame, Sideway frame, and explicitly manual/visually identified S/R.

## Important separation of point distances

Current source evidence contains several distances with different roles:

- `7–14` points: wick-contact/confluence strength in the frame-building method;
- `<= ~200` points: close-to-frame entry context in a specific teaching setup;
- `~100` points: example-specific body-collection near miss;
- `~200` points: example-specific post-SIG destruction case.

None may be silently promoted to a universal PA-location tolerance.

## What remains unresolved

The current bounded source set does not uniquely close:

1. exact nearest-0/5 selection when two candidates are equally or nearly close;
2. exact rounding/tie convention for broker price precision;
3. exact PAT-to-frame qualification geometry: wick touch, body intersection, close, penetration, or distance by source family;
4. exact allowed penetration/tolerance for ordinary PAT location;
5. priority when multiple support/resistance families disagree;
6. deterministic construction of manually identified generic S/R outside named source families;
7. Sideway-frame exact construction (delegated to RQ-005);
8. Por Chon boundary/retirement details (delegated to RQ-006).

## Safe measurable representation

For research, the Daily Frame may be represented as:

```text
reference_price = SOURCE_SUPPORTED_0_OR_5_STATISTICAL_REFERENCE
upper = reference_price + 500 project points
lower = reference_price - 500 project points
```

but the selector that turns an arbitrary 07:00 market price into one unique `reference_price` remains parameterized until snap/tie semantics are closed.

Location events must record:

```text
location_source_type
source_timeframe
frame_or_zone_id
side = SUPPORT | RESISTANCE
price_or_zone_bounds
distance_points
qualification_state = TRUE | FALSE | UNKNOWN
rule_variant
```

If family-specific qualification is unresolved, fail closed / `UNKNOWN` rather than auto-promoting a PAT.

## Relationship to earlier experiments

Historical `<=200`, expected-side/crossed-side and other Daily Frame variants remain research history. Their outcomes do not establish the canonical location geometry.

The old Daily-side SUPPORT was already superseded as current confirmation by the invalidation-aware re-anchor retest, which closed inconclusive due to sample insufficiency.

## Closure

```text
SOURCE_BACKED_CONSTRUCTION_PARAMETERIZED
```

Daily Frame arithmetic and directional location semantics are materially source-backed. Exact snap/tie and PAT-to-frame qualification/tolerance remain explicit parameters/unknowns.

## Next queue item

Promote `RQ-004 — M5 brake and frame-standing state machine`.
