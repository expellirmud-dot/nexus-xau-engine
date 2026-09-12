# 07:00 Data-Driven Missing-Condition Discovery Design — 2026-09-12

Status: DESIGN CHECKPOINT / EXPLORATORY ONLY / NO CANONICAL RULE PROMOTION

## Goal

Use the price/research data already present in the project to discover which currently unresolved variables add information to the 07:00 Thailand preparation/entry problem, without allowing historical outcomes to invent instructor rules.

The research question is not:

> Which threshold backtests best?

It is:

> At 07:00, which pre-existing market/run/context states and subsequent confirmation-state changes are associated with completion of the already-active source-supported run?

## Data inventory actually present

### Historical M1 Bid

- 2022-09-01 -> 2023-03-31
  - 305,280 M1 rows
  - 205,923 positive-volume rows
  - 180 active days
  - 150 days with an active 00:00 UTC bar
  - cache metadata reports complete range / no missing cache dates

- 2023-09-01 -> 2023-11-23
  - 120,960 rows
  - cache metadata reports complete range / no missing cache dates
  - useful additional replication period, although not pristine because the project has used this era elsewhere

- 2024-09 -> 2024-11
  - 95,040 rows
  - 57 active days
  - 44 days with an active 00:00 UTC bar
  - cache incomplete; missing dates must be excluded whenever a feature/outcome window intersects them

- 2025-09 -> 2025-11
  - 90,720 rows
  - 55 active days
  - 47 days with an active 00:00 UTC bar
  - cache incomplete; missing dates must be excluded

### Broker-matched MT5 M1

2026-05-26 -> 2026-09-01:

- 97,341 M1 rows
- 85 active days
- 71 days with an active 00:00 UTC bar
- columns include OHLC, volume, spread, real_volume
- already used by project research; therefore development/validation evidence, not pristine confirmation

Existing processed bars already include M5/H1/H4/D1. M15/M30 can be derived deterministically from M1 as existing research code already does.

## Important finding from old 07:00 research

The existing remaining-run engine is not a full H1/H4/D implementation.

It currently:

- detects an H1 PAT2-BODY research proxy;
- creates H1-only origin runs;
- uses nominal H1 1,000 project points;
- chooses the latest same-direction eligible H1 origin;
- does not persist an origin timeframe because the origin is always H1.

Therefore old `REMAINING_RUN_STATE_*` CSVs must not be interpreted as the full teaching statement that active H1/H4/D runs may be relevant at 07:00.

## Important failure learned from re-anchor work

After applying the project's source-partial post-SIG destruction filter to the old H1 proxy:

- discovery: 34 / 300 candidate events retained an inherited origin;
- 2024: 1 / 71 retained;
- 2025: 0 / 74 retained.

The prior broad inherited-run representation therefore collapses when a stronger invalidation constraint is applied.

This does not prove inherited remaining run is wrong.

It shows the old autonomous H1 PAT2-BODY proxy + origin-selection/invalidation representation is not a safe basis for the full 07:00 method.

The new design must preserve origin identity/timeframe and must separate source labels from research proxies.

## MTF evidence already available

Existing candidate-side counts after de-duplicating lookback variants:

- discovery: 285
- 2024: 47
- 2025: 29

For the exact-completion MTF proxy, alignment counts are concentrated at 1–2 timeframes:

- discovery: 1 TF=143, 2 TF=115, 3 TF=26, 4 TF=1
- 2024: 1 TF=27, 2 TF=16, 3 TF=4
- 2025: 1 TF=13, 2 TF=13, 3 TF=3

This strongly argues against inventing an "all H1/M30/M15/M5 must align" rule. Existing cross-period MTF results are also inconclusive.

## Proposed research architecture

Use three linked tables instead of one blended trade table.

### Table A — `0700_DAY_STATE`

One row per valid market day at:

`07:00 Asia/Bangkok = 00:00 UTC`

Only information known at or before the cutoff is allowed.

Fields:

```text
day_id
cutoff_utc
data_source
data_quality_state

price_at_cutoff

daily_frame_reference
daily_frame_upper
daily_frame_lower

completed_h1_ohlc
completed_h4_ohlc
completed_d1_ohlc

h1_body_size
h1_range
h1_close_position
h1_upper_wick
h1_lower_wick

h4 equivalents
d1 equivalents
```

For the new-video 50% uncertainty, store multiple measurements as features without selecting one as the teacher rule:

```text
h1_close_vs_previous_body_mid
h1_close_vs_previous_range_mid
h1_close_vs_current_body_mid
h1_close_vs_current_range_mid
body_fraction_of_range
close_fraction_of_range
```

These fields let historical data tell us whether any relation exists. They do not identify what the instructor meant by 50%.

### Table B — `0700_ORIGIN_CANDIDATE`

One row per possible pre-07:00 origin/run.

Do not prematurely choose one winner.

```text
day_id
origin_id
origin_tf = H1 | H4 | D1
origin_side
origin_known_at
origin_anchor_price
origin_source_class
origin_detector = SOURCE_LABEL | RESEARCH_PROXY
origin_validity_state
origin_target_definition
nominal_run_points_or_range
consumed_points_at_0700
consumed_ratio_at_0700
remaining_points_or_range_at_0700
origin_age_hours
point_check_state
invalidation_reason
```

If multiple origins coexist, retain all.

Derived context:

```text
same_direction_origin_count
same_direction_origin_tf_set
opposite_direction_origin_count
origin_conflict_state
```

This allows the data to study H1-only, H4-only, H1+H4 same-direction, conflicting origins, etc., without inventing a priority rule.

### Table C — `0700_CONFIRMATION_EVENT`

