# Phase 1 Dukascopy ↔ Exness Overlap Sensitivity Contract V0.1 — 2026-09-16

Status: FROZEN PRE-IMPLEMENTATION / PRE-OUTCOME / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract ID: `PHASE1_DUKASCOPY_EXNESS_OVERLAP_SENSITIVITY_V0.1`

## Purpose

Measure whether source-family differences between Dukascopy BID M1 and the Exness-branded archive change frozen V2 H4 PAT/origin representation on bounded overlapping real-data windows.

This is a representation-sensitivity test. It is not a strategy-performance test, feed-equivalence claim, or authorization to concatenate the two feeds.

## Source families

- Dukascopy: cached/exported `XAUUSD` BID M1 candles, provenance retained as `DUKASCOPY_BID_M1`.
- Exness: validated `XAUUSDm` tick archive reconstructed as deterministic BID M1 using `ARCHIVE_BID_M1_V0.1`, provenance retained as `EXNESS_BRANDED_ARCHIVE`.

Source identity MUST remain separate in every result.
## Frozen windows

Window selection is frozen from existing local availability and chronology position before any PAT/origin comparison is run.

1. `2022-09-01T00:00:00Z -> 2022-10-01T00:00:00Z`
   - earliest complete cached Dukascopy overlap month in the current multi-period research chunks;
   - Exness September 2022 archive is locally present and validated.
2. `2023-09-01T00:00:00Z -> 2023-10-01T00:00:00Z`
   - next existing September block in a separate cached Dukascopy chunk;
   - the chunk metadata missing dates are in late November, outside this frozen window;
   - Exness September 2023 archive is locally present and validated.
3. `2026-08-24T00:00:00Z -> 2026-08-25T00:00:00Z`
   - existing direct Dukascopy BID M1 day;
   - already inspected previously for cross-feed price alignment, so it is an engineering stress window, not fresh validation;
   - Exness August 2026 archive is locally present and validated.

2024/2025 September chunks are deliberately excluded from V0.1 because their existing Dukascopy cache metadata records missing September dates. They MUST NOT be silently repaired or used as clean sensitivity windows.
## Input eligibility

A window is comparable only when both source representations are readable with their declared provenance.

Exness input MUST pass the existing archive manifest, local-file, half-open window, and known-gap guards before BID M1 reconstruction.

Dukascopy input MUST:

- use the frozen BID M1 CSV/chunk or direct-day file already present locally;
- have UTC-aware timestamps and valid OHLC;
- preserve the input file SHA-256 and metadata reference;
- contain no duplicate timestamp after normalization;
- never fabricate, forward-fill, interpolate, or infer a missing M1 bar.

If either source cannot support the frozen interval from observed data, classify the affected window as `INCOMPARABLE_INPUT_GAP`. Do not shrink the interval after seeing PAT/origin results.
## Comparison pipeline

For each eligible frozen window:

1. load Dukascopy BID M1 and Exness archive-derived BID M1 independently;
2. compare M1 timestamp coverage and OHLC differences on common timestamps;
3. resample each source independently to H4 with the existing project resampler;
4. detect frozen V2 `PAT2 FULL-RANGE` H4 events independently;
5. build frozen adjacent-post-SIG H4 origins independently;
6. for origins created within the frozen window, evaluate each source's local origin lifecycle through the common window end using that source's own M1 path;
7. compare event/origin/state representations without merging source data.

PAT event identity key:

`(side, known_at)`

Origin identity key:

`(side, origin_known_at)`

For matched origins, compare anchor price, terminal/active state, consumed points, and point-check touch timestamp descriptively.
## No invented tolerance

No price-distance, timestamp, count, anchor, consumed-points, or mismatch tolerance is introduced in V0.1.

Numeric differences are reported descriptively. Structural comparison uses exact keys and exact categorical state equality.

Do not tune a tolerance after observing the windows.

## Frozen window classifications

Each window receives exactly one top-level classification:

- `EXACT_OBSERVED_STATE_EQUIVALENCE` — PAT identity sets, origin identity sets, matched anchor prices, lifecycle states, consumed points, and touch timestamps are all exactly equal on the observed window;
- `STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE` — PAT/origin identity sets and matched lifecycle state categories are equal, but one or more numeric/timestamp representation values differ;
- `STATE_DIVERGENCE_OBSERVED` — PAT identity, origin identity, or matched lifecycle state category differs between feeds;
- `INCOMPARABLE_INPUT_GAP` — required observed input/provenance is unavailable or an existing fail-closed gap guard rejects the window.

M1 timestamp-count or OHLC differences are always recorded separately and do not by themselves define strategy performance.
## Interpretation gate

`EXACT_OBSERVED_STATE_EQUIVALENCE` on bounded windows is not universal feed equivalence.

`STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE` is evidence that structural V2 state may be robust on the observed windows while price-sensitive fields remain feed-dependent.

`STATE_DIVERGENCE_OBSERVED` is direct evidence that a Dukascopy-derived state cannot be silently relabeled as Exness state.

No classification in V0.1 automatically establishes a canonical COMPLETE seed at the 2015 Exness boundary.

Any later initialization representation MUST keep source family attached and requires a separately frozen decision about how cross-feed numeric/state differences are represented.

## Prohibited uses

- no strategy Win Rate, expectancy, profitability, or trade-P&L scoring;
- no broker-fill or slippage claim;
- no holdout reveal;
- no order send;
- no outcome-based window selection;
- no concatenating Dukascopy and Exness as if one continuous feed;
- no arbitrary warmup or origin expiry;
- no filling missing bars.
## Required implementation outputs

For every window, persist:

- frozen window start/end and eligibility status;
- Dukascopy input path/SHA/metadata reference;
- Exness source month path/SHA/validator version;
- M1 row counts, common timestamp count, source-only timestamp counts;
- descriptive common-timestamp OHLC difference statistics;
- H4 bar timestamp counts and source-only timestamps;
- PAT identity set comparison;
- origin identity set comparison;
- matched-origin anchor/state/consumed/touch comparison;
- top-level frozen classification;
- explicit `economic_scoring=DISABLED`, `holdout_scoring=DISABLED`, `order_send=DISABLED` markers in the engineering report only.

## Required tests before real comparison

1. exact identical synthetic feeds classify `EXACT_OBSERVED_STATE_EQUIVALENCE`;
2. identical structural state with numeric anchor/consumed differences classifies `STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE`;
3. PAT/origin/state-category mismatch classifies `STATE_DIVERGENCE_OBSERVED`;
4. missing/ineligible input classifies or fails closed as `INCOMPARABLE_INPUT_GAP`;
5. source identity/provenance remains separate;
6. no comparison tolerance field is accepted or emitted;
7. no P&L, Win Rate, expectancy, broker-fill, holdout score, or order action is produced.
## Next step after contract freeze

Implement only the comparison runner and synthetic classification tests, then run the three frozen real overlap windows as engineering sensitivity checks.

Real Exness V2 remains `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED` throughout this work. A sensitivity result cannot promote seed completeness by itself.