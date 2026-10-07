# Nexus-XAU-Engine — Project Review + Master To-Do / Trigger Map — 2026-10-07

Status: HUMAN-READABLE REVIEW CHECKPOINT / NAVIGATION + ANTI-FORGETTING / DOES NOT REPLACE CANONICAL CLAIM AUTHORITY

Reviewed against machine state at `2026-10-07T23:17:30+07:00`.

Machine state at review:

- repository: `main@c0fd68696780f7444b50dcdbdc6b45cf4ed64894`;
- working tree: clean;
- `main == origin/main`;
- project workstream: `0700_METHOD_COMPLETION`;
- current version: `0700_MINIMAL_V2.0`;
- latest prior progress checkpoint: `docs/PHASE1_REMAINING_DEPENDENCY_ACTIONABILITY_AUDIT_2026-09-17.md`;
- current OPEN dependency count: 12;
- current `ACTIONABLE_NOW`: 0;
- real Exness V2 remains `DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED`;
- protected holdout scoring, economic scoring, and automatic order sending remain disabled.

This document exists so a new session can understand the Project from first principles without restarting old research. Where this review conflicts with Current State, canonical claims, readiness, or a later checkpoint, the later machine authority wins.

## 1. What the Project is actually trying to build

Phase 1 is a bounded XAU decision process around the project-confirmed `07:00 Asia/Bangkok = 00:00 UTC` checkpoint.

It is not a generic 24/7 auto-trader and is not required to trade every day.

The intended process is:

`collect all legitimately knowable pre-07:00 evidence -> reconstruct deterministic state -> classify known/conflicting/unknown conditions -> PASS when evidence is insufficient -> allow a candidate only when the required state is supported`.

`PASS / NO TRADE / STUDY` is a first-class correct output.

Success means process correctness, traceability, reproducibility, safe handling of unknowns, and evidence-driven versioning. It does not mean forcing a market entry or manufacturing a target Win Rate.
## 2. How the Project evolved

### Phase A — reconstruct the teaching/source relationships

The Project first extracted and reconciled the source material instead of jumping directly to an EA.

Current source-backed or source-closed pieces include:

- 07:00 checkpoint normalized to Asia/Bangkok / 00:00 UTC;
- H1 primary run reference = 1,000 project points;
- H4 primary/full run reference = 1,500 project points, with continuation references toward 3,000;
- D1/Day run family has evidence around 5,000–10,000 project points, but the exact stage/set transition is not closed;
- PAT2 uses the midpoint of the **previous full candle range including wick**: `(high + low) / 2`; strict directional close beyond midpoint is required and equality fails;
- literal point-check contact destroys that origin/reference; a near miss survives;
- Daily Frame uses completed H4 context, a nearby statistical/minor `0/5` reference, then `+/-500` project points;
- S/R is contextual/zone-based rather than one universal dead price; reviewed strong-zone family uses H4-first then H1 fallback;
- M5 Entry #2 / retest topology is source/visual backed at signal level, while exact broker fill remains outside source closure.

Important exclusions were preserved instead of guessed: PAT3 combined arithmetic, universal D1 stage selection, universal exact Daily Frame snap/tolerance, universal Sideway routing, a universal conflict winner, and exact execution mechanics.

### Phase B — historical relationship research

The Project then used historical 07:00 datasets to ask which state relationships survive across periods.

Historical V1 work found that `PATH_REMAINING` was a better research target representation than blindly starting a fresh full target from confirmation.

A strong positive raw association was also observed between H4 consumed/run-progress and target-first ordering. Some small empirical bins looked extremely strong and could easily create a false impression of a near-100% rule.

Later geometry-null control changed the interpretation: the primary consumed residual was non-positive in both Discovery and Replication after controlling target/point-check geometry.

Current authority is therefore:

`H4 consumed association = explained or dominated by geometry under the current representation`.

Consumed remains useful state information, but it is **not established as an independent predictive signal** and no consumed threshold is authorized.

### Phase C — freeze a narrow deterministic representation

`0700_MINIMAL_V2.0` was frozen before new V2 outcomes were inspected.

V2 deliberately narrowed the problem to:

