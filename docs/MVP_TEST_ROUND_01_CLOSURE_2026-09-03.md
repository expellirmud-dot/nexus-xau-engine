# NEXUS XAU MVP Set #1 — Test Round 01 Closure — 2026-09-03

Status: CLOSED RESEARCH ROUND / NOT A SYSTEM BACKTEST

## Frozen target

```text
Daily Frame 07:00
-> SW / Location
-> SIG H1 / H4
-> H1 1,000 project points / H4 1,500 project points
```

This round uses the hypothesis-first method. Each bounded question is closed by evidence rather than left open indefinitely.

Dataset used:

- Symbol: XAUUSDm
- M1 historical range: 2026-05-26 00:00 UTC -> 2026-09-01 23:59 UTC
- M1 bars: 97,341
- Project point size used by research reports: 0.01 price
- Chronological splits already established in the project:
  - DEV: before 2026-07-01 UTC
  - VAL: 2026-07-01 through 2026-07-31 UTC
  - TEST: 2026-08-01 onward in this dataset

Important: all results below are component research results. They are not canonical system win rate, loss rate, expectancy, or proof of profitability.

---

## Q1 — Daily Frame proximity alone

Prior closure:

`INCONCLUSIVE / MIXED`

The simple statement “closer to the direction-correct Daily Frame is better than far from the frame” was not robust across all frozen metrics and both H1/H4 held-out results.

This prevented the project from treating Daily-Frame proximity alone as the edge.

---

## Q2 — Direction-correct Daily-Frame side relation

Question:

> Within broad H1/H4 PAT topology candidates, does a near-frame candidate that remains on the expected support/resistance side outperform a near-frame candidate whose wick extreme crosses beyond the line and a far-frame control?

Research representation:

- BUY: PAT-window low relative to Daily-Frame lower/support line.
- SELL: PAT-window high relative to Daily-Frame upper/resistance line.
- Positive signed distance = PAT extreme remains on expected/inside side.
- Negative signed distance = PAT extreme crosses beyond line.
- Near/far analysis buckets are DEV q25/q75 only; they are not trading thresholds.
- A wick crossing is NOT declared invalid canonical location because exact accepted penetration remains unresolved.

### H1 result — SUPPORTED for this representation

Validation:

```text
EXPECTED_SIDE_NEAR    n=47   target-first=0.8723   target-reach=1.0000
CROSSED_SIDE_NEAR     n=61   target-first=0.7541   target-reach=0.8525
FAR_CONTROL           n=122  target-first=0.8443   target-reach=0.9508
```

Test:

```text
EXPECTED_SIDE_NEAR    n=50   target-first=0.9400   target-reach=0.9600
CROSSED_SIDE_NEAR     n=41   target-first=0.8780   target-reach=0.9268
FAR_CONTROL           n=97   target-first=0.8144   target-reach=0.9588
```

Frozen two-metric criterion is satisfied on both held-out splits.

Closure:

`H1 = SUPPORTED`

Meaning:

The H1 data supports the hypothesis that the candidate's relation to the correct Daily-Frame side contains additional information beyond absolute proximity alone, under this explicit research representation.

It does NOT prove the canonical touch/penetration rule.

### H4 result — INCONCLUSIVE

Validation expected-side-near has only 6 events; Test crossed-side-near has only 9 events. These are below the predeclared minimum group size of 10.

Closure:

`H4 = INCONCLUSIVE_DUE_SAMPLE_SIZE`

The H4 numbers are directionally interesting, but the project does not upgrade them to SUPPORTED from a sparse subset.

Source outputs:

- `results/MVP_Q2_DAILY_FRAME_LOCATION_RELATION_2026-05-26_2026-09-01.json`
- `results/MVP_Q2_DAILY_FRAME_LOCATION_RELATION_EVENTS_2026-05-26_2026-09-01.csv`

---

## Q2b — Source-backed <=200-point Daily-Frame proximity

Primary teaching image evidence states a demonstrated Daily-Frame entry condition of `ชิดกรอบ <=200 points`, with setup-context wording that price can also pierce S/R by around 200 points.

Question:

> Do broad H1/H4 PAT topology candidates within 200 project points of the direction-correct Daily Frame outperform candidates beyond 200 points?

### H1

Validation:

```text
<=200   n=17   target-first=0.8824   target-reach=1.0000
>200    n=498  target-first=0.8012   target-reach=0.9337
```

Test:

```text
<=200   n=25   target-first=0.9200   target-reach=0.9200
>200    n=436  target-first=0.8326   target-reach=0.9472
```

The Validation near group is below the minimum 20-event requirement, and Test target-reach is lower for <=200 despite higher target-first.

Closure:

`H1 = INCONCLUSIVE`

### H4

Validation <=200 n=8; Test <=200 n=11. Sample requirement is not met.

Closure:

`H4 = INCONCLUSIVE_DUE_SAMPLE_SIZE`

Interpretation:

The 200-point teaching condition remains a source-backed setup rule, but this broad topology-only dataset does not independently confirm it as an outcome-improving universal filter. Outcome cannot supersede the teaching source either way.

Source output:

- `results/MVP_Q2B_DAILY_FRAME_200PT_2026-05-26_2026-09-01.json`

---

## Q3 — Does SW add information beyond Location?

Evidence review result:

The project knows the Sideway lifecycle/state concept, but a reproducible canonical SW detector is still absent.

Unresolved items include:

- exact upper/lower SW frame construction;
- exact `กรอบ SW ครบ` completion event;
- exact breakout / false-break rule;
- exact exit / new-SIG transition;
- point tolerances.

Existing engine state:

`Sideway state/event shell = supported`

`Canonical numeric detector = NOT_IMPLEMENTED / HUMAN_CONFIRM`

Therefore a historical SW label cannot currently be generated without inventing geometry.

Closure:

`Q3 = NOT_TESTABLE_WITH_CURRENT_EVIDENCE`

This is a closed result for this test round. It does not trigger indefinite evidence collection.

---

## Q4a — Does >50% PAT midpoint geometry add information?

Question:

> Starting from H1/H4 PAT2/PAT3 color topology, does applying the source-backed >50% midpoint relation improve forward outcome behavior?

Because the exact midpoint denominator is unresolved, two explicitly named research variants were tested:

- `BODY` = midpoint of open/close.
- `FULL_RANGE` = midpoint of high/low.

Outcome performance is not allowed to decide which definition is the true teaching definition.

### H1 PAT2 BODY — SUPPORTED

Validation:

```text
PASS  n=170  target-first=0.8176  target-reach=0.9412
FAIL  n=84   target-first=0.7738  target-reach=0.8929
```

Test:

```text
PASS  n=164  target-first=0.8598  target-reach=0.9695
FAIL  n=71   target-first=0.7465  target-reach=0.9014
```

Closure:

`H1_PAT2_BODY = SUPPORTED as a research variant`

This means BODY-midpoint PAT2 is worth prioritizing for source cross-check / later interaction testing.

It does NOT mean historical performance has proven BODY is the canonical teacher denominator.

### Remaining midpoint variants

```text
H1_PAT2_FULL_RANGE   = INCONCLUSIVE
H1_PAT3_BODY         = INCONCLUSIVE
H1_PAT3_FULL_RANGE   = INCONCLUSIVE
H4_PAT2_BODY         = INCONCLUSIVE (held-out fail group too small)
H4_PAT2_FULL_RANGE   = INCONCLUSIVE (held-out fail group too small)
H4_PAT3_BODY         = INCONCLUSIVE
H4_PAT3_FULL_RANGE   = INCONCLUSIVE
```

PAT3 remains especially partial because small-body and SELL equal-wick thresholds are intentionally not invented.

Source outputs:

- `results/MVP_Q4A_PAT_MIDPOINT_OUTCOME_2026-05-26_2026-09-01.json`
- `results/MVP_Q4A_PAT_MIDPOINT_OUTCOME_EVENTS_2026-05-26_2026-09-01.csv`

---

## Exploratory interaction probe — NOT a closure result

After seeing Q2 and Q4a results, an exploratory query inspected:

```text
H1 PAT2
+ BODY midpoint pass
+ Daily-Frame location relation
```

