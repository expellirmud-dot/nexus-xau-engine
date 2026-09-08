# RQ-009 — Body Collection Candidate Priority Source Exhaustion

Status: `SEARCH_HIERARCHY_CLOSED / UNIVERSAL_BODY_COLLECTION_WINNER_SOURCE_INCOMPLETE_CURRENT_BATCH`

Date: 2026-09-09 Asia/Bangkok

## Question

When more than one source-compatible Body Collection candidate remains, does the current source batch define one universal winner rule for:

- same-timeframe complete candidates;
- multiple lower-timeframe completion candidates;
- multiple valid component/reference prices that could produce the two forecast references?

The project must answer this without selecting a winner from historical Win/Loss outcomes.

## Sources reviewed

Primary Body Collection source:

- `oCcG3dUjrgw` — EP.5 Body Collection, rendered transcript + prior synchronized visuals.

Cross-check sources:

- `UV5NijhjfJ8` — EP.4 M5 brake / S/R use of ซอกไส้คู่.
- `16KoS7d-koI` — EP.6 M1/M5 entry / S/R candidate discussion.

Prior checkpoints:

- `docs/RQ009_EP5_BODY_COLLECTION_CANDIDATE_SEARCH_ORDER_CLOSURE_2026-09-09.md`
- `docs/RQ009_EP5_TWO_REFERENCE_METHOD_RATIONALE_2026-09-09.md`
- `docs/RQ009_EP5_CROSS_TF_ALIGNMENT_REFERENCE_SELECTION_SHOWN_FORM_2026-09-09.md`
- `docs/RQ009_BODY_COLLECTION_VS_SR_PARTIAL_COMPONENT_RECONCILIATION_2026-09-09.md`

Local targeted scan artifact remains gitignored:

- `youtube/_evidence/rq009_candidate_priority_scan_2026-09-09.txt`

No outcome data was used.

## What is already deterministic from source

### Search hierarchy

EP.5 repeatedly closes the following search order:

```text
1. Search the setup/reference timeframe first.
2. Begin with roughly 2-4 prior candles.
3. If structure is not found, continue farther back.
4. If the setup timeframe cannot complete the required structure,
   step down one timeframe sequentially.
5. For the primary taught chain:
   H4 -> H1 -> M30
```

This is deterministic **search authority**, not candidate ranking.

### One source-shown cross-TF completion topology

The reviewed source+visual example closes:

```text
parent/reference TF:
    ซอก + ไส้ -> two existing reference levels

lower TF:
    คู่ aligns with an existing parent reference
    -> completes full structure
    -> no third forecast line
```

This explains one repeated setup family but does not establish a universal reducer/winner for unseen component permutations.

## Targeted candidate-priority scan

A targeted scan was performed for language such as:

- choose first / look at this set first;
- nearest first;
- first candidate;
- forecast reference 1/2;
- 2-4 candles;
- fall back one timeframe;
- incomplete three components;
- combine/assist from lower timeframe.

### EP.5 result

EP.5 contains the contextual phrase around `1:05:57`:

```text
มองชุดนี้ก่อน
```

The surrounding sequence is a worked chart explanation. It tells the learner which demonstrated set the instructor is discussing first, but it does not state a general algorithm such as:

```text
always choose newest
always choose nearest
always choose first chronological set
always choose freshest
```

No Body Collection-specific universal `เลือกที่ใกล้ที่สุดก่อน` rule was found in the reviewed EP.5 material.

### EP.6 nearest-first result

EP.6 around `1:10:53-1:11:29` and `1:14:38-1:15:32` explicitly allows nearby alternative `ซอก/คู่` choices and says, in that reviewed context:

```text
เลือกที่ใกล้ที่สุดก่อน
```

The surrounding lesson is support/resistance-zone construction and comparison. The source also says nearby alternatives may both be acceptable and discusses overlapping Day/H4 S/R as stronger.

Therefore this evidence supports:

