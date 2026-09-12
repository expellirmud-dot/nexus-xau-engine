# RQ-014 — 07:00 PAT3 Combined Multi-Candle Geometry

Status: QUEUED — source review only / no outcome-selected arithmetic

## Queue note

This question is queued, not active. The 07:00 existing-knowledge audit showed PAT3 is not required for the first minimal H4/PAT2-only 07:00 V2. Resume this source review only if the minimal V2 later requires PAT3 or if the project intentionally broadens the detector.

## Why this matters now

The 07:00 workstream has already closed several source gaps that were still marked unresolved in the stale 2026-09-09 central state:

- D1 staged run distance;
- Daily Frame / S-R selector semantics;
- PAT2 >50% midpoint denominator.

The remaining PA/PAT geometry blocker with the highest direct source value is PAT3 multi-candle arithmetic.

This worksheet is active because a future source-faithful 07:00 detector must not silently reuse PAT2 arithmetic for PAT3 variants that explicitly refer to multiple candles combined.

## Current workstream state

Read first:

`docs/0700_WORKSTREAM_STATE.json`

This file is the compact current-state dashboard for the 07:00 workstream and points to current closures, frozen historical representations, and residual gaps.

## Already known

### PAT2

Source-closed on 2026-09-13:

```text
midpoint_basis = prior full candle range, wick included
midpoint = (prior.high + prior.low) / 2
directional confirming body/close passes the midpoint
full engulfing is stronger but not mandatory
```

Authority:

`docs/0700_PAT50_DENOMINATOR_SOURCE_CLOSURE_2026-09-13.md`

### PAT3 source topology

The primary lesson contains multiple PAT3 variants.

Known source wording includes:

- variant 1: confirming body exceeds half of the red candle;
- variant 2: confirming green body exceeds half of two red candles combined;
- variant 3: first green alone is insufficient, while two green candles together confirm beyond half of the red candle.

Exact multi-candle arithmetic for variants 2 and 3 is not yet source-closed.

## Active bounded question

Can the mapped PA/PAT sources discriminate among candidate geometric meanings for:

- “two red candles combined”;
- “two green candles together”;
- “exceed/pass half”;

without using historical outcome performance?

## Primary sources

1. https://youtu.be/1E_PYPor1qQ
   - local/source-mapped primary PA/PAT lesson
   - target window: ~15:22–17:56

2. https://youtu.be/NwMl2cUMb-A
   - secondary PA/PAT foundation cross-check
   - search for PAT3 / three-candle / half / combined / wick-body explanation

Use local media/transcript in:

`D:\nexus-xau-engine-repo\youtube`

when present.

Use Remote Chrome / `agent-browser --cdp 9222` only when local evidence is absent or the live YouTube transcript/visual is more useful.

## Method order

```text
check SOURCE_COVERAGE_LEDGER
-> read existing PAT closure/checkpoints
-> review exact transcript windows
-> inspect synchronized chart visuals for referential speech
-> audio cross-check only where wording is material
-> classify exact arithmetic as SOURCE_CLOSED or UNKNOWN
-> do not run outcome comparison to select a formula
```

## Candidate geometries that must remain separate until source discrimination

PAT3 variant 2 candidates include:

- sum of two red real-body lengths;
- combined high-to-low envelope;
- directional open-to-close span across two candles;
- teacher-specific visual aggregate.

PAT3 variant 3 candidates include:

- sum of two green real-body lengths;
- final close position only;
- union/envelope geometry;
- sequential visual confirmation rather than arithmetic summation.

These candidates are not claims.

## Explicit non-goals

Do not:

- backfit the PAT3 formula from Q1-Q4 outcomes;
- rewrite Q1-Q4 historical PAT2 BODY-proxy results;
- promote PAT2 full-range arithmetic to PAT3 without source evidence;
- claim PAT performance edge, Win Rate, expectancy, or profitability;
- alter RQ-010/RQ-011 frozen holdout semantics.

## Closure criteria

Close RQ-013 when one of these is true:

1. source evidence discriminates an exact PAT3 arithmetic/sequence representation; or
2. available mapped source remains non-discriminating and the exact arithmetic is durably recorded as UNKNOWN with reviewed windows and reopen triggers.

Both outcomes are valid closure.

## Expected durable updates on closure

- closure/checkpoint document;
- `docs/0700_WORKSTREAM_STATE.json`;
- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json` if authority changes;
- `docs/SOURCE_COVERAGE_LEDGER.json`;
- `research_queue/QUEUE.json`;
- `docs/CURRENT_RESEARCH_STATE.json`;
- commit/push after validation.

## Next action

Continue the already-started review:

`docs/0700_PAT3_COMBINED_GEOMETRY_REVIEW_START_2026-09-13.md`

Do not open a new unrelated 07:00 source question until this bounded review reaches a durable decision state.
