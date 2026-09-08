# RQ-009 — Cross-Frame / Setup-Family Priority Source Boundary

Status: `CONTEXT_HIERARCHY_SOURCE_BACKED / UNIVERSAL_CONFLICT_RESOLVER_SOURCE_INCOMPLETE_CURRENT_BATCH`

Date: 2026-09-09 Asia/Bangkok

## Question

When several timeframe states or setup families coexist, does the current source batch define enough authority/routing to decide every conflict deterministically?

Examples of the unresolved class include:

```text
H4 directional context vs H1 opposite PA/SIG
higher-TF Sideway vs lower-TF SIG
Frame condition vs apparently valid SIG
Trend direction vs countertrend lower-TF setup
multiple active setup families at once
```

The goal is to separate a source-backed **context hierarchy** from an analyst-created universal veto table.

## Sources reviewed

Primary current-batch sources:

- `ESHDuiVPJow` — EP.2 `Trend ชนะ Frame, Frame ชนะ SIG`.
- `vcdN51_OrPE` — system-summary graph lifecycle and multi-timeframe traversal.
- `UV5NijhjfJ8` — M5 Brake context.
- `16KoS7d-koI` — lower-timeframe entry context.
- `1E_PYPor1qQ` — PA/SIG confirmation and same-timeframe structure context.

Prior readiness reference:

- `docs/RQ008_FULL_SYSTEM_PROOF_READINESS_CLOSURE_2026-09-08.md`

Local targeted scan artifact remains gitignored:

- `youtube/_evidence/rq009_cross_frame_priority_scan_2026-09-09.txt`

No outcomes were used to choose a hierarchy.

## 1. Source explicitly teaches an importance hierarchy

EP.2 repeatedly states:

```text
Trend ชนะ Frame
Frame ชนะ SIG
```

and explains that SIG is the last layer in the sequence of travel/context importance.

Around the early lesson, the instructor explicitly says learners should order importance rather than focus on SIG alone.

Safe semantic hierarchy:

```text
TREND CONTEXT
    > FRAME / SUPPORT-RESISTANCE CONTEXT
        > SIG / PA TRIGGER CONTEXT
```

This is a conceptual/context authority ordering, not yet a complete Boolean conflict table.

## 2. Multi-timeframe analysis is top-down

The system-summary source says timeframe review should proceed:

```text
large timeframe -> smaller timeframe
```

EP.2 independently says larger-timeframe trend is stronger/easier to interpret and teaches using H1+ for trend, with H4 emphasized as a major trading timeframe.

Additional source examples say that when a lower timeframe appears noisy or misleading, a larger timeframe can continue to drive price.

Safe source rule:

```text
HTF context must be known before interpreting LTF trigger/state.
```

This does not imply `HTF always cancels LTF`.

## 3. Higher timeframe can explain apparent lower-timeframe contradiction

Current-batch examples explicitly show:

- a lower-timeframe PA/SIG can appear to fail because a larger timeframe continues to push price;
- when H4's own run is exhausted, the source says current movement may be carried by Day/Week;
- important S/R is checked using larger timeframes where relevant;
- lower-timeframe M5 braking may not hold against an H4/Day impulse if the relevant strong higher-timeframe S/R has not been reached.

Therefore:

```text
LTF_TRIGGER must not be interpreted in isolation from active HTF cycle/frame/trend.
```

## 4. But higher-timeframe state is not a universal veto

A critical EP.2 Q&A asks whether, while **Day is Sideway**, H1/H4 SIG can still be traded.

The instructor answers that H1/H4 SIG can be followed because the Day Sideway range is large enough for lower-timeframe runs, while still emphasizing that the larger-timeframe trend should be considered as the primary context.

This directly rejects an oversimplified rule such as:

```text
IF HTF_SIDEWAY:
    reject all LTF SIG
```

Likewise, the source's lifecycle teaching allows smaller timeframes to complete full runs inside a larger-timeframe Sideway/pullback structure.

Safe representation:

```text
HTF state constrains/interprets LTF opportunity;
HTF state does not automatically invalidate every LTF setup.
```

## 5. Frame can override apparent SIG meaning

The system-summary source contains direct examples where a PA/SIG is present but its post-SIG structure is damaged and the move is described as occurring under the **frame condition**, including the explicit phrase in substance:

```text
กรอบชนะซิ
```

This is consistent with EP.2's hierarchy.

Safe state interpretation:

