# NEXUS XAU MVP Set #1 — Hypothesis-First Test Plan — 2026-09-03

Status: ACTIVE TEST CONTRACT

## Frozen target

```text
Daily Frame 07:00
-> SW / Location
-> SIG H1 / H4
-> H1 1,000 project points / H4 1,500 project points
```

This is the current first research target. The purpose is not to decode the entire teaching system before testing. The purpose is to use historical data to answer bounded questions and use those answers to decide what must be decoded next.

## Closure states

Every question must end in exactly one of:

- `SUPPORTED`
- `NOT_SUPPORTED`
- `INCONCLUSIVE`
- `NOT_TESTABLE_WITH_CURRENT_EVIDENCE`

`INCONCLUSIVE` and `NOT_TESTABLE_WITH_CURRENT_EVIDENCE` are valid closed outcomes for that experiment. They do not automatically trigger an endless request for more evidence.

## Test ladder

### Q1 — Daily Frame adds information by itself?

Question:

> Does direction-correct proximity to the 07:00 Daily Frame improve outcomes versus far-from-frame H1/H4 PAT topology candidates?

Method:

- BUY measured to Daily-Frame lower/support line.
- SELL measured to Daily-Frame upper/resistance line.
- DEV determines near/far buckets; VAL and TEST are held out.
- No SW, remaining-run or full SIG qualification included.

Current result:

`INCONCLUSIVE / MIXED`

Interpretation:

Daily-Frame proximity alone is not yet supported as a consistently useful filter across both H1 and H4 held-out data. This question is closed at this level.

### Q2 — Location relation matters?

Question:

> For the same broad H1/H4 candidate family, does being on the direction-correct side/location of the Daily Frame outperform wrong-side / non-location candidates?

Required measurable fields:

```text
side
expected_support_or_resistance
pattern_low/high
signed_distance_to_frame
location_relation
forward MFE/MAE
1,000/1,500 target behavior
```

This can be tested without knowing the entire SW rule.

Closure rule:

- `SUPPORTED` only if direction-correct location improves pre-registered metrics on held-out data.
- mixed evidence => `INCONCLUSIVE`.

### Q3 — SW adds information beyond Location?

Question:

> After controlling for Daily-Frame Location, does SW state materially improve or change the outcome distribution?

Rules:

- Do not invent a canonical SW threshold.
- If current evidence cannot create a reproducible SW label/feature, return `NOT_TESTABLE_WITH_CURRENT_EVIDENCE` and close this version of Q3.
- Historical/labeled teaching cases may later enable a new version of Q3.

### Q4 — H1/H4 SIG qualification adds information?

Question:

> Within Daily-Frame/Location-qualified events, does stronger source-backed SIG qualification outperform broad PAT topology candidates?

Approach:

- start broad and add only supported SIG components;
- compare each increment against the previous layer;
- do not call topology-only events valid SIGs.

Possible sequence:

```text
PAT topology
-> PAT geometry variants
-> correct Location
-> supported post-SIG semantics
-> multi-TF confluence features
```

Each increment receives its own closure state.

### Q5 — Run objective behaves as claimed?

Question:

> Once an H1/H4 setup is known at decision time, how often and under what state does price complete H1=1,000 or H4=1,500 project points?

Metrics:

```text
target reached
first-hit against neutral adverse barrier
MFE
MAE
time-to-target
state at decision time
```

The neutral adverse barrier is a research control, not a canonical SL.

### Q6 — Full MVP chain

Only after Q2–Q5 have measurable variants, evaluate:

```text
07:00 Daily Frame
+ SW/Location
+ H1/H4 SIG
+ 1,000/1,500 run objective
```

Compare against controls:

1. PAT/topology only.
2. Daily Frame only.
3. Location only.
4. SIG without Daily Frame.
5. Full chain.

Use DEV / VAL / TEST chronology and no future information at decision time.

## Remaining-run refinement

Direct relative guidance later introduced inherited remaining-run state. Therefore Q5/Q6 should eventually compare two explicitly separated hypotheses:

- `FRESH_TARGET_CONTROL`: reset 1,000/1,500 from the candidate entry.
- `INHERITED_REMAINING_RUN`: reconstruct originating SIG run and target only the unfinished portion.

The fresh-target version is a control, not assumed canonical. The inherited-run version follows the newer relative guidance once its anchor semantics are measurable.

## When the main target is considered answered

The first target is considered answered when:

1. the full-chain variant can be replayed without future data;
2. each required component has a reproducible measurable representation or an explicit closed `NOT_TESTABLE` status;
3. the full-chain historical result is evaluated on held-out data;
4. the conclusion is recorded as one of `SUPPORTED / NOT_SUPPORTED / INCONCLUSIVE`;
5. no performance metric is mislabeled as canonical win rate unless entry, SL/invalidation, costs and execution rules are separately frozen.

The goal is to obtain a defensible answer, not to force a profitable result.

## Operating principle

```text
QUESTION
-> measurable variable(s)
-> comparison/control
-> pre-declared closure rule
-> historical test
-> CLOSED RESULT
-> choose next question from the result
```

Do not return to "collect evidence indefinitely before testing" as the default research mode.