- H4 origins only;
- H4 nominal run = 1,500 project points;
- PAT2 FULL-RANGE detector;
- literal M1 point-check semantics;
- M5-only post-07:00 PAT2 confirmation lane for this research version;
- remaining-run representation instead of a fresh 1,500 from confirmation;
- explicit PASS states for ambiguity, unresolved source geometry, conflicts, destroyed origins, completed runs, bad data, and unknown states.

This preserved a clean distinction between `research candidate` and `action eligibility`.
### Phase D — real data and replay engineering

The Project then separated market-data acquisition from research logic and execution.

Implemented data/replay capabilities now include:

- validated MT5 OHLC/timeframe reconstruction for the current broker/runtime dataset;
- restart-safe MT5 tick collector with checkpoint/status/gap/provenance surfaces;
- Exness-branded tick archive acquisition and validation across the available 2015–2026 range;
- known-gap ledger and fail-closed archive-window adapter;
- deterministic archive Bid-tick -> M1 reconstruction;
- Archive -> frozen V2 integration;
- restart-safe V2 origin-state carry with digest/provenance/version checks, exact detector bridge, no fabricated handoff bars, and explicit seed-completeness semantics.

These engineering layers are useful even though canonical multi-year real V2 scoring is still blocked at the initial prehistory state.

### Phase E — solve the prehistory/origin-seed problem instead of hiding it

The earliest proven Exness archive tick is `2015-08-10T00:00:00Z`.

Because H4 origins have no fixed expiry and point-check destruction requires literal observed contact, an active origin created before the archive boundary can theoretically survive into the observed period.

The Project tested two tempting shortcuts and rejected both:

1. **Dukascopy -> Exness exact state transfer:** frozen overlap V0.2 showed PAT/origin/state divergence in all three preselected overlap windows. Silent exact relabeling is `NOT_SUPPORTED`.
2. **Finite Exness warmup until old origins disappear:** mathematically falsified. For any finite observed path, valid hypothetical BUY/SELL prehistory anchors can be constructed outside finite observed extrema and remain ACTIVE under literal-contact/no-expiry semantics.

Further audit found no proven same-source Exness history before 2015-08-10 and no independently justified finite historical XAUUSDm price/anchor domain.

Therefore current canonical initial origin state is a **STRUCTURAL UNKNOWN / BLOCKING** dependency.

More post-2015 calculation does not solve this in principle. The blocker reopens only with genuinely new evidence or a separately authorized lifecycle semantic change.

### Phase F — governance, explainability, and execution boundary

The Project then hardened how unknowns and operational state are represented:

- every unresolved readiness dependency now has an epistemic class plus an orthogonal blocking axis;
- generic `UNKNOWN` is rejected by preflight;
- the pilot operations scaffold can expose version identity, readiness blockers, unknown classifications, feed/data health, deterministic reasons, and reference-only rollback identity;
- working-tree/Git/state identity mismatches fail closed;
- current MT5 commission/fee/swap schema observability is implemented without converting current observations into historical cost assumptions.

Current runtime cost evidence confirms commission/fee/swap fields are observable and current swap metadata is readable, but there were zero XAUUSDm deal-cost samples in the bounded account-history probe and exact historical cost schedules remain unresolved.
## 3. How the current Phase 1 engine works conceptually

### Step 1 — establish trustworthy input and time

- normalize the 07:00 checkpoint to 00:00 UTC;
- preserve broker/feed/source identity;
- reject known gaps/provenance mismatches rather than fill them;
- reconstruct only information legitimately knowable by the checkpoint.

Effect: bad chronology, source drift, or missing history must become data-quality/unknown state rather than silently changing the market state.

### Step 2 — reconstruct H4 PAT2 origins

PAT2 FULL-RANGE is detected from completed H4 candles.

BUY requires prior bearish + current bullish + current close strictly above the prior full-range midpoint.

SELL requires prior bullish + current bearish + current close strictly below the prior full-range midpoint.

The adjacent post-SIG H4 candle supplies the research anchor:

- BUY anchor = adjacent post-SIG low;
- SELL anchor = adjacent post-SIG high.

