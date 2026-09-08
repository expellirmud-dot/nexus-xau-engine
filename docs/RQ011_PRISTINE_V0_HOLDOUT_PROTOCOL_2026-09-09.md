# RQ-011 — Pristine V0.1 Holdout Labeling, Reservation, and Scoring Protocol

Date: 2026-09-09 Asia/Bangkok
Status: `PROTOCOL_FROZEN_FOR_COMMIT / HOLDOUT_UNOPENED`

V0 implementation freeze commit:

```text
75866d2 — engine: freeze deterministic Mode2 signal-run V0
```

Target engine/schema:

```text
SIG_MODE2_SIGNAL_RUN_V0.1
```

## Purpose

Define the prospective holdout procedure **before** any pristine V0.1 outcome is opened or scored.

This protocol is a research-method convention. Except where explicitly tied to existing source-backed V0 semantics, it is not an instructor/source rule.

---

# 1. Evidence classes

## Fact / frozen V0 engineering contract

Already frozen before RQ-011:

- H1/H4 externally pre-outcome-labeled Mode-2 events only;
- BUY requires a valid-support label; SELL requires a valid-resistance label;
- `post_sig_closed_at` is the actual knowledge/close instant, not candle-open timestamp;
- point-check and Mode-2 run anchor share the normalized post-SIG reference in V0.1;
- literal broker-tick contact destroys the active point-check;
- one-tick near miss survives;
- target is a price frozen before outcome and supplied by the manifest;
- same-bar target + point-check is `AMBIGUOUS_SAME_BAR`;
- V0.1 has no broker fill/cost/P&L semantics;
- V0.1 result labels are signal/run outcomes, not trade/system Win rate.

## Research conventions introduced by this protocol

The prospective boundary, event-lock procedure, administrative horizon, sample stopping rule, correction policy, confidence-interval reporting, and one-time scoring procedure below are **project methodology**, not instructor claims.

---

# 2. Prospective boundary

The pristine period must begin only after this protocol itself is frozen and pushed.

Activation rule:

```text
protocol_freeze_commit is pushed to origin
-> activation checkpoint records that commit hash
-> prospective boundary = first 07:00 Asia/Bangkok boundary strictly after the push/freeze
-> first eligible M1 price bar = first bar whose open timestamp >= prospective boundary
```

The `07:00 Asia/Bangkok` alignment is used here as a project operational boundary so the holdout starts on a clean daily boundary. Its use as the **holdout activation clock** is a research convention, not a claim that every V0 signal must originate at 07:00.

No data at or after the prospective boundary may be used to alter V0.1 code, event geometry, eligibility criteria, target construction policy, or this protocol while retaining the same holdout identity.

If such a change is needed:

```text
invalidate current holdout version for confirmatory use
-> create new engine/protocol version
-> establish a new future prospective boundary
```

---

# 3. Separation of collection, labeling, and scoring

The holdout workflow has three roles/stages even if they run on the same machine at different times.

## Stage A — raw price collection

Raw M1 Bid OHLC may be collected/stored after the prospective boundary, but it must not be used for rule development.

Required dataset metadata snapshot:

```text
broker/server identifier
symbol
chart/data side = Bid OHLC
Digits
Point
Trade Tick Size / tick_size
source export method
UTC/timezone normalization method
first timestamp
last timestamp
data-file SHA256
```

The runtime tick grid is dataset-specific and must not be silently inherited from an older XAUUSDm capture.

## Stage B — blinded walk-forward labeling

A labeler must operate on a **progressive-reveal packet** that contains price/context data only through the current decision time.

The labeler must not be shown forward bars after the checkpoint being labeled.

The labeling process proceeds chronologically and cannot jump directly to visually interesting later outcomes.

At each H1/H4 decision checkpoint the labeling system records one of:

```text
NO_EVENT
ELIGIBLE_MODE2_EVENT
AMBIGUOUS_OR_CONFLICT
EXCLUDED_DATA_OR_PROVENANCE
```

This checkpoint ledger is necessary to reduce cherry-picking risk. It records non-events as well as selected events.

For an `ELIGIBLE_MODE2_EVENT`, the complete V0.1 manifest fields must be frozen before forward reveal, including:

- event identity;
- side/timeframe;
- PA/source label;
- location label + provenance;
- PA confirmation time;
- post-SIG knowledge time;
- point-check price + provenance;
- run anchor;
- target price + provenance;
- horizon end;
- parent/context tags;
- source/label provenance.