Chronological event stream after 07:00.

Do not inspect only the eventual winning entry.

Record every eligible state change/candidate known at the time.

```text
day_id
origin_id_or_context_id
event_id
event_known_at
minutes_since_0700

side
frame_side
signed_distance_to_valid_frame_side

h1_pa_proxy
m30_pa_proxy
m15_pa_proxy
m5_pa_proxy
alignment_count
aligned_tf_set

m1_brake_state
m5_brake_state
retest_state
frame_stand_state
structure_confirm_state
event_sequence_index
```

Unknown exact brake thresholds stay feature/state fields or externally labeled values. They are not optimized into canonical gates.

## Outcome table

Outcome is measured separately from feature generation.

Primary outcomes should not be P&L while SL/fill rules remain incomplete.

For each candidate/context record:

```text
future_mfe_points
future_mae_points
time_to_remaining_target
remaining_target_reached
origin_target_level_reached
first_competing_boundary
same_bar_ambiguity
```

Where the source target is not uniquely known, store separate named target representations rather than choose the best one after outcome.

### SL research

Do not search for a universal fixed-point SL by optimization.

Instead record structural references such as:

```text
post_sig_point_check
daily_frame_boundary
completed_h1_extreme
completed_h4_extreme
video_sl_reference_when_resolved
```

Then measure whether each reference is touched before the target and the MAE distribution.

Historical performance may tell us which geometry is informative; it cannot prove which reference the instructor intended.

## Missing-question experiments

### Q1 — Which origin context matters at 07:00?

Compare descriptive/conditional behavior across:

- H1 origin only
- H4 origin only
- D origin only where target semantics are usable
- H1+H4 same direction
- multiple same-direction origins
- opposite-direction origin conflict
- no active origin

Do not pick a winner first.

### Q2 — Does origin age/consumed run contain information?

Use continuous variables:

- origin_age_hours
- consumed_ratio_at_0700
- remaining_points_at_0700

Use rank relation, smooth/quantile summaries, and time-to-target analysis.

Do not turn a fitted bend point into a canonical expiry threshold.

### Q3 — Does more MTF alignment add information?

Current evidence is inconclusive and all-four alignment is extremely rare.

Study:

- count as continuous/ordinal feature;
- exact aligned TF set;
- interaction with Daily Frame side;
- interaction with origin TF/context.

Do not impose a minimum count.

### Q4 — What is the video's 50% role?

Calculate all plausible, clearly labeled geometric representations before outcome.

Compare their relationship to:

- remaining-target reach;
- MFE;
- MAE;
- M1/M5 reversal occurrence;
- time to first confirmation.

This can eliminate representations that carry no information, but only source/visual clarification can identify the teacher's exact denominator.

### Q5 — What does M1/M5 brake/retest add beyond PA?

Use nested state comparison:

```text
PA only
PA + first brake
PA + brake + move-away
PA + structural retest
PA + retest + frame stand
PA + retest + structure confirmation
```

Measure incremental change; do not assume every state is mandatory.

### Q6 — Which structural SL reference is viable?

For each structural reference, measure:

- distance from candidate;
- touched before target?;
- MAE relative to reference;
- reference survival by setup state.

Do not choose a fixed-point stop from best historical performance.

## Period usage

Recommended role separation:

1. 2022-09 -> 2023-03
   - primary discovery
   - complete cached range
   - largest historical sample

2. 2023-09 -> 2023-11-23
   - additional replication
   - complete cached range
   - not pristine, so replication only

3. 2024-09 -> 2024-11 and 2025-09 -> 2025-11
   - cross-regime replication
   - strict missing-date/window exclusion required

4. MT5 2026-05-26 -> 2026-09-01
   - broker-matched engineering/validation
   - spread field available
   - already used, therefore not final untouched confirmation

5. Future prospective data
   - only after a rule version is frozen
   - preserve current holdout protocol identity; do not contaminate V0.1 with this exploratory 07:00 work

## Statistical approach

Start with relationships, not thresholds:

- event counts and missingness;
- conditional rates;
- MFE/MAE distributions;
- Spearman/rank relationships;
- quantile summaries;
- time-to-target / survival-style summaries;
- state-transition frequencies;
- interactions by period/regime.

Use day/origin identity to avoid pretending repeated candidates from one day are independent observations.

Any candidate rule discovered historically must be frozen and tested on a later period before promotion.

## First implementation checkpoint

Build a new generator:

`0700_state_dataset_v1`

that emits:

1. `0700_day_state.csv`
2. `0700_origin_candidates.csv`
3. `0700_confirmation_events.csv`

for the complete 2022-09 -> 2023-03 discovery period first.

V1 should reuse existing:

- M1 loader/resampler;
- Mae Pla Daily Frame code;
- event known-at/no-lookahead conventions;
- MTF PAT2-BODY proxy only as explicitly labeled research proxy;
- outcome infrastructure;
- missing-data auditing.

V1 must not yet:

- produce a trading Win rate;
- pick a canonical H1/H4/D priority;
- optimize an SL;
- define the video's 50% denominator;
- require a hard MTF count;
- overwrite current V0.1 holdout semantics.

## Decision

The existing data is sufficient to begin a disciplined search for the missing 07:00 relationships.

The existing old event tables are useful as research history and reusable infrastructure, but are not sufficient as the new master dataset because they collapse H1/H4/D identity and the old inherited-H1 proxy becomes extremely sparse after stronger invalidation filtering.

The next correct step is to regenerate state from raw M1 around each 07:00 boundary, preserve all candidate origins/context explicitly, then study how post-07:00 confirmation states relate to the inherited run.
