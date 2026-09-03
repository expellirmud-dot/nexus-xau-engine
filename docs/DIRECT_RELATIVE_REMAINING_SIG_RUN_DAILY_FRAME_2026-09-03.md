# Direct Relative Guidance — Remaining SIG Run Before Daily-Frame Entry — 2026-09-03

Status: DIRECT RELATIVE GUIDANCE / MATERIAL MVP SEMANTIC UPDATE

## Source wording supplied by project owner

> กรอบวันต้องดู Sig (รอบวิ่งtf h1h4 d ) ที่ยังเหลือรอบวิ่ง
> สมมุติ ก่อน07.00 น. H4 วิ่งไปแค่1000. ยังคงค้างอีก500. ในTP1  พอ07.00 น. H1 30 15 5 ปิด Pa buy  กดเข้าออดเดอร์แถวกรอบวัน ได้เลย

## Safe interpretation

This guidance materially refines MVP Research Set #1.

The 1,000 / 1,500 point numbers should not automatically be treated as a fresh target measured from every new 07:00 daily-frame entry.

Instead:

```text
1. Find an active SIG/run on H1/H4/D that has not completed its expected run.
2. Measure how much of that originating SIG run has already occurred before 07:00.
3. Compute the remaining run.
4. After 07:00, if price is at/around the Daily Frame and a qualifying BUY/SELL PA closes on the allowed lower timeframe(s), the Daily Frame can be used as an entry location to participate in the remaining run.
```

### Explicit example supplied

```text
H4 nominal TP1 run = 1,500 project points
Already run before 07:00 = 1,000 points
Remaining H4 TP1 run = 500 points
After 07:00, qualifying PA Buy around Daily Frame -> candidate entry to participate in the remaining 500-point H4 run
```

This means `remaining_run` is a state variable inherited from an earlier SIG, not necessarily a new full objective starting at the 07:00 entry.

## Research consequence

The prior simple chain:

```text
07:00 Daily Frame -> SW/Location -> SIG H1/H4 -> target 1000/1500 from new entry
```

is too crude.

The safer updated chain is:

```text
ACTIVE SIG/RUN CONTEXT (H1/H4/D)
-> how much of the originating run is already consumed?
-> remaining_run > 0 ?
-> 07:00 Daily Frame
-> Location / SW state
-> qualifying PA on allowed entry timeframe(s)
-> candidate entry toward remaining_run
```

For historical research this creates measurable fields such as:

```text
origin_sig_tf
origin_sig_direction
origin_sig_anchor
nominal_round_points
run_consumed_before_0700
remaining_run_points_at_0700
entry_pa_tf
entry_pa_time
entry_distance_to_daily_frame
remaining_run_reached_after_entry
MFE / MAE / time_to_remaining_target
```

## Important unresolved wording

The phrase:

```text
H1 30 15 5 ปิด PA buy
```

is mechanically ambiguous.

It may mean one of the following:

1. PA Buy may close on **any one** of H1 / M30 / M15 / M5 and qualify; or
2. multiple/all listed timeframes must align/close PA Buy; or
3. these are examples of acceptable entry timeframes with an unstated hierarchy.

Do not choose among these without confirmation.

## D timeframe status

This guidance explicitly mentions SIG run context on `H1 H4 D`.

For MVP Set #1, D should therefore be preserved as a possible higher-timeframe active-run context, even if the first simplified entry/measurement focus remains H1/H4. The exact D run distance and whether D is required or optional in the first test must follow existing source-backed project semantics and must not be invented.

## Provenance guard

This is direct relative guidance relayed by the project owner. It is not yet first-party instructor evidence unless independently matched to original teaching material.

It is strong enough to revise the research hypothesis and measurement plan, but unresolved multi-timeframe PA qualification must remain parameterized/blocked from canonical production logic.
