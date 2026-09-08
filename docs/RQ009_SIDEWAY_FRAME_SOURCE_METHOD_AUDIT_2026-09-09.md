# RQ-009 — Sideway Frame Source-Method Audit — 2026-09-09

Status: ACTIVE CHECKPOINT / SOURCE METHODS PARTIALLY CLOSED, UNIVERSAL AUTO-GEOMETRY NOT CLOSED

## Question

Do the current local videos provide one universal deterministic OHLC construction for the Sideway frame, or do they support multiple source methods / timeframe-dependent representations that must remain separate?

## Sources reviewed

- `vcdN51_OrPE` system-summary transcript
- `1E_PYPor1qQ` PA/PAT lesson transcript + local visual window around ~1:29:46
- `ESHDuiVPJow` Trend/Frame/SIG lesson transcript + local visual windows around ~1:37:57, ~1:38:05, ~1:43:55, ~1:44:04
- EP.4 / EP.6 transcript evidence for equal-high/equal-low, W/M and frame-retest behavior

All screenshots/frames are local evidence under gitignored `youtube/_evidence` and are not committed to Git.

## 1. Sideway is a dynamic multi-level structure, not one fixed-width box

The source material repeatedly shows that Sideway can:

- exist on H1/H4/D/W and other timeframes;
- contain multiple internal PA/SIG sets (`SIG ชน SIG`);
- have several usable support/resistance levels;
- expand when an existing boundary fails and a new structural extreme is established;
- continue until price actually chooses a direction / a new SIG carries price out;
- flip old resistance to support, or old support to resistance, after an actual break and return/retest.

`vcdN51_OrPE` explicitly gives examples of support 1, support 2 and support 3 inside/around an expanding Sideway structure and says the trader does not know in advance which one will brake/hold.

Therefore the canonical engine must not represent Sideway as one forever-fixed pair of lines chosen once and never updated.

## 2. Source method A — body-primary / body-only frame preference

`1E_PYPor1qQ` ~1:29:46 states directly in substance:

```text
when I draw a Sideway frame, I draw only the candle body;
some people may use the wick, but I use the body.
```

The same lesson repeatedly uses body-standing semantics at meaningful frames:

- BUY PA body closes/stands on/above support/frame;
- SELL PA body should remain below resistance while wick excursions can occur;
- frame standing/not-standing is judged primarily from body relation.

### Visual cross-check

The synchronized local chart at ~1:29:46 shows several horizontal frame/reference lines around the current H1 structure while the instructor is discussing a body-based Sideway frame. The displayed working boundaries are not simply the furthest visible wick extremes of the whole chart.

Safe representation for this source method:

```text
SIDEWAY_FRAME_METHOD_A = BODY_PRIMARY / BODY_ENVELOPE
```

Exact candle-selection start/end and tie handling are still not mathematically specified.

## 3. Source method B — body first, wick as a second structural layer / envelope

`ESHDuiVPJow` ~1:37:49–1:38:22 describes Day Sideway construction approximately as:

```text
first draw from body;
second set can use wick;
label/separate body price and wick price;
or cover the structure because a higher-TF wick is lower-TF body structure.
```

Later ~1:43:55–1:44:12 the instructor says some people separate body and wick, while she may draw a body-covering frame because the large-timeframe wick contains lower-timeframe body information.

### Visual cross-check

At ~1:38:05 the local synchronized frame visibly shows a translucent rectangular Sideway zone drawn across the cluster of candle bodies. Several long wick extensions protrude materially outside the rectangle. This is strong visual evidence against a naive rule:

```text
Sideway upper = maximum wick high of all visible candles
Sideway lower = minimum wick low of all visible candles
```

The visual is instead consistent with a body/envelope structural zone, with wick information treated as an additional layer rather than mandatory full-range boundaries.

Safe representation for this source method:

```text
SIDEWAY_FRAME_METHOD_B = BODY_CORE + OPTIONAL_WICK_STRUCTURAL_LAYER / ENVELOPE
```

## 4. These methods must not be silently collapsed

Current evidence supports at least two instructor/source representations:

