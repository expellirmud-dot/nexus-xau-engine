import json
from pathlib import Path

p = Path(r"D:\nexus-xau-engine-repo\docs\CANONICAL_CLAIM_REGISTER_2026-09-03.json")
d = json.loads(p.read_text(encoding="utf-8"))
d["updated_at"] = "2026-09-13T05:03:39+07:00"
claims = d.get("claims", [])
by_id = {c.get("claim_id"): c for c in claims if isinstance(c, dict)}

pat2 = by_id.get("PAT2_GEOMETRY")
if pat2:
    pat2["canonical_statement"] = (
        "PAT2 is a two-candle directional reversal. Full engulfing is stronger/cleaner but not mandatory. "
        "For the single prior-candle >50% reference, the current source-closed midpoint basis is the full prior candle range including wick: "
        "midpoint=(prior.high+prior.low)/2. The directional confirming body/close must pass that midpoint. "
        "This closure is PAT2-specific and must not be silently generalized to PAT3 multi-candle arithmetic."
    )
    pat2["status"] = "ACTIVE_SOURCE_BACKED_PAT2_FULL_RANGE_MIDPOINT_CLOSED_PAT3_SEPARATE"
    refs = list(dict.fromkeys((pat2.get("source_refs") or []) + [
        "docs/0700_PAT50_DENOMINATOR_SOURCE_CLOSURE_2026-09-13.md"
    ]))
    pat2["source_refs"] = refs
    pat2["risk_flags"] = [
        "PAT3_MULTI_CANDLE_ARITHMETIC_UNRESOLVED",
        "PAT_LOCATION_FRAME_QUALIFICATION_SEPARATE",
        "DO_NOT_REWRITE_HISTORICAL_Q1_Q4_BODY_PROXY_RESULTS",
        "OHLC_EQUALITY_IMPLEMENTATION_CONVENTION_OPEN"
    ]
    pat2["supersession_note"] = (
        "Supersedes the older current-state wording that PAT2 denominator was unresolved. "
        "Historical Q1-Q4 BODY-midpoint proxy results remain frozen history."
    )

d1 = {
    "claim_id": "D1_RUN_FAMILY_0700",
    "canonical_statement": (
        "Current source evidence supports a Day/D1 run magnitude family around 5,000-10,000 project points, "
        "with H1/H4 runs able to complete inside larger Day space and Day completion not globally implying H4 completion. "
        "The exact 5,000-to-10,000 stage/set transition and active-stage selection at 07:00 remain unresolved. "
        "Do not reduce this to one universal D1 scalar."
    ),
    "status": "ACTIVE_SOURCE_BACKED_RANGE_STAGE_EXACT_TRANSITION_OPEN",
    "engine_permission": "RESEARCH_CONTEXT_METADATA_ONLY_NO_SINGLE_D1_TARGET",
    "source_refs": [
        "docs/0700_D1_DAY_RUN_SOURCE_REREVIEW_2026-09-13.md",
        "docs/DIRECT_RELATIVE_CHAT_EVIDENCE_2026-09-01.md"
    ],
    "risk_flags": [
        "DO_NOT_PROMOTE_D1_5000_AS_UNIVERSAL_SINGLE_TARGET",
        "DO_NOT_PROMOTE_D1_10000_AS_UNIVERSAL_SINGLE_TARGET",
        "EXACT_STAGE_TRANSITION_OPEN",
        "MULTI_SIG_SET_ACCOUNTING_OPEN",
        "DAY_SIDEWAY_WIDTH_IS_NOT_NATIVE_RUN_DISTANCE"
    ],
    "provenance_note": (
        "Later 2026-09-13 re-review narrows an earlier stronger staged closure. "
        "Chronology/reconciliation makes the range-stage statement current authority."
    )
}
if "D1_RUN_FAMILY_0700" in by_id:
    by_id["D1_RUN_FAMILY_0700"].update(d1)
else:
    claims.append(d1)

h4rel = {
    "claim_id": "H4_0700_CONSUMED_STATE_RELATION",
    "canonical_statement": (
        "Under the frozen 07:00 historical research representations, H4 consumed/run-progress state at 07:00 shows a broad positive replicated relationship "
        "with PATH_REMAINING target-first ordering across discovery and replication. Q3 retained positive conditional information after controlling for age and recent MTF; "
        "Q4 preserved the positive relation after upper-tail removal but did not show strict monotonicity. This is a research relationship, not a threshold, instructor rule, trade win rate, or profitability claim."
    ),
    "status": "ACTIVE_RESEARCH_REPLICATED_RELATION_NO_THRESHOLD",
    "engine_permission": "CARRY_AS_CONTINUOUS_FEATURE_IN_NEW_VERSIONED_0700_RESEARCH_ONLY",
    "source_refs": [
        "docs/0700_Q2_CONTINUOUS_MTF_CROSS_PERIOD_2026-09-12.md",
        "docs/0700_Q3_DISTINCT_INFORMATION_CROSS_PERIOD_2026-09-12.md",
        "docs/0700_Q4_H4_CONSUMED_SHAPE_CROSS_PERIOD_2026-09-12.md",
        "docs/0700_EXISTING_KNOWLEDGE_SUFFICIENCY_AUDIT_2026-09-13.md"
    ],
    "risk_flags": [
        "NO_CONSUMED_THRESHOLD",
        "Q4_TOP_BIN_NOT_SYSTEM_WIN_RATE",
        "H1_DOES_NOT_SHARE_THE_SAME_REPLICATED_RELATION",
        "HISTORICAL_PAT2_BODY_PROXY",
        "NO_TRADE_PNL_MODEL"
    ],
    "provenance_note": "Outcome-derived research relationship. It cannot upgrade source provenance or create a teaching rule."
}
if "H4_0700_CONSUMED_STATE_RELATION" in by_id:
    by_id["H4_0700_CONSUMED_STATE_RELATION"].update(h4rel)
else:
    claims.append(h4rel)

pathrel = {
    "claim_id": "0700_PATH_REMAINING_RESEARCH_RELATION",
    "canonical_statement": (
        "For the frozen Q1 07:00 proxy/scoring representation, PATH_REMAINING_AT_CONFIRMATION ranked above absolute ORIGIN_TARGET_LEVEL on resolved target-vs-point-check ordering in both discovery and replication. "
        "This aligns with direct project guidance that a 07:00 entry participates in an inherited remaining run rather than resetting a fresh full target, but Q1 itself is not instructor-intent proof."
    ),
    "status": "ACTIVE_USER_GUIDANCE_PLUS_REPLICATED_RESEARCH_REPRESENTATION",
    "engine_permission": "USE_PATH_REMAINING_AS_VERSIONED_RESEARCH_TARGET_NO_TRADE_WIN_CLAIM",
    "source_refs": [
        "docs/DIRECT_RELATIVE_REMAINING_SIG_RUN_DAILY_FRAME_2026-09-03.md",
        "docs/0700_Q1_ORIGIN_CONTEXT_REPLICATION_2026-09-12.md"
    ],
    "risk_flags": [
        "NOT_TRADE_WIN_RATE",
        "HISTORICAL_PAT2_BODY_PROXY",
        "EXACT_ENTRY_FILL_OPEN",
        "DO_NOT_RESET_FRESH_FULL_RUN_FROM_0700_ENTRY"
    ],
    "provenance_note": "Direct project guidance supplies remaining-run semantics; Q1 provides representation-level empirical support."
}
if "0700_PATH_REMAINING_RESEARCH_RELATION" in by_id:
    by_id["0700_PATH_REMAINING_RESEARCH_RELATION"].update(pathrel)
else:
    claims.append(pathrel)

d["claims"] = claims
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("updated", p, "claims", len(claims))
