# RQ-009 — EP.5 Cross-Timeframe Component Completion

Date: 2026-09-09 Asia/Bangkok
Source: original YouTube EP.5 `oCcG3dUjrgw` rendered Show transcript + synchronized original-video screenshots
Status: `SOURCE+VISUAL_CLOSURE / HIERARCHICAL CROSS-TF COMPLETION SUPPORTED`

## Why this checkpoint exists

Earlier RQ-009 notes often described Body Collection as finding `ซอก + ไส้ + คู่` on the same timeframe first, with fallback to a lower timeframe when the structure was incomplete. That remained ambiguous on an important detail:

```text
Does fallback mean discard the higher-TF partial structure and restart entirely on the lower TF,
or can missing components be completed from the next lower TF?
```

EP.5 contains a direct worked example that answers this for at least one taught setup.

No outcome data is used in this closure.

## Direct source sequence

Around `1:01:43-1:02:05`, the instructor says the required entry/reference point is not visible on H4, so the analysis steps down to H1.

Around `1:02:17-1:02:35`, the instructor identifies on H1:

- a `ซอก`;
- an `ไส้`;
- and says the `คู่` exists but is located in M30.

Around `1:02:45-1:02:53`, the instructor says the pair in M30 lines up and that this produces the `โซนซอกไส้คู่` that had been drawn.

Safe semantic sequence:

```text
H4 target context
-> H4 complete component set not available
-> inspect H1
-> H1 supplies ซอก + ไส้
-> M30 supplies คู่
-> aligned components together complete the taught Body Collection zone
```

## Synchronized visual evidence

Local ignored evidence:

- `youtube/_evidence/oCcG3dUjrgw/visual_ep5/candidate_priority/1-02-17.png`
- `youtube/_evidence/oCcG3dUjrgw/visual_ep5/candidate_priority/1-02-53.png`

At `1:02:17`, the original chart is shown while the instructor identifies the first component structure.

At `1:02:53`, the chart is visibly on `30m`, and the instructor visually points to the historical candle relation while the subtitle/transcript states that the M30 structure supplies the pair and completes the `ซอกไส้คู่` zone.

The visual and transcript therefore agree on the cross-TF completion path.

## What this closes

Source-backed for the shown H4 workflow:

1. Search the setup timeframe first.
2. If the required Body Collection structure is incomplete, step down sequentially.
3. Lower-timeframe inspection can **complete missing components** of the higher-level Body Collection construction; it is not necessarily a full restart that discards already identified higher-TF components.
4. The shown example uses:

```text
H1: ซอก + ไส้
M30: คู่
=> combined aligned Body Collection zone
```

5. The lower-TF component must geometrically align with the candidate zone/reference structure; the source wording says the M30 pair “ตรงกัน” before calling the zone complete.

## Important correction to earlier research framing

The source does not support a universal rule:

```text
all three components must always be found on exactly one timeframe
```

A safer representation is:

```text
primary_tf = setup/reference timeframe
search hierarchy = primary TF -> next lower TF -> next lower TF as taught
component provenance retained per TF
zone may be completed by aligned components across this hierarchy
```

This also weakens the analyst assumption that `ซอก`, `ไส้`, and `คู่` always represent three independent same-TF prices that must somehow be reduced into two forecast references.

## What remains open

- Exact geometric criterion for saying a lower-TF component `ตรงกัน` / aligns with the higher-TF partial structure.
- Whether every Body Collection setup family permits component mixing across TFs or only the taught fallback cases.
- Exact priority when multiple H1 or M30 components could complete the same higher-TF partial candidate.
- Broker/feed equality normalization.
- Exact two-reference selection/assembly when several source-valid aligned component references coexist.
- Universal wick selection.
- Cross-family priority versus Sideway/other location structures.

## Safe research representation

For research-only detector design:

```text
BodyCollectionCandidate:
  setup_tf
  component_refs[] = {
      type: SOK | WICK | PAIR,
      source_tf,
      source_price,
      source_candle_ids,
      alignment_status
  }
  completion_path = [setup_tf, fallback_tf_1, fallback_tf_2]
  status = COMPLETE only when source-required components are present and aligned
```

Do not flatten component provenance to one timeframe.
Do not invent an alignment tolerance from backtest outcomes.
Do not combine arbitrary distant lower-TF components merely because they improve results.

## Decision

Result: `SOURCE+VISUAL_CLOSURE` for hierarchical cross-timeframe component completion in the shown H4 workflow.

Current source-backed interpretation is now:

```text
same-TF first
-> sequential fallback if incomplete
-> preserve valid partial components
-> lower TF may supply missing aligned component(s)
-> completed aligned structure yields Body Collection zone
```

This materially narrows the exact-reference-selection problem and supersedes any current interpretation that requires all three components to originate from one timeframe in every valid setup.