Because this interaction question was examined after the TEST-period component results were already known, it is not promoted as a fresh confirmatory held-out result.

Use it only to design the next predeclared interaction experiment or to prioritize a future untouched period.

---

## What changed in our understanding

Before this round:

```text
Daily Frame -> Location -> SW -> SIG -> run
```

was mainly a teaching chain that we were trying to decode completely before testing.

After this round:

1. Daily-Frame proximity alone is not enough to establish a robust H1/H4 filter.
2. H1 relation to the correct Daily-Frame side carries measurable information in the tested representation.
3. The exact <=200-point teaching proximity rule is not independently confirmed by this broad topology-only sample; result is inconclusive.
4. SW cannot yet be tested honestly because its detector is not reproducible.
5. H1 PAT2 BODY-midpoint qualification adds measurable information versus topology-only PAT2 in both held-out splits.
6. Most other midpoint/TF combinations remain inconclusive rather than being forced into a conclusion.

This is concrete progress toward the frozen target even though the full chain is not yet testable.

---

## Data-leakage / next-test guard

The current TEST period has now been inspected for Q1, Q2, Q2b and Q4a.

Therefore:

- those tests retain their declared closures;
- a NEW hypothesis invented because of these observed TEST results must be labeled `EXPLORATORY` if evaluated on the same TEST period;
- confirmatory status for such a newly invented interaction should use an untouched later period or another explicitly untouched dataset.

This prevents repeated historical querying from manufacturing apparent certainty.

---

## Next bounded work

1. Preserve Q2 H1 Location relation and Q4a H1 PAT2 BODY as research-supported components, without promoting either to canonical teaching truth.
2. Build Q5 measurement around the source-backed H1=1,000 / H4=1,500 run objectives, separating descriptive target behavior from strategy win rate.
3. Keep `FRESH_TARGET_CONTROL` separate from the newer `INHERITED_REMAINING_RUN` hypothesis.
4. Do not run a canonical full-chain Q6 until SW and required SIG/remaining-run fields have reproducible representations; partial-chain queries on the current TEST period are exploratory only.

---

## Q5 — Descriptive H1=1,000 / H4=1,500 run-objective behavior

Question:

> In the broad H1/H4 PAT-topology candidate population, how common is forward movement reaching the source-backed run distances H1=1,000 and H4=1,500 project points?

This is descriptive only. It does not qualify candidates as valid SIGs and does not establish strategy win rate.

### H1 = 1,000 points

```text
DEV   n=615  target reached anywhere=0.9382  symmetric target-first=0.7886
VAL   n=526  target reached anywhere=0.9373  symmetric target-first=0.8080
TEST  n=471  target reached anywhere=0.9469  symmetric target-first=0.8386
```

Median MFE remained far above 1,000 points in all three splits:

```text
DEV  5,640.2
VAL  4,265.35
TEST 4,956.8 project points
```

### H4 = 1,500 points

```text
DEV   n=166  target reached anywhere=0.9699  symmetric target-first=0.8916
VAL   n=145  target reached anywhere=0.9310  symmetric target-first=0.8207
TEST  n=121  target reached anywhere=0.9339  symmetric target-first=0.8347
```

Median MFE also remained far above 1,500 points:

```text
DEV  8,973.05
VAL  6,983.1
TEST 6,841.9 project points
```

Closure:

`Q5 = DESCRIPTIVE_BASELINE_ESTABLISHED`

Interpretation:

The 1,000/1,500 teaching distances are not rare forward-path distances in this broad candidate/horizon construction. Therefore the central research problem is not merely whether price can travel those distances. The higher-value question is whether the Daily Frame / Location / SW / SIG state identifies the useful direction and timing with better adverse-path behavior than controls.

Guard:

- Topology candidates are not valid PA/SIG labels.
- Existing outcome anchors are the earlier fresh-target research control, not the newer inherited remaining-run model.
- Symmetric adverse barriers are controls, not SL rules.
- Do not describe the above rates as strategy win rate.

Source output:

- `results/MVP_Q5_RUN_OBJECTIVE_DESCRIPTIVE_2026-05-26_2026-09-01.json`
