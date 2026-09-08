# RQ-009 — Evidence Boundary Audit + Minimal Executable Scope

Date: 2026-09-09 Asia/Bangkok
Status: `AUDIT_CLOSED / MINIMAL_DETERMINISTIC_SIGNAL_RUN_V0_SELECTED`

## Decision question

After exhausting the current source batch for the major RQ-009 blockers, what is the smallest executable research scope that can be made deterministic **without inventing trading rules**, and is the project ready to prepare a genuinely untouched holdout for that scope?

## Executive decision

The first executable scope should **not** be a full trade system yet.

The smallest defensible version is:

```text
SIG_MODE2_EXTERNALLY_LABELED_SIGNAL_RUN_V0
```

This V0 measures a source-backed **signal/run lifecycle**, not trade Win/Loss.

It deliberately excludes any family whose autonomous setup detection, structural geometry, or execution mechanics still require unsourced choices.

Result:

```text
V0 SIGNAL/RUN REPLAY: READY TO IMPLEMENT
V0 FUTURE HOLDOUT PROTOCOL: READY TO DEFINE AFTER CODE/INPUT CONTRACT FREEZE
CANONICAL TRADE WIN/LOSS: NOT READY
SYSTEM WIN RATE: NOT ESTABLISHED
```

---

# 1. Evidence-boundary classification

The remaining project knowledge is divided into four operational classes.

## Class A — source-backed deterministic or deterministic engineering contract

These may be used directly when their documented preconditions are satisfied.

### A1. Time / no-lookahead / event knowledge

- Mae Pla preparation context: `07:00 Asia/Bangkok` where that family is used.
- Closed-candle knowledge boundaries must be respected.
- Every replay event stores `known_at`; future bars before `known_at` are prohibited.
- Same-bar target/stop ordering without tick data remains `AMBIGUOUS_SAME_BAR`.

### A2. PA direction/location semantics

- BUY PA/PAT is valid only at support.
- SELL PA/PAT is valid only at resistance.

Important boundary: the semantic is deterministic, but **autonomous support/resistance qualification geometry is not**. Therefore V0 may consume a pre-labeled valid-location event; it may not silently derive location from an unsourced distance tolerance.

### A3. Post-SIG Mode-2 state timing

For the reviewed source family:

```text
PA confirmed
-> post-SIG candle closes/confirms
-> wick becomes active point-check
-> earliest taught entry-family candle is the following candle
```

V0 uses only the **signal state / knowledge time** portion. It does not require a broker entry fill.

### A4. Active point-check destruction

Source-backed and broker-grid normalized:

```text
touch/contact of active point-check -> destroyed
one-tick near miss -> survives
```

For verified Bid OHLC data:

```text
literal contact := normalized Low <= point_check <= normalized High
```

No positive fuzzy tolerance is added.

### A5. Literal price-grid normalization

For runtime-verified symbol metadata:

- literal same price = same integer broker tick;
- off-grid values fail closed;
- broker-grid normalization is separate from structural zone tolerance and order execution.

### A6. Context hierarchy metadata

Source supports:

```text
Trend > Frame > SIG
HTF -> LTF analysis
```

V0 records this provenance/context but does not create a universal HTF veto rule.

### A7. Signal/run outcome protocol

The project already has deterministic research mechanics for:

- MFE;
- MAE;
- target touch;
- adverse/reference touch;
- first-hit ordering;
- `AMBIGUOUS_SAME_BAR`;
- no-lookahead `known_at`.

These are valid **signal/run research statistics**, not trade Win rate.

---

## Class B — explicit ambiguity that the engine can preserve safely

These do not need to be guessed. They may be represented as first-class states.

### B1. Body Collection multiple candidates

If more than one source-compatible candidate remains and no source-specific shown-form resolver applies:

```text
AMBIGUOUS_MULTI_CANDIDATE
```

Preserve all candidates. Do not choose newest/nearest/freshest/best-backtest.

### B2. Unresolved Body Collection reference selection

If a candidate cannot be resolved to the source-shown two-reference topology:

```text
UNRESOLVED_REFERENCE_SELECTION
```

### B3. Multi-timeframe / multi-family conflict

If several setup families remain valid and no explicit source route resolves them:

```text
MULTI_FAMILY_AMBIGUITY
```

Do not implement `higher timeframe always wins`.

### B4. Same-bar path ordering

When the same available OHLC bar contains both competing outcome boundaries:

```text
AMBIGUOUS_SAME_BAR
```

Do not force Win/Loss ordering without finer data.

### B5. Multiple independent SIG instances

Destroyed instance stops; other independently valid instances may survive. If source does not define priority among simultaneous surviving instances, preserve instance identity rather than selecting one from outcomes.

---

## Class C — source-incomplete family geometry; new evidence required

These must not be auto-filled from historical performance.

### C1. Autonomous PAT detector

Still source-incomplete:

- PAT2 exact >50% denominator;
- PAT3 exact combined-candle arithmetic;
- PAT1 numeric wick/body geometry;
- small-body / Doji / equal-wick tolerances where applicable.

