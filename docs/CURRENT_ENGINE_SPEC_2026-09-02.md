# NEXUS XAU Engine — Current Implementation Spec

Snapshot date: 2026-09-02

Purpose: this document is the implementation handoff for the Python replay/backtest/live-assistant engine. It consolidates the latest project evidence into one source-of-truth snapshot so implementation does not depend on chat memory.

This file does **not** erase or replace the underlying evidence files. When a rule is disputed, inspect the cited source documents and preserve the conflict rather than guessing.

---

## 0. Status vocabulary

Every rule in the engine should carry one of these statuses:

- `CONFIRMED` — direct user evidence, primary slide, or primary transcript is strong enough to implement the stated behavior.
- `PARAMETERIZED` — topology/workflow is supported, but one or more numeric thresholds/tolerances remain unresolved. Code the shell and expose the unknowns as configuration.
- `HUMAN_CONFIRM` — engine may identify a candidate, but should not autonomously promote it to a final trade decision without human review.
- `NOT_IMPLEMENTED` — evidence is insufficient for a reliable detector/decision rule.

Do not convert `PARAMETERIZED`, `HUMAN_CONFIRM`, or `NOT_IMPLEMENTED` into invented numeric rules.

---

## 1. Evidence precedence

Use evidence in this order:

1. User-direct project evidence.
2. Primary teaching screenshots/slides.
3. User-supplied full timestamp transcripts.
4. Attributable public instructor material.
5. Third-party summaries.
6. Analyst inference.

A newer stronger source supersedes a weaker older shorthand, but the older record must remain preserved in Git history/evidence files.

Primary implementation references for this snapshot:

- `docs/DIRECT_PAT_GEOMETRY_RULES_2026-09-01.md`
- `docs/PAT3_PRIMARY_VISUAL_CROSSCHECK_2026-09-01.md`
- `docs/PA_PAT_TRANSCRIPT_FORENSICS_2026-09-01.md`
- `docs/M5_BRAKE_TRANSCRIPT_FORENSICS_2026-09-01.md`
- `docs/transcripts/EP5_BODY_COLLECTION_FULL_ANALYSIS.md`
- `docs/RULEBOOK.md`
- `docs/OPEN_GAPS.md`
- `docs/EVIDENCE_REGISTER.md`
- `docs/READINESS_SCORECARD.md`

Important: `RULEBOOK.md` and `OPEN_GAPS.md` contain some statements that predate later PAT/M5 evidence. This snapshot resolves only the items explicitly updated by stronger later evidence.

---

## 2. Scope and architecture

Target instrument: `XAUUSD`.

Target execution environment discussed: MT5 / Exness.

The system is currently a **research-first human-in-the-loop assistant**, not a live autonomous EA.

### Backtest / research path

```text
Historical XAUUSD data (CSV / M1 Bid+Ask / tick where available)
→ Python Data Source Adapter
→ Timeframe Builder
→ Rule/State Engine
→ Replay / Backtest
→ Local logs/reports
→ optional Supabase result publication
```

### Live-assistant path

```text
MT5 / Exness live market data
→ Python Engine
→ Signal / Engine Event / Reason Log
→ Supabase
→ Vercel/PWA dashboard
→ Human reads signal
→ Human places order in MT5 mobile/desktop
```

Supabase is **not** the market-data source. Vercel is **not** the trading brain. Python is the source of trading decisions.

---

## 3. Market-data rules

### 3.1 Closed-candle rule — CONFIRMED

Trading-pattern classification must use closed candles on the working timeframe. Do not confirm PAT/SIG from an unfinished candle.

### 3.2 Live data

Preferred live source: the same/near-same broker feed as execution, ideally MT5/Exness, to minimize M1/M5 price-feed mismatch.

Suggested adapter interface:

```text
MT5LiveSource
CSVSource
DukascopySource
DatabaseSource
```

The rule engine must consume a normalized OHLC/tick contract independent of the source.

### 3.3 Historical backtest status

As of this snapshot, **no full historical strategy backtest has been run yet**. There is no verified project win rate.

Any percentages mentioned in instructor teaching are heuristics/anecdotes unless the project itself measures them on historical data.

---

## 4. Broker metadata / points

Known demo specification recorded by the project:

- Digits: 2
- Tick size: 0.01
- Contract size: 100
- Tick value shown: 0.1
- Bid chart mode

In that specific demo environment:

```text
1 point = 0.01 price
500 points = 5.00 price
1,000 points = 10.00 price
```