Effect: PAT geometry determines which origins exist, their anchor prices, and therefore all later run/point-check geometry.

### Step 3 — determine whether each H4 origin survives to 07:00

An origin is eligible only if it is known by the cutoff, its 1,500-point nominal H4 run has not already completed, literal M1 range contact has not already touched its anchor, and the required input history is valid.

Consumed progress is the maximum favorable excursion from the anchor. It is continuous state metadata; there is no consumed threshold.

Effect: the system carries the unfinished inherited run rather than pretending every 07:00 opportunity starts from zero.

### Step 4 — build Daily Frame/context

The current research representation uses completed H4 context + nearby 0/5 statistical/minor reference + `+/-500` project points.

Exact universal PAT-to-frame qualification geometry is not source-closed. Therefore coarse location can be recorded for research, but automated action must fail closed when exact source-compatible location qualification is unknown.

Effect: Daily Frame can organize/contextualize the research state without being promoted into an unsupported trading filter.

### Step 5 — wait for post-07:00 M5 PAT2 confirmation

V2.0 uses the first narrow research lane: M5 PAT2 FULL-RANGE, same side as the H4 origin, known after 07:00 and before the next 07:00.

Recent multi-timeframe alignment may be recorded as metadata; there is no MTF-count gate.

Effect: confirmation is time-causal and does not leak after-the-fact information into the 07:00 state.

### Step 6 — recheck the inherited origin immediately before confirmation

If the point-check was touched first, the origin is dead.

If the H4 nominal run completed first, the origin is finished.

No later M5 signal may revive either state.

Effect: signal detection cannot overwrite lifecycle truth.

### Step 7 — calculate remaining-run research target

`remaining = 1500 - consumed_at_confirmation`.

The research target uses confirmation close +/- remaining points according to side.

This is a research convention, not a broker-fill claim.

Effect: the target represents participation in the unfinished inherited run rather than resetting a fresh full H4 run from entry.

### Step 8 — preserve multiple origins and conflicts

Each surviving H4 origin remains separate in research.

There is no source-closed universal origin winner. Opposite-direction origin context is not a proven automatic veto.

If multiple origins create materially conflicting actionable states and no resolver exists, action lane returns `PASS_CONFLICT_UNRESOLVED`.

Effect: the engine does not cherry-pick whichever historical origin produced the best outcome.

### Step 9 — explicit terminal taxonomy

Days/rows can end as research candidates or explicit PASS/record states such as no origin, completed run, destroyed point-check, frame tie, no confirmation, unresolved source geometry, conflict, data-quality failure, or unknown state.

Effect: the system can safely know that it does **not** know enough.
## 4. What we currently know, what it affects, and how we handle it

