# 07:00 Historical Data Readiness and Test Strategy — 2026-09-13

Status: DATA-READINESS CHECKPOINT / REAL-FIRST DEVELOPMENT / SYNTHETIC FOR CONTROLLED LOGIC TESTS

## Purpose

Determine whether the data already stored in the repository is sufficient to begin the next narrow 07:00 version, what kinds of situations can be tested now, and where synthetic/constructed data is appropriate.

This checkpoint follows the project-level operating principle:

`docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md`

No new YouTube/source review was required for this audit.

---

# 1. Real historical data currently available

## A. Complete Dukascopy discovery period

File:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2022-09-01_2023-03-31.csv`

Metadata:

- date range: 2022-09-01 -> 2023-03-31
- M1 rows: 305,280
- missing cache dates: none
- complete cache range: true
- SHA256: `d6247b3d671e051e93876dcf8612f83f14d6dd49b08ba58a243a58049e2eeb55`

Existing 07:00 Dataset V1 output:

- day-state rows: 150
- origin-candidate rows: 13,400
- confirmation events: 22,529

Role:

`READY FOR V2 DEVELOPMENT / NOT PRISTINE`

This period has already been used extensively in Q1-Q4 and earlier research.

It is valuable for:

- rebuilding the detector;
- comparing BODY-proxy history vs new PAT2 FULL-RANGE representation;
- failure taxonomy;
- state-distribution analysis;
- debugging.

It must not be presented as untouched confirmation.

---

## B. Complete Dukascopy replication period

File:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2023-09-01_2023-11-23.csv`

Metadata:

- date range: 2023-09-01 -> 2023-11-23
- M1 rows: 120,960
- missing cache dates: none
- complete cache range: true
- SHA256: `f5749ffc8dc55f095fd9b1519f54a3b1fe3902a96124adf9f330e48db9d83341`

Existing 07:00 Dataset V1 output:

- day-state rows: 60
- origin-candidate rows: 2,805
- confirmation events: 8,876

Role:

`READY FOR FROZEN V2 CROSS-PERIOD REPLICATION / NOT PRISTINE`

This period was already used as replication in Q1-Q4.

It remains useful to ask whether a newly source-corrected representation preserves direction across the same two historical periods.

It is not a fresh holdout.

---

## C. Broad Dukascopy 2022-09 -> 2023-08 period

File:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2022-09-01_2023-08-31.csv`

Metadata:

- M1 rows: 499,680
- requested days: 365
- days with data: 347
- failed dates: 18
- complete range: false

This period has already been used in MTF alignment and Sideway proxy studies.

Role:

`EXPLORATORY / CONTAMINATED FOR CONFIRMATORY USE / GAP-AWARE ONLY`

Any replay must exclude windows that cross known failed dates.

Do not treat April-August 2023 as a pristine reserve merely because Q1-Q4 did not use all of it; project-level outcome behavior from this range has already been inspected.

---

## D. Dukascopy 2024 Sep-Nov

File:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2024-09-01_2024-11-30.csv`

Metadata:

- M1 rows: 95,040
- missing cache dates: 25
- complete range: false

This period was already used in older remaining-run / inherited-origin studies.

Role:

`STRESS TEST ONLY UNTIL GAPS ARE REPAIRED OR STRICTLY EXCLUDED`

It is not pristine confirmation.

---

## E. Dukascopy 2025 Sep-Nov

File:

`data/raw/dukascopy/chunks/XAUUSD_M1_BID_2025-09-01_2025-11-30.csv`

Metadata:

- M1 rows: 90,720
- missing cache dates: 28
- complete range: false

This period was also used in older studies.

Role:

`STRESS TEST ONLY UNTIL GAPS ARE REPAIRED OR STRICTLY EXCLUDED`

It is not pristine confirmation.

---

## F. Broker MT5 data — 2026

Primary consolidated file:

`data/raw/XAUUSDm_M1_MT5_2026-05-26_2026-09-01.csv`

Direct audit:

- M1 rows: 97,341
- first timestamp: 2026-05-26 00:00 UTC
- last timestamp: 2026-09-01 23:59 UTC
- unique dates containing data: 85
- exact 00:00 UTC bars: 71

