# Phase 1 V2 Origin-State Carry Requirement Matrix V0.1 — 2026-09-16

Status: IMPLEMENTATION TRACEABILITY / SYNTHETIC LOGIC EVIDENCE ONLY / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract: `docs/PHASE1_V2_ORIGIN_STATE_CARRY_CONTRACT_V0.1_2026-09-15.md`
Implementation: `src/nexus_xau/replay/v2_state_carry.py`
Tests: `tests/test_v2_state_carry.py`

## Interpretation rule

Pytest case count is not the contract requirement count.

The frozen contract contains 14 required pre-implementation tests. This matrix maps each requirement to explicit evidence by test name. Supplemental engineering guards are listed separately.

Synthetic evidence below establishes logic/invariant behavior only. It does not establish market profitability, Win Rate, expectancy, broker fill, or trade execution performance.
## Contract requirements 1–7

| # | Frozen requirement | Explicit test evidence | Status |
|---|---|---|---|
| 1 | Full synthetic replay and split replay match post-checkpoint V2 state | `test_synthetic_split_replay_matches_unsplit_post_checkpoint_state` | PASS |
| 2 | Historical consumed progress is preserved and future progress updates by maximum | `test_consumed_progress_preserves_floor_and_updates_by_future_maximum` | PASS |
| 3 | Multiple same-side and opposite-side active origins survive independently | `test_multiple_same_side_and_opposite_origins_survive_independently` | PASS |
| 4 | Exact point-check contact after restart terminates carried origin | `test_carried_origin_point_check_after_restart` | PASS |
| 5 | Target completion after restart terminates carried origin | `test_carried_origin_target_completion_after_restart` | PASS |
| 6 | Same-bar target/point-check remains ambiguous | `test_carried_origin_same_bar_terminal_remains_ambiguous` | PASS |
| 7 | H4 PAT/origin creation straddling checkpoint matches unsplit replay | `test_h4_pat_origin_straddling_checkpoint_matches_unsplit` | PASS |
## Contract requirements 8–14

| # | Frozen requirement | Explicit test evidence | Status |
|---|---|---|---|
| 8 | Earliest post-checkpoint M5 PAT confirmation matches unsplit replay | `test_m5_confirmation_straddling_checkpoint_matches_unsplit` | PASS |
| 9 | `UNKNOWN_PREHISTORY` cannot promote itself to `COMPLETE` through forward continuation | `test_unknown_prehistory_cannot_promote_by_forward_continuation` | PASS |
| 10 | Checkpoint digest mutation is rejected | `test_checkpoint_digest_mutation_is_rejected` | PASS |
| 11 | V2/carry semantic-version mismatch is rejected | `test_checkpoint_semantic_version_mismatch_is_rejected` (parametrized for carry contract and V2 version) | PASS |
| 12 | Bridge provenance mismatch is rejected | `test_bridge_provenance_mismatch_is_rejected`; `test_bridge_source_provenance_digest_mismatch_is_rejected`; `test_bridge_payload_digest_mismatch_is_rejected` | PASS |
| 13 | Source-family transition is rejected unless separately authorized | `test_source_family_transition_is_rejected` | PASS |
| 14 | Carry layer introduces no P&L, Win Rate, expectancy, broker-fill, order-send, or profitability fields | `test_no_economic_or_execution_fields_introduced_by_carry_layer` | PASS |

## Supplemental audit guards

- Restart persistence: `test_checkpoint_json_roundtrip_and_digest`, `test_checkpoint_atomic_file_roundtrip`.
- Exact detector bridge continuity/no fabricated minute: `test_bridge_internal_m1_hole_is_rejected`.
- Handoff hole/no fill: `test_handoff_hole_is_rejected_without_fabrication`, `test_handoff_gap_policy_mismatch_is_rejected`.
- COMPLETE cannot be caller-promoted from ordinary bounded history: `test_complete_seed_cannot_use_ordinary_checkpoint_api`, `test_direct_complete_checkpoint_without_evidence_is_rejected`.
- COMPLETE requires independently bound evidence: `test_complete_seed_requires_independent_evidence_file`, `test_complete_seed_evidence_identity_mismatch_is_rejected`, `test_complete_seed_evidence_file_mutation_is_rejected`.
- Synthetic evidence cannot silently enter canonical runtime: `test_synthetic_checkpoint_requires_explicit_fixture_opt_in`.
- Integration representation version cannot silently drift: `test_integration_representation_version_mismatch_is_rejected`.

## Current conclusion

All 14 frozen contract requirements have explicit synthetic logic/invariant test evidence.

This does **not** authorize real Exness V2 continuation. Real Exness remains fail-closed as `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED` until a defensible independently evidenced `COMPLETE` seed exists.

Dukascopy-to-Exness initialization remains unauthorized pending a separately frozen overlap-sensitivity contract.