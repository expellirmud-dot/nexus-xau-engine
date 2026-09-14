# Phase 1 Tick Replay Engineering Implementation V0.1 — 2026-09-15

Status: IMPLEMENTED / SYNTHETIC CONTRACT PASS / FULL REGRESSION PASS / ENGINEERING SMOKE PASS / NO NEW STRATEGY OUTCOME OPENED

Contract:
`docs/PHASE1_TICK_REPLAY_ENGINEERING_CONTRACT_V0.1_2026-09-15.md`

Implementation:
`src/nexus_xau/replay/tick_reference.py`

Synthetic tests:
`tests/test_tick_reference_replay.py`

## Purpose

Implement the frozen pre-outcome tick replay contract without changing `0700_MINIMAL_V2.0` signal semantics and without opening new strategy outcomes.

## Implemented primitives

- timezone-aware monotonic Bid/Ask tick-frame validation;
- equal timestamps allowed; timestamp regression rejected;
- Ask < Bid rejected;
- per-row spread = Ask - Bid;
- first reference entry strictly after confirmation known_at;
  - BUY = Ask;
  - SELL = Bid;
- reference fills carry:
  - `REFERENCE_NOT_BROKER_FILL`;
  - `UNMODELED_NOT_ASSUMED_ZERO`;
- externally supplied stop/target level mechanics without choosing stop/TP geometry;
- side-correct executable quote handling:
  - BUY exits use Bid;
  - SELL exits use Ask;
- gap-through stop returns the observed executable quote rather than the ideal stop level;
- equal-timestamp stop/target conflict returns `AMBIGUOUS_SAME_TIMESTAMP`;
- explicit window exclusions for:
  - archive gap;
  - insufficient warmup;
  - incomplete horizon;
- raw input frame is not mutated;
- no P&L or Win Rate output fields are produced.

## Synthetic contract result

Targeted Ruff:
`PASS`

Targeted pytest:
`10 passed`

The first synthetic run exposed one implementation defect before any real-data smoke:
- supplied-level validation incorrectly applied BUY level ordering to SELL.
- defect was corrected to side-specific level validation.
- matching-row/raw-ordinal selection was also tightened to the first source-order row satisfying the trigger.
- no historical strategy outcome was opened or used to make this correction.

## Repository regression

Broader Ruff:
`python -m ruff check src tests scripts`

Result:
`PASS`

Full repository pytest:
`PASS`

Observed progress:
- 24%
- 48%
- 73%
- 97%
- 100%

Only pre-existing/deprecation-class warnings were emitted.

## Engineering smoke on already-inspected archive data

Source:
`data/raw/exness_tick_history/archive/XAUUSDm/2026/Exness_XAUUSDm_2026_08.zip`

Scope:
- first 100 rows only;
- representative month already inspected and validated before this implementation;
- no signal selection, target result, strategy outcome, Win Rate or P&L was opened.

Observed:
- first timestamp: `2026-08-02T22:01:30.647Z`
- last timestamp in smoke subset: `2026-08-02T22:01:45.299Z`
- known_at used: first timestamp
- first strictly-later tick: `2026-08-02T22:01:31.816Z`
- Bid: `4072.695`
- Ask: `4073.035`
- observed spread: approximately `0.340`
- BUY reference entry: `4073.035` (Ask)
- SELL reference entry: `4072.695` (Bid)
- fill marker: `REFERENCE_NOT_BROKER_FILL`
- slippage marker: `UNMODELED_NOT_ASSUMED_ZERO`

Interpretation:
The frozen reference-entry mechanics operate on real archived Bid/Ask rows as specified.
This is an engineering smoke only and does not establish broker fill equivalence or trading performance.

## Remaining boundary

Still unresolved / intentionally not invented:
- exact archive-to-current-MT5 feed identity;
- strategy trade-stop geometry;
- historical broker fill slippage;
- full commission/fee/swap treatment for economic P&L;
- position sizing/risk cap for supervised trading.

Automatic order sending remains disabled.
V0.1 holdout outcome scoring remains disabled.

## Next bounded task

Build the reusable archive-window adapter/gap-mask layer that supplies only explicitly eligible tick windows to the frozen replay primitives, then validate that adapter with synthetic fixtures and already-inspected engineering windows before any broad multi-year tick-level outcome replay.
