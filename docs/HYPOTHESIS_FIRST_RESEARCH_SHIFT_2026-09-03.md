# NEXUS XAU — Hypothesis-First Research Shift — 2026-09-03

Status: ACTIVE RESEARCH-METHOD CORRECTION

## Problem identified by project owner

The project had drifted toward an exhaustive rule-decoding workflow:

```text
find source rule -> discover ambiguity -> request more evidence -> discover another ambiguity -> repeat
```

This preserved provenance but created no clear finish line for many practical questions. Useful historical data was underused because the project implicitly waited for the full methodology to be decoded before testing anything meaningful.

## Corrected research principle

Use historical data to test bounded hypotheses before the entire trading methodology is decoded.

```text
QUESTION
-> define measurable proxy/component
-> freeze evaluation rule BEFORE looking at held-out results
-> run DEV / VAL / TEST
-> classify SUPPORTED / NOT_SUPPORTED / INCONCLUSIVE
-> use that answer to decide which source rule is worth decoding next
```

Source decoding and hypothesis testing are complementary, not sequential dependencies.

### What testing CAN do

- show whether a candidate component adds measurable information;
- reject components that do not appear useful under the tested representation;
- identify interactions worth decoding more deeply;
- reveal which unknowns materially change outcomes;
- reduce the number of questions that need human/source clarification.

### What testing CANNOT do

- turn an unsupported threshold into a canonical production rule merely because it backtests well;
- prove instructor semantics that were never observed;
- replace valid entry/SL/invalidation definitions when claiming a true strategy win rate;
- upgrade weak provenance into direct evidence.

## First concrete component test

Question:

> Does proximity to the direction-correct 07:00 Daily Frame add measurable directional information to H1/H4 PAT topology candidates?

Design:

- validated XAUUSDm M1 history: 2026-05-26 through 2026-09-01;
- 07:00 Asia/Bangkok mapped to 00:00 UTC;
- BUY candidates measured against Daily-Frame lower/support line;
- SELL candidates measured against Daily-Frame upper/resistance line;
- DEV q25/q75 distance buckets define `near` and `far` once, then frozen for VAL/TEST;
- outcomes reused the existing topology negative-control machinery;
- this is a component test, NOT a system backtest.

Result:

```text
OVERALL: MIXED_OR_INCONCLUSIVE
H1: INCONCLUSIVE_OR_MIXED
H4: INCONCLUSIVE_OR_MIXED
```

Held-out examples:

### H1

VAL:
- near target-first: 0.806
- far target-first: 0.844
- near target-reach: 0.917
- far target-reach: 0.951

TEST:
- near target-first: 0.912
- far target-first: 0.814
- near target-reach: 0.945
- far target-reach: 0.959

Direction reverses between VAL and TEST on target-first, so proximity alone is not robustly established for H1.

### H4

VAL:
- near target-first: 0.821
- far target-first: 0.750
- near target-reach: 0.964
- far target-reach: 0.833

TEST:
- near target-first: 0.920
- far target-first: 0.636
- near target-reach: 0.960
- far target-reach: 1.000

H4 shows an interesting target-first advantage for near candidates on both held-out splits, but the TEST target-reach metric does not satisfy the pre-registered rule. Therefore the correct classification remains INCONCLUSIVE, not "Daily Frame works".

## What this answer closes

It closes the narrow question in its current representation:

> Daily-Frame proximity by itself, applied to topology-only H1/H4 candidates, is NOT yet established as a robust standalone filter across held-out data.

This is a real answer, even though it is not a positive answer.

## What question should come next

Recent relative guidance says Daily Frame is used with an unfinished inherited SIG run, not in isolation.

Therefore the next higher-value hypothesis is:

> Does Daily-Frame proximity become informative specifically when an H1/H4/D SIG still has remaining run at 07:00?

This is now a targeted decoding problem: reconstructing `origin SIG -> consumed run -> remaining run` matters more than requesting broad additional explanations about Daily Frame.

A second controlled interaction can then test graded lower-TF alignment:

```text
remaining SIG run + Daily Frame
vs
remaining SIG run + Daily Frame + 1/2/3/4 aligned lower TFs
```

## New finish-line rule

Every research question must have, before execution:

1. exact question;
2. measurable representation;
3. comparison/control;
4. held-out decision rule;
5. one of three terminal statuses: SUPPORTED / NOT_SUPPORTED / INCONCLUSIVE.

`INCONCLUSIVE` is a valid completed result. It does not automatically create a request for more evidence. More evidence is requested only when the result identifies a specific ambiguity whose resolution is expected to change the next decision-relevant test.
