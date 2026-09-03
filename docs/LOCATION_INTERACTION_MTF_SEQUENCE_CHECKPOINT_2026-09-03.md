# Location Interaction / MTF / Sequential Decision Checkpoint — 2026-09-03

Status: RESEARCH CHECKPOINT

## Evidence conclusions

Confirmed from existing primary project evidence:
- BUY PA/PAT requires support.
- SELL PA/PAT requires resistance.
- Wrong-location patterns are rejected as valid directional PA.
- Explicitly qualified larger-timeframe S/R context is stronger than a smaller-timeframe look-alike.
- Exact PAT-to-line/zone touch tolerance is still unresolved.
- Exact wick/body/close/penetration rule is still unresolved.
- Full H1/H4/D/W conflict hierarchy is still unresolved.

No new primary evidence in the current repository closes those numeric gaps, so no threshold was selected from historical outcome.

## New code

### `src/nexus_xau/engine/location_interaction.py`
Stores threshold-free candle-vs-line/zone geometry:
- wick/body intersection
- open/close inside zone
- full candle/body above or below
- nearest distance
- penetration above/below

This allows future labeled examples to be measured without embedding a guessed tolerance.

### `src/nexus_xau/engine/mtf_location.py`
Implements only the source-backed higher-TF guard:
- qualified higher-TF contradiction -> REJECT;
- unresolved higher-TF qualification -> WAIT;
- agreeing higher-TF context does not auto-promote TAKE because the full hierarchy remains unresolved.

### `src/nexus_xau/engine/pat_sequence.py`
Connects PAT -> Location -> post-SIG as a no-hindsight event sequence:

```text
PAT_COMPLETED -> WAIT_LOCATION
unresolved location -> WAIT_LOCATION_RULE
wrong location -> SKIP
qualified location -> WAIT_POST_SIG
post-SIG destroys PA -> RE_EVALUATE / SIDEWAY candidate
post-SIG not destroyed under partial check -> WAIT_FULL_SIG_VALIDATION
```

Location qualification is not treated as an order/entry, and non-destruction alone is not promoted to a fully valid SIG.

## Validation

- Pytest: 56/56 passed.
- Ruff: passed for all new modules/tests.

## Remaining blocker

Canonical valid PAT/SIG statistics remain blocked by:
1. exact PAT-to-S/R touch/penetration rule;
2. final PAT geometry thresholds;
3. full post-SIG frame/wick validity;
4. entry and invalidation/exit mechanics;
5. enough chart-aligned valid and invalid location labels.

## Next step

Build a location truth set from chart-aligned positive/negative teaching examples, extract the new raw interaction features, and keep future outcome hidden while defining the rule.