Consequence:

```text
AUTONOMOUS_CANONICAL_PAT_DETECTION = NOT READY
```

### C2. Autonomous location / structural S/R qualification

Still open:

- exact PAT-to-support/resistance interaction geometry;
- generic structural zone tolerance;
- universal wick selection / S/R certification;
- cross-family location priority.

### C3. Body Collection universal geometry

Still source-incomplete:

- arbitrary cross-TF component permutations outside the shown topology;
- universal unseen two-reference resolver;
- same-TF/lower-TF candidate winner;
- exact cross-TF structural alignment tolerance;
- exact `TOUCHED/REVALIDATED -> COLLECTED/USED` OHLC transition;
- exact post-touch S/R revalidation.

### C4. Sideway autonomous detector and exit geometry

Still source-incomplete:

- exact frame start/end and bounds;
- BODY_PRIMARY vs BODY_CORE+WICK method routing;
- exact frame-complete predicate;
- exact valid breakout / false-break predicate;
- confirming-candle count;
- retest zone tolerance;
- cross-TF frame priority.

### C5. M1/M5 Brake autonomous quantitative gates

Still open:

- force threshold;
- weakening ratio;
- rejection wick threshold;
- standing tolerance / all-vs-majority logic;
- exact pivot window;
- universal zone-family geometry.

### C6. Exhaustive cross-frame conflict matrix

The contextual hierarchy is source-backed, but a universal deterministic matrix for all named timeframe/family conflicts is not present in the current batch.

### C7. Several Por Chon production details

Core cutoff/high-selection is source-backed, but exact bar inclusion/ties/standing geometry and universal reversal execution remain partial. Exclude Por Chon from V0.

---

## Class D — implementation convention requiring an explicit frozen research specification

These are not instructor facts. They may be chosen for a research implementation only if labeled clearly and frozen **before** outcome inspection.

### D1. Broker execution fill

Current source does not universally define:

- confirmation-close fill;
- next-open fill;
- first qualifying tick;
- exact Point #2 fill;
- fixed offset fill.

Any future trade replay must define `execution_fill_model` explicitly and must not call it the instructor's exact rule.

### D2. Bid/Ask, spread, slippage, commission and cost model

Bar-level Bid data does not itself provide full order execution. A trade-level model must state the assumed execution side/data source/cost treatment.

### D3. Research point / broker point conversion

Broker tick size and project/course point are separate concepts. Any conversion used in a specific research calculation must be explicit and versioned.

### D4. Runtime environment contract

Broker/server/symbol/digits/tick size/chart mode/data modality must be verified at runtime. Hardcoding one captured XAUUSDm environment as universal is prohibited.

---

# 2. Minimal executable scope selected

## V0 name

```text
SIG_MODE2_EXTERNALLY_LABELED_SIGNAL_RUN_V0
```

## Why Mode 2

Mode 2 is selected instead of Mode 1 because its decisive source state is known only after the post-SIG candle closes. This avoids silently inventing an intrabar Mode-1 trigger.

It is selected instead of M5 Brake / Body Collection / Sideway entry because those families still contain larger autonomous structural-geometry gaps.

## V0 is not an autonomous signal detector

Input events must be labeled **before outcome inspection** as source-compatible Mode-2 SIG instances.

Required input contract per event:

```text
signal_id
side = BUY | SELL
signal_tf = H1 | H4               # first implementation scope
pa_kind/source_label
pa_confirmed_at
location_label = VALID_SUPPORT | VALID_RESISTANCE
location_label_provenance
post_sig_closed_at
point_check_price
point_check_price_provenance
run_anchor_price
run_target_price OR frozen source-backed target-distance construction
parent_context_tf/context_tags
source_or_label_provenance
label_known_before_outcome = true
```

The event loader must fail closed if required provenance fields are absent.

## V0 allowed timeframes

Start with:

```text
H1
H4
```

because the project already preserves source-backed nominal run distances for these research layers and has validated resampled price data.

Do not add D1, Por Chon, Body Collection, Sideway entry, or M5 Brake merely to increase event count.

## V0 state path

```text
LABELED_MODE2_SIG
-> POST_SIG_CONFIRMED / POINT_CHECK_ACTIVE
-> RUN_ACTIVE
-> one of:
     RUN_TARGET_REACHED
     POINT_CHECK_DESTROYED
     AMBIGUOUS_SAME_BAR
     HORIZON_EXHAUSTED
```

If a source-defined replacement/new SIG is introduced in the input labels, it is a **new signal instance**. Do not silently re-anchor the old instance.

## V0 outcome measurements

Per event:

- target reached before destruction;
- point-check destroyed before target;
- same-bar ambiguity;
- neither within frozen horizon;
- MFE;
- MAE;
- time to target / destruction where observable;
- state/context tags.

Required public label for this result:

```text
SIGNAL/RUN OUTCOME
```

Prohibited labels:

