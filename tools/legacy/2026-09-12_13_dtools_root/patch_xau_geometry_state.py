import json, datetime, os
root = r"D:\nexus-xau-engine-repo"
now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
checkpoint = "docs/0700_MINIMAL_V2_REPLICATION_GEOMETRY_CONTROL_2026-09-13.md"
rq_ws = "research_queue/active/RQ-015_0700_PATH_REMAINING_GEOMETRY_CONTROL.md"

# Workstream dashboard
p = os.path.join(root, "docs", "0700_WORKSTREAM_STATE.json")
d = json.load(open(p, encoding="utf-8"))
d["updated_at"] = now
d["status"] = "MINIMAL_V2_REPLICATION_INTERPRETED_GEOMETRY_CONTROL_ACTIVE"
d["active_question"] = {
    "rq_id": "RQ-015",
    "title": "07:00 PATH_REMAINING Geometry Control",
    "status": "ACTIVE_GEOMETRY_CONFOUND_FALSIFICATION",
    "worksheet": rq_ws,
    "question": "Does H4 consumed/run-progress retain stable information after a frozen target-vs-point-check geometry baseline is accounted for?",
    "next_action": "Freeze the geometry-null analysis representation before any additional outcome scoring or threshold/model work.",
    "replication_checkpoint": checkpoint,
}
for item in d.get("replicated_research_findings", []):
    if item.get("topic") == "H4 consumed/run-progress state":
        item["state"] = "REPLICATED_ASSOCIATION_GEOMETRY_CONFOUNDED"
        item["current"] = (
            "H4 consumed_ratio_at_0700 retains a broad positive association with PATH_REMAINING "
            "target-first ordering in V2.0 Discovery and unchanged-code Replication, but explicit "
            "target/point-check geometry control is strongly collinear with consumed and removes "
            "the positive residual rank relation in both periods. Independent market information "
            "is not established."
        )
        item["guards"] = [
            "No consumed-ratio threshold.",
            "Do not call consumed an independent market signal.",
            "Historical Q3/Q4 age/MTF controls did not control target/point-check geometry.",
            "No trading score or Win Rate claim.",
        ]
        refs = item.setdefault("refs", [])
        if checkpoint not in refs:
            refs.append(checkpoint)
