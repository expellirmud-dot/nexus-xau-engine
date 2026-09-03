# NEXUS XAU — Research Evidence Output Architecture — 2026-09-03

Status: ACTIVE DESIGN

## Objective

Use the smallest tool/output that can defensibly answer each research question.

MT5 is optional. CSV/JSON/Python are sufficient when a hypothesis is numerical and can be closed without chart inspection.

## Core pipeline

```text
RAW HISTORICAL DATA
-> Python feature/event builder
-> canonical event table (CSV)
-> query / comparison
-> machine-readable result (JSON)
-> human-readable closure summary
-> optional visual inspection only when needed
```

## Layer 1 — Event table (primary evidence)

One row = one historical decision/candidate event.

Candidate columns for MVP Set #1:

```text
event_id
decision_time_utc
decision_time_bangkok
timeframe
side
pat_family
daily_frame_reference
daily_frame_support
daily_frame_resistance
signed_distance_to_frame_points
location_relation
sw_state
sig_qualification_state
aligned_tf_count
aligned_tf_set
origin_sig_tf
nominal_run_points
run_consumed_points
remaining_run_points
known_at_utc
mfe_points
mae_points
target_reached
target_hit_at
first_hit_control
time_to_target_minutes
split   # DEV / VAL / TEST
```

Unknown or unresolved fields are stored explicitly as `UNKNOWN` / null, not guessed.

## Layer 2 — Query / experiment

Each experiment reads the same event table and asks a bounded question.

Example:

```text
Q: Does correct Daily-Frame location improve H1 BUY outcomes?

Filter:
  timeframe = H1
  side = BUY

Compare:
  location_relation = CORRECT
  vs
  location_relation = WRONG_OR_NONLOCATION

Metrics:
  target reach
  target-first control
  MFE
  MAE
  time-to-target

Held-out rule:
  DEV may define analysis buckets.
  VAL / TEST decide closure.
```

Do not manually browse the full chart to decide the answer after seeing the outcome.

## Layer 3 — Closure report

Every bounded test emits a compact report containing:

```text
QUESTION
INPUT DATA RANGE
NUMBER OF EVENTS
WHAT WAS MEASURED
CONTROL / COMPARISON
VAL RESULT
TEST RESULT
CLOSURE = SUPPORTED / NOT_SUPPORTED / INCONCLUSIVE / NOT_TESTABLE_WITH_CURRENT_EVIDENCE
WHAT THIS ANSWER DOES NOT PROVE
NEXT QUESTION (only if materially implied by the result)
```

This report is the normal human-facing answer. The user should not need to inspect raw CSV unless desired.

## Visual inspection ladder

Visual tools are escalation tools, not mandatory output.

### Level A — No visual

Use when the question is fully numerical.

Examples:
- Does distance to Daily Frame correlate with target behavior?
- Does 3-TF alignment outperform 1-TF alignment?
- How much run remains at 07:00?

Output:
- CSV + JSON + concise closure summary.

### Level B — Static Python chart

Use when a handful of cases need shape/context inspection but MT5 is unnecessary.

Possible output:
- candlestick image around decision time;
- Daily Frame lines;
- candidate PA/SIG marker;
- target/control levels;
- labels generated from the same event row.

This is often preferable for the project owner because it is a fixed annotated image rather than an interactive trading terminal.

### Level C — MT5 visual inspector

Use only when native MT5 candle/timeframe behavior or interactive replay adds value.

Architecture:

```text
Python event/query result
-> export selected event rows to CSV/JSON
-> MT5 research indicator/EA reads selected events
-> draw frame / marker / labels on corresponding historical chart
```

MT5 must not be the statistical judge. It is a visual audit/replay surface.

## Can CSV queries also be shown in MT5?

Yes, if desired.

A query such as:

```text
H1 BUY + correct location + aligned_tf_count >= 3
```

can produce a selected-events CSV. A future MT5 inspector can read that file and draw only those historical events on the chart.

Therefore CSV query and MT5 visualization are compatible; they are separate stages.

## Tool-selection rule

For each question, choose in this order:

```text
Can CSV/JSON metrics close it?
  YES -> stop there.
  NO -> would a static annotated chart close it?
          YES -> generate static chart.
          NO -> use MT5 replay/inspector if native platform context is required.
```

Never add MT5 complexity merely because it is available.

## Confirmation standard

A result is accepted as the answer to a bounded hypothesis when:

1. the measurement uses only information knowable at decision time;
2. the input event construction is reproducible;
3. the comparison/control was defined before interpreting held-out results;
4. VAL/TEST are reported separately;
5. the experiment ends in a declared closure state;
6. unresolved semantic fields are not silently filled;
7. visual review, when used, is an audit of event construction rather than a replacement for the numerical test.

## Recommended implementation priority

1. Keep Python + Pandas as the research engine.
2. Standardize one event-table schema.
3. Standardize one JSON closure-report schema.
4. Add simple static case-chart export for selected rows.
5. Build MT5 inspector only after there is a concrete research question that static output cannot answer.

This keeps the research process simple, auditable, and aligned with the project goal: obtain defensible answers rather than maximize tooling complexity.
