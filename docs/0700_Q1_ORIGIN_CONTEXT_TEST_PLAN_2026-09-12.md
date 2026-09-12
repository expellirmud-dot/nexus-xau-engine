# 07:00 Q1 — Origin Context × First Confirmation Test Plan — 2026-09-12

Status: FROZEN BEFORE Q1 OUTCOME CALCULATION / EXPLORATORY DISCOVERY PLAN

## Question

At the 07:00 Thailand boundary, among H1/H4 research-proxy origins that:

1. have a source-supported nominal run not yet completed; and
2. whose proxy point-check has not been literally contacted before the cutoff,

how do origin timeframe/context and the first post-07:00 PA-proxy confirmation relate to completion of the inherited remaining run?

This is a bounded relationship question.

It is **not** a request to choose the best backtest rule.

## Evidence boundary

Source/user-direct guidance supports:

- active H1/H4/D run context may remain unfinished at 07:00;
- H1 nominal run = 1,000 project points;
- H4 nominal run = 1,500 project points;
- after 07:00, qualifying PA around Daily Frame can be used to participate in the remaining run;
- more same-direction H1/M30/M15/M5 PA agreement is stronger graded confluence;
- literal point-check contact is a destruction concept.

Still unresolved:

- canonical autonomous PAT/SIG detection;
- exact D run distance;
- origin priority when multiple H1/H4/D contexts coexist;
- exact minimum MTF alignment count;
- exact M1/M5 brake/retest quantitative gate;
- universal SL / broker execution.

Therefore Q1 uses proxy inputs and signal/run outcomes only.

## Input dataset

Use the frozen V1 feature generator:

`src/nexus_xau/research/state_0700_dataset_v1.py`

Discovery source:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2022-09-01_2023-03-31.csv`

This period is discovery data, not untouched confirmation.

## Eligible 07:00 origin

For Q1, an origin row is eligible only when:

```text
origin_tf in {H1, H4}
origin_validity_state == INCOMPLETE_NOMINAL_RUN_RESEARCH_PROXY
source_partial_survival_proxy == true
```

No winner is chosen if several eligible origins coexist.

Every eligible origin retains identity.

D1 is excluded from target scoring because exact D run distance is unresolved.

## Context identity

For each `day_id + side`, record before outcome:

```text
context_id
same-side eligible origin count
same-side origin TF set: H1 | H4 | H1,H4
opposite-side eligible origin present?
direction conflict state
```

Multiple origins within a context remain separate origin rows.

No priority such as H4 > H1 is introduced.

## Confirmation selection variants

Because source does not establish a single exact qualifying timeframe/sequence, freeze two descriptive variants before outcome.

### Variant A — FIRST_ANY_PA_PROXY

For each eligible `day_id + side` context:

select the chronologically first post-07:00 PAT2-BODY proxy event in:

`H1 / M30 / M15 / M5`

with matching direction.

No Daily Frame side gate and no MTF count gate are imposed.

### Variant B — FIRST_EXPECTED_SIDE_PA_PROXY

For the same context:

select the chronologically first matching-direction proxy event whose frozen Daily Frame relation is:

`EXPECTED_SIDE`

Again, no MTF minimum is imposed.

If no qualifying event exists before the next operational 07:00 boundary:

`NO_CONFIRMATION_BEFORE_NEXT_0700`

This is retained, not deleted.

## Candidate knowledge time

The event is known only at its closed-bar `event_known_at`.

No outcome bar before that timestamp may be used.

## Recheck origin at candidate time

An origin that was incomplete at 07:00 may complete before the selected confirmation.

Before outcome scoring, recompute favorable progress only through bars strictly before `event_known_at`.

If nominal run is already complete:

`ORIGIN_COMPLETED_BEFORE_CONFIRMATION`

The row remains in the audit output but is not scored as a post-confirmation remaining-run opportunity.

This prevents falsely crediting an entry for a run that was already finished.

## Outcome horizon

Primary Q1 horizon:

`selected confirmation known_at -> next active 07:00 Thailand boundary`

Operationally this is the next `0700_day_state.cutoff_utc` after the current day.

This is a research accounting boundary, not an instructor expiry rule.

The last day without a later cutoff is:

`RIGHT_CENSORED_NO_NEXT_0700`

## Target representations

Historical outcome is not allowed to choose instructor intent.

Both representations are measured and kept separate.

### A — PATH_REMAINING_AT_CONFIRMATION

```text
consumed_before_confirmation
    = maximum favorable progress from proxy origin anchor
      strictly before confirmation known_at

remaining_at_confirmation
    = nominal_run_points - consumed_before_confirmation

candidate target
    = confirmation close +/- remaining_at_confirmation
```

### B — ORIGIN_TARGET_LEVEL

```text
BUY  target = origin anchor + nominal run
SELL target = origin anchor - nominal run
```

The candidate's directional distance to that absolute target is measured at confirmation time.

Neither representation is promoted from discovery performance.

## Competing structural boundary

Use the proxy origin anchor as the point-check boundary.

After confirmation, measure literal M1 range contact with:

`origin_anchor_price`

This is a source-partial structural comparator, **not a universal trade SL**.

## First-hit categories

For each target representation, within the frozen horizon:

```text
TARGET_FIRST
POINT_CHECK_FIRST
AMBIGUOUS_SAME_BAR
NEITHER_BEFORE_NEXT_0700
```

If target and point-check are first touched in the same available M1 bar:

`AMBIGUOUS_SAME_BAR`

Do not guess intrabar order.

## Additional descriptive outcomes

Measure:

```text
MFE from confirmation close
MAE from confirmation close
target reached?
point-check reached?
time_to_target_minutes
time_to_point_check_minutes
remaining_at_confirmation_points
origin_target_distance_at_confirmation_points
```

These are signal/run research statistics, not trade P&L.

## Primary grouping variables

No threshold search.

Describe outcomes by:

```text
origin_tf: H1 vs H4
same-side context TF set: H1 / H4 / H1,H4
opposite-side surviving context present: yes/no
confirmation frame_side
confirmation event_tf
alignment_count_exact
```

Origin age, consumed ratio and remaining points stay continuous descriptive variables.

They may be related to outcomes with rank/quantile summaries later, but no cutoff is selected in Q1.

## Independence guard

Rows sharing the same `day_id + side` context are not independent trials.

Report both:

- origin-level rows;
- unique context counts.

Do not describe origin-row N as N independent experiments.

## Discovery closure

Discovery Q1 produces:

1. an origin-confirmation-outcome event table;
2. descriptive group summaries;
3. unresolved / no-confirmation / pre-confirmation-completed counts;
4. no production rule.

No context is declared canonical from discovery.

The next replication step must run the **same frozen implementation/spec** on a later historical period before any relationship is considered replicated.

Recommended first replication:

`2023-09-01 -> 2023-11-23`

because the local cache metadata reports a complete range with no missing cache dates.

## Claims prohibited by Q1

Q1 may not claim:

- system Win rate;
- trade Win rate;
- expectancy;
- best SL;
- canonical origin priority;
- canonical MTF minimum;
- exact instructor 50% denominator;
- exact D run;
- profitability.

A favorable historical relation is only a research observation until replicated and source boundaries remain correctly labeled.
