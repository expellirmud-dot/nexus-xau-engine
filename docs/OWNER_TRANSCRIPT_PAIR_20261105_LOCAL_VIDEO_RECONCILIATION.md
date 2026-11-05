# Owner Transcript Pair 2026-11-05 — Local Phone Video Reconciliation

Status: NEW_PRIMARY_TRANSCRIPT_RECONCILED / NO_CANONICAL_CHANGE / SOURCE_VISUAL_PATH_CLOSED_FOR_NUMERICS / OWNER_CLARIFICATION_REQUIRED / PRE-OUTCOME / ORDER_SEND_DISABLED

## 1. Why this document exists

On 2026-11-05 (18:20 Asia/Bangkok) the owner supplied two timestamped Thai
transcript text files and re-supplied the two matching phone recordings:

| file | bytes | SHA-256 |
|---|---|---|
| `VID_1.txt` (transcript) | 6,028 | `e3684b29438e6b6261a479743f109ecf96127eaac579aa1f95f9368249d3131a` |
| `VID_2.txt` (transcript) | 3,572 | `b7c9640d47e5773f4bb156d204a71facfe252a8d4a485c7641c478707cf12a50` |
| `VID_1.mp4` | 233,104,051 | `156353e5d19cb2f8cbe059e1cc7a61bcc455b0eae4916f5847fcb24a5dce122c` |
| `VID_2.mp4` | 122,892,640 | `efc27e0803a8126a0caca2b1cffe729b926951b9b35d62bd38b1fac75ffd5efc` |

