# NEXUS XAU MVP Research Set #1 — 2026-09-03

Status: ACTIVE USER-APPROVED FIRST RESEARCH SET

## Why this set exists

The project owner asked whether a deliberately simplified subset can be used as the first historical-data test instead of waiting for every part of the full Mae Pla / Por Chon system to be fully decoded.

A relative then directly replied in substance:

- the simplified set is acceptable;
- use only the 1,000 / 1,500 point objectives for the day;
- once the day's objective has been achieved, stop and trade again on another day;
- the relative also mentioned withdrawing the achieved money, which is a live-money management suggestion rather than a backtest signal rule.

The project owner therefore approves this as the first research set.

## MVP Set #1

```text
Daily Frame 07:00
-> SW / Location
-> SIG H1 / H4
-> H1 objective = 1,000 project points
-> H4 objective = 1,500 project points
-> after the day's objective is achieved, stop evaluating further entries for that day in the one-target-per-day research variant
```

## Important interpretation guard

The owner's use of `90%` in the conversation is NOT evidence of a 90% win rate, 90% probability of profit, or 90% system accuracy.

It is treated only as conversational shorthand for: the simplified set is sufficiently complete/acceptable to start testing before the entire broader system is known.

No performance percentage is established by this conversation.

## What belongs in the historical test

1. Construct the canonical 07:00 Asia/Bangkok daily frame using the currently supported project mapping.
2. Determine SW / Location using only source-backed or explicitly parameterized definitions; unresolved geometry must not be silently invented.
3. Identify H1/H4 SIG candidates only to the extent current SIG semantics support them.
4. Measure forward movement from the defined SIG/post-SIG reference toward:
   - H1: 1,000 project points
   - H4: 1,500 project points
5. Record MFE, MAE, time-to-objective, first-hit information and state/context.
6. In a separate `ONE_TARGET_PER_DAY` variant, stop evaluating later entries after the first qualifying daily objective is reached.

## What does NOT belong in the first test unless independently required by evidence

- Por Chon ATH / over-round logic
- half retrace / swing retrace
- Body Collection advanced logic
- M1/M5 brake entry refinement
- universal SL assumptions
- invented RR values
- invented Sideway thresholds
- invented PAT tolerances

These can be added later as controlled increments if the base set is insufficient.

## Live-money statement separation

Relative guidance such as `ได้แล้วถอนเงินออกเลย เล่นอีกทีก็อีกวัน` is preserved as direct practical guidance.

For research purposes it is split into two meanings:

### Measurable research rule

```text
After the first qualifying daily target is reached, no further entries are counted for that day in the one-target-per-day variant.
```

### Live account behavior

```text
Withdraw achieved money.
```

The withdrawal action is NOT a signal-generation rule and is not needed to evaluate whether the setup has edge. It should not be conflated with win rate or expectancy.

## Questions this first set can answer

If the unresolved SW/Location/SIG pieces are made measurable without guessing, the historical dataset can answer:

- How often does a valid H1 setup reach 1,000 points?
- How often does a valid H4 setup reach 1,500 points?
- Does the 07:00 frame add measurable information versus PAT/SIG shape alone?
- Does correct Location improve outcomes?
- Does SW state materially change outcomes?
- How many days produce at least one qualifying target?
- What changes when enforcing one successful target per day?
- How large are adverse excursions before the objective is reached?
- How stable are these results across development / validation / test periods?

## What this set still cannot prove by itself

Until entry, SL/invalidation and all required SIG/Location semantics are frozen, this set must NOT be called a complete trading-system backtest and must NOT be used to claim canonical Win rate, Loss rate, expectancy or monthly income.

The first objective is narrower:

```text
Does the simplified 07:00 + SW/Location + H1/H4 SIG + fixed-run structure contain useful, repeatable information in historical data?
```

## Research principle

This checkpoint follows the project's Measurement-to-Question method:

```text
What can be measured?
-> What should it be compared with?
-> Which uncertainty will that measurement close?
```

The purpose is to reduce uncertainty one controlled component at a time rather than reconstructing the entire trading methodology before any evidence can be tested.
