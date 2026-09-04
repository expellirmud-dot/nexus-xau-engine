# Daily Frame + Remaining Run Interaction Plan — 2026-09-04

Status: FROZEN COMPONENT TEST

## Question

Within H1 events already classified as `INHERITED_REMAINING_RUN`, does a direction-correct H1 PAT2 BODY candidate located within the source-backed 200-project-point Daily Frame proximity have better `PATH_REMAINING` completion behavior than inherited-run candidates outside that proximity?

## Why this question is pre-existing

The project target was already defined as:

`Daily Frame 07:00 -> SW/Location -> SIG H1/H4 -> remaining run / objective`

The Remaining Run round closed the standalone state effect as inconclusive/regime-dependent and retained `PATH_REMAINING` as a research representation. This test therefore evaluates the pre-existing interaction target rather than inventing a new rule from the latest outcomes.

## Frozen representation

- 07:00 Asia/Bangkok = 00:00 UTC.
- Daily Frame candidate builder: nearby statistical reference ending 0/5, upper/lower = +/-500 project points; snap tie remains unresolved and all equally-near candidates are considered.
- BUY location price = minimum Low of the two H1 PAT2 candles.
- SELL location price = maximum High of the two H1 PAT2 candles.
- BUY compares to Daily Frame lower/support line.
- SELL compares to Daily Frame upper/resistance line.
- signed distance >= 0 means the PAT extreme remains on the expected/inside side of the directional frame line.
- absolute distance <= 200 project points is the source-backed proximity variant.
- inherited-run state and `PATH_REMAINING` target come from the already-frozen Remaining Run experiment.

## Groups

### EXPECTED_SIDE_WITHIN_200

- state = INHERITED_REMAINING_RUN
- signed directional frame distance >= 0
- absolute distance <= 200 points

### OUTSIDE_200_CONTROL

- state = INHERITED_REMAINING_RUN
- absolute distance > 200 points

`CROSSED_SIDE_WITHIN_200` is retained descriptively but not silently called invalid, because project evidence allows some frame penetration in certain setup contexts and the exact PAT-to-frame penetration rule remains unresolved.

## Outcome

Primary target = `PATH_REMAINING` from candidate completion.

Metrics:

- resolved target-first rate using the existing symmetric 1,000-point adverse research barrier,
- target reach rate.

Secondary descriptive metrics use the existing fresh-target MFE/MAE only for path context; they do not redefine the remaining target.

## Closure rule

Minimum 10 events in both `EXPECTED_SIDE_WITHIN_200` and `OUTSIDE_200_CONTROL`.

Per period:

- `SUPPORT` if expected-side-within-200 has higher PATH_REMAINING target-first rate and no-lower PATH_REMAINING reach rate than outside-200 control.
- `OPPOSE` if both are lower/equal in the reverse direction, with target-first strictly lower.
- otherwise `MIXED`.
- below minimum => `INSUFFICIENT`.

Cross-period project interpretation:

- two or more usable later periods all SUPPORT => `MULTIPERIOD_SUPPORT_REQUIRES_FRESH_CONFIRMATION`.
- two or more usable later periods all OPPOSE => `MULTIPERIOD_NOT_SUPPORTED`.
- otherwise `INCONCLUSIVE`.

Because outcome summaries for 2024/2025 have already been inspected in the standalone Remaining Run round, no result from those periods may be labeled untouched fresh confirmation. They can test cross-period consistency only.

## Non-claims

- <=200 is not promoted to universal PAT location tolerance.
- PAT2 BODY is not canonical full PA/SIG.
- Daily Frame exact snap/tie rule remains unresolved.
- Outcome cannot prove teacher intent.
- No strategy win rate is produced.