Transcript text copies are staged in the repository at
`docs/transcripts/OWNER_TRANSCRIPT_VID20260912_163822_2026-11-05.txt` and
`docs/transcripts/OWNER_TRANSCRIPT_VID20260912_164004_2026-11-05.txt`;
raw/durable copies are at
`D:\tools\nexus-video-evidence\_incoming\2026-11-05_owner_transcripts\`.

### Identity result (Source Fact)

- `VID_1.mp4` is **byte-identical** to `_incoming/2026-09-12/VID_20260912_163822.mp4`
  (`156353e5…`), the file bound by `docs/NEW_SOURCE_VIDEO_INTAKE_2026-09-12.md`.
- `VID_2.mp4` is **byte-identical** to `_incoming/2026-09-12/VID_20260912_164004.mp4`
  (`efc27e08…`).
- Transcript coverage matches the media exactly: `VID_1.txt` runs 00:00–01:31
  against a 91.82 s clip; `VID_2.txt` runs 00:00–00:48 against a 48.23 s clip.
  This binds each transcript to its clip without guessing.

### Statement correction

An interim status picture produced earlier on 2026-11-05 described these two
clips as "never extracted / nobody has opened them". That was **wrong** and is
corrected here. Recorded state before this document:

- 2026-09-12: two machine ASR passes (15 s and 8 s chunking) plus periodic and
  scene-change frames (53 frames) were produced, and
  `docs/NEW_SOURCE_VIDEO_INTAKE_2026-09-12.md` recorded six material
  ambiguities;
- 2026-10-08: an **owner-supplied timestamped transcript of the same pair** was
  reviewed together with direct visual review, producing
  `docs/VIDEO_SOURCE_EVIDENCE_SL_TP_WICK_REANCHOR_2026-10-08.md` and the
  geometry re-anchor contract/result, plus ledger entry
  `LOCAL_VIDEO_SL_TP_WICK_20260912_REVIEW_20261008`.

The true gap was narrower and is now closed by this document: the first 10
seconds of each clip had never been inside a reviewed window, and the raw
verbatim text with its per-segment quotations had not been preserved in the
repository.

## 2. Hash-pair provenance thread (must not be silently merged)

Two byte-different copies of these recordings are in the durable evidence tree:

| pair | 163822 | 164004 | durations | used by |
|---|---|---|---|---|
| 2026-09-12 intake | `156353e5…` | `efc27e08…` | 91.82 / 48.23 | `NEW_SOURCE_VIDEO_INTAKE_2026-09-12.md`; this document's dense frames |
| 2026-10-07 "(1)" copies | `056594f6…` | `8ad37be9…` | ~91.82 / ~48.23 | `LOCAL_VIDEO_SL_TP_WICK_20260912_REVIEW_20261008` ledger entry and the 2026-10-08 visual review |

Same names, same durations, different bytes. It is reasonable that a messaging
re-export produced the "(1)" pair, but **byte-level equivalence of content
across the two pairs is not established**, and the 2026-10-08 statement "the
SHA-256 values of the current conversation uploads and the copied local
originals match exactly" applies to the "(1)" pair, not to the 2026-09-12 pair
that today's transcripts are bound to.

Recorded rule for future work: any visual claim must name which hash pair the
frames came from. Mixed-pair citation is a provenance defect.

## 3. Medium constraint — the visual escalation path is closed for numbers

Both worker reviews (sparse frames 2026-09-12/2026-10-08, and 60 new dense
frames produced 2026-11-05) agree on the medium:

`hand drawing with a ballpoint pen on paper inside a translucent plastic sleeve`

There is no charting application, no timeframe toolbar, no price axis, no clock,
and **no numeric text or tally marks anywhere in either clip**.

Consequence for method: the normal escalation chain
`TRANSCRIPT -> SYNCHRONIZED VISUAL -> AUDIO CROSS-CHECK` cannot confirm, from
visual evidence, any of the following: timeframe identity (H1/H4/Day/M1/M5),
the 1,000 / 1,500 / 5,000 point distances, the 100-point stop buffer, the ">50%"
relation, or which drawn line is support versus resistance. Those are
audio/transcript-only evidence in this source. Promotion of any numeric value
from this pair therefore requires either a better-audio pass or direct owner /
instructor clarification, not additional frame extraction.

## 4. Dense-frame results (Source Fact, 60 frames, 2026-11-05)

Extraction root: `D:\tools\nexus-video-evidence\bursts_2026-11-05_vid20260912\`
(spec `spec.json` + `spec_r2.json`, each burst dir has a `manifest.json` with
captured times and the video hash).

| # | window | visible finding | vs transcript claim |
|---|---|---|---|
| D1 | 163822 0–10 s | page is **already inked at 0 s** (~4 strokes: hatched block, tall vertical with top tick, closed loop, right tick); outline box appears ~2.5 s; more strokes by 10 s | PARTIAL — marks do appear in the window, but "starts drawing the candle at 00:00" cannot be literally true; whether the vertical is a "low wick" is NOT DECIDABLE |
| D2 | 163822 55–70 s | the handwritten two-character label "SL" first appears between 57.5 s and 60 s; one extra small flag-like mark ~62.5–65 s | CONSISTENT with SL being discussed/marked in the 00:43–01:05 segment |
| D3 | 163822 72.5–87.5 s | no numerals, no tally, no measurement bar, no "TP"/"TP2" text; two minor marks at ~85–87.5 s | NOT DECIDABLE |
| D4 | 164004 0–5 s | 2 horizontal lines at 0 s, a **third drawn live within the first second**; arrow-like right end at 3 s; dots at left ends by 5 s. The same sheet already carries the 163822 candle figure **and its "SL" label** | CONSISTENT for "three lines drawn 00:00–00:10"; roles of lower/middle/upper NOT DECIDABLE |
| D5 | 164004 26–44 s | a small box/loop on the upper line at ~36–40 s; a vertical bar with arrowhead drawn **above** the upper line at ~42–44 s; nothing above the line at 26 s | CONSISTENT as a "target at/above the upper frame" gesture sequence; distance-from-wick measurement NOT DECIDABLE |

New structural fact from D4: **the two clips are one continuous drawing session
on one sheet**, with 164004 recorded after 163822 (the 163822 candle figure and
its "SL" label are already on the page at 164004 0 s). The pair should be read
as one lesson, not two independent examples.

## 5. Transcript delta versus the 2026-09-12 and 2026-10-08 checkpoints

| prior open item | what the 2026-11-05 verbatim adds | residual |
|---|---|---|
| intake #1 exact opening-wick term | verbatim `ไส้อนุมาน` twice, explicitly "ยังไม่จบชั่วโมง" (hour not yet closed) | term is owner-transcribed phonetics; the 2026-10-08 doc already maps it to `PROVISIONAL_WICK_WHILE_PARENT_BAR_OPEN`. No canonical owner |
| intake #2 `>50%` denominator | verbatim `เนื้อปิดขึ้นไปเกิน เกิน 50% ของตัวนี้` — the reference is deictic ("of this one"), pointing at an on-page object that carries no label | **still unresolved**; must not be merged with `PAT2_GEOMETRY` (prior-candle full-range midpoint), which explicitly may not be generalised |
| intake #3 SL line/reference | `ไส้...ก็คือจุดเช็ค SL จุดวาง SL` and the "SL" label appearing at 57.5–60 s (D2) is the first direct text-on-page alignment between transcript wording and a visible mark | SL *reference object* source-backed as before; numeric buffer remains the 164004 example only |
| intake #4 speaker identity ~64–80 s | the verbatim shows a second voice (`อ๋อ`, `อือ`, and one bracketed line at 00:53) | interlocutor presence is now visible in the text, but who speaks which line is still not established |
| intake #5 H1/H4 to 1,000/1,500 mapping | **see section 6** — the mapping is distributed across the two clips, not inside one | attribution correction required; the frozen 1,500 value keeps verbatim support |
| intake #6 video-2 M5/PA wording | verbatim `เกิด PA Buy ที่ M5 หรือ M1 ... แตะ Body ปุ๊บขึ้นเลย` | timeframe label is audio-only; "แตะ Body" matches `POST_SIG_CANDIDATE_BODY_GUARD` family, still partial |
| intake #7 "100%" phrasing | verbatim `TP เนี่ย 100% แล้วพันจุด` immediately followed by `แต่ 1,000 จุด` | supports the existing non-win-rate reading ("target fully reached"), consistent with the 2026-09-12 warning; `SYSTEM_WIN_RATE` stays blocked |

## 6. Clip-attribution correction (documentation defect, low semantic impact)

`docs/VIDEO_SOURCE_EVIDENCE_SL_TP_WICK_REANCHOR_2026-10-08.md` lists, under its
"Video 2 (`163822`)", the itemisation:

`H1 = 1,000 points; H4 = 1,500 points; Day = 5,000 points`

Against the 2026-11-05 verbatim this attribution is not accurate:

- `163822` (00:12–00:20, 01:06–01:31) says TP1 of H1 = 1,000 points from the
  wick, then `ถ้าให้ TP2 ก็ นับจากจุดเนี้ยขึ้นไป 1,500 จุด` and
  `H1 ก็ เอ้ย Day ก็ 5,000 จุด` (an audible self-repair). It never says "H4".
- `164004` (00:30–00:48) is the clip that says `สมมุติ H1 1,000 จุด` and
  `H4 1,500 จุดขึ้นมางี้ เราเก็บที่ 1,500 จุด`.

Impact assessment, stated honestly:

- The frozen V2.1 value `H4_RUN_POINTS = 1500.0` keeps direct verbatim support —
  from `164004`, not from `163822`. The constant is not invalidated.
- The frozen V2.1 anchor rule (`origin/post-SIG anchor ± full nominal run`) is
  unaffected; `ไส้อนุมาน`/`ไส้หลังซิก` provisional-then-confirmed wick logic is
  unchanged.
- One genuinely new reading enters the record: inside `163822` the value 1,500 is
  labelled **TP2 of the same H1 round**, while `164004` labels 1,500 as the **H4
  distance**. Whether these are the same number used for two purposes, or an
  imprecise on-the-fly label, is NOT decided here and is a question for the owner.
- The inverted clip numbering in the 2026-10-08 document ("Video 1" = 164004) is
  the likely cause of the mix-up and should be avoided in future citations: cite
  by file id + hash, not by "Video 1/2".

This is recorded as an observation, not as a reopening of the closed conclusion.

## 7. Spelling variant preserved, not normalised

`ไส้หลังซิก` (2026-11-05 transcript, and `docs/POST_SIG_LIFECYCLE_SOURCE_VISUAL_CLOSURE_2026-09-08.md`)
versus `ไส้รังซิก` (rendered in the 2026-10-08 re-anchor document).
Per the 2026-10-08 rule already in force, engine behaviour must not depend on the
uncertain phonetic spelling; both spellings are kept in the record and the
semantic labels remain the authority.

## 8. What this document does not do

- No canonical claim was created, changed, upgraded, or demoted.
- No new RQ was activated and no WO-055 admission record was filed.
- No threshold, tolerance, denominator, priority, or geometry was chosen.
- No State Packet was computed; the 2026-11-05 input-route decision (a/b/c) is
  still open and independent of this source lane.
- Holdout scoring, economic scoring, Win/Loss, expectancy and order send remain
  disabled.

## 9. Colloquial-Thai glossary layer (same day, second owner-supplied file)

`VID_Trade.txt` was supplied on 2026-11-05 as "Thai words used informally".
Staged at `docs/transcripts/OWNER_GLOSSARY_COLLOQUIAL_THAI_TRADE_TERMS_2026-11-05.txt`
(SHA-256 `279ee165a9d3a923a56f9c0f50cbf352b83a48145d43bd5a10f14418b866ad4c`)
with a durable copy beside the transcripts.

Evidence tier: **owner-supplied reference glossary, not primary source.** The
file is an explainer that attaches an etymology and an "international
equivalent" to each term; it states no rule and no condition from the teacher.
It is therefore treated as analyst-inference reference material.

Legitimate use (accepted):

- it reduces ASR term risk on colloquial wording — `ปิดฟ้า` = a candle closing
  higher than it opened, `100 เดียว` = the spoken form of "100 จุด";
- its spelling `ไส้หลังซิก` matches the 2026-11-05 transcript and
  `docs/POST_SIG_LIFECYCLE_SOURCE_VISUAL_CLOSURE_2026-09-08.md`, which is the
  second independent occurrence of that spelling and makes the 2026-10-08
  rendering `ไส้รังซิก` the weaker variant;
- `ซิก = Signal` is consistent with the existing `post-SIG` semantic label.

Rejected imports (must not enter the research record as facts or rules):

| glossary statement | why rejected |
|---|---|
| `100 เดียว = 100 จุด = 10 pips` | the Project has no pip unit anywhere; the only unit authority is `PROJECT_POINT_SIZE = 0.01` (price per point), so 100 points = 1.00 price unit. The pip equivalence is an external convention and is not adopted |
| `สากลเรียก Rejection Wick / Liquidity Sweep / Invalidation Level / Incomplete Cycle / Bullish Continuation Momentum` | mapping this teacher's paper drawings onto external SMC/price-action vocabulary would manufacture rules the source never stated; prohibited by the evidence-first doctrine |
| "ไส้อนุมาน is a term the instructor coined himself" | an origin claim about the teacher with no supporting source; kept as unverified |
| "รอบวิ่งค้าง = momentum must continue until the cycle completes" | this reads as an unfinished-run completion rule; `PATH_REMAINING` remains a `HISTORICAL_VERSIONED_RESEARCH_REPRESENTATION` per FIND-0003 and the clips still give no re-anchor-at-entry support |

It does **not** answer the three open owner questions:

1. `1,500` — the glossary groups `1,000 / 1,500 / 5,000` as "TP1, TP2 และ Day"
   and drops any H4 label, which is the `163822` reading and is in mild tension
   with the `164004` verbatim `H4 1,500 จุด`;
2. `>50%` — not mentioned at all;
3. whether the `100 จุด` stop buffer is example-only or a rule — described, not
   decided.

## 10. Structured state updated by this pass

- `research_findings/FINDINGS.json` gained `FIND-0005`
  (`LOCAL_VIDEO_PAIR_20260912__VERBATIM_ATTRIBUTION_AND_VISUAL_PATH_LIMIT`, status OPEN,
  non-blocking) with observations `OBS-0012`..`OBS-0015`.
- `docs/SOURCE_COVERAGE_LEDGER.json` gained
  `LOCAL_VIDEO_PAIR_20260912_OWNER_VERBATIM_DENSE_20261105`
  (`SOURCE_CLOSED_WITH_RESIDUAL_OPEN`), citing the `156353e5… / efc27e08…` pair.
  Entry `LOCAL_VIDEO_SL_TP_WICK_20260912_REVIEW_20261008` is left unchanged as the
  historical record of the `(1)`-pair review; the two entries are the pair thread of §2.
- `docs/CURRENT_RESEARCH_STATE.json`, `docs/0700_WORKSTREAM_STATE.json`, the canonical
  claim register, and `research_queue/QUEUE.json` were deliberately not touched: this
  pass changed no workstream state and admitted no RQ.

## 11. Next actions

1. Owner clarification, in priority order:
   (i) is 1,500 the H4 run distance, the H1 TP2 extension, or both in different
   contexts; (ii) what is the ">50%" measured against in the closing candle;
   (iii) confirm whether the "100 จุด" stop buffer is example-only or a rule.
   Each of these is decision-critical and would require a WO-055 admitted RQ
   before any canonical change.
2. If a better-audio pass is desired for the speaker-identity window
   (163822 ~53–80 s), that is a bounded machine task; the audio, not more frames,
   is the limiting evidence.
3. Dense frames are retained outside the repository per media policy; this
   document plus the manifests are the durable citation surface.