Status: `PARAMETERIZED` by broker runtime metadata.

Do not hard-code this conversion as universal. Query/verify symbol metadata at runtime.

---

## 5. Core lifecycle

High-level cycle supported across project evidence:

```text
SIG → TP/RUN → RETRACE/REST → SIDEWAY → next SIG
```

An equivalent teaching view starts at Sideway:

```text
SIDEWAY → SIG → TP → RETRACE/REST → SIDEWAY
```

Exact Sideway start/completion/exit transitions remain incomplete.

Status:

- lifecycle state objects: `CONFIRMED`
- exact full transition detector: `PARAMETERIZED / NOT_IMPLEMENTED`

---

## 6. PA / PAT taxonomy

### 6.1 Family map — CONFIRMED

The five visual forms are:

```text
PAT1
PAT2
PAT3 variant 1
PAT3 variant 2
PAT3 variant 3
```

Do not model them as PAT1–PAT5.

`PAT` denotes candle count:

- PAT1 = 1 candle
- PAT2 = 2 candles
- PAT3 = 3 candles

Pattern windows may overlap. A three-candle region can be PAT3 while its last two candles can also form PAT2.

Implementation consequence: pattern labels must be many-to-many over candle windows, not exclusive.

---

## 7. Hard PA location qualification

Latest user-direct rule:

```text
BUY PA/PAT = valid only at support
SELL PA/PAT = valid only at resistance
```

Status: `CONFIRMED`.

```pseudo
valid_pa_buy  = shape_match_buy  and at_support
valid_pa_sell = shape_match_sell and at_resistance
```

A correct-looking pattern at the wrong location must be rejected as PA.

### Important separation

M1/M5 frame-brake/counter-retrace entries can occur in prepared TP-complete/frame contexts. That is a separate entry family and does **not** redefine the PAT location rule above.

### Still unresolved

`at_support` / `at_resistance` exact numeric tolerance is unknown.

Status of location tolerance: `PARAMETERIZED`.

---

## 8. PAT1

### Confirmed topology

- one candle
- long wick/rejection appearance
- small body
- BUY at support only
- SELL at resistance only
- transcript indicates PAT1 color can vary; same-direction color may be preferred, but opposite color is not automatically invalid

### Unknown numeric geometry

- minimum directional wick/body ratio
- maximum body fraction of candle range
- exact support/resistance touch tolerance
- quantitative preference by candle color

Implementation status: `PARAMETERIZED / HUMAN_CONFIRM`.

Candidate feature shell:

```pseudo
pat1_candidate(c):
    small_body_feature(c)
    long_rejection_wick_feature(c)
    closed(c)
    location_filter(direction)
```

Do not select numeric wick/body thresholds without evidence-tagged configuration.

---

## 9. PAT2

### BUY — latest user-direct geometry

```text
C1 red/bearish
C2 green/bullish
C2 closes more than 50% of C1
location = support only
```

Candidate:

```pseudo
c1.bearish
c2.bullish
c2.close > midpoint_reference(c1)
at_support
closed(c2)
```

### SELL

```text
C1 green/bullish
C2 red/bearish
C2 closes more than 50% of C1 in sell direction
location = resistance only
```

Candidate:

```pseudo
c1.bullish
c2.bearish
c2.close < midpoint_reference(c1)
at_resistance
closed(c2)
```

### Transcript correction / unresolved measurement basis

The primary transcript says candle #2 closes around the 50% level of candle #1 and does not require full engulfing. User-direct evidence strengthens the directional relation to `>50%`, but the exact denominator/reference is still unresolved:

- real body midpoint?
- full High–Low midpoint?
- another Fibonacci/chart construction?

Also unresolved: equality/tolerance around 50%.

Implementation status: topology/location `CONFIRMED`; midpoint denominator/tolerance `PARAMETERIZED`.

Required config concept:

```text
pat_midpoint_basis = BODY | FULL_RANGE | UNKNOWN
pat_midpoint_tolerance_points = UNKNOWN
```

Until resolved, run alternative parameterizations in research mode and label the variant used.

---

## 10. PAT3

### BUY — latest user-direct geometry

```text
C1 red
C2 red or green
C2 small body
C3 green
C3 closes >50% of BOTH C1 and C2
location = support only
```

Candidate:

```pseudo
c1.bearish
c2.color in {bullish, bearish}
small_body(c2)
c3.bullish
c3.close > midpoint_reference(c1)
c3.close > midpoint_reference(c2)
at_support
closed(c3)
```

