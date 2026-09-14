import json
from pathlib import Path

paths = {
    "DISCOVERY": Path(r"D:\nexus-xau-engine-repo\results\0700_Q1_ORIGIN_CONTEXT\DISCOVERY_2022_09_TO_2023_03\REPORT.json"),
    "REPLICATION": Path(r"D:\nexus-xau-engine-repo\results\0700_Q1_ORIGIN_CONTEXT\REPLICATION_2023_09_TO_2023_11_23\REPORT.json"),
}

def resolved_rate(counts):
    t=counts.get("TARGET_FIRST",0)
    p=counts.get("POINT_CHECK_FIRST",0)
    return t/(t+p) if t+p else None

def extract(report):
    v=report["summary"]["variants"]["FIRST_ANY_PA_PROXY"]
    groups=v["groups"]
    out={
        "origin_rows":v["origin_rows"],
        "scored_rows":v["scored_rows"],
        "scored_contexts":v["scored_contexts"],
        "candidate_states":v["candidate_state_counts"],
        "path_counts":v["path_remaining"]["first_hit_counts"],
        "path_resolved_target_first":resolved_rate(v["path_remaining"]["first_hit_counts"]),
        "origin_level_counts":v["origin_level"]["first_hit_counts"],
        "origin_level_resolved_target_first":resolved_rate(v["origin_level"]["first_hit_counts"]),
        "by_origin_tf":{},
        "by_context_tf":{},
        "by_conflict":{},
        "frame_side":groups["confirmation_frame_side"],
        "confirmation_tf":groups["confirmation_event_tf"],
        "alignment":groups["alignment_count_exact"],
    }
    for k,d in groups["origin_tf"].items():
        out["by_origin_tf"][k]={
            "counts":d["path_remaining"],
            "resolved_target_first":resolved_rate(d["path_remaining"]),
            "mfe_median":d["mfe_median"],"mae_median":d["mae_median"],
            "origin_rows":d["origin_rows"],"contexts":d["contexts"],
        }
    for k,d in groups["context_origin_tf_set"].items():
        out["by_context_tf"][k]={
            "counts":d["path_remaining"],
            "resolved_target_first":resolved_rate(d["path_remaining"]),
            "mfe_median":d["mfe_median"],"mae_median":d["mae_median"],
            "origin_rows":d["origin_rows"],"contexts":d["contexts"],
        }
    for k,d in groups["direction_conflict_present"].items():
        out["by_conflict"][k]={
            "counts":d["path_remaining"],
            "resolved_target_first":resolved_rate(d["path_remaining"]),
            "mfe_median":d["mfe_median"],"mae_median":d["mae_median"],
            "origin_rows":d["origin_rows"],"contexts":d["contexts"],
        }
    return out

out={}
for label,path in paths.items():
    out[label]=extract(json.loads(path.read_text(encoding="utf-8")))

print(json.dumps(out,ensure_ascii=False,indent=2))