| Topic | Current authority/state | What it affects | Current handling |
|---|---|---|---|
| 07:00 time | `07:00 Asia/Bangkok = 00:00 UTC` | cutoff, no-lookahead, daily state | canonical for Phase 1 replay |
| H1 run | source-backed 1,000 project points | historical/source context | not used as V2 origin timeframe |
| H4 run | source-backed primary/full 1,500 project points | lifecycle, consumed, remaining target | canonical V2 run representation |
| H4 continuation | references toward 3,000 exist | broader run context | not promoted into a universal V2 stage rule |
| D1/Day run | source-backed family around 5,000–10,000 | higher-timeframe context | exact stage transition/07:00 stage selection remains open; excluded from Minimal V2 |
| PAT2 midpoint | previous full candle range including wick | PAT detection -> origin/confirmation set | source-closed; equality fails |
| PAT3 | combined-candle arithmetic unresolved | broader signal families | excluded from PAT2-only V2 |
| Point-check | literal M1 range contact destroys; near miss survives | origin lifecycle | canonical frozen lifecycle semantics |
| Daily Frame | completed H4 context + nearby 0/5 reference +/-500 | contextual location | coarse research metadata allowed; exact action qualification fails closed when unknown |
| S/R | zone/structure, not one dead price | context/location | reviewed strong-zone family H4-first/H1-fallback; no universal numeric tolerance |
| M5 confirmation | PAT2 FULL-RANGE research lane | post-07 confirmation | M5-only in V2.0 by project scope, not universal instructor rule |
| Multiple origins | no universal winner | target/action conflict | retain separately for research; PASS action on unresolved material conflict |
| Opposite origin | not supported as automatic veto | context/conflict | metadata only unless a real actionable conflict exists |
| PATH_REMAINING | historically ranked ahead of absolute origin target under frozen V1 proxy | target representation | V2 uses remaining inherited run; not proof of profitability |
| H4 consumed | raw association replicated historically but geometry-null residual non-positive | state interpretation | keep as state metadata; no threshold and no independent-signal claim |
| Synthetic fixtures | good for exact logic/invariant falsification | engineering correctness | allowed; never market-performance evidence |
| Real historical/forward data | needed for actual market-state/relationship evidence | robustness/replication | freeze representation first, then replay separated periods |
| Dukascopy vs Exness | structural PAT/origin divergence observed on all three frozen V0.2 windows | prehistory seed/feed equivalence | never silently relabel Dukascopy state as Exness state |
| Exness prehistory | same-source proven history does not predate 2015-08-10; no finite anchor domain | canonical initial H4 origin state | structural blocker; real V2 remains unseeded |
| Finite forward warmup | mathematically cannot close unbounded unknown prehistory under current lifecycle | seed completeness | do not spend more compute on arbitrary warmup |
| Archive continuity | deterministic gap/window guards implemented | later canonical replay eligibility | evaluate per interval only after seed blocker closes |
| Current MT5 cost metadata | current swap fields + deal commission/fee/swap schema observable | future execution economics | preserve current-runtime provenance; do not extrapolate backward |
| Historical execution costs | exact historical commission/fee/swap schedule unknown | P&L/expectancy/profitability | blocking until new evidence or a separately justified economic claim boundary |
| Fill/slippage | market ticks alone do not reveal actual fills | economic proof | requires supervised execution evidence / new historical evidence |
| Trade stop geometry | chart point-check is not automatically a trade SL | realized P&L | requires source-backed or owner-direct convention before outcome scoring |
| Position sizing/risk cap | policy not defined by source research | supervised pilot safety | requires explicit frozen convention |
| Holdout | tooling/activation lock implemented, outcomes unopened | strong final confirmation | keep pristine until authorized trigger |
| Explainability/operations | reason/audit, health, version identity, rollback scaffold implemented | supervised operations | non-executing, fail-closed, order/holdout/economic scoring disabled |

## 5. What the historical tests taught us

`0700_MINIMAL_V2.0` Discovery used 150 07:00 days and produced 67 research-candidate days / 84 candidate rows. Replication used 60 days and produced 33 research-candidate days / 42 candidate rows.

Those runs are useful for state/relationship falsification, but they are not trade counts and not a system Win Rate.

The key lesson from RQ-015 is methodological: a variable may correlate strongly with outcome ordering and still fail to provide independent information once the geometry that mechanically determines both target and point-check distances is controlled.

Therefore future research must keep asking not only `A correlates with outcome?` but also `is A independent of the geometry/conditioning variables that generate both A and outcome?`.
## 6. MASTER TO-DO / TRIGGER LIST — DO NOT DROP ANY ITEM

Current machine registry has **12 OPEN dependencies** and **0 ACTIONABLE_NOW** under existing evidence/authorization.

### A. Waiting for genuinely new evidence

1. `U-P1-08-ORIGIN-SEED-REOPEN` — `STRUCTURAL_UNKNOWN / BLOCKING`
   - Need: evidence sufficient to close pre-2015 Exness origin-state completeness.
   - Valid trigger: verified same-source Exness history before 2015-08-10; or a defensible finite historical anchor domain; or an authorized source-backed lifecycle semantic change.
   - When triggered: rerun seed-completeness proof from the new premise, then only if COMPLETE evidence exists unlock canonical archive replay.
   - Do not: rerun arbitrary finite warmup or silently import Dukascopy state.