```text
SYSTEM WIN RATE
TRADE WIN RATE
PROFITABILITY
EXPECTANCY
```

because V0 has no broker execution fill/cost model and is not an autonomous full setup detector.

---

# 3. What V0 deliberately excludes

```text
PAT auto-detection
support/resistance auto-detection
Sideway auto-detection
Body Collection candidate generation as an entry system
Mode 1 intrabar entry
M5 Brake entry
Por Chon entry
broker fill simulation
spread/slippage/commission P&L
trade position sizing
profit factor
drawdown
system Win/Loss claim
```

These exclusions are a strength: they keep V0 deterministic instead of broad but assumption-heavy.

---

# 4. Holdout decision

## Can a pristine holdout be prepared for V0?

Yes — **after the V0 input contract, replay code, and tests are frozen**.

The holdout should be future/untouched relative to the frozen implementation and must not reuse periods already inspected for prior discovery as a final confirmation period.

Required order:

```text
1. Freeze V0 specification.
2. Implement V0 replay and unit tests using synthetic / already-inspected development fixtures only.
3. Freeze event-labeling protocol and provenance schema.
4. Freeze the code/version hash.
5. Only then reserve/collect a genuinely untouched future price period + labels.
6. Labels must be created without viewing future outcome after each event's known_at.
7. Lock the holdout event manifest before outcome scoring.
8. Run once under the frozen decision rule.
```

Do not choose thresholds or revise labels after seeing holdout results.

## Holdout duration / event-count threshold

Not fixed by source.

Do not invent a minimum event count merely to produce a result. Statistical sufficiency should be declared in a separate protocol before the holdout is opened.

---

# 5. Transition from V0 to trade-level V1

A future trade representation may be opened only after V0 infrastructure is stable.

At minimum V1 must add, as explicit research conventions where source remains silent:

```text
execution_fill_model
Bid/Ask price source
spread/slippage/cost model
SL execution price rule
TP/exit execution rule
re-entry/replacement trade accounting
same-bar trade ordering policy or tick-data resolution
```

If setup detection is to become autonomous rather than externally labeled, PAT/location geometry must also be closed or an externally labeled truth-set must remain part of the production research contract.

V1 results must still be called a **Research Trade Representation** unless every claimed source/implementation boundary is stated correctly.

---

# 6. Decision table

| Area | Class | V0 handling |
| --- | --- | --- |
| Mode-2 post-SIG knowledge time | A | include |
| Point-check touch destruction | A | include |
| Broker literal tick equality/contact | A | include |
| No-lookahead / same-bar ambiguity | A | include |
| PAT exact denominator/arithmetic | C | exclude; event pre-label required |
| Exact support/resistance geometry | C | exclude; location pre-label required |
| Body Collection candidate winner | B/C | exclude from V0; preserve ambiguity elsewhere |
| Sideway exact geometry | C | exclude |
| M5 Brake quantitative gates | C | exclude |
| Cross-family winner | B/C | reject/flag ambiguous input rather than choose |
| Exact broker fill | D | not needed for V0 signal/run layer |
| Spread/slippage/cost | D | not needed for V0 signal/run layer |
| Future holdout | methodology | prepare only after V0 freeze |

---

# 7. Devil's advocate

V0 can still fail to answer the larger business question.

Reasons:

1. externally labeled events can create labeling bias;
2. signal/run success may not translate into executable trade profitability;
3. point-check destruction may occur after a hypothetical trade would already have been stopped for another source-family reason;
4. H1/H4-only scope may not represent all system states;
5. future market regime may differ from historical development periods;
6. label scarcity may make the first untouched holdout statistically insufficient.

Therefore a favorable V0 result must **not** be interpreted as proof that the full trading system works.

---

# 8. Thesis breakers / conditions that block V0

Do not score an event if:

- setup/location label was created after seeing the outcome;
- point-check level cannot be traced to a pre-outcome source/labeled event;
- runtime price-grid metadata is unverified for the dataset contract;
- competing valid family conflict is unresolved and would materially change the event interpretation;
- target construction is not frozen before outcome;
- same-bar target/destruction ordering is unresolved and no finer data exists;
- source/provenance identity is missing.

Such events are `EXCLUDED_OR_AMBIGUOUS`, not wins or losses.

---

# 9. Final audit conclusion

The project no longer needs to wait for every source gap before making executable progress.

The correct decomposition is:

```text
FULL AUTONOMOUS TRADING SYSTEM
    -> still not ready

MINIMAL SOURCE-BACKED SIGNAL/RUN REPLAY
    -> ready to implement under externally labeled setup/location inputs

TRADE WIN/LOSS
    -> later layer requiring frozen execution/cost conventions

SYSTEM WIN RATE
    -> still not claimable
```

This closes the RQ-009 evidence-boundary audit and selects the next engineering checkpoint: implement the V0 event manifest/schema + deterministic Mode-2 signal/run replay using existing no-lookahead outcome infrastructure, without opening a holdout yet.