An event with no pre-outcome frozen target price is not eligible for the primary holdout.

## Stage C — scoring

Outcome scoring is prohibited until:

1. the stopping rule is satisfied;
2. the label/checkpoint ledger is sealed;
3. all eligible event horizons have ended or terminal events are known under the frozen rule;
4. the raw data files are hashed/sealed;
5. the exact V0.1 code commit and protocol commit are recorded in a scoring lock.

Only then may the scorer reveal/use forward bars.

---

# 4. Append-only label lock

The labeling/audit ledger must be append-only in project history.

Recommended machine representation:

```text
one canonical JSON record per checkpoint/event
+ previous-record SHA256
+ current-record SHA256
+ Git commit/push checkpoint
```

Each record should include:

```text
record_index
checkpoint_time
record_created_at
record_type
visible_data_until
payload
previous_record_sha256
record_sha256
engine_version
protocol_version
```

Rules:

- never overwrite an old label record;
- corrections append a new record referencing the original;
- original payload/hash remains recoverable;
- no force-selected candidate deletion after outcome;
- Git history + record hash chain is audit evidence, not a claim of cryptographic immutability against a malicious repository administrator.

A separate implementation checkpoint should build/validate this ledger before holdout activation.

---

# 5. Eligibility rule

An event counts toward the primary prospective sample only if all conditions are true **before forward outcome reveal**:

```text
known_at >= prospective boundary
signal_tf in {H1, H4}
source-compatible Mode-2 label exists
BUY -> VALID_SUPPORT
SELL -> VALID_RESISTANCE
point-check/anchor provenance exists
target price/provenance exists and is frozen
all prices lie on locked dataset tick grid
all required timestamps are timezone-aware
label_known_before_outcome = true
no unresolved multi-family conflict that changes event interpretation
no material missing/corrupt source data through known_at
unique signal_id
```

If one condition fails, the checkpoint remains in the audit ledger but does not become a primary eligible event.

The exclusion reason must be known without using the future result.

---

# 6. Administrative horizon convention

The source does not establish a universal time-expiry for every Mode-2 run. V0.1 nevertheless requires a finite `horizon_end` for reproducible research accounting.

Research convention:

```text
horizon_end = post_sig_closed_at + 30 calendar days
```

This is an **administrative censoring rule**, not an instructor rule and not a claim that the signal becomes invalid after 30 days.

If neither target nor point-check is reached by that instant:

```text
HORIZON_EXHAUSTED
```

The 30-day horizon must not be changed after seeing holdout outcomes. A future version may test another administrative horizon only on a new holdout/version or as clearly labeled sensitivity analysis outside the primary confirmation result.

---

# 7. Primary stopping rule

No minimum sample size comes from the instructor/source. A project methodology rule is therefore preregistered from precision rather than observed performance.

Primary collection stops at the first chronological decision-time batch that brings the cumulative eligible count to **at least 100 events**.

If event #100 shares the same `post_sig_closed_at` / decision checkpoint with one or more additional eligible events, the entire same-time batch is included. The protocol must not choose only one simultaneous event to make the count land exactly on 100. Final primary `N` may therefore be slightly greater than 100.

Reason for the 100-event target convention:

- under an independence approximation, a category proportion near the worst-case `p = 0.5` with about 100 observations has an approximate 95% sampling half-width near 10 percentage points;
- the round target is chosen before outcome access for operational simplicity;
- it is a precision/reporting convention, not an edge threshold and not evidence that 100 events makes the trading system profitable.

Important dependence caveat: H1/H4 signals can overlap in time, share market regimes, or cluster around the same price movement. Therefore 100 labeled events must **not** be described as 100 independent experiments. The nominal interval rationale above does not guarantee effective-sample precision under clustering. Primary reporting must disclose temporal overlap/clustering and treat Wilson intervals as nominal descriptive intervals rather than proof of an independent-trial sampling model.

All four V0 result categories count as outcomes of an eligible event:

```text
TARGET_FIRST
POINT_CHECK_FIRST
AMBIGUOUS_SAME_BAR
HORIZON_EXHAUSTED
```

Ambiguous or horizon-exhausted results are **not deleted** to improve resolved-event statistics.