d["latest_checkpoint"] = checkpoint
m = d.get("minimal_v2", {})
m.update({
    "status": "IMPLEMENTATION_FROZEN_DISCOVERY_REPLICATION_INTERPRETED_GEOMETRY_CONFOUND_IDENTIFIED",
    "real_outcomes_opened": True,
    "discovery_execution_status": "DONE_RESULT_INTERPRETED",
    "replication_execution_status": "DONE_RESULT_INTERPRETED",
    "replication_checkpoint": checkpoint,
})
d["minimal_v2"] = m
d["active_durable_job"] = {
    "job_id": "XAU-0700-MINIMAL-V2-REPLICATION-20260913",
    "job_path": r"D:\tools\nexus-durable-work\_agent\jobs\XAU-0700-MINIMAL-V2-REPLICATION-20260913\job.json",
    "status": "DONE_RESULT_INTERPRETED",
    "execution_layer": "D:/tools/nexus-durable-work Local Work Agent",
    "success_probe": "results/0700_MINIMAL_V2/REPLICATION_2023_09_TO_2023_11_23/REPORT.json",
    "restart_rule": "Do not rerun Discovery or Replication. Use checkpointed results; active work is RQ-015 geometry-null control.",
    "live_status_verified": "DONE",
}
d["replication_result_summary"] = {
    "days": 60,
    "research_candidate_days": 33,
    "research_candidate_rows": 42,
    "resolved_rows": 39,
    "target_first": 16,
    "point_check_first": 23,
    "neither": 2,
    "ambiguous_same_bar": 1,
    "consumed_rho_0700": 0.5033,
    "geometry_rho_outcome": 0.6855,
    "partial_consumed_rho_given_geometry": -0.1578,
    "interpretation": "REPLICATED_ASSOCIATION_GEOMETRY_CONFOUNDED_INDEPENDENT_EFFECT_NOT_ESTABLISHED",
}
with open(p, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")

# Current research state
p = os.path.join(root, "docs", "CURRENT_RESEARCH_STATE.json")
s = json.load(open(p, encoding="utf-8"))
s["updated_at"] = now
s["mode"] = "RESTART_SAFE_0700_GEOMETRY_CONTROL"
s["completed_checkpoint"] = "0700_MINIMAL_V2_REPLICATION_GEOMETRY_CONTROL_CHECKPOINTED"
s["next_steps"] = [
    "Use the compact global continuity capsule on reconnect; do not rerun V2.0 Discovery or Replication.",
    "Load the V2.0 replication/geometry-control checkpoint and active RQ-015.",
    "Freeze a geometry-null analysis specification before further scoring.",
    "Test whether consumed retains stable residual information after geometry control in both periods.",
    "Do not promote consumed thresholds, PAT3 expansion, or trade-level claims before resolving the geometry confound.",
]
oq = s.get("operational_research_queue", {})
oq.update({
    "active_id": "RQ-015",
    "active_worksheet": rq_ws,
    "queue_state": "ACTIVE_0700_PATH_REMAINING_GEOMETRY_CONTROL",
})
s["operational_research_queue"] = oq
w = s.get("active_0700_workstream", {})
w.update({
    "active_rq": "RQ-015",
    "worksheet": rq_ws,
    "current_goal": "Resolve whether H4 consumed/run-progress contains information beyond PATH_REMAINING target/point-check geometry.",
    "current_assessment": (
        "V2.0 unchanged-code Replication reproduces the broad consumed association, but a new "
        "falsification control shows strong geometry confounding. Independent market-predictive "
        "information from consumed is not established."
    ),
    "latest_checkpoint": checkpoint,
})
s["active_0700_workstream"] = w
m = s.get("minimal_v2", {})
m.update({
    "status": "IMPLEMENTATION_FROZEN_DISCOVERY_REPLICATION_INTERPRETED_GEOMETRY_CONFOUND_IDENTIFIED",
    "next": "Freeze and execute RQ-015 geometry-null control without semantic tuning or thresholds.",
    "real_discovery_opened": True,
    "real_discovery_execution_status": "DONE_RESULT_INTERPRETED",
    "real_replication_opened": True,
    "real_replication_execution_status": "DONE_RESULT_INTERPRETED",
    "replication_checkpoint": checkpoint,
    "replication_summary": {
        "days": 60,
        "candidate_days": 33,
        "candidate_rows": 42,
        "resolved_rows": 39,
        "target_first": 16,
        "point_check_first": 23,
        "neither": 2,
        "ambiguous_same_bar": 1,
        "consumed_rho_0700": 0.5033,
        "geometry_rho_outcome": 0.6855,
        "partial_consumed_rho_given_geometry": -0.1578,
    },
})
s["minimal_v2"] = m
s["active_durable_job"] = {
    "job_id": "XAU-0700-MINIMAL-V2-REPLICATION-20260913",
    "job_path": r"D:\tools\nexus-durable-work\_agent\jobs\XAU-0700-MINIMAL-V2-REPLICATION-20260913\job.json",
    "status": "DONE_RESULT_INTERPRETED",
    "execution_layer": "D:/tools/nexus-durable-work Local Work Agent",
    "success_probe": "results/0700_MINIMAL_V2/REPLICATION_2023_09_TO_2023_11_23/REPORT.json",
    "restart_rule": "Do not rerun Discovery or Replication. Resume RQ-015 from the geometry-control checkpoint.",
    "live_status_verified": "DONE",
    "result_exists_nonempty": True,
}
s["geometry_control"] = {
    "status": "ACTIVE_RQ015_FREEZE_NEXT",
    "checkpoint": checkpoint,
    "discovery": {
        "rho_consumed_outcome": 0.5131,
        "rho_geometry_outcome": 0.6148,
        "rho_consumed_geometry": 0.8668,
        "partial_consumed_given_geometry": -0.0502,
    },
    "replication": {
        "rho_consumed_outcome": 0.5033,
        "rho_geometry_outcome": 0.6855,
        "rho_consumed_geometry": 0.8282,
        "partial_consumed_given_geometry": -0.1578,
    },
    "safe_interpretation": "REPLICATED_ASSOCIATION_GEOMETRY_CONFOUNDED_INDEPENDENT_EFFECT_NOT_ESTABLISHED",
}
with open(p, "w", encoding="utf-8") as f:
    json.dump(s, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("PATCHED_WORKSTREAM_AND_CURRENT_STATE")
