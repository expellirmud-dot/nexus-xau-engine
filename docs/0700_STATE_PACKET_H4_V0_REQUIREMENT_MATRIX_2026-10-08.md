# 07:00 State Packet H4 V0 Requirement Matrix — 2026-10-08

Status: FROZEN PRE-IMPLEMENTATION TRACEABILITY / STATE-ONLY / HOLDOUT UNSCORED / ORDER SEND DISABLED

Contract: `docs/0700_STATE_PACKET_H4_V0_CONTRACT_2026-10-08.md`

Planned implementation:
- `src/nexus_xau/research/state_packet_0700.py`
- `scripts/state_packet_0700.py`

Planned tests:
- `tests/test_state_packet_0700.py`

| ID | Requirement | Planned evidence |
|---:|---|---|
| 1 | Packet cutoff is 07:00 Asia/Bangkok = 00:00 UTC | `test_checkpoint_must_map_to_0700_thailand` |
| 2 | Origin lifecycle uses only observations before checkpoint | `test_post_checkpoint_rows_cannot_change_snapshot` |
| 3 | Fixed H4 target uses V2.1 origin anchor +/- 1500 project points | `test_fixed_origin_target_matches_v21_geometry` |
| 4 | Literal point-check exact touch destroys | `test_exact_point_check_touch_is_terminal` |
| 5 | Near miss does not destroy | `test_point_check_near_miss_survives` |
| 6 | Target-first maps to RUN_COMPLETE | `test_target_first_maps_to_run_complete` |
| 7 | Same-bar target and point-check maps to ambiguity | `test_same_bar_terminal_is_ambiguous` |
| 8 | SOURCE_PURE incomplete prehistory fails closed | `test_source_pure_unknown_prehistory_fails_closed` |
| 9 | OPERATIONAL_EXPLICIT_EPOCH is labeled project convention | `test_operational_epoch_is_explicit_convention` |
| 10 | Input must cover declared operational epoch | `test_operational_epoch_missing_input_fails_data_health` |
| 11 | Active BUY-only state is BULLISH_CONTEXT | `test_buy_only_context_summary` |
| 12 | Active SELL-only state is BEARISH_CONTEXT | `test_sell_only_context_summary` |
| 13 | Opposite-side or multiple same-side origins fail action on conflict | `test_multiple_origins_fail_closed_on_conflict` |
| 14 | No active origin yields PASS_NO_ACTIVE_ORIGIN | `test_no_active_origin_is_explicit_pass` |
| 15 | Daily Frame context is research representation and action qualification stays unknown | `test_daily_frame_authority_boundary` |
| 16 | Unknowns distinguish state blockers from downstream execution/P&L blockers | `test_unknown_classification_separates_downstream` |
| 17 | Packet contains no P&L, Win Rate, expectancy, fill, slippage, sizing or order action fields | `test_packet_has_no_execution_or_outcome_fields` |
| 18 | Real validated MT5 engineering data can produce a packet using only data available at checkpoint | bounded state-calculation smoke; no outcome scoring |

## Freeze rule

If implementation reveals a semantic ambiguity that changes any requirement above,
stop and create an explicit contract amendment before changing behavior. Do not
use later market outcomes to choose the interpretation.