```text
A. body-primary/body-only preference
B. body-core plus optional wick layer / higher-TF envelope interpretation
```

They are not necessarily logically contradictory: the second source explicitly explains that a higher-timeframe wick can represent lower-timeframe body structure. However, current evidence does not provide one universal deterministic routing rule that says exactly when method A versus method B must be used.

Therefore:

```text
NO UNIVERSAL SIDEWAY_OHLC_BOUNDARY_FORMULA IS CLOSED YET.
```

The engine should preserve `sideway_frame_method/source_id/source_tf` rather than selecting one method from historical performance.

## 5. Width examples are contextual, not universal thresholds

The reviewed sources contain Sideway widths ranging from roughly 500–600 points, ~1,000 points, ~2,000–3,000 points, and much larger higher-timeframe examples.

One lesson says a Sideway frame intended for a particular 1,500-point H4 trade should have roughly 2,000+ points of space. That is a setup/target-space condition in that teaching context, not proof that every Sideway frame must be >=2,000 points.

Therefore do not encode:

```text
sideway_width >= 2000
```

as a universal system rule.

## 6. Source-backed lifecycle / expansion semantics

The combined sources materially support the following state shell:

```text
candidate Sideway structure
-> body/core S/R references form
-> repeated alternating PA/SIG / high-low behavior inside structure
-> internal support/resistance may develop in multiple levels
-> boundary may hold OR fail
-> if boundary fails, frame may expand / role-flip after retest
-> true directional exit is recognized after price actually leaves and the carrying SIG/structure becomes evident
```

The source explicitly says we cannot reliably know beforehand which internal SIG will be the one that carries price out of the frame.

This agrees with RQ-001 multi-instance SIG semantics and prevents look-ahead labeling.

## 7. Trading-side semantics inside Sideway

Source-backed qualitative handling:

- avoid repeatedly fading every touch;
- first/second touches are preferred in some teaching examples;
- direction/trend advantage matters;
- if Sell side is advantaged, look near the upper frame rather than buying against it;
- if Buy side is advantaged, look near the lower frame rather than selling against it;
- after a confirmed exit, wait for pullback/retest where old resistance may become support and old support may become resistance;
- ordinary body-collection/SIG hunting should not be blindly applied inside Sideway.

These are source behavior/context rules, not a complete autonomous execution formula.

## 8. What is now closed vs still open

### Closed / materially strengthened

- Sideway frame is structural and dynamic, not a universal fixed-width rectangle.
- Body relation is primary in both reviewed source methods.
- Full visible wick extrema are not universally the Sideway boundaries.
- A body-only source method exists.
- A body-core + optional wick/envelope source method exists.
- Sideway can expand and have multiple S/R levels.
- S/R role flip after actual exit/retest is source-backed.
- Exact width examples are setup/timeframe dependent.

### Still open

- deterministic candle-selection algorithm that starts a Sideway frame;
- universal routing between BODY_ONLY and BODY_PLUS_WICK_LAYER methods;
- exact upper/lower OHLC formulas for each method;
- equality/tolerance when bodies/levels are nearly aligned;
- exact formal `frame complete` event;
- exact automatic false-break vs valid-exit predicate before source-defined confirmation;
- cross-timeframe priority when several Sideway frames coexist.

## 9. Engineering consequence

Safe state/metadata representation now:

```text
SidewayFrameCandidate {
  source_video_id
  source_method = BODY_PRIMARY | BODY_CORE_WICK_LAYER | UNKNOWN
  source_timeframe
  body_core_upper/lower (when externally/source-labeled)
  wick_layer_upper/lower (optional)
  internal_support_levels[]
  internal_resistance_levels[]
  lifecycle_state
  expansion_parent_id
  role_flip_state
  evidence_ref
}
```

Do not auto-fill unknown bounds with performance-selected thresholds.

## 10. RQ-009 consequence

This closes a major misconception but does not yet make Sideway fully autonomous. For the fastest route to a bounded trade proof, continue prioritizing `SIG_ENTRY_MODE_2` outside unresolved Sideway cases first. Keep Sideway cases as a separately labeled setup/state until its exact source-method routing is closed.