### SELL

```text
C1 green
C2 green or red
C2 small body
C2 upper/lower wicks approximately equal
C3 red
C3 closes >50% of BOTH C1 and C2 in sell direction
location = resistance only
```

Candidate:

```pseudo
c1.bullish
c2.color in {bullish, bearish}
small_body(c2)
approx_equal_wicks(c2)
c3.bearish
c3.close < midpoint_reference(c1)
c3.close < midpoint_reference(c2)
at_resistance
closed(c3)
```

Do not mirror the equal-wick requirement from SELL to BUY unless another direct source confirms it.

Primary PAT3 slide evidence confirms the three BUY and three SELL visual variants/topology/location, but does not independently define the numeric >50% denominator.

### Remaining numeric gaps

- 50% denominator/reference
- equality/tolerance around 50%
- exact `small_body(c2)` threshold
- exact equal-wick tolerance on SELL
- variant-specific wick details if any

Implementation status: topology/location `CONFIRMED`; numeric geometry `PARAMETERIZED / HUMAN_CONFIRM`.

---

## 11. Post-SIG reference / run anchor

### Mapping — CONFIRMED by primary transcript

```text
PAT1 → post-SIG reference candle #2
PAT2 → post-SIG reference candle #3
PAT3 → post-SIG reference candle #4
```

If the reference candle has no relevant wick:

```text
BUY → use Low
SELL → use High
```

The post-SIG reference is the run-count anchor and can also be used as a structural/SL reference in demonstrated setups.

### Post-SIG validity — CONFIRMED concept

A post-SIG reference that disturbs/exceeds the PA or relevant frame invalidates the setup. The engine must support re-evaluation/replacement, not just a permanent boolean signal.

State shell:

```text
CANDIDATE_PA
→ CANDIDATE_SIG
→ VALID_POST_SIG
or
→ INVALIDATED_BY_POST_SIG
→ SIDEWAY / REEVALUATE
→ NEW_PA / NEW_SIG
```

A ~200-point destruction example exists but is example-specific. Do not universalize 200 points.

Implementation status: state model `CONFIRMED`; exact destruction tolerance `PARAMETERIZED`.

---

## 12. SIG timeframes and run distances

Primary trading SIG timeframes confirmed by relative/project evidence:

```text
H1
H4
D1
W1
```

PA can occur on every timeframe. Course terminology uses SIG from H1 upward.

Recorded run distances:

```text
H1    1,000 points
H4    1,500 points first/full round; references toward 3,000
D1    5,000–10,000 points
W1    15,000–30,000 points
MN    30,000–50,000 points in broader lesson/run material
```

PAT family does not change same-timeframe TP/run distance.

Implementation status: run-distance configuration `CONFIRMED`, broker point conversion `PARAMETERIZED`.

---

## 13. M1/M5 Brake entry model

### 13.1 Same abstract concept — CONFIRMED

M1 and M5 use the same abstract brake/entry sequence. M1 is finer/noisier; M5 is safer in the teaching.

### 13.2 Zone first — CONFIRMED

A prepared zone/frame must exist before searching for the brake pattern.

```pseudo
if not zone_active:
    reject brake_setup
if price_reaches(zone):
    enable brake_search
```

Exact zone construction can still be unresolved by setup family.

### 13.3 Five logical force stages — CONFIRMED

```text
ใหญ่ยาว / LARGE_FORCE
→ อ่อนแรง / WEAKENING
→ Reject / REJECTION
→ เปลี่ยนสี / COLOR_SHIFT
→ Retest / RETEST
```

These stages are logical features; multiple stages may occur in the same candle.

Do not require one candle per stage.

### 13.4 Entry phase separation — CONFIRMED

```text
ENTRY_1_SCOUT = first brake/reaction, higher-risk, optional
ENTRY_2_RETEST = preferred confirmation entry
```

Do not make Entry 1 mandatory.

### 13.5 Structural retest — CONFIRMED concept

A full retest is stronger than merely standing on a line.

BUY concept:

```text
first brake
→ move up / away
→ interact with resistance / opposite structure
→ return to switched support
→ retest candidate
```

SELL mirrors this.

### 13.6 Frame standing — PARTIAL / PARAMETERIZED

Transcript supports:

- start counting from first candle touching frame
- observe roughly 4–10 closed candles on M1/M5
- bodies standing/holding on the proper side are primary evidence
- wick on line may contribute

Unknown:

