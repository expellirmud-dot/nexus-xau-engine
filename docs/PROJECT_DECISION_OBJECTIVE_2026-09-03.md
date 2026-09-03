# NEXUS XAU — Project Decision Objective

Date: 2026-09-03
Status: PROJECT-LEVEL OBJECTIVE / RESEARCH GOVERNANCE

## 1. Why this project exists

This project is not being developed merely to produce a BUY/SELL signal or to maximize a single-trade win rate.

The project owner wants to build a system that can support a more independent, multi-source working life. Current income/work paths include photography and development of an online-freelance workflow. If the investment research eventually proves durable, investing/trading may become a third income path alongside photography and online work.

The project therefore matters beyond experimentation. It is intended to become a serious decision system that can be studied, audited and improved over time. This personal motivation must increase research discipline, not lower the evidence threshold.

Important separation:

- Personal/life importance explains **why the project matters**.
- It must never be used as evidence that a trading rule works.
- Financial need must not force a positive research conclusion.

## 2. Revised project goal

The system should learn to recognize its own state and choose the best-supported action available at that moment.

It should eventually be able to answer questions such as:

- When should the current thesis remain active?
- When should the system change interpretation?
- When should a setup be avoided?
- When should the system wait rather than act?
- When should an existing position be reduced or exited?
- When should a loss be accepted rather than defended?
- When should trading stop temporarily because the state is unclear or hostile?
- When is the evidence strong enough to continue holding risk?

The goal is NOT:

```text
maximize profit on every trade
or
minimize pain on every trade
```

The goal is:

```text
Given only the information that was available at time t,
choose the action with the strongest evidence-adjusted trade-off
between expected opportunity and acceptable risk,
then update that decision when new evidence arrives.
```

This is a sequential decision problem, not a one-event classification problem.

## 3. Decision quality is not the same as realized outcome

A decision can be good and still lose money.
A decision can be poor and still make money.

Therefore research must record two different judgements:

### Ex-ante decision quality

Was the action justified by the information, state and rules available at the time?

### Ex-post outcome

What actually happened afterward?

These must never be collapsed into one label.

Example:

```text
Valid H1 BUY SIG + valid support context + acceptable risk
-> ENTER was justified
-> market later invalidates SIG
-> EXIT/ACCEPT LOSS was then justified
-> realized trade = LOSS
-> sequence may still represent two correct decisions
```

The system should not label the original decision as wrong merely because the final P/L was negative.

## 4. Multi-event model

A trade/setup must be represented as a sequence:

```text
STATE_0
  -> EVENT_1
  -> DECISION_1
  -> STATE_1
  -> EVENT_2
  -> DECISION_2
  -> STATE_2
  -> EVENT_3
  -> DECISION_3
  -> ...
  -> TERMINAL OUTCOME
```

An event may include, for example:

- PAT completes;
- valid/invalid support-resistance interaction becomes known;
- post-SIG reference candle closes;
- post-SIG wick is preserved or destroyed;
- M5 confirms or fails;
- higher timeframe changes context;
- TP/run completes;
- run becomes OVERRUN;
- opposite PA appears;
- Sideway forms;
- body-collection zone is reached, consumed or invalidated;
- a stop/invalidation condition occurs.

A decision may include research actions such as:

```text
WAIT
SKIP
ENTER
HOLD
REDUCE_RISK
EXIT
ACCEPT_LOSS
RE-ANCHOR
RE-EVALUATE
STOP_TRADING_THIS_SETUP
```

These action names are research-state vocabulary. They do not become live execution rules until their exact conditions are evidence-backed.

## 5. The system should evaluate paths, not only Event 1

A single initial signal can lead to multiple paths.

Example shell:

```text
EVENT 1: valid PAT/SIG appears
  -> possible action: ENTER or WAIT

EVENT 2A: post-SIG remains valid
  -> HOLD may remain justified

EVENT 2B: post-SIG is destroyed
  -> EXIT / ACCEPT_LOSS / RE-EVALUATE may become superior

EVENT 3A: normal run reaches TP
  -> do not automatically counter-trade
  -> inspect OVERRUN / RETRACE state

EVENT 3B: opposite PA appears after OVERRUN
  -> HALF_RETRACE candidate

EVENT 3C: no opposite PA
  -> SWING_RETRACE candidate

EVENT 4: new PA replaces the prior setup
  -> old thesis may be retired and system re-anchored
```

The correctness of Decision 1 must therefore not be judged only by the terminal result. Decisions 2, 3 and 4 can materially change the final outcome.

## 6. What “best decision” means for engineering

The project owner does not require one philosophical definition of “best”. That is acceptable at the project-goal level.

For research and coding, however, a measurable objective will eventually be required. It should be built from several dimensions rather than one metric:

- expected return / expectancy;
- probability and size of adverse movement;
- MAE and MFE distribution;
- drawdown contribution;
- probability of ruin or unacceptable portfolio damage;
- state-specific historical performance;
- opportunity cost of waiting/skipping;
- transaction cost, spread and slippage;
- uncertainty / evidence quality;
- effect of the next likely state transition.

