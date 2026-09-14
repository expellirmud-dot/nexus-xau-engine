import json
from pathlib import Path

p = Path(r"D:\nexus-xau-engine-repo\docs\SOURCE_COVERAGE_LEDGER.json")
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = "2026-09-13T05:03:39+07:00"
entries = d.get("entries", [])
by_id = {e.get("coverage_id"): e for e in entries if isinstance(e, dict)}

old_pat = by_id.get("PAT2_PAT3_HALF_BASIS_1422_1756")
if old_pat:
    old_pat["status"] = "SUPERSEDED"
    old_pat["superseded_by"] = "PAT2_FULL_RANGE_DENOMINATOR_20260913"
    old_pat["finding"] = (
        "Historical 2026-09-09 review correctly preserved ambiguity at that time. "
        "A later cross-source 2026-09-13 review closed the PAT2 single-prior-candle midpoint basis as full candle range including wick. "
        "PAT3 combined-candle arithmetic remains unresolved."
    )
    old_pat["residual_unknowns"] = ["PAT3_COMBINED_CANDLE_ARITHMETIC"]
    old_pat["checkpoint_refs"] = list(dict.fromkeys((old_pat.get("checkpoint_refs") or []) + [
        "docs/0700_PAT50_DENOMINATOR_SOURCE_CLOSURE_2026-09-13.md"
    ]))
    old_pat["last_reviewed_at"] = "2026-09-13"

new_entries = [
    {
        "coverage_id": "PAT2_FULL_RANGE_DENOMINATOR_20260913",
        "source_id": "1E_PYPor1qQ+NwMl2cUMb-A",
        "source_title": "Primary PA/PAT lesson + EP.1 foundation cross-check",
        "topic": "PAT2 >50% denominator / midpoint basis",
        "window": "1E_PYPor1qQ ~00:13:48-00:14:38; NwMl2cUMb-A ~00:56:14-00:58:14",
        "reviewed_modalities": ["YOUTUBE_TRANSCRIPT", "REMOTE_CHROME", "CROSS_SOURCE_RECONCILIATION"],
        "status": "SOURCE_CLOSED_WITH_RESIDUAL_OPEN",
        "finding": (
            "PAT2 single-prior-candle 50% midpoint basis is the full prior candle range including wick: midpoint=(high+low)/2. "
            "Directional confirming body/close must pass the midpoint. Full engulfing is stronger but not mandatory."
        ),
        "residual_unknowns": [
            "PAT3_VARIANT2_COMBINED_DENOMINATOR",
            "PAT3_VARIANT3_COMBINED_SEQUENCE",
            "PAT_LOCATION_FRAME_QUALIFICATION_SEPARATE"
        ],
        "claim_ids": ["PAT2_GEOMETRY"],
        "checkpoint_refs": ["docs/0700_PAT50_DENOMINATOR_SOURCE_CLOSURE_2026-09-13.md"],
        "reopen_triggers": [
            "CONTRADICTION_WITH_NEW_PRIMARY_SOURCE",
            "DIRECT_INSTRUCTOR_CLARIFICATION",
            "SOURCE_MAPPING_ERROR"
        ],
        "last_reviewed_at": "2026-09-13"
    },
    {
        "coverage_id": "EP2_D1_RUN_REREVIEW_0130_0257_20260913",
        "source_id": "ESHDuiVPJow",
        "source_title": "EP.2 เทรน ชนะ กรอบ กรอบ ชนะ Sig",
        "topic": "Day/D1 run magnitude family, nested H1/H4 runs, and Day-vs-H4 lifecycle",
        "window": "~01:30:58-01:42:24; ~02:56:55-02:57:02",
        "reviewed_modalities": ["LOCAL_TRANSCRIPT", "LOCAL_MP4", "TARGETED_REVIEW", "CROSSCHECK_WITH_PRIOR_PROJECT_EVIDENCE"],
        "status": "SOURCE_CLOSED_WITH_RESIDUAL_OPEN",
        "finding": (
            "Day/D1 teaching supports magnitude references around 5,000-10,000 project points, allows nested H1/H4 runs inside larger Day/Sideway space, "
            "and shows Day completion can coexist with still-active H4. The exact 5K->10K stage/set transition is not closed and no single universal D1 scalar is promoted."
        ),
        "residual_unknowns": [
            "EXACT_D1_STAGE_TRANSITION",
            "ACTIVE_DAY_STAGE_SELECTION_AT_0700",
            "MULTI_SIG_SET_ACCOUNTING"
        ],
        "claim_ids": ["D1_RUN_FAMILY_0700"],
        "checkpoint_refs": [
            "docs/0700_D1_DAY_RUN_SOURCE_REREVIEW_2026-09-13.md",
            "docs/0700_D1_DAY_RUN_SOURCE_CLOSURE_2026-09-13.md"
        ],
        "reopen_triggers": [
            "NEW_DISCRIMINATING_DAY_STAGE_SOURCE",
            "DIRECT_INSTRUCTOR_CLARIFICATION",
            "SOURCE_MAPPING_ERROR"
        ],
        "last_reviewed_at": "2026-09-13"
    },
    {
        "coverage_id": "EP3_DAILY_SR_SELECTOR_20260913",
        "source_id": "jBEM-vWYj_o",
        "source_title": "EP.3 แนวรับ - แนวต้าน",
        "topic": "Daily/strong S-R zone selector semantics and lifecycle",
        "window": "~00:20:00; ~01:25:35; ~01:38:17-01:46:13; ~02:17:03-02:35:16",
        "reviewed_modalities": ["REMOTE_CHROME", "YOUTUBE_TRANSCRIPT", "TARGETED_SOURCE_REVIEW"],
        "status": "SOURCE_CLOSED_WITH_RESIDUAL_OPEN",
        "finding": (
            "S/R is a zone rather than one universal dead price; cross-TF overlap and body/wick structural mapping matter; fresh/unused state matters; "
            "used zones may remain active until structural break; multiple H4 zones may coexist; reviewed strong-zone workflow searches H4 first then H1 fallback."
        ),
        "residual_unknowns": [
            "EXACT_0_5_SNAP_TIE_ROUNDING",
            "UNIVERSAL_NUMERIC_ZONE_TOLERANCE",
            "EXACT_WICK_BODY_CLOSE_QUALIFICATION",
            "UNIVERSAL_CROSS_FAMILY_WINNER",
            "UNIVERSAL_7_14_POINT_GATE_NOT_CLOSED"
        ],
        "claim_ids": [],
        "checkpoint_refs": ["docs/0700_DAILY_FRAME_SR_SELECTOR_SOURCE_CLOSURE_2026-09-13.md"],
        "reopen_triggers": [
            "NEW_PRIMARY_SOURCE_WITH_EXACT_SELECTOR_GEOMETRY",
            "DIRECT_INSTRUCTOR_CLARIFICATION",
            "MATERIALLY_NEW_QUESTION_NOT_COVERED_BY_PRIOR_REVIEW"
        ],
        "last_reviewed_at": "2026-09-13"
    }
]

for new in new_entries:
    cid = new["coverage_id"]
    if cid in by_id:
        by_id[cid].update(new)
    else:
        entries.append(new)

d["entries"] = entries
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("updated", p, "entries", len(entries))
