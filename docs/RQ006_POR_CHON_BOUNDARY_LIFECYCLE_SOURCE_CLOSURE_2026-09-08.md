# RQ-006 — Por Chon Boundary / Old-Frame Lifecycle Source Closure — 2026-09-08

Status: CLOSED / `SOURCE_BACKED_CORE_BOUNDARY_PARTIAL_LIFECYCLE`

## Question

Close the remaining source-backed Por Chon cutoff, high-selection and old-frame lifecycle semantics far enough for a provenance-safe replay representation, while retaining one-bar/tie/priority ambiguities explicitly.

## Evidence basis

First-party Por Chon source package already consolidated in:

- `docs/DIRECT_USER_POR_CHON_SPEAKER_IDENTITY_2026-09-03.md`
- `docs/POR_CHON_1900_TRANSCRIPT_CLOSURE_2026-09-03.md`
- `docs/POR_CHON_VISUAL_STANDING_FRAME_EVIDENCE_2026-09-03.md`
- `docs/PRIMARY_IMAGE_EVIDENCE_2026-09-01.md`

The project owner directly identified the speaker as Por Chon. YouTube transcript wording retains ASR risk, but the core cutoff/high-selection statements are repeated across many timestamps and are visually/contextually corroborated.

## Daily cutoff semantics

Source-backed operational rule:

```text
Por Chon uses a daily 19:00 cutoff.
Evaluate the relevant H4 highs that are known before the cutoff.
Post-19:00 movement belongs to the next cutoff window.
```

Project-owner-confirmed clock interpretation:

```text
19:00 Asia/Bangkok = 12:00 UTC
```

This timezone mapping is a canonical project interpretation of the Thai teaching clock, not a literal instructor quote saying `Asia/Bangkok`.

## New-high frame condition

Repeated source wording supports:

```text
candidate_high - previous_por_chon_high_frame > 1000 project points
```

The teacher repeatedly says `เกิน 1,000` / more than 1,000. Therefore the semantic comparator is strict `>` rather than an assumed `>=`.

Because the transcript is YouTube ASR, an exact mechanically sensitive `==1000` live case should still preserve provenance/precision caution rather than silently introduce a broker-tick epsilon.

## Candidate high selection

Source-backed object:

```text
candidate = highest H4 wick/high achieved in the completed pre-cutoff window
```

If the >1000 condition is satisfied, that candidate becomes the new Por Chon high frame. If not, keep the prior frame; do not manufacture a new one.

## H4 cutoff / 19:00 -> 23:00 visual context

Visual evidence materially clarifies that:

- frame construction uses the completed pre-19:00 high-selection window;
- the post-19:00 H4 candle can interact with the selected frame;
- in the demonstrated chart schedule the 19:00->23:00 H4 candle is evaluated at its completed 23:00 checkpoint for standing/retest behavior.

This supports a no-lookahead implementation principle:

```text
construction candidates must be fully known before the cutoff;
post-cutoff H4 information cannot retroactively alter the completed prior window.
```

Still unresolved is the exact broker/chart H4 label/inclusion convention at the boundary if a feed labels a candle by open-time versus close-time in a way that creates an off-by-one implementation choice.

## Old-frame lifecycle — important closure

First-party transcript evidence states that earlier Por Chon frames can remain usable later as prior reference / brake / support-resistance frames.

Therefore:

```text
new Por Chon frame creation != delete all older Por Chon frames
```

Safe data model:

```text
PorChonFrame {
    frame_id
    created_cutoff
    price
    source_h4_bar
    status = CREATED | HISTORICAL_REFERENCE | ...
}
```

Do not overwrite history with one mutable `current_frame_price` field if that destroys older reference frames.

## Standing / break usage

First-party visual evidence supports:

- wick penetration alone is not sufficient to declare frame failure;
- candle-body relation to the frame is a primary standing/break criterion;
- completed H4 checkpoints are used to assess standing/retest state.

Exact body geometry remains unresolved:

- both open+close on valid side?
- close-only sufficient?
- body intersection allowed?
- directional symmetry for every case?

Do not reduce this to `wick_cross => broken` or `close_side => stand` as a universal final rule.

## Remaining unresolved details

1. exact broker/chart H4 bar inclusion/labeling at the 19:00 boundary;
2. broker-tick/equality handling for an exactly-1000-point mechanical case despite strict source semantics;
3. identity tie handling if multiple H4 bars share exactly the same highest high (price itself is identical, but source-bar identity can differ);
4. priority/ranking when several old Por Chon frames coexist near price;
5. exact retirement condition, if any, for an old frame that should stop being considered;
6. exact body geometry for `ยืนกรอบ` / `หลุดกรอบ`.

## Safe replay representation

```text
for each completed local 19:00 cutoff window:
    collect H4 bars fully known before cutoff
    candidate_price = max(H4.high)
    if candidate_price - latest comparison frame > 1000 project points:
        create a new frame instance at candidate_price
    else:
        create no new frame

retain older frame instances as historical references
post-cutoff bars belong to the next evaluation window
```

The phrase `latest comparison frame` reflects the source's previous Por Chon high reference. Multi-frame usage priority after creation remains separate and unresolved.

## Closure decision

```text
SOURCE_BACKED_CORE_BOUNDARY_PARTIAL_LIFECYCLE
```

Core cutoff/high-selection/>1000/new-frame/persistence semantics are source-backed. Exact one-bar boundary labeling, tie/source identity, retirement priority and body-standing geometry remain parameterized/human-confirm.

## Next queue item

Promote `RQ-007 — Entry, SL, and invalidation geometry`.