A future decision policy may therefore use an evidence-adjusted objective such as:

```text
decision_score = expected_opportunity
                 - risk_cost
                 - uncertainty_penalty
                 - execution_cost
                 - portfolio_damage_penalty
```

This formula is only a conceptual shell. We must NOT assign weights until evidence and risk policy are defined.

## 7. Research implication: from Win Rate to Policy Quality

Win rate and loss rate remain important, but they become components rather than the final objective.

The project should eventually report at least four layers:

### Layer A — Setup statistics

- valid setup frequency;
- Win/Loss under frozen entry/exit rules;
- expectancy;
- MAE/MFE;
- losing streaks;
- drawdown.

### Layer B — State statistics

Results conditional on:

- SIG active;
- post-SIG valid/destroyed;
- RUNNING;
- TP_COMPLETE;
- OVERRUN;
- RETRACING;
- SIDEWAY;
- BODY_COLLECTION;
- MTF alignment/conflict.

### Layer C — Decision-transition statistics

Examples:

- ENTER -> HOLD;
- ENTER -> INVALIDATE -> EXIT;
- WAIT -> later ENTER;
- SKIP -> opportunity missed / loss avoided;
- TP_COMPLETE -> HOLD vs EXIT;
- OVERRUN -> counter vs wait;
- destroyed SIG -> re-anchor vs remain in old thesis.

### Layer D — Full path / policy statistics

Evaluate complete sequences, not isolated actions:

```text
Path A: ENTER -> HOLD -> TP
Path B: ENTER -> INVALIDATE -> ACCEPT LOSS
Path C: WAIT -> NEW SIG -> ENTER -> TP
Path D: SKIP -> SIDEWAY
Path E: TP COMPLETE -> WAIT -> OVERRUN -> NEW STATE
```

This is the level at which the system can start answering which response is historically preferable in different states.

## 8. Counterfactual requirement

When possible, each decision event should preserve alternative actions that were available at the time.

For example:

```text
At EVENT_2:
actual policy action = EXIT
alternatives = HOLD / REDUCE / RE-ANCHOR
```

Research may then compare what would have happened under each alternative using future data, while clearly marking those alternatives as counterfactual analysis.

Critical rule:

Future outcome may evaluate an already-defined policy, but must NOT be used to invent the rule after seeing the result.

## 9. No-hindsight requirement

Every replay decision must persist:

```text
visible_data_until
event_time
state_before
evidence_available
candidate_actions
chosen_action
rule_ids_used
state_after
future_data_used = false
```

Only after the action is frozen may future bars be revealed to score the outcome.

This is required to prevent hindsight bias.

## 10. Risk acceptance is part of the system

Loss is not automatically a system failure.

The system must distinguish:

- planned/acceptable loss;
- invalidation loss;
- avoidable loss caused by violating rules;
- model error;
- regime/state where the system should not have participated;
- extreme/rare event beyond normal historical assumptions.

A mature system should know not only how it attempts to profit, but also:

```text
when to stop being right
when to admit the thesis is no longer valid
how much damage is acceptable
when uncertainty itself is a reason to stay out
```

## 11. Project-owner context recorded on 2026-09-03

The project owner described the broader personal reason for taking this work seriously:

- after leaving a long-term municipal job of approximately 12 years, the former single-employer income path ended;
- current primary work/income includes photography;
- a separate online-freelance project is being developed in parallel;
- a validated investment system could potentially become another income path, not necessarily limited to gold and possibly extending to a conventional stock portfolio;
- the preferred long-term direction is not avoidance of work, but development of multiple self-built systems that can support life without depending entirely on one full-time employer;
- the enjoyable part is not only the possibility of earning money, but the process of building systems that are capable of sustaining themselves and improving over time.

This context is recorded so future project work retains the seriousness and purpose behind the research. It is not a performance claim and must not affect statistical conclusions.

## 12. Governance decision — effective immediately

From this checkpoint onward, the project should optimize for:

```text
QUALITY OF SEQUENTIAL DECISIONS UNDER UNCERTAINTY
```

rather than:

```text
MAXIMUM SINGLE-SIGNAL WIN RATE
```

Win/Loss/expectancy research continues, but every future strategy result should be interpreted within the event/state sequence that produced it.

## 13. Immediate next engineering consequences

1. Keep the existing outcome harness.
2. Add an `EventRecord` / `DecisionTransitionRecord` schema before canonical strategy backtesting.
3. Freeze source-backed PAT/SR/post-SIG/entry/invalidation rules before policy scoring.
4. Record state before and after every decision.
5. Preserve alternative actions for later counterfactual testing when possible.
6. Score both individual actions and complete paths.
7. Report loss acceptance and rule-compliant exits separately from setup failures.
8. Keep project motivation separate from research evidence.

This document is a project charter for decision quality. It does not promote any unresolved trading rule to production status.