After the final qualifying same-time batch is locked, raw price collection continues until the latest frozen 30-day horizon among primary events ends (or until all primary events have already reached a terminal result). Events from later decision checkpoints do not enter the primary sample; they may be retained in a separate future dataset but cannot be mixed into the primary sample post hoc.

---

# 8. Reporting rule

Primary reporting is descriptive and uncertainty-aware. It has **no pass/fail profitability gate**.

Report at minimum:

```text
N eligible >= 100 (include complete final same-known_at batch)
count + proportion for each of 4 result categories
nominal 95% Wilson interval for each category proportion, explicitly caveated for event dependence
BUY/SELL counts
H1/H4 counts
events per calendar/market day and simultaneous/overlapping-event counts
MFE ticks distribution
MAE ticks distribution
terminal-time distribution
all pre-outcome exclusions by reason
all correction records
raw-data / manifest / code hashes
```

Do not report:

```text
SYSTEM WIN RATE
TRADE WIN RATE
EXPECTANCY
PROFIT FACTOR
REALIZED P&L
```

from V0.1.

A convenience statistic such as `TARGET_FIRST / eligible events` may be reported only as a clearly named **signal/run target-first proportion**, with ambiguous and horizon-exhausted categories still displayed separately.

No result threshold will be used to decide after the fact whether V0.1 “passed”. Any later hypothesis test or promotion criterion requires a separate preregistered research question and a new confirmatory dataset if the criterion was chosen after viewing V0.1 holdout results.

---

# 9. Correction and exclusion policy

## Before forward outcome reveal

A mislabeled field may be corrected by appending a correction record, provided the reason and replacement value are determined using only information available through the original `visible_data_until`.

## After any forward outcome has been revealed

Event-defining fields must not be changed for the primary result.

If a material defect is discovered later:

```text
retain original record
append defect record
mark event PRIMARY_EXCLUDED_POST_LOCK_DEFECT
report exclusion transparently
never replace it with a newly favorable label in the same primary sample
```

Raw feed corruption or vendor correction must also be recorded. If the original raw data cannot support a trustworthy replay, affected events are excluded by the preregistered data-defect rule; they are not silently repaired based on desired outcome.

The primary sample is not backfilled with hand-selected replacement events after post-outcome exclusions. Any impact on sample size is reported as a protocol deviation and may require a fresh confirmatory sample.

---

# 10. Reproducibility / one-time score

Before scoring, create a scoring lock containing at least:

```text
engine_commit = 75866d2 or exact descendant containing only non-semantic protocol tooling
protocol_freeze_commit
activation_lock_commit
checkpoint-ledger final SHA256
V0 event-manifest SHA256
raw M1 data SHA256(s)
tick-size/environment snapshot SHA256
scoring command/version
```

The first scoring run produces a versioned result artifact and its SHA256.

Re-running byte-identical inputs/code for reproduction is allowed. Changing event eligibility, horizon, target, tick handling, point-check semantics, or scoring classification after viewing results is not a reproduction; it is a new analysis/version and must be labeled as such.

---

# 11. Holdout contamination breakers

The V0.1 pristine holdout is no longer confirmatory if any of these occurs before primary scoring:

- code/rule change caused by inspecting post-boundary outcomes;
- label/target/location created after viewing its future bars;
- selective omission of bad-looking eligible events;
- selective inclusion of good-looking later events;
- target/horizon changed after result;
- ambiguous same-bar cases force-classified using OHLC guesswork;
- future price data is used to resolve a pre-outcome multi-family conflict;
- candidate generation/labeling jumps ahead in time because a later outcome looked interesting.

If contamination occurs, preserve the data as exploratory history but establish a new future boundary for the next confirmatory version.

---

# 12. Decision

This protocol closes the methodological ambiguity around how V0.1 should be prospectively tested without pretending it is a complete trading system.

Frozen intent for activation:

```text
V0.1 code frozen
-> protocol frozen/pushed
-> next 07:00 Asia/Bangkok boundary activates prospective period
-> blinded chronological labeling + append-only audit
-> first chronological batch reaching at least 100 eligible events locked in full
-> 30-day per-event administrative follow-up
-> seal hashes
-> one V0.1 scoring run
-> report signal/run outcome distribution only
```

Holdout status at this checkpoint:

```text
UNOPENED / UNSCORED
```

A separate activation/tooling checkpoint is required before the prospective period is considered live.
