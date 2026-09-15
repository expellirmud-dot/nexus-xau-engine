# Phase 1 Dukascopy ↔ Exness Overlap Sensitivity Implementation V0.1 — 2026-09-16

Status: IMPLEMENTED PRE-REAL-RUN / SYNTHETIC CLASSIFICATION VALIDATED / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract: `docs/PHASE1_DUKASCOPY_EXNESS_OVERLAP_SENSITIVITY_CONTRACT_V0.1_2026-09-16.md`
Implementation: `src/nexus_xau/research/dukascopy_exness_overlap_sensitivity.py`
Tests: `tests/test_dukascopy_exness_overlap_sensitivity.py`

## Freeze purpose

Freeze the comparison representation before opening the three real overlap-window results.

The implementation reuses existing project acquisition/replay paths:

- Dukascopy normalized UTC OHLC CSV loader and existing cached/exported BID M1 files;
- Exness validated archive manifest and known-gap ledger;
- existing Exness archive-window loader;
- existing deterministic archive BID-to-M1 reconstruction;
- existing project resampler and frozen V2 H4 PAT2/origin/lifecycle functions.

No new downloader, feed-merging layer, synthetic market model, or execution model is introduced.
## Frozen comparison semantics

- source families remain distinct in every report;
- there is no comparison tolerance parameter and no tolerance field is emitted;
- PAT identity key is `(side, known_at)`;
- origin identity key is `(side, origin_known_at)`;
- matched origins compare anchor, lifecycle state category, consumed points, and point-check touch timestamp exactly;
- M1/H4 OHLC differences are descriptive only;
- missing/ineligible input is fail-closed as `INCOMPARABLE_INPUT_GAP`; no fill/interpolation is permitted.

Top-level classifications are exactly:

- `EXACT_OBSERVED_STATE_EQUIVALENCE`;
- `STRUCTURAL_STATE_EQUIVALENCE_NUMERIC_DIVERGENCE`;
- `STATE_DIVERGENCE_OBSERVED`;
- `INCOMPARABLE_INPUT_GAP`.
## Contract-test traceability

1. exact identical synthetic feeds → `test_identical_synthetic_feeds_are_exact_state_equivalence`;
2. structural state preserved with numeric divergence → `test_constant_price_offset_preserves_structure_but_changes_numeric_state`;
3. PAT/origin structural divergence → `test_pat_structure_change_is_state_divergence`;
4. missing/ineligible source input → `test_empty_source_frame_is_incomparable_input_gap`;
5. source provenance remains separate → `test_source_provenance_stays_separate`;
6. no tolerance accepted or emitted → `test_no_tolerance_is_accepted_or_emitted`;
7. no trade-performance/execution claim fields → `test_no_trade_performance_or_execution_claim_fields_are_produced`.

All seven contract tests pass before any frozen real-window run.

## Validation before real-window observation

- relevant implementation regression: 46/46 PASS;
- targeted Ruff: PASS;
- full repository pytest durable job `XAU-OVERLAP-IMPL-FULLPYTEST-20260916`: exit code 0;
- persisted full-suite progress log contains 370 completed test dots;
- broader Ruff durable job `XAU-OVERLAP-IMPL-RUFF-20260916` over `src tests scripts`: PASS, exit code 0.

The failed later `pytest --collect-only` attempt is not a logic failure; collection was interrupted by existing Windows permission errors under old `results/pytest-tmp-*` directories. Test-count evidence above comes from the already-completed durable full-suite log.