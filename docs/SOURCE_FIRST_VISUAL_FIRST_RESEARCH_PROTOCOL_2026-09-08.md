# NEXUS XAU Engine — Source-First / Visual-First Research Protocol — 2026-09-08

Status: ACTIVE USER-DIRECT RESEARCH METHOD

## Decision

The project will no longer default to `run-first` for every unresolved rule.

The preferred order is now:

```text
1. inspect primary source first
2. inspect video + synchronized transcript + nearby visual frames
3. extract source-backed semantics and mark what is closed/open
4. only compute or run historical data for ambiguities that remain materially unresolved
5. use bounded experiments to test relationships, representations, or implementation choices that source evidence cannot close directly
6. never use favorable backtest outcomes to rewrite source semantics
```

## Why this changes the workflow

Earlier work often had to infer hidden rule geometry by defining several measurable variants, running them on historical data, and comparing how their relationships changed. This remains useful when the source does not expose a mechanically usable rule.

Now the project has a local video evidence path:

```text
MP4 + YouTube transcript
-> synchronized evidence window
-> nearby visual frames
-> NEXUS vision inspection
-> source-backed claim extraction
```

Therefore source review should be attempted before constructing empirical variants.

## What source-first can close efficiently

Use video/audio/transcript first for questions such as:

- which candle or wick the instructor is pointing at;
- whether a frame is based on body, wick, high/low, open/close, or a visual relation;
- which timeframe is on screen;
- ordering such as Trend -> Frame -> SIG;
- spoken times such as 07:00 / 19:00 and their contextual meaning;
- qualitative state changes such as stand, break, reject, retest, reset, re-evaluate;
- whether an example is universal, conditional, or merely illustrative when the wording makes that distinction explicit.

When the visual source is sufficient, do not invent extra numeric proxies merely because they are easy to backtest.

## When computation is still required

Computation remains necessary when any of the following applies:

1. The instructor/source wording is incomplete or ambiguous in a mechanically important way.
2. Visual examples show a relationship but do not define an exact numeric boundary.
3. Multiple plausible representations remain after source review.
4. The project needs to measure whether a source-backed feature adds empirical information across historical periods.
5. The question concerns frequency, distribution, interaction, robustness, or outcome behavior rather than semantic definition.
6. We need to test whether an implementation reproduces known source examples without leakage.

## Required decision split

For every unresolved item, classify it before running data:

```text
SOURCE_CLOSED
SOURCE_PARTIAL
VISUAL_AMBIGUOUS
NUMERICALLY_UNDEFINED
EMPIRICAL_RELATION_NEEDED
IMPLEMENTATION_VALIDATION_NEEDED
```

Only the latter five may justify computation, and the exact reason must be recorded before the run.

## Efficiency rule

Do not run a large historical experiment to answer a question that can be closed directly from the primary teaching source.

Conversely, do not force a visual interpretation to become an exact threshold if the source does not state one. In that case keep the ambiguity explicit and use threshold-free or multi-variant empirical analysis only when it can add information without outcome-driven retuning.

## Evidence hierarchy for this workflow

```text
Primary video/audio + synchronized visual context
> YouTube ASR transcript with timestamp (ASR risk retained)
> direct project-owner clarification
> derived analyst extraction
> research representation
> empirical outcome
```

The hierarchy is about semantic authority, not statistical usefulness. Empirical results may be highly useful but cannot upgrade a research proxy into a source fact.

## Expected time saving

The main saving should come from reducing unnecessary search over rule variants. Instead of testing many candidate formulas for every concept, first use the source to eliminate impossible interpretations and close any directly visible mechanics. Historical computation is then reserved for the smaller residual uncertainty set.

This is expected to reduce compute time and analyst iteration, but the amount saved must not be claimed numerically until measured.

## Current project consequence

For the current post-SIG lifecycle question, the next preferred action is source/video review of relevant SIG, reset, re-evaluation, wick/body, and lifecycle examples before another broad empirical run.

If the source still cannot close whether destruction causes full reset versus older-origin re-evaluation, only then proceed to a bounded empirical representation test, preserving both variants and avoiding outcome-selected thresholds.