- exact point tolerance around frame
- all candles vs majority/sequence
- straddle handling
- whether 10 is hard max vs observation guideline

### 13.7 Structure confirmation — CONFIRMED concept

BUY features:

- higher low / raised low
- reclaim/break local high or prior short-term down structure

SELL features:

- lower high
- lose support / break local low

Exact pivot-window parameters remain unresolved.

### 13.8 Overlap / false first brake

First brake can fail/overlap/sweep. Teaching mentions ~300 points as ordinary example and ~500 in high volatility. These are not universal thresholds.

Status: event/state `CONFIRMED`; numeric threshold `PARAMETERIZED`.

### 13.9 Frame-brake entry vs SIG entry

Keep separate accounting:

```text
FRAME_BRAKE_ENTRY != SIG_ENTRY
```

Frame-brake entry:

- no native SIG run anchor at entry
- manage by nearby frame/practical target in the lesson
- can later hold if a SIG develops

SIG entry:

- use post-SIG anchor
- use timeframe run table

This separation is mandatory for backtest reporting.

---

## 14. Body collection (`เก็บบอดี้`)

Workflow supported by primary transcript:

```text
WAIT_H4_PA
→ FIND_REFERENCE_ZONE
→ WAIT_ZONE_TOUCH
→ WAIT_SMALL_TF_PA
→ WAIT_FRAME_BRAKE/CONFIRM
→ ENTRY_CANDIDATE
→ ZONE_CONSUMED
```

Supported details:

- H4-focused setup family
- historical left-side candle structures
- `ซอก + ไส้ + คู่`
- H4 search first; H1 fallback; M30 can appear in fallback examples
- roughly 2–4 historical candles in discussed search window
- all three `ซอก + ไส้ + คู่` stronger than two
- nearest relevant zone can be prioritized among nearby candidates
- lower-TF M1/M5 PA alignment used at zone; M5 taught as safer
- used/completed zones are retired; untouched zones may persist
- do not blindly apply normal body-collection setup inside Sideway

Still unresolved:

- exact `ซอก` OHLC formula
- exact `คู่` geometry
- equality/tolerance
- exact zone boundaries
- exact TOUCH/COLLECTED/RETIRED events
- exact invalidation
- whether lower-TF PA is mandatory in every variant

Implementation status:

- workflow/state schema: `CONFIRMED`
- exact detector geometry: `NOT_IMPLEMENTED / HUMAN_CONFIRM`

---

## 15. Half retrace (`พักครึ่ง`)

Directly supported concept:

- qualifying timeframe has over-run its normal run
- opposite PA drives pullback
- measure from driver post-SIG anchor to furthest extreme
- midpoint is arithmetic 50%

```text
half_level = (sig_anchor + extreme_price) / 2
```

50% is a reference; price does not have to touch it exactly.

Still unresolved:

- exact opposite-PA qualifier used for classification
- when extreme freezes
- dynamic recomputation behavior
- entry trigger
- invalidation
- setup-specific SL/TP

Implementation status:

- midpoint calculator: `CONFIRMED`
- setup detector/entry: `PARAMETERIZED / HUMAN_CONFIRM`

---

## 16. Swing retrace (`พักสวิง`)

Supported distinction:

- over-run present
- no opposite PA driving the pullback
- upward example measures from wick of qualifying green candle to highest wick, then midpoint

Working distinction:

```text
HALF_RETRACE  = post-SIG anchor + opposite PA present
SWING_RETRACE = qualifying candle anchor + opposite PA absent
```

Still unresolved:

- exact qualifying start candle when several candidates exist
- exact extreme freeze/update behavior
- entry and invalidation

Implementation status:

- midpoint utility once anchors supplied: `CONFIRMED`
- anchor selection/setup detector: `NOT_IMPLEMENTED / HUMAN_CONFIRM`

---

## 17. Fibonacci

Direct evidence supports 61.8 as a level the teacher may watch contextually.

Do not encode 61.8 as a mandatory universal entry.

50% arithmetic midpoint is directly verified in the retrace example.

Status: contextual levels `PARAMETERIZED`.

---

## 18. Daily / Mae Pla frame

Known project evidence:

- preparation around 07:00 Thai-time context
- inspect completed Day/H4/H1
- H4 wick ends used for major frame references
- daily frame concept uses upper/lower/minor S/R
- references to statistical prices ending in 0 or 5
- +/-500-point subframe concept
- H4/H1 wick contact examples around 7–14 points

Still unresolved:

- exact 0/5 snap/tie/rounding formula
- exact timezone/server-time normalization
- deterministic priority among candidate wick contacts

Implementation status: `HUMAN_CONFIRM / NOT_IMPLEMENTED` for final automatic frame construction.

---

## 19. Por Chon ATH frame

Known direct project rules:

- require roughly 1,000-point run from previous ATH condition before a new frame is eligible
- use H4 highest price/High in the stated 19:00–19:00 interval associated with the new ATH
- if required conditions are not met, do not create a new frame
- once created, frame persists
- acts as important S/R/navigation reference
- compare proximity/confluence with Mae Pla frame

Still unresolved:

- exact timezone meaning of 19:00–19:00
- boundary inclusivity
- tie handling
- replacement/retirement details

Implementation status: `PARAMETERIZED / HUMAN_CONFIRM`.

Earlier 12:00 UTC claims are quarantined unless stronger evidence revives them.

---

## 20. Sideway

Confirmed concepts:

- separate setup family / state
- post-SIG destruction can transition interpretation to Sideway
- SIGs inside Sideway do not necessarily have full normal run space
- duration is not fixed
- repeated/equal lows/highs appear in examples
- M5 lesson combines frame/zone interactions, brake behavior, standing, PA, and structure
- limited repeated frame entries are discussed in examples

Still unresolved major blocker:

- exact upper/lower frame construction
- exact `กรอบ SW ครบ` completion event
- exact breakout/false-break rule
- exact exit/new-SIG transition
- point tolerances

Implementation status:

- Sideway state/event shell: `CONFIRMED`
- canonical detector: `NOT_IMPLEMENTED / HUMAN_CONFIRM`

Do not import generic textbook `2–3 swing` formulas as system facts.

---

## 21. Multi-timeframe relationship

Supported:

- larger timeframe context is stronger
- H4 is repeatedly emphasized for planning
- H1 relation matters with H4
- M1/M5 used for entry refinement/brake
- M15/M30 appear as relationship/confirmation in project teaching

Still missing complete deterministic conflict matrix:

```text
H1 Buy vs H4 Sell
H4 vs D1
D1 vs W1
small-TF opposite PA: normal retrace vs thesis break
```

Implementation status: feature/context storage `CONFIRMED`; automatic conflict resolver `NOT_IMPLEMENTED / HUMAN_CONFIRM`.

---

## 22. Risk / SL / TP

### Confirmed/usable

- post-SIG anchor drives SIG run measurement
- post-SIG wick can be SL reference in demonstrated contexts
- frame-based and M1/M5 lessons contain SL examples

### Context-specific examples only

Teaching mentions values such as 50–150, 200–300, 300 points and breakeven adjustments after certain moves. None is proven universal.

Do not build one universal SL engine from these examples.

Implementation status:

- measurement/logging fields: `CONFIRMED`
- universal risk engine: `NOT_IMPLEMENTED`

---

## 23. Research/backtest implementation boundary

### Safe to build now

```text
broker metadata + point conversion
normalized OHLC/tick data model
M1 → M5/M15/M30/H1/H4/D/W aggregation
closed-bar replay loop
PAT candidate windows with overlapping labels
PAT direct color/topology features
parameterized 50% midpoint feature
hard BUY-support / SELL-resistance qualification shell
post-SIG mapping PAT1#2 / PAT2#3 / PAT3#4
no-wick fallback
post-SIG invalidation/replacement state
SIG run-distance calculator
M1/M5 shared brake feature-state model
ENTRY_1_SCOUT vs ENTRY_2_RETEST
retest structure shell
4–10 frame-standing observation shell
higher-low/lower-high/local-break features
body-collection workflow state shell
half midpoint calculator
swing midpoint calculator when anchors supplied
Daily/ATH candidate state objects
Sideway state shell
TAKE / WAIT / REJECT / NEED_HUMAN_CONFIRM decisions
versioned event logging
local replay report
separate FRAME_BRAKE vs SIG_ENTRY accounting
```

### Not safe to finalize autonomously

```text
exact PAT1 numeric detector
exact PAT2/PAT3 midpoint denominator/tolerances
exact PAT3 small-body/equal-wick thresholds
exact support/resistance location tolerance
final body-collection geometry detector
final Sideway detector
exact M5 force thresholds
universal risk/SL logic
full multi-TF conflict resolver
full Mae Pla/Por Chon automatic frame engine
live autonomous MT5 execution
```

---

## 24. Required parameter registry

