import json, datetime, os
root = r"D:\nexus-xau-engine-repo"
now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

# Canonical claim: narrow consumed interpretation after geometry control.
p = os.path.join(root, "docs", "CANONICAL_CLAIM_REGISTER_2026-09-03.json")
d = json.load(open(p, encoding="utf-8"))
c = next(x for x in d["claims"] if x.get("claim_id") == "H4_0700_CONSUMED_STATE_RELATION")
c["canonical_statement"] = (
    "Under frozen 07:00 historical and V2.0 research representations, H4 consumed/run-progress "
    "state is reproducibly associated with PATH_REMAINING target-first ordering across Discovery "
    "and Replication. New V2.0 geometry control shows consumed is strongly entangled with the "
    "relative target/point-check distances created by the PATH_REMAINING scoring construction; "
    "after rank-residualizing against a scale-free geometry diagnostic, the positive residual "
    "relation does not persist in either period. Independent market-predictive information from "
    "consumed is therefore NOT ESTABLISHED. This remains a research association, not a threshold, "
    "teaching rule, trade Win Rate, or profitability claim."
)
c["status"] = "ACTIVE_RESEARCH_REPLICATED_ASSOCIATION_GEOMETRY_CONFOUNDED"
c["engine_permission"] = "CARRY_AS_CONTINUOUS_RESEARCH_FEATURE_ONLY_WITH_EXPLICIT_GEOMETRY_CONTROL"
for r in [
    "docs/0700_MINIMAL_V2_DISCOVERY_FIRST_OUTCOME_2026-09-13.md",
    "docs/0700_MINIMAL_V2_REPLICATION_GEOMETRY_CONTROL_2026-09-13.md",
]:
    if r not in c.setdefault("source_refs", []):
        c["source_refs"].append(r)
for f in [
    "TARGET_POINT_GEOMETRY_CONFOUND",
    "INDEPENDENT_EFFECT_NOT_ESTABLISHED",
    "Q3_AGE_MTF_CONTROL_DID_NOT_CONTROL_TARGET_POINT_GEOMETRY",
]:
    if f not in c.setdefault("risk_flags", []):
        c["risk_flags"].append(f)
c["provenance_note"] = (
    "Historical Q3/Q4 remain valid association evidence, but the current interpretation is "
    "narrowed by V2.0 geometry falsification control. Do not describe consumed as an established "
    "independent market signal until RQ-015 resolves the geometry-null question."
)
d["updated_at"] = now
with open(p, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")

# Queue: close RQ-013 and promote RQ-015.
p = os.path.join(root, "research_queue", "QUEUE.json")
q = json.load(open(p, encoding="utf-8"))
q["active"] = {
    "id": "RQ-015",
    "title": "07:00 PATH_REMAINING Geometry Control",
    "worksheet": "research_queue/active/RQ-015_0700_PATH_REMAINING_GEOMETRY_CONTROL.md",
    "status": "ACTIVE_GEOMETRY_CONFOUND_FALSIFICATION",
    "latest_checkpoint": "docs/0700_MINIMAL_V2_REPLICATION_GEOMETRY_CONTROL_2026-09-13.md",
    "governing_objective_ref": "docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md",
    "current_summary": (
        "V2.0 unchanged-code replication is complete. Consumed association replicates, but "
        "geometry control shows strong target/point-distance confounding and no positive residual "
        "relation after geometry adjustment. Freeze/test geometry-null control next."
    ),
}
q["queue_state"] = "ACTIVE_0700_PATH_REMAINING_GEOMETRY_CONTROL"
for x in q.get("items", []):
    if x.get("id") == "RQ-013":
        x["status"] = "CLOSED_V2_REANCHOR_DISCOVERY_REPLICATION_COMPLETE"
        x["worksheet"] = "research_queue/closed/RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md"
        x["closure_ref"] = "docs/0700_MINIMAL_V2_REPLICATION_GEOMETRY_CONTROL_2026-09-13.md"
        x["closure_summary"] = (
            "07:00 state was re-anchored, V2.0 frozen, Discovery interpreted, unchanged-code "
            "Replication completed, and geometry confounding identified. Follow-up moved to RQ-015."
        )
if not any(x.get("id") == "RQ-015" for x in q.get("items", [])):
    q["items"].append({
        "id": "RQ-015",
        "title": "07:00 PATH_REMAINING Geometry Control",
        "type": "RESEARCH_FALSIFICATION",
        "status": "ACTIVE_GEOMETRY_CONFOUND_FALSIFICATION",
        "why_now": (
            "V2.0 Discovery and Replication reproduce consumed association, but explicit control "
            "shows strong confounding with target/point-check geometry and no positive residual rank relation."
        ),
        "depends_on": ["RQ-013"],
        "blocks": [
            "independent interpretation of H4 consumed/run-progress",
            "future threshold/model use of consumed",
            "safe expansion of 07:00 scoring logic",
        ],
        "preferred_method": (
            "Freeze geometry-null representation -> preserve all outcome states -> compare Discovery "
            "and Replication -> distinguish scoring geometry from market information; no threshold optimization."
        ),
        "worksheet": "research_queue/active/RQ-015_0700_PATH_REMAINING_GEOMETRY_CONTROL.md",
        "checkpoint_ref": "docs/0700_MINIMAL_V2_REPLICATION_GEOMETRY_CONTROL_2026-09-13.md",
        "current_summary": "Active bounded falsification. Independent consumed effect is not established.",
    })
po = [x for x in q.get("priority_order", []) if x != "RQ-015"]
if "RQ-014" in po:
    po.insert(po.index("RQ-014"), "RQ-015")
else:
    po.append("RQ-015")
q["priority_order"] = po
with open(p, "w", encoding="utf-8") as f:
    json.dump(q, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("PATCHED_CLAIM_AND_QUEUE")