Existing native-MT5 resample validation already established:

- M5 local/native mismatch: 0
- H1 mismatch: 0
- H4 mismatch: 0
- D1 mismatch: 0

Existing counts:

- M5: 19,500
- H1: 1,625
- H4: 438
- D1: 85

Role:

`BROKER-SPECIFIC ENGINEERING / CROSS-FEED / REAL-STATE STRESS TEST`

This is extremely useful for:

- checking 07:00 timestamp behavior on the intended MT5-style feed;
- validating resampling;
- observing real broker spread field behavior;
- testing deterministic state reconstruction;
- comparing Dukascopy-vs-MT5 feature behavior.

It is not pristine because it has already been inspected in earlier negative controls.

It is also not final execution-quality data because it is M1 bar data, not complete Bid+Ask tick-level fill data.

---

# 2. Is the existing real data sufficient to begin 0700_MINIMAL_V2?

## Decision

`YES`

It is sufficient for:

1. source-correct detector implementation;
2. deterministic replay;
3. failure/unknown-state discovery;
4. discovery-vs-replication comparison;
5. cross-feed engineering validation;
6. measuring how often the system chooses ENTER vs PASS;
7. identifying the next missing information.

It is **not** sufficient for a final untouched performance claim because all current major historical periods have either:

- already influenced project understanding;
- been used in prior outcome studies;
- or contain known data gaps.

Therefore the next real-data phase is:

`DEVELOPMENT / REPLICATION / FAILURE DISCOVERY`

not:

`FINAL CONFIRMATORY CLAIM`

---

# 3. Current real-data sample available for the H4 lead

Under the historical Q4 representation:

Discovery H4 resolved rows:

- 90 origin rows
- 82 contexts

Replication H4 resolved rows:

- 39 origin rows
- 36 contexts

Combined resolved H4 historical rows:

- 129 origin rows
- 118 period-specific contexts before any cross-period dedup concern

This is enough to justify building and debugging the source-correct V2 representation.

It is not a large enough or clean enough basis for a guaranteed-performance claim.

---

# 4. Real situations that should be tested first

The first V2 replay should explicitly produce a state/result table for at least these situations.

## A. Normal eligible H4 remaining-run cases

- BUY
- SELL
- low consumed state
- middle consumed state
- high consumed state

Important:

Consumed state remains continuous.

Do not recreate Q4 empirical bins as production thresholds.

## B. Point-check lifecycle

- point-check untouched before 07:00
- point-check touched before 07:00 -> ineligible
- point-check destroyed after 07:00 before confirmation
- target reached before point-check
- point-check reached before target

## C. Confirmation cases

- no post-07:00 PAT2
- first M5 PAT2 qualifies
- PAT2 appears but does not pass FULL-RANGE midpoint
- multiple PAT2 confirmations
- confirmation happens after origin already completed
- confirmation happens after point-check destruction

## D. Daily Frame / location states

- unambiguous Daily Frame reference
- expected-side confirmation
- crossed-side confirmation retained as research state
- 0/5 selector ambiguity -> PASS/UNKNOWN
- insufficient location evidence -> PASS

## E. Origin multiplicity

- one valid H4 origin
- multiple same-side H4 origins
- opposite-side surviving origin present
- unresolved winner -> preserve ambiguity / PASS if action cannot be uniquely determined

## F. Outcome ordering

- TARGET_FIRST
- POINT_CHECK_FIRST
- AMBIGUOUS_SAME_BAR
- NEITHER before frozen horizon

Do not delete ambiguous/neither cases.

## G. Data-quality states

- missing M1 window
- incomplete warm-up history
- incomplete post-confirmation horizon
- duplicate timestamp
- unexpected timestamp gap
- broker/feed mismatch

These must produce explicit exclusion/PASS states rather than silent interpolation.

---

# 5. Can we create artificial numbers/scenarios ourselves?

## Yes — and we should.

But synthetic data has a different job from real historical data.

### Synthetic data is appropriate for controlled logic tests

Examples:

1. PAT2 close exactly at 50%.
2. PAT2 close one tick above midpoint.
3. PAT2 close one tick below midpoint.
4. Point-check touched exactly.
5. Point-check missed by one tick.
6. Daily Frame 0/5 perfect tie.
7. Target and point-check touched inside the same M1 bar.
8. Several origins simultaneously active.
9. Origin completes one bar before confirmation.
10. Point-check destroyed one bar before confirmation.
11. Missing M1 bar exactly around 07:00.
12. Duplicate confirmation event.
13. Unknown/unrepresented state -> must PASS.
14. BUY/SELL mirror symmetry.
15. Boundary timestamps at 06:59:59 / 07:00 / 07:00:01 Thailand mapping.

These scenarios are valuable because one variable can be changed at a time.

### Synthetic data can prove

- formula correctness;
- boundary handling;
- state-machine transitions;
- invariants;
- fail-closed behavior;
- mirror symmetry;
- no-lookahead;
- deterministic replay;
- correct UNKNOWN/PASS behavior.

### Synthetic data cannot prove

- market frequency;
- market edge;
- win probability;
- profitability;
- robustness to real regime changes.

Therefore:

```text
SYNTHETIC DATA = ENGINEERING / LOGIC EVIDENCE
REAL DATA      = MARKET / FREQUENCY / RELATIONSHIP EVIDENCE
```

Both are required.

They are not interchangeable.

---

# 6. Recommended test order

## Stage 1 — synthetic contract suite

Before opening new V2 outcomes:

Build synthetic fixtures for exact boundaries and invariants.

Goal:

`prove the engine does exactly what the frozen specification says`

not prove that the market strategy wins.

## Stage 2 — real discovery replay

Use:

`2022-09-01 -> 2023-03-31`

Questions:

- how many 07:00 states are eligible?
- how many become PASS?
- what failure/unknown categories appear?
- how does PAT2 FULL-RANGE change event population relative to historical BODY proxy?
- does H4 consumed-state relation remain visible?

## Stage 3 — same-code real replication

Use unchanged V2 code on:

`2023-09-01 -> 2023-11-23`

No semantic code change between Stage 2 and Stage 3.

## Stage 4 — broker/feed stress test

Use MT5:

`2026-05-26 -> 2026-09-01`

Purpose:

- feed behavior;
- timestamp correctness;
- feature/state reproducibility;
- engineering differences.

Do not call this fresh confirmation.

## Stage 5 — damaged-data stress tests

Use 2024/2025 only with explicit gap masks or after repairing the cache.

Purpose:

- robustness;
- exclusion behavior;
- regime diversity.

Not fresh confirmation.

## Stage 6 — genuine future confirmation

After V2 or later version is frozen:

- prospective chronological collection;
- or a genuinely untouched range that has not influenced rule design.

This is where a strong conditional success rate gains confirmatory meaning.

---

# 7. What to record from every replay

Every 07:00 day should end in one explicit state, including non-trades.

Minimum day-level outputs:

- date / 07:00 known_at;
- source feed + hash/version;
- eligible H4 origins;
- selected/unresolved origin state;
- consumed ratio;
- remaining points;
- point-check status;
- Daily Frame status;
- PAT2 FULL-RANGE confirmation status;
- ENTER_CANDIDATE / PASS / UNKNOWN / DATA_EXCLUDED;
- reason code;
- target/invalidation outcome only after scoring phase;
- unseen-state fingerprint/category if applicable.

This is important because the project learns as much from:

`WHY WE DID NOT TRADE`

as from:

`WHAT HAPPENED AFTER AN ENTRY`

---

# 8. Current conclusion

The project does **not** need more broad source collection before beginning the next development loop.

Existing real history is sufficient to build and challenge a narrow 07:00 V2.

The best next sequence is:

```text
freeze minimal V2
-> synthetic boundary/invariant tests
-> real discovery replay
-> failure/unknown taxonomy
-> unchanged-code replication
-> only then ask which missing information is worth researching
```

This directly implements the project objective:

prepare the decision path as completely as current evidence permits, and when a genuinely new situation appears, PASS first and learn from it rather than forcing a trade.