```text
if source-defined SIG validity is broken and frame remains active,
classify movement under frame context rather than forcing the damaged SIG to remain the driver.
```

This does not define all possible simultaneous valid-SIG versus valid-frame conflicts.

## 6. Trend context is primary but not an autonomous entry signal

EP.2 teaches trading with the trend and warns against repeatedly fighting a strong trend, especially on larger timeframes.

However, the system still requires frames/zones and PA/SIG/entry-family conditions for actual entry.

Therefore:

```text
TREND = context/authority layer
not
TREND = standalone exact entry trigger
```

The engine must not create entries solely because trend has top conceptual priority.

## 7. Safe cross-frame state model

The current source supports this evaluation order:

```text
1. Establish larger-timeframe trend/cycle context.
2. Establish relevant frame / S/R / Sideway context.
3. Evaluate PA/SIG and its lifecycle validity in that context.
4. Evaluate the specific entry family (SIG Entry, Frame Brake, Body Collection, Sideway route, etc.).
5. If the source explicitly routes a state (e.g. damaged SIG -> frame context), follow that route.
6. If several still-valid setup families conflict and no source-specific route resolves them,
   preserve MULTI_FAMILY_AMBIGUITY rather than inventing a veto/winner.
```

## 8. What is NOT established as a universal rule

The current batch does not establish a complete deterministic table such as:

```text
H4 BUY + H1 SELL -> always BUY
H4 SELL + M5 BUY -> always reject M5 BUY
Day SIDEWAY + H4 SIG -> always accept
Week UP + Day SELL -> always reject Day SELL
SIG_ENTRY and FRAME_BRAKE valid together -> always choose family X
BODY_COLLECTION and SIDEWAY route valid together -> always choose family Y
```

Some examples support contextual decisions, but not a universal exhaustive matrix.

The source also does not provide one numeric score for timeframe strength or a universal weighting formula.

## 9. Engine permission

Safe now:

- evaluate timeframe context top-down;
- preserve `trend > frame > SIG` as source-backed contextual hierarchy;
- allow explicit source-defined routing, including frame context replacing a damaged SIG interpretation;
- allow lower-timeframe runs inside a higher-timeframe Sideway where the source family permits it;
- attach `parent_context_tf`, `frame_tf`, `trigger_tf`, and `entry_family` provenance to every candidate;
- emit `MULTI_FAMILY_AMBIGUITY` when simultaneous valid families remain unresolved.

Not safe:

- generic higher-TF veto of all lower-TF opposite signals;
- hidden timeframe score;
- nearest/highest-TF winner selected from backtest performance;
- collapsing all entry families into one universal trade object before family-specific rules are frozen.

## 10. Decision

```text
TREND > FRAME > SIG CONTEXT HIERARCHY:
  SOURCE BACKED

TOP-DOWN HTF -> LTF ANALYSIS:
  SOURCE BACKED

HTF CONTEXT CAN EXPLAIN / CONSTRAIN LTF:
  SOURCE BACKED

HTF ALWAYS VETOES OPPOSITE LTF:
  NOT SOURCE BACKED

DAY SIDEWAY CAN CONTAIN TRADEABLE H1/H4 RUNS:
  SOURCE BACKED IN REVIEWED CONTEXT

UNIVERSAL MULTI-TF / MULTI-FAMILY CONFLICT MATRIX:
  SOURCE INCOMPLETE IN CURRENT BATCH
```

## 11. Reopen only if

- a primary source explicitly supplies conflict-routing rules for named timeframe/family combinations;
- direct instructor/project-owner clarification defines a deterministic priority matrix;
- a new setup-family source establishes its relation to the existing hierarchy;
- source/timestamp mapping is corrected.

Historical performance is not a valid way to choose the missing priority matrix.

## 12. Research consequence

With this checkpoint, another hidden assumption can be removed from the future replay engine: it does not need to pretend every simultaneous valid setup has one canonical winner.

The system can now preserve source-backed hierarchy and explicit ambiguity separately.

The remaining blockers to canonical full-system Win/Loss are primarily:

- unresolved PAT exact denominator/arithmetic where required for autonomous detection;
- exact structural-zone/frame geometry for families that remain source-incomplete;
- explicit family-specific execution/cost models rather than source-claimed fill;
- deciding which source-incomplete families are excluded from the first frozen executable system version;
- reserving a genuinely pristine holdout only after that executable version is frozen.
