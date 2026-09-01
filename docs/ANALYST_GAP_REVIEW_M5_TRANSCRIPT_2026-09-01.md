# Analyst Gap Review after M1/M5 Brake Transcript — 2026-09-01

Scope: full user-supplied M1/M5 entry transcript associated with video `16KoS7d-koI`, current PA/PAT evidence, and canonical repository state.

This review preserves prior gap reviews rather than replacing them. The objective is to identify what the dedicated M5 lesson actually closes and what still prevents deterministic research/backtest coding without guessed thresholds.

## Executive finding

The dominant blocker has changed again.

Before this source, M5 `เบรก`/entry was partly a semantic and workflow problem. After this source, the workflow is highly constrained:

`prepared zone -> read force -> weakening -> rejection -> color change -> first move -> retest -> PA/frame standing/local structure -> preferred phase-2 entry`

The remaining M5 gap is now mostly **numeric geometry and tolerance**, not conceptual discovery.

Canonical readiness currently records workflow ~88% and deterministic coding ~78%.

## What is now sufficiently understood for architecture

1. M1/M5 share one abstract brake-entry model.
2. Brake search is enabled only at a prepared zone.
3. The five force states are logical states, not necessarily five candles.
4. First reaction is not the preferred default entry; phase 2/retest is.
5. A real retest requires structure movement away and return, not merely candles sitting on a frame.
6. Frame-standing begins from first touch and is observed over roughly 4–10 candles.
7. PA + standing + local structure decides whether price is being supported/rejected versus crushed through.
8. Buy/Sell local structure uses higher-low/lower-high and local high/low destruction concepts.
9. Overlap/false first brake is expected and requires reevaluation.
10. M5 frame entry and SIG entry are different strategy families and must be labeled separately in backtest.

## P0 — remaining blockers

### 1. PAT exact OHLC geometry

Still blocks exact PA qualification inside the M5 workflow:

- PAT1 wick/body threshold;
- PAT2 50% denominator/tolerance;
- PAT3 v1/v2/v3 exact geometry;
- support/resistance tolerance and edge cases.

This remains the biggest shared dependency because M5 confirmation repeatedly relies on PA.

### 2. Quantitative candle-force states

The transcript gives the sequence but not exact equations for:

- `ใหญ่ยาว`;
- `อ่อนแรง`;
- rejection wick;
- color-change strength.

These should remain feature placeholders rather than guessed ATR/body ratios.

### 3. Exact frame-standing predicate

Known: first touch starts count, 4–10 candle observation, body primary, wick may contribute.

Unknown:

- exact body-vs-line inequality;
- point tolerance;
- allowed wick penetration;
- whether every candle or a majority must stand;
- handling when move occurs after 10 candles.

### 4. Canonical Sideway frame construction/completion

M5 lesson gives strong behavior examples — equal highs/lows, repeated frame interaction, PA, standing — but does not provide one exact algorithm for SW upper/lower bounds and `frame complete`.

### 5. Ground-truth OHLC corpus

The transcript provides many labeled narrative examples but the project still lacks enough OHLC-synchronized positive and negative cases to determine thresholds empirically without overfitting.

Minimum next dataset should include:

- Buy/Sell valid brake;
- no-retest failure;
- first-brake overlap failure;
- frame-standing success/failure;
- sideway equal-low/equal-high setups;
- `เจิด` continuation through zone;
- phase-1 entry stopped then phase-2 succeeds;
- M1 refinement vs M5 confirmation.

## P1 — important but not first blocking layer

### `คู่` and body-collection completion

This lesson adds confidence that `ซอก+ไส้+คู่` together are stronger and nearest relevant zone is preferred, but exact `คู่` geometry and `body_collection_completed()` still need source extraction.

### Half/Swing exact mechanics

Classification/midpoint is strong, but swing-anchor selection, extreme finalization, entry and invalidation remain open.

### Multi-timeframe conflict matrix

M1/M5 relation is much clearer, but H1/H4/D/W conflict arbitration and exact M15/M30 same-direction metric remain incomplete.

### Daily/ATH edge semantics

0/5 snap/tie algorithm and exact 19:00 boundary timezone semantics remain open.

### Risk-mode selection

The transcript gives separate context-specific ranges:

- M1 precision SL ~50–150;
- frame SL ~200–300;
- breakeven after substantial favorable movement with spread allowance.

What is not yet formal is which mode is selected for which setup and how it changes by volatility/spread.

## Critical implementation warning

Do not convert qualitative candle language into arbitrary numeric thresholds merely to make the detector run.

For example, avoid silently choosing:

```text
large_body >= 1.5 * ATR
weakening <= 0.6 * previous_body
wick >= 2 * body
```

unless a source or a backtest-calibrated research experiment explicitly establishes those numbers. Such values may be useful as experimental parameters, but must be tagged `ANALYST_ASSUMPTION`, not system rules.

## Recommended engineering split

### Source-backed deterministic/state layer

Can be coded now:

- zone-required gate;
- state progression;
- first vs second entry classification;
- retest topology;
- frame-standing counter metadata;
- PA dependency interface;
- local-structure feature interface;
- overlap/reevaluation state;
- frame-entry vs SIG-entry accounting.

### Experimental feature layer

May be coded only with explicit assumption tags:

- large-candle threshold;
- weakening ratio;
- rejection ratio;
- frame tolerance;
- pivot lookback;
- overlap buffer.

### Exact layer

Disabled until evidence closes it:

- `confirm_m5_brake_exact()`;
- exact PAT detector;
- exact Sideway detector;
- unattended execution decisions.

## Next evidence priority

1. Final candle-reading lesson — highest value for `ใหญ่ยาว`, `อ่อนแรง`, body/wick/volume geometry and likely the last 20% of PA/M5 force qualification.
2. Dedicated Sideway/frame lesson — exact SW construction, complete/false-break/exit.
3. Source with `คู่` shown clearly against chart/OHLC — close body collection geometry.
4. Replay labeling of 20–50 real cases — convert qualitative rules into regression-testable examples before any threshold fitting.

## Conclusion

The project is now past the phase of asking “what is M5 brake?”. The research question is now “what exact measurable candle/frame inequalities reproduce the teacher’s labels without inventing rules?”. That is a substantially narrower and more tractable problem.