# V0.1 Holdout Progressive-Reveal Runner Contract Freeze — 2026-09-13

Status: FROZEN_BEFORE_RUNNER_IMPLEMENTATION / PRE-ACTIVATION / UNSCORED

## Purpose

Freeze the operational shell needed to execute the already-frozen RQ-011 prospective holdout protocol without allowing direct misuse of the lower-level RQ-012 ledger primitive.

This checkpoint does not alter V0.1 engine semantics, RQ-011 eligibility, target construction, tick handling, stopping rule, scoring rule, or activation identity.

## Existing frozen authority

- engine freeze commit: `75866d2`
- protocol freeze commit: `43c29be`
- activation lock: `docs/RQ012_V0_HOLDOUT_ACTIVATION_LOCK_2026-09-13.json`
- prospective boundary: `2026-09-14T07:00:00+07:00`
- ledger target: `results/holdout/v0/checkpoints.jsonl`
- outcome scoring: disabled

## Runner role

The runner is an execution guard around existing primitives. It may:

1. validate the activation lock;
2. validate a progressive-reveal checkpoint packet;
3. enforce chronological append order;
4. validate an eligible V0.1 event using the frozen RQ-010 event schema;
5. append a canonical hash-chained checkpoint record.

It must not score outcomes, replay forward bars, select candidates from future data, alter targets, or classify `TARGET_FIRST` / `POINT_CHECK_FIRST`.

## Activation gate

Before the prospective boundary:

- validation/status inspection is allowed;
- ledger append is forbidden;
- no post-boundary raw price data may be inspected for labeling.

For an append:

```text
now >= prospective_boundary
checkpoint_time >= prospective_boundary
visible_data_until <= checkpoint_time
checkpoint_time <= now
```

All timestamps must be timezone-aware.

## Chronology gate

Checkpoint records are chronological.

A new `checkpoint_time` must be greater than or equal to the previous checkpoint time. Equal times are allowed so a complete same-decision-time batch can be represented without arbitrary ordering by outcome.

Jumping backward in decision time is forbidden.

## Allowed decision record types

Only the four RQ-011 Stage-B checkpoint classes are allowed by this runner:

- `NO_EVENT`
- `ELIGIBLE_MODE2_EVENT`
- `AMBIGUOUS_OR_CONFLICT`
- `EXCLUDED_DATA_OR_PROVENANCE`

Correction/defect/sealing/scoring workflows are separate future bounded tooling and are not silently invented here.

## Progressive-reveal payload guard

Payload content must be derivable from information visible through `visible_data_until`.

The runner must recursively reject outcome/scoring fields, including outcome labels or forward-derived metrics such as:

- result / outcome / score;
- target_hit_at / point_check_hit_at / terminal_at;
- MFE / MAE;
- bars_observed;
- win/loss, win rate, expectancy, profit factor, realized P&L.

This is a fail-closed keyword/field guard, not proof that a human labeler has not inferred an outcome from some other field. Audit discipline still applies.

## Eligible event guard

For `ELIGIBLE_MODE2_EVENT`:

- payload must contain one frozen V0.1 event mapping;
- event must pass `SigMode2SignalRunEvent.from_mapping`;
- `post_sig_closed_at >= prospective_boundary`;
- `checkpoint_time == post_sig_closed_at`;
- `visible_data_until == checkpoint_time`;
- administrative horizon must be exactly 30 calendar days after `post_sig_closed_at`;
- `label_known_before_outcome=true` remains mandatory;
- target/point-check/location/source provenance remains mandatory through the frozen event schema.

The runner does not independently invent a target or location label.

## Non-event / ambiguous / excluded records

For the other three decision classes:

- payload must remain outcome-free;
- checkpoint and visibility gates still apply;
- reason/context fields may be recorded when known at the checkpoint.

These records remain in the audit ledger and are not deleted because they are non-events.

## Activation identity invariant

Every append must revalidate the tracked activation lock and require:

- engine freeze `75866d2`;
- protocol freeze `43c29be`;
- boundary `2026-09-14T07:00:00+07:00`;
- outcome scoring disabled.

The runner uses the ledger path from the activation lock rather than accepting an arbitrary output path by default.

## Raw collection boundary

Stage A raw M1 collection remains separate from Stage B labeling.

Existing `src/nexus_xau/data/mt5_export.py` is reused rather than reimplemented. A later collection command may wrap it, but this runner must not read forward raw bars to validate a Stage-B label.

## Validation target

Before this runner is considered ready:

- focused runner tests pass;
- existing RQ-012 ledger tests remain passing;
- full repository pytest passes;
- Ruff passes;
- research preflight passes;
- no holdout ledger record is created before the boundary;
- no holdout outcome is opened or scored.

## Interpretation boundary

Successful implementation means only:

`PRE-ACTIVATION EXECUTION GUARD READY / HOLDOUT STILL UNSCORED`

It does not mean the prospective holdout has begun, that any eligible event exists, or that any performance result is known.
