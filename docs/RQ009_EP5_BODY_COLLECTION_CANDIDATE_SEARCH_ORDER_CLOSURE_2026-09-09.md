# RQ-009 — EP.5 Body Collection Candidate Search-Order Closure

Status: `SOURCE_BACKED_SEARCH_HIERARCHY / SAME_TF_MULTI_CANDIDATE_PRIORITY_OPEN`

Date: 2026-09-09 Asia/Bangkok

## Objective

Close only the search-order semantics that the EP.5 source actually teaches when looking for `ซอก + ไส้ + คู่`. Do not invent a winner-selection rule for cases where multiple valid candidate clusters exist on the same timeframe.

## Source

Primary source:

- YouTube Video ID: `oCcG3dUjrgw`
- Lesson: `EP.5 วิชาเก็บบอดี้ #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว`
- Rendered YouTube Show transcript with timestamps
- Playable visual source reviewed in the preceding EP.5 checkpoints

Relevant source anchors:

- `40:58-41:51` — same-timeframe structure first; if not found, reduce one timeframe
- `43:06-43:39` — initially inspect approximately 2-4 prior candles; H4 can fall back to H1
- `1:01:43-1:02:53` — worked example: H4 structure unavailable, inspect H1; a component can be resolved from M30 in the shown example
- `1:05:49-1:06:12` — instructor explicitly says “มองชุดนี้ก่อน” in a worked comparison, but this is contextual example selection, not a general ranking theorem
- `1:19:13-1:19:37` — explicit fallback chain H4 -> H1 -> M30 and “2-4 candles; if not found, look farther back”

## Source-backed closure

### 1. Same timeframe has first search authority

The source repeatedly teaches that Body Collection should first be constructed from `ซอก + ไส้ + คู่` in the same timeframe as the setup being planned.

Safe search rule:

```text
SEARCH CURRENT SETUP TF FIRST
```

For the lesson’s primary H4 use case:

```text
H4 setup -> search H4 first
```

This is source semantics, not an analyst optimization.

### 2. Timeframe fallback is sequential, not arbitrary

When the three required conditions cannot be completed in the current timeframe, the source explicitly allows stepping down one timeframe.

The strongest explicit Q&A gives:

```text
H4 incomplete -> inspect H1
H1 incomplete -> inspect M30
```

Therefore a source-faithful search routine must not mix all timeframes into one undifferentiated candidate pool and then choose whichever later backtests best.

### 3. Approximately 2-4 prior candles is an initial search window, not a hard expiry

The source says to look back roughly 2-4 historical candles first.

Later Q&A explicitly states that if the structure is still not found, continue looking farther back.

Safe interpretation:

```text
INITIAL_LOOKBACK ~= 2-4 prior candles
IF NOT FOUND -> continue farther into history
```

Therefore:

- 2-4 candles is not a hard maximum age;
- an older candidate is not automatically invalid merely because it is older than four candles;
- no age threshold should be selected from outcomes.

### 4. Candidate search should preserve source components, not collapse to one nearest price

The source method searches for the structural components `ซอก + ไส้ + คู่`, then uses the resulting historical price references to construct forecast areas.

A faithful detector should therefore return structured candidate records rather than only one numeric level.

Recommended research representation:

```text
candidate = {
  timeframe,
  source_candles,
  sok_reference,
  sai_reference,
  khu_reference,
  support_or_resistance_context,
  fresh_or_touched_state,
  source_timestamp/provenance
}
```

This representation does not yet assert that every candidate can be detected automatically; exact universal geometry remains partially open.

## What the source does NOT yet close

### Same-timeframe multi-candidate ranking remains unresolved

The reviewed source does not provide a universal rule for a case such as:

```text
H4 candidate A valid
H4 candidate B valid
H4 candidate C valid
```

It does not clearly establish that the engine must always choose:

- newest candidate;
- oldest candidate;
- nearest-to-current-price candidate;
- freshest/untouched candidate;
- narrowest zone;
- strongest pair/body relation;
- nearest support/resistance;
- or any performance-ranked candidate.

The phrase “มองชุดนี้ก่อน” in a worked example demonstrates an instructor-selected example context but is not enough to promote one universal ranking algorithm.

Current status:

```text
SAME_TF_SEARCH_ORDER = SOURCE_BACKED
SAME_TF_MULTI_CANDIDATE_WINNER_RULE = UNKNOWN
```

## Interaction with zone lifecycle

The previous EP.5 lifecycle closure established that:

```text
fresh / unused
-> touched / requires context re-evaluation
-> used / body-collection completed
-> retired / re-plan
```

This lifecycle information can be attached to candidate records, but it still does not prove that `freshest always wins` when several valid same-TF candidates coexist.

Freshness is therefore a candidate attribute, not yet a universal ranking rule.

## Engineering implication

Safe now:

1. enumerate same-TF source-compatible candidates;
2. search current TF before lower-TF fallback;
3. begin with roughly 2-4 prior candles;
4. expand farther back if no candidate is found;
5. preserve all valid same-TF candidates if more than one exists;
6. attach lifecycle/provenance metadata;
7. only fall back to the next timeframe when the current timeframe cannot supply the required structure according to the frozen representation.

Not safe yet:

```text
winner = newest(candidate)
winner = nearest_price(candidate)
winner = freshest(candidate)
winner = best_backtest(candidate)
```

unless later primary source evidence explicitly establishes that ranking rule.

## Research consequence

This removes one ambiguity from Body Collection implementation: the engine can now have a source-backed deterministic **search hierarchy** without pretending that it has a deterministic **winner ranking** among multiple same-timeframe candidates.

The remaining high-value blockers are narrower:

1. universal OHLC geometry / zone assembly for all valid `ซอก + ไส้ + คู่` forms;
2. same-TF multi-candidate priority when several valid zones coexist;
3. exact executable entry/fill convention after source-backed lower-TF confirmation;
4. PAT2/PAT3 exact >50% denominator/arithmetic;
5. cross-frame/timeframe priority where several setup families coexist.

## Guard

Do not use historical Win/Loss outcomes to choose the missing candidate-ranking rule. If the source never defines a unique winner, preserve the ambiguity explicitly or test multiple frozen representations only as research variants with no canonical promotion from performance alone.
