# Decision Path + Post-SIG Partial Closure — 2026-09-03

Status: CHECKPOINT / RESEARCH ENGINEERING

## Purpose

Implement the project-level decision objective as a restart-safe, no-hindsight event sequence and close only the portion of post-SIG invalidation that is directly supported by primary transcript evidence.

## 1. Sequential decision-path schema implemented

File:

`src/nexus_xau/engine/decision_path.py`

The research engine can now persist one decision path as ordered transition records containing:

```text
path_id
event_index
event_time
visible_data_until
state_before
event_type
evidence_available
candidate_actions
chosen_action
rule_ids_used
state_after
future_data_used = false
```

Supported research action vocabulary includes:

```text
WAIT
SKIP
ENTER
HOLD
REDUCE_RISK
EXIT
ACCEPT_LOSS
RE_ANCHOR
RE_EVALUATE
STOP_TRADING_THIS_SETUP
```

This is a research/audit schema only. It does not authorize live execution.

## 2. Why this matters

The project no longer treats one setup as a single binary prediction.

Target model:

```text
STATE_0
-> EVENT_1
-> DECISION_1
-> STATE_1
-> EVENT_2
-> DECISION_2
-> STATE_2
-> EVENT_3
-> DECISION_3
-> ...
-> TERMINAL OUTCOME
```

A losing terminal P/L therefore does not automatically mean every earlier decision was wrong. Each decision can later be scored using only evidence available at that event.

## 3. No-hindsight enforcement

`DecisionTransitionRecord` rejects:

- missing/invalid path IDs;
- event index below 1;
- timezone-naive event timestamps;
- `visible_data_until` later than the event time;
- a chosen action not listed among candidate actions;
- records marked as using future data.

`validate_decision_path()` additionally enforces:

- one path ID per sequence;
- contiguous event numbering;
- monotonic event time;
- continuity from previous `state_after` to next `state_before`.

## 4. Post-SIG destruction — partial source-backed closure

File:

`src/nexus_xau/engine/post_sig.py`

Primary transcript evidence previously recorded states that the post-SIG wick/reference must not disturb or extend beyond the PA; examples show destruction when the later reference extends past the PA structure.

The engine now safely encodes only the strict extreme condition:

```text
BUY:
  if post_sig_low < PA_low
  -> POST_SIG_EXTREME_DESTRUCTION = REJECT / CONFIRMED

SELL:
  if post_sig_high > PA_high
  -> POST_SIG_EXTREME_DESTRUCTION = REJECT / CONFIRMED
```

Important: the reverse is NOT promoted to a valid SIG.

If the post-SIG candle remains inside the PA extreme:

```text
Decision = WAIT
EvidenceStatus = PARAMETERIZED
```

because full post-SIG validity still depends on unresolved frame/wick semantics.

## 5. What this closes

Closed at engineering level:

- event-by-event no-hindsight decision recording;
- sequential state-continuity validation;
- a confirmed sufficient condition for rejecting a clearly destroyed post-SIG reference when it exceeds the PA extreme.

## 6. What remains open

The following must NOT be inferred from this checkpoint:

- remaining inside the PA extreme = valid post-SIG;
- exact requirement that the reference must remain inside a frame;
- exact meaningful-wick threshold;
- equality/tolerance at the PA extreme;
- whether specific setup families add stricter destruction tests;
- canonical entry/exit action after destruction;
- PAT-to-S/R exact interaction/tolerance.

Therefore `POST_SIG_EXTREME_DESTRUCTION` is a partial reject rule, not a full SIG detector.

## 7. Validation

Latest project checks after this checkpoint:

```text
pytest: 37/37 passed
ruff: all checks passed for decision_path.py, post_sig.py and their tests
```

Tests added:

- `tests/test_decision_path.py`
- `tests/test_post_sig.py`

## 8. Next resume point

Highest priority remains the evidence track:

1. Recover exact PAT-to-support/resistance interaction by source family.
2. Continue post-SIG evidence for frame interaction and wick validity.
3. Connect frozen valid events into DecisionTransitionRecord sequences.
4. Only after source-backed entry/invalidation rules are frozen, use future outcome data to score actions and complete paths.

The outcome harness must remain a falsification/scoring tool and must not be used to invent missing rules.
