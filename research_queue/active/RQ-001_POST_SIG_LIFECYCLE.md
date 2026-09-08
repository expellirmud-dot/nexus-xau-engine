# RQ-001 — Post-SIG lifecycle after reference destruction

Status: ACTIVE
Priority: HIGHEST CURRENT DECISION-CRITICAL QUESTION
Method: SOURCE-FIRST / VISUAL-FIRST / TARGETED-COMPUTATION-ONLY-IF-NEEDED

## Exact question

After a current post-SIG reference / inherited origin is structurally destroyed or invalidated, what does the teaching system do next?

Candidate lifecycle meanings to distinguish without assuming any is correct:

1. full reset: the old inherited run/setup is no longer active and the system waits for a new valid PA/SIG;
2. older-origin re-evaluation: if the newest origin is destroyed, an older still-valid same-direction origin may become active again;
3. another source-defined lifecycle not yet represented by the current engine.

## Why this is active now

The source-partial invalidation-aware re-anchor changed the inherited population materially:

- 2022/23 legacy 285 -> reanchored 34
- 2024 legacy 47 -> reanchored 1
- 2025 legacy 29 -> reanchored 0

The corrected retest therefore closed `INCONCLUSIVE_AFTER_SOURCE_PARTIAL_REANCHOR`, and the old Daily-side SUPPORT is historical/confounded rather than current confirmation.

The largest remaining ambiguity is no longer whether the legacy result looked good. It is whether the active-origin lifecycle representation itself matches the teaching system.

## Already known

- Post-SIG reference index is source-backed as PAT1->2, PAT2->3, PAT3->4, with BUY low / SELL high reference when the directional wick is absent.
- A post-SIG reference that disturbs/exceeds the PA invalidates the old setup and triggers re-evaluation/new-PA handling at a safe partial semantic level.
- Exact numeric destruction geometry is not fully closed.
- Current re-anchor logic deliberately used a source-partial representation and preserved the unresolved older-origin question.
- Backtest outcomes cannot decide source provenance or invent the lifecycle rule.

## Still unknown

- Does destruction terminate the inherited run completely?
- Can an older surviving origin become active again after a newer origin is destroyed?
- Does the teacher explicitly require waiting for a new PA/SIG?
- Is there a distinction between destroying the post-SIG reference, destroying the PA, consuming the run, and completing the setup?
- Does lifecycle behavior differ by PAT type, timeframe, direction, or market state?
- What exact wording/visual condition corresponds to `กวน/ทำลาย PA` in the source examples?

## Sources to inspect first

Local source batch in `D:\nexus-xau-engine-repo\youtube`:

1. `ESHDuiVPJow` — EP.2 Trend -> Frame -> SIG
2. `vcdN51_OrPE` — system summary
3. `1E_PYPor1qQ` — PAT1 / PA behavior
4. `UV5NijhjfJ8` — M5 brake / order-entry context
5. `16KoS7d-koI` — M1/M5 entry detail

Existing evidence/docs to compare:

- `docs/PA_PAT_TRANSCRIPT_FORENSICS_2026-09-01.md`
- `docs/SOURCE_PARTIAL_REANCHORED_DAILY_SIDE_CLOSURE_2026-09-08.md`
- `docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json`
- `docs/VIDEO_EVIDENCE_PIPELINE_2026-09-08.md`
- `docs/SOURCE_FIRST_VISUAL_FIRST_RESEARCH_PROTOCOL_2026-09-08.md`

## Tools to use

Before building anything new, read `TOOLS.md`.

Primary local tooling already available:

- `D:\tools\nexus-video-evidence\extract_frames.py`
- `D:\tools\ie-coder-bridge-image-patch`

Use synchronized video evidence windows around relevant transcript timestamps. If pointer movement matters, increase frame density. If ASR wording materially changes lifecycle interpretation and transcript+visual is insufficient, activate `ENG-001` audio extraction/alignment rather than guessing.

## Search concepts / source language

Do not treat this list as exhaustive. Search transcript/source context around terms such as:

- SIG / ซิก
- PA / พีเอ
- กวน / ทำลาย / เสีย / พัง
- ใหม่ / เก่า / ก่อนหน้า / ย้อน
- จบรอบ / รอบ / วิ่งครบ / เหลือ
- รอ / เกิดใหม่ / หาใหม่ / ใช้อันใหม่
- ไส้หลัง / แท่งหลัง / แท่งถัดไป
- ยืน / หลุด / เบรก / กลับตัว

The goal is semantic discovery, not keyword counting.

## Work phases

### Phase A — transcript map

Search all five transcripts for lifecycle-relevant passages and build a candidate timestamp list with surrounding wording.

Output: timestamp map grouped by video and semantic theme.

### Phase B — visual evidence windows

For each material passage, inspect nearby frames before/during/after the statement. Record what chart element, PA, SIG, wick, frame, or pointer the instructor is referring to.

Output: evidence bundle references and visual notes.

### Phase C — direct vs interpreted claim table

For each candidate rule, separate:

- direct source wording/visual fact;
- normalized transcript interpretation;
- analyst inference;
- unresolved alternative.

Output: claim table with confidence/provenance and contradiction flags.

### Phase D — source closure decision

Attempt to close one of these states:

- `SOURCE_SUPPORTS_FULL_RESET`
- `SOURCE_SUPPORTS_OLDER_ORIGIN_REEVALUATION`
- `SOURCE_SUPPORTS_OTHER_EXPLICIT_LIFECYCLE`
- `SOURCE_REMAINS_AMBIGUOUS`

Do not force a binary result if the source distinguishes multiple cases.

### Phase E — targeted computation only if needed

Use computation only if source evidence leaves multiple measurable lifecycle interpretations and historical data can test consequences without selecting a teaching rule from performance.

Allowed examples:

- count how often candidate state differs under two source-compatible lifecycle representations;
- compare population composition and relationship stability;
- measure threshold-free age/consumed-progress/timing relations.

Not allowed:

- choose the lifecycle rule because it produces the best target-first rate;
- invent an age, buffer, expiry, or consumed-run threshold from historical outcomes;
- treat a better backtest as proof of what the instructor meant.

## Closure criteria

RQ-001 may close when at least one of the following is true:

1. primary source evidence sufficiently establishes lifecycle semantics and the claim register can be updated; or
2. evidence establishes multiple conditional cases and those conditions are explicit enough to represent; or
3. after bounded review, the source remains genuinely ambiguous and the worksheet closes `INCONCLUSIVE/BLOCKED` with the exact missing evidence named.

Closure must include:

- source video IDs and timestamps;
- visual/audio crosscheck status where material;
- direct/derived separation;
- resulting state-machine representation or explicit unresolved alternatives;
- impact on previous re-anchor research;
- affected canonical claims;
- whether computation remains necessary;
- next promoted queue item.

## Non-goals / guards

- Do not retune invalidation/equality from outcomes.
- Do not add a 200-point destruction buffer unless source evidence explicitly supports it.
- Do not add expiry timers or age gates from backtest performance.
- Do not assume older-origin reactivation merely because it restores sample size.
- Do not assume full reset merely because re-anchor sample becomes small.
- Preserve the historical legacy Daily-side result and the source-partial inconclusive retest.

## Current next action

Build the transcript timestamp map for the five local videos, beginning with `ESHDuiVPJow` and `vcdN51_OrPE`, then inspect synchronized visual windows around the strongest lifecycle passages before running any new broad historical experiment.
