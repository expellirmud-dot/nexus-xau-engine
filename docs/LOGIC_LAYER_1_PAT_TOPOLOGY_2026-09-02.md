# Logic Layer 1 — PAT Topology / Candle Primitives

Date: 2026-09-02
Branch: `build/python-replay-engine`

## Purpose

Implement only PAT facts that are currently deterministic from project evidence while keeping unresolved numeric geometry fail-closed.

Primary evidence basis:

- `docs/CURRENT_ENGINE_SPEC_2026-09-02.md`
- `docs/DIRECT_PAT_GEOMETRY_RULES_2026-09-01.md`

## Implemented safely

### Candle primitives

The engine can now compute, without strategy assumptions:

- bullish / bearish / exact doji direction;
- full candle range;
- real-body size;
- upper wick;
- lower wick;
- body fraction of full range;
- real-body midpoint;
- full-range midpoint;
- explicit `is_closed` state.

Computing both midpoint forms does **not** select either one as the PAT 50% rule.

### Closed-candle guard

PAT topology evaluation returns `WAIT / CONFIRMED` if any candle in the PAT window is unfinished.

### Hard location qualification contract

The topology evaluator accepts `at_required_location` as an external qualification:

- `False` => hard `REJECT / CONFIRMED`;
- `None` => `WAIT / HUMAN_CONFIRM`;
- `True` => proceed to the remaining shape checks.

The evaluator does not invent the numeric support/resistance proximity tolerance.

### PAT window / post-SIG mapping

Implemented as fixed evidence-backed metadata:

```text
PAT1 = 1 candle -> post-SIG reference #2
PAT2 = 2 candles -> post-SIG reference #3
PAT3 = 3 candles -> post-SIG reference #4
```

### PAT2 deterministic topology

BUY requires:

```text
C1 bearish -> C2 bullish
```

SELL requires:

```text
C1 bullish -> C2 bearish
```

Wrong color order can be rejected deterministically.

A correct color order is **not** promoted to `TAKE`; it remains `WAIT / PARAMETERIZED` because the 50% measurement basis/tolerance is unresolved.

### PAT3 deterministic topology

BUY:

```text
C1 bearish
C2 red or green
C3 bullish
```

SELL:

```text
C1 bullish
C2 red or green
C3 bearish
```

Wrong confirmed topology can be rejected. A topology pass remains `WAIT / PARAMETERIZED` because small-body, >50%, and SELL equal-wick numeric tolerances remain unresolved.

## Intentionally not implemented

No numeric value has been invented for:

- PAT1 long-wick/body ratio;
- PAT1 small-body threshold;
- PAT2/PAT3 50% denominator (`BODY` vs `FULL_RANGE`);
- midpoint equality/tolerance;
- PAT3 small-body threshold;
- PAT3 SELL equal-wick tolerance;
- support/resistance proximity tolerance.

Therefore this layer is a **candidate topology / rejection layer**, not a signal generator and not a trade-entry system.

## Next engineering gate

After unit tests pass locally, the safe next step is to run topology-only research scans over the validated M1/M5/H1/H4/D1 dataset and record candidate counts without calling them valid PAT signals. Location and unresolved geometry must remain separate evidence fields.