2. `U-P1-10-CROSS-SERVER-FEED-EQUIVALENCE` — `IRREDUCIBLE_OR_NOT_YET_REDUCIBLE / BLOCKING`
   - Need: exact enough broker/server/feed identity for execution-quality claims.
   - Valid trigger: direct broker/server identity evidence or same-feed historical execution-quality route.
   - When triggered: freeze a comparison/equivalence contract before inspecting outcomes.
   - Do not: assume archive, Dukascopy, Demo server, or a later runtime are exactly interchangeable.

3. `U-P1-10-HISTORICAL-COST-SCHEDULE` — `IRREDUCIBLE_OR_NOT_YET_REDUCIBLE / BLOCKING`
   - Need: historical account/broker commission, fee, and financing schedule sufficient for replayed economic P&L.
   - Valid trigger: verified historical schedules covering intended replay intervals, or a separately justified economic-claim boundary that does not require exact schedule reconstruction.
   - When triggered: preserve server/account/time provenance and freeze cost treatment before economic scoring.
   - Do not: project current Trial17 swap values or empty XAU deal samples backward through history.

### B. Waiting for explicit owner policy and/or supervised execution authorization

4. `U-P1-10-FILL-SLIPPAGE` — `IRREDUCIBLE_OR_NOT_YET_REDUCIBLE / BLOCKING`
   - Need: actual fill/slippage evidence sufficient for economic claims.
   - Trigger: separately authorized supervised execution protocol plus relevant evidence.
   - When triggered: freeze acquisition/protocol first, then collect actual deals/fills.
   - Do not: infer broker fill from chart touch or historical Bid ticks.

5. `U-P1-10-STOP-GEOMETRY` — `STRUCTURAL_UNKNOWN / BLOCKING`
   - Need: trade-level stop/invalidation geometry.
   - Trigger: source-backed stop rule or explicit owner-direct convention frozen before outcome scoring.
   - When triggered: create a new trade-construction version and test it separately.
   - Do not: silently equate chart point-check with actual SL.

6. `U-P1-11-POSITION-SIZING` — `STRUCTURAL_UNKNOWN / BLOCKING`
   - Need: frozen position-sizing convention.
   - Trigger: owner-direct or separately justified risk-sizing policy.
   - When triggered: freeze units/account-risk mapping before supervised pilot use.
   - Do not: optimize sizing from historical profitability.

7. `U-P1-11-RISK-CAP` — `STRUCTURAL_UNKNOWN / BLOCKING`
   - Need: explicit risk cap.
   - Trigger: owner-direct risk-limit convention.
   - When triggered: freeze account/session/trade limits before pilot execution.
   - Do not: infer acceptable risk from past winning samples.

8. `U-P1-13-TRADE-RISK-CONVENTIONS` — `STRUCTURAL_UNKNOWN / REQUIRED_LATER`
   - Need: integrated trade/risk conventions for any execution phase.
   - Trigger: execution separately authorized and sizing/risk/stop conventions available.
   - When triggered: bind the conventions into the supervised-pilot version and audit layer.
   - Do not: enable automatic order sending merely because research logic is stable.

### C. Waiting for future runtime observation

9. `U-P1-12-PRISTINE-CONFIRMATION` — `RUNTIME_OBSERVABLE / REQUIRED_LATER`
   - Need: authorized pristine/future confirmation under the frozen version.
   - Trigger: holdout activation conditions + explicit authorization are satisfied.
   - When triggered: reveal/score only under the frozen protocol and immutable version identity.
   - Do not: open outcomes just because calendar time has passed.

10. `U-P1-10-XAU-DEAL-COST-SAMPLES` — `RUNTIME_OBSERVABLE / REQUIRED_LATER`
   - Need: actual current/future XAUUSDm commission/fee/swap deal samples.
   - Trigger: naturally occurring authorized XAUUSDm deals or separately authorized supervised deals.
   - When triggered: use the existing read-only cost probe and preserve current source identity.
   - Do not: interpret zero samples as zero cost.

### D. Downstream only — do not run early

11. `U-P1-08-CANONICAL-WINDOW-CONTINUITY` — `RUNTIME_OBSERVABLE / REQUIRED_LATER`
   - Need: gap/continuity eligibility for each canonical replay interval.
   - Trigger: origin-seed blocker first closes and a canonical interval is selected.
   - When triggered: run existing archive manifest/gap/window guards per interval.
   - Do not: spend compute validating downstream replay windows while canonical initialization remains impossible.

12. `U-P1-13-FINAL-DECISION-VERSION` — `DERIVABLE / REQUIRED_LATER`
   - Need: final frozen version identity for pilot.
   - Trigger: upstream decision-critical blockers close.
   - When triggered: derive/freeze version from governed project state before pilot activation.
   - Do not: choose the final version by looking at protected holdout outcomes.
## 7. Closed routes / DO NOT REPEAT without a new trigger

- Do not restart broad YouTube/source review before checking current closures and source coverage.
- Do not reopen PAT2 midpoint discovery; FULL prior candle range including wick is source-closed for PAT2.
- Do not rewrite historical Q1–Q4 BODY-proxy results as if they used FULL-RANGE PAT2.
- Do not convert the old high-consumed empirical bins into a production threshold or near-100% system claim.
- Do not treat H4 consumed as an independent predictor under current authority; geometry-null control closed that interpretation.
- Do not use legacy Daily Frame side-support results from pre-reanchor origin selection as current confirmation.
- Do not impose a universal MTF-count gate or opposite-origin veto; current evidence does not support either.
- Do not choose a winning H4 origin from historical outcomes when multiple origins coexist.
- Do not concatenate/relabel Dukascopy and Exness state as one feed.
- Do not attempt to obtain COMPLETE seed by longer finite post-2015 warmup.
- Do not fabricate missing ticks/M1 bars or treat one successful day/month as continuity proof.
- Do not infer historical commission/fee/swap from current runtime values.
- Do not infer broker fills/slippage from chart/tick contact.
- Do not open protected holdout outcomes before activation authorization.
- Do not enable automatic order sending under the current Phase 1 state.

## 8. Operational rules that protect the research

Before substantive work in a new/reconnected session:

`D:\tools\NEXUS-START\RESUME_WORK.cmd --project xau`

Then verify repository/Git, Current State, latest checkpoint, unknown registry, actionability matrix, and durable jobs before starting anything new.

Use existing tools/modules before creating replacements.

For any long/multi-year/expensive run, use durable machine-side execution and inspect persisted receipts before retrying.

Freeze decision representation/rules before opening the outcomes they will be judged on.

After each coherent checkpoint: update state, validate structured files, run relevant tests/preflight/Ruff/`git diff --check`, commit, push, and verify clean sync.

Destructive Git/history/evidence actions require explicit permission.

## 9. How to resume when a trigger arrives

1. Run project resume and confirm machine state.
2. Identify exactly which OPEN dependency the new trigger satisfies.
3. Read that registry entry, actionability entry, and its evidence refs.
4. Decide whether the trigger closes a premise or merely adds another observation.
5. Freeze a new contract/representation before inspecting decision-relevant outcomes.
6. Implement the narrowest change that addresses the named dependency.
7. Falsify with synthetic/controlled tests where appropriate.
8. Use real data only for the market/economic claim that real data can actually support.
9. Preserve superseded history and explain why authority changed.
10. Reclassify the residual unknown instead of pretending the whole dependency disappeared.

## 10. Current bottom line

The Project is no longer missing a basic research architecture.

It already has:

- a bounded Phase 1 objective;
- source/provenance governance;
- a frozen deterministic H4/PAT2/M5 research engine;
- discovery/replication history;
- geometry-null falsification discipline;
- real MT5/archive data acquisition and replay plumbing;
- restart-safe state carry;
- explicit structural prehistory blocker proof;
- machine-enforced unknown classification;
- explainable/fail-closed pilot operations scaffolding;
- current-runtime cost observability;
- a trigger-based remaining-dependency map.

What prevents stronger claims now is not lack of calculation effort. The remaining barriers are specific missing premises: prehistory completeness, exact feed/execution equivalence, historical economics, fill/slippage, trade stop/risk policy, future/pristine confirmation, and downstream final-version readiness.

Until one of those premises receives a real trigger, the correct Project state is to preserve evidence, avoid reopening closed routes, and wait rather than manufacture certainty.