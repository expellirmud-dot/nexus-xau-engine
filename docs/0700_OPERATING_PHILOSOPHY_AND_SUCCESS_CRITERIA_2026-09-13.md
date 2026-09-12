# 07:00 Operating Philosophy and Success Criteria — 2026-09-13

Status: PROJECT-LEVEL OPERATING PRINCIPLE / MUST BE READ BEFORE 07:00 RESEARCH OR IMPLEMENTATION

Authority: OWNER-DIRECT PROJECT OBJECTIVE

## Why this document exists

The 07:00 workstream is not a generic auto-trading application.

It is not designed to:

- trade continuously;
- scan every market at every time;
- force an entry every day;
- imitate a generic indicator bot;
- maximize the number of trades;
- hard-code a finite checklist of historical winning patterns and reject everything else blindly.

The project goal is narrower and more demanding:

> At the 07:00 decision point, assemble every piece of information that is legitimately knowable by then, convert it into a reproducible market/run state, and act only when the current state is sufficiently understood and supported by evidence.

Anything unknown is allowed to produce:

`PASS / NO TRADE / NEEDS REVIEW`

That is a valid system outcome, not a failure of the system.

---

## Core idea

The project should try to close as many avoidable failure doors as possible **before** allowing an entry.

This does not mean claiming that every trade can be guaranteed to win.

It means the system should be built so that:

- all relevant pre-07:00 evidence is considered;
- known invalidation states are detected;
- known conflicting states are represented rather than ignored;
- unresolved geometry is not guessed;
- unsupported situations can be rejected;
- every decision is traceable to data and versioned rules;
- the system never has to trade simply because 07:00 has arrived.

The intended direction is therefore:

```text
all knowable pre-07:00 history
        ↓
07:00 state snapshot
        ↓
known / supported?
   ├─ NO  -> PASS + record unknown
   └─ YES -> continue validation
                ↓
          qualifying confirmation?
             ├─ NO  -> PASS
             └─ YES -> candidate action
```

---

## What "success" means for this project

Success is **not** defined as:

- "the bot always opens a trade";
- "the bot trades all day";
- "the bot has a marketing-style win-rate claim";
- "the system contains 100 hard-coded winning scenarios";
- "a backtest can be tuned until no losing sample remains."

Success is defined in layers.

### 1. Process correctness

Aim for 100% in what the system can control:

- no look-ahead;
- correct data timestamp handling;
- deterministic state reconstruction;
- reproducible calculations;
- correct source/rule version;
- complete audit trail;
- explicit UNKNOWN/PASS states;
- no silent fallbacks;
- no outcome-selected rule changes.

### 2. Decision coverage

The system should know the difference between:

- a state it understands;
- a state it partially understands;
- a genuinely unseen state.

A new state is not forced into the closest known pattern.

### 3. Selective participation

The system may trade rarely if that is what evidence requires.

The target is not "maximum participation."

The target is:

`high-confidence participation only when current evidence justifies it`

### 4. Learning from new states

If real operation or historical replay produces a new state that the system cannot classify safely:

```text
new/unseen state
-> do not trade
-> record exact state
-> investigate source/data
-> determine whether a new rule/state representation is justified
-> freeze a new version
-> validate separately
```

This is how the knowledge base grows.

Do not patch the live rule ad hoc after seeing one failure.

---

## The "100 known situations + situation 101" principle

A useful mental model is:

Suppose the project currently understands 100 materially different situations.

The implementation is **not**:

`if not exactly one of these 100 patterns -> reject forever`

Instead:

- the 100 known situations represent the current boundary of justified knowledge;
- the engine should generalize from evidence-backed state variables where appropriate;
- if a materially new state "101" appears and cannot be safely mapped to the current model, the correct immediate action is PASS;
- state 101 is then added to the research queue;
- only after evidence/source/replication supports an update does a new version learn to handle it.

This is controlled expansion, not brittle hard-coding.

---

## Why the 07:00 scope is different from a generic auto-trader

A generic always-on bot must handle:

- many market regimes;
- many times of day;
- continuously changing liquidity;
- repeated opportunities;
- broad execution conditions;
- a much larger state space.

The 07:00 project intentionally compresses the decision problem.

It may use information from outside 07:00, but only as **history feeding the 07:00 state**.

Examples:

- what happened overnight;
- which H4/H1 run is still active;
- how much of a run has already been consumed;
- which point-checks survived;
- which higher-timeframe structure is active;
- where price sits relative to the Daily Frame;
- recent multi-timeframe agreement;
- relevant pre-07:00 invalidations.

The system does not need to make trading decisions throughout those earlier hours.

It only needs to summarize them correctly for the 07:00 decision process.

---

## Historical-data development loop

Historical data is not used merely to ask:

`Did this formula win?`

It is used to discover:

- which states are already handled;
- where known logic fails;
- which failures share a common cause;
- which state variables are missing;
- which source question should be reopened;
- which situations should become explicit PASS states;
- whether a candidate relationship survives different periods.

The loop is:

```text
freeze current knowledge
-> replay historical data
-> inspect failures / unknowns
-> classify failure causes
-> ask what information was missing
-> research only that missing information
-> freeze next version
-> test on separate data
```

Do not use the same data both to invent and to prove a rule without labeling that limitation.

---

## Real data versus synthetic data

Both are useful, but for different purposes.

### Real historical data

Use real data first for:

- discovery of actual market states;
- frequency of situations;
- realistic sequencing;
- no-lookahead replay;
- distribution shifts;
- empirical relationship testing;
- replication across periods.

Real data is required for market-performance evidence.

### Synthetic / constructed data

Synthetic data is useful for controlled engineering and logic tests.

Use it to create exact cases such as:

- point-check touched by one tick;
- point-check missed by one tick;
- PAT2 exactly at 50%;
- PAT2 just above/below 50%;
- ambiguous 0/5 tie;
- target and invalidation on the same bar;
- missing candle;
- duplicate signal;
- several origins active simultaneously;
- an unseen state that should become PASS.

Synthetic data is especially valuable because it lets us control one variable at a time.

However:

> Synthetic data cannot prove that a trading relationship works in the real market.

It validates logic, invariants, boundary behavior, and failure handling.

Therefore:

`synthetic = engineering proof`

`real historical / forward data = market evidence`

Do not merge those two evidence classes.

---

## Current development priority

Before broad new source hunting:

1. use the existing 07:00 knowledge base;
2. freeze a narrow versioned 07:00 specification;
3. replay the real historical dataset already prepared;
4. inspect failures and unknown states;
5. create synthetic edge-case tests where exact logic needs controlled verification;
6. reopen YouTube/source research only for named gaps discovered by replay or specification work.

This prevents repeated source review and keeps research driven by actual unresolved questions.

---

## Non-negotiable project behavior

Every new session/agent working on the 07:00 project must know:

- this project is not a generic auto-trader;
- PASS is a first-class outcome;
- unknown states must be recorded, not guessed;
- all pre-07:00 information may feed the 07:00 state if legitimately knowable by then;
- historical failures are research inputs, not invitations to overfit;
- synthetic data is for controlled logic testing, not market-performance proof;
- versioned rules must be frozen before judging them;
- current authority must be read before reopening old research.

---

## Current authority links

Start with:

1. `docs/0700_WORKSTREAM_STATE.json`
2. `docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md`
3. `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`
4. `docs/SOURCE_COVERAGE_LEDGER.json`
5. `research_queue/QUEUE.json`

This document defines **why** the 07:00 system exists and how success is interpreted.

The workstream state defines **what is currently known and what is next**.


## Human-understandable UI / explainability requirement

The owner must not be required to trust hidden equations that only NEXUS understands.

A later 07:00 UI should expose, in understandable language and visual state:

- current timeframe/context;
- active origin/run;
- consumed and remaining run state;
- point-check status;
- Daily Frame/location;
- PA/PAT/SIG state and definitions;
- relevant wick/body/zone references;
- confirmation state;
- conflicting or unresolved evidence;
- final decision: ENTER / PASS / STUDY;
- plain-language reason for that decision;
- source links/timestamps where useful.

The UI is an explainability and inspection layer. It must display the evidence used by the engine and must not invent or override research logic.

This requirement exists because project success includes human auditability and shared understanding, not only correct hidden computation.