```text
S/R_SELECTION_CONTEXT:
    nearest-first guidance exists
```

It does **not** establish:

```text
BODY_COLLECTION_MULTI_CANDIDATE_WINNER = nearest
```

because EP.4/EP.6 explicitly distinguish S/R use of `ซอกไส้คู่` from the Body Collection workflow.

## Current-batch negative result

Across the reviewed EP.5/EP.4/EP.6 material, no universal Body Collection-specific rule was found that says, when multiple valid candidates coexist, always select:

- newest;
- oldest;
- nearest to current price;
- farthest;
- freshest / untouched;
- narrowest zone;
- strongest-looking body;
- highest-timeframe overlap;
- nearest S/R;
- lowest/highest numeric reference;
- first one discovered by code;
- best historical performer.

Likewise, the current source batch does not define a universal rule for choosing among multiple lower-TF components that could complete the same parent candidate.

## Two-reference selection remains family-specific

The source intentionally uses two forecast references and one repeated shown topology explains how those two references can already exist before the lower-TF pair completes the structure.

For unseen configurations, the current batch still does not define one universal mapping from:

```text
multiple valid structural/component references
-> exactly two forecast references
```

Therefore no `min/max`, average, nearest/farthest, newest/oldest, or generic 3->2 arithmetic transform may be introduced.

## Safe engine behavior

For source-compatible research candidates:

```text
1. Apply the source-backed timeframe/search hierarchy.
2. Preserve component and timeframe provenance.
3. Preserve lifecycle state as an attribute, not a ranking theorem.
4. Enumerate all candidates that remain valid under the frozen source representation.
5. If exactly one candidate remains -> deterministic candidate available.
6. If multiple candidates remain and no source-specific shown-form resolver applies:
       status = AMBIGUOUS_MULTI_CANDIDATE
       preserve all candidates
       do not emit a canonical winner.
7. If multiple component/reference prices cannot be resolved to the taught two-reference topology:
       status = UNRESOLVED_REFERENCE_SELECTION
```

A downstream research experiment may compare pre-frozen alternative ranking policies, but performance must not promote one policy into the canonical instructor rule.

## Important distinction

```text
SEARCH ORDER != WINNER RANKING
S/R NEAREST-FIRST != BODY COLLECTION NEAREST-FIRST
FRESHNESS ATTRIBUTE != FRESHEST-ALWAYS-WINS
SHOWN EXAMPLE ORDER != UNIVERSAL PRIORITY
```

This distinction is now durable project knowledge.

## Decision

```text
BODY_COLLECTION_SEARCH_HIERARCHY:
  SOURCE BACKED / CLOSED

SAME-TF MULTI-CANDIDATE UNIVERSAL WINNER:
  SOURCE INCOMPLETE IN CURRENT BATCH

LOWER-TF MULTI-COMPLETION UNIVERSAL WINNER:
  SOURCE INCOMPLETE IN CURRENT BATCH

UNSEEN TWO-REFERENCE UNIVERSAL REDUCER:
  SOURCE INCOMPLETE IN CURRENT BATCH

EP6 S/R NEAREST-FIRST:
  SOURCE BACKED ONLY IN REVIEWED S/R CONTEXT
  NOT TRANSFERABLE AS UNIVERSAL BODY COLLECTION PRIORITY
```

## Reopen only if

- a new primary Body Collection source explicitly teaches candidate priority;
- direct instructor/project-owner clarification defines the winner rule;
- a new visual/source family explicitly resolves an unseen multi-candidate case;
- a source/timestamp mapping error is found.

Historical outcomes are not a reopen trigger.

## Next decision-critical step

The largest remaining project blocker is no longer a hidden candidate-priority assumption: ambiguity can be represented explicitly. Next, audit **cross-frame/setup-family priority** to determine whether the source defines which active timeframe/setup family has authority when several valid structures coexist. If not, close that as an explicit multi-family ambiguity before deciding whether the system is ready for frozen research representations and holdout design.