The engine should explicitly expose unresolved values instead of burying them in code.

Minimum registry:

```text
pat1.min_wick_to_body_ratio = UNKNOWN
pat1.max_body_fraction = UNKNOWN
pat.midpoint_basis = UNKNOWN   # BODY | FULL_RANGE | future verified method
pat.midpoint_tolerance_points = UNKNOWN
pat3.small_body_threshold = UNKNOWN
pat3.sell_equal_wick_tolerance = UNKNOWN
location.support_resistance_tolerance_points = UNKNOWN
m5.large_force_threshold = UNKNOWN
m5.weakening_ratio = UNKNOWN
m5.rejection_wick_threshold = UNKNOWN
m5.frame_standing_tolerance_points = UNKNOWN
m5.frame_standing_min_count = 4      # source-backed observation lower bound
m5.frame_standing_max_count = 10     # source-backed observation upper bound; not assumed hard max
sideway.* = UNKNOWN
body_collection.*_geometry = UNKNOWN
daily_frame.snap_rule = UNKNOWN
por_chon.timezone_boundary = UNKNOWN
risk.universal_sl = NOT_DEFINED
```

Every backtest report must record the parameter set and `rule_version` used.

---

## 25. Replay event schema requirements

Every detector decision should be reproducible.

Minimum event payload:

```text
timestamp
symbol
timeframe
OHLC window / candle ids
market data source
broker/server/timezone metadata
active frame/zone ids
PAT labels matched
location qualification
post-SIG reference
SIG state
M5 brake features
structure features
decision = TAKE | WAIT | REJECT | NEED_HUMAN_CONFIRM
reason codes
parameters used
rule_version
engine_version
```

Log rejected candidates too. Do not log only winners/accepted trades.

---

## 26. Ground-truth / validation requirement

The project still needs a labeled truth set for validation.

Target: at least 20–50 labeled positive/negative examples across important cases, including:

- PAT1/2/3 BUY and SELL
- correct shape / wrong location
- valid and disturbed post-SIG
- overlapping PAT labels
- M5 first-brake false vs second/retest valid
- body-collection valid/invalid zones
- Sideway valid/false exits
- setups that must be skipped

Each case should ideally record:

```text
time/date
broker/server/timezone
symbol
TF
OHLC/screenshot
teacher/relative label
reason
frame/zone relation
expected detector label
outcome (for validation only, not for defining the label)
```

---

## 27. Backtest protocol

No project win rate is valid until this protocol starts producing measured results.

Recommended research workflow:

```text
1. Validate parser/timeframe aggregation on small known files.
2. Replay manually labeled truth-set cases.
3. Compare detector output vs labels.
4. Run historical candidate extraction.
5. Separate setup families in reporting.
6. Record parameter/rule version.
7. Use multiple historical periods/market regimes.
8. Preserve a holdout/out-of-sample period not used to tune rules.
9. Only after detector validity is acceptable, measure trading outcomes.
```

Do not use a tiny hand-selected sample to advertise a system win rate.

---

## 28. Current product modes

### Mode A — Research Replay

```text
Historical data → Python → local report
```

Can run without Supabase or Vercel.

### Mode B — Human-in-the-loop Live Assistant

```text
Live MT5 data → Python → Supabase → Vercel/PWA → human → MT5 order
```

Appropriate before autonomous execution if unresolved rules are surfaced as `NEED_HUMAN_CONFIRM`.

### Mode C — Autonomous execution

Not approved by this snapshot. Requires successful detector validation, historical/out-of-sample testing, demo validation, and closure/containment of rule gaps.

---

## 29. Explicit non-claims

This snapshot does **not** claim:

- any verified project win rate
- any guaranteed profitability
- universal 300-point SL
- universal 300-point overlap threshold
- universal 61.8 entry
- exact PAT midpoint denominator
- exact Sideway construction
- fully deterministic production EA readiness

If a report, UI, or code comment states otherwise, treat it as a bug unless a newer evidence document explicitly supports the claim.

---

## 30. Implementation handoff rule

For Python development, this file is the current top-level implementation snapshot as of 2026-09-02.

When new evidence arrives:

1. preserve the old evidence and this snapshot in Git history;
2. add/modify a dedicated evidence file first;
3. compare the new rule with this snapshot;
4. quarantine conflicts explicitly;
5. update the implementation spec only when the evidence justifies it;
6. increment `rule_version` for behavior-changing rule updates;
7. never silently substitute analyst assumptions for missing rules.
