# Frame Standing Partial Closure — 2026-09-03

Status: CHECKPOINT / PARAMETERIZED RESEARCH RULE

## Evidence source

Primary M1/M5 brake transcript previously extracted in `docs/M5_BRAKE_TRANSCRIPT_FORENSICS_2026-09-01.md`.

## Source-backed facts

The lesson materially supports:

- zone/support-resistance is prepared before the brake/pattern search;
- the pattern is evaluated inside the zone and is not tied to one exact quote;
- frame-standing observation starts from the first candle touching the frame;
- M1/M5 examples use roughly 4–10 closed candles to judge whether price can stand/hold at the frame;
- candle bodies are the primary standing evidence;
- wick-on-line can contribute but is secondary/weaker;
- BUY and SELL are directional mirrors around support/resistance.

## Still unresolved

The transcript does not close:

- exact point tolerance around the frame;
- whether every candle must stand correctly or only a majority/sequence;
- exact treatment of bodies straddling the frame;
- whether 10 candles is a hard maximum or an observation guideline;
- whether this frame-standing rule applies identically to every PA/PAT setup family.

Therefore this is NOT a canonical PAT-location detector.

## Engineering implementation

Created:

`src/nexus_xau/engine/frame_standing.py`

Research objects:

- `FrameStandingBar`
- `FrameStandingConfig`
- `evaluate_frame_standing()`

Explicit research parameters:

```text
tolerance_price
minimum_bars
maximum_bars
minimum_body_fraction_on_correct_side
```

Behavior:

- fewer than the required observation bars -> `WAIT / CONFIRMED` because the source explicitly describes a multi-candle observation window;
- configured standing variant has no qualifying bodies -> `REJECT / PARAMETERIZED`;
- configured variant has qualifying bodies -> `WAIT / PARAMETERIZED`, never auto-promoted to valid PA/SIG.

This deliberately preserves the distinction between source-backed topology/state semantics and unresolved numeric thresholds.

## Validation

Latest project status:

```text
pytest: 41/41 passed
ruff: all checks passed
```

## Next evidence target

The highest-value remaining location question is narrower now:

1. exact PAT-to-line/zone touch/penetration rule outside the M1/M5 frame-standing confirmation context;
2. exact tolerance/all-vs-majority rule for frame-standing;
3. whether larger-TF S/R can deterministically override a lower-TF PAT and how that priority is measured;
4. map these rules into `DecisionTransitionRecord` only after source-backed qualification is frozen.

Do not use historical outcome to select these thresholds.
