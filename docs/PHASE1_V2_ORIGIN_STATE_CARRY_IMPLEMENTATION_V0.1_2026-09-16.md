# Phase 1 V2 Origin-State Carry Implementation V0.1 — 2026-09-16

Status: IMPLEMENTED / SYNTHETIC LOGIC VALIDATED / REAL EXNESS SEED STILL FAIL-CLOSED / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract: `docs/PHASE1_V2_ORIGIN_STATE_CARRY_CONTRACT_V0.1_2026-09-15.md`
Traceability: `docs/PHASE1_V2_ORIGIN_STATE_CARRY_REQUIREMENT_MATRIX_V0.1_2026-09-16.md`
Implementation: `src/nexus_xau/replay/v2_state_carry.py`
Core hook: `src/nexus_xau/research/minimal_v2_0700.py`
Tests: `tests/test_v2_state_carry.py`

## Result

The finite carry representation survives synthetic split-vs-unsplit falsification under the frozen V2 semantics when the seed state is complete.

This implementation does not solve unknown prehistory. Real Exness continuation remains `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED` until an independently evidenced COMPLETE seed exists.

## Implemented guards

- deterministic serialized active-origin carry state and checkpoint digest;
- exact observed eight-hour M1 detector bridge with provenance and bridge digest;
- exact checkpoint-minute handoff with no fill or interpolation;
- source-family, symbol, M1 representation, integration-version, contract-version, and V2-version guards;
- historical consumed-progress floor is preserved and future progress updates by maximum;- multiple active origins remain independent across the checkpoint;
- incomplete historical seed state remains incomplete during ordinary forward continuation;
- the dedicated complete-checkpoint constructor verifies evidence identity and evidence-file hash;
- synthetic-complete checkpoints require explicit fixture opt-in and remain non-canonical.

## Validation evidence

- targeted Carry + Minimal V2 + Archive V2 regression: 59/59 PASS;
- targeted Ruff for carry/core/tests: PASS;
- full repository pytest durable job `XAU-V2-CARRY-FULLPYTEST-20260916`: 363 tests PASS, exit code 0;
- broader Ruff durable job `XAU-V2-CARRY-RUFF-20260916` over `src tests scripts`: PASS, exit code 0;
- research preflight before Current State reconciliation: PASS.
## Readiness reconciliation

- P1-08 remains partial because canonical real replay still lacks a defensible complete active-H4-origin seed at the archive boundary and continuity/gap eligibility must remain fail-closed;
- P1-10 no longer treats Archive-to-V2 integration as pending; V0.2 is implemented and the remaining blockers are execution economics and execution-representation evidence;
- historical wording that described provenance-preserving Archive-to-V2 integration as pending is retained here as superseded chronology rather than deleted.

## Guard status

- Dukascopy-to-Exness initialization remains unauthorized pending a separately frozen overlap-sensitivity contract;
- protected holdout scoring remains disabled;
- automatic order sending remains disabled;
- no Win Rate, expectancy, profitability, or exact broker-fill claim is authorized by this implementation.