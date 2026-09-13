from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CORE_PATHS = [
    Path("AGENTS.md"),
    Path("PROJECT_BOOTSTRAP.md"),
    Path("docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md"),
    Path("skills/README.md"),
    Path("skills/SKILLS_MANIFEST.json"),
    Path("skills/nexus-xau-research/SKILL.md"),
    Path("docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md"),
    Path("docs/STATE_AUTHORITY_CONTRACT_2026-09-13.md"),
    Path("TOOLS.md"),
    Path("docs/CURRENT_RESEARCH_STATE.json"),
    Path("docs/0700_WORKSTREAM_STATE.json"),
    Path("docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json"),
    Path("docs/SOURCE_COVERAGE_LEDGER.json"),
    Path("research_queue/QUEUE.json"),
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise TypeError(f"Expected JSON object: {path}")
    return data


def parse_iso_datetime(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def validate_state_consistency(
    *,
    state: dict[str, Any],
    queue: dict[str, Any],
    canonical: dict[str, Any],
    ledger: dict[str, Any],
    workstream: dict[str, Any],
    activation_lock: dict[str, Any] | None,
) -> dict[str, Any]:
    authority = state.get("state_authority") or {}
    if not isinstance(authority, dict) or authority.get("scope") != "PROJECT_CURRENT":
        return {
            "status": "FAIL",
            "reason": "PROJECT_STATE_SCOPE_UNDECLARED",
            "scope": authority.get("scope") if isinstance(authority, dict) else None,
        }

    active_raw = queue.get("active")
    if active_raw is not None and not isinstance(active_raw, dict):
        return {
            "status": "FAIL",
            "reason": "QUEUE_ACTIVE_INVALID",
        }
    active = active_raw or {}
    operational = state.get("operational_research_queue") or {}
    if not isinstance(operational, dict):
        return {
            "status": "FAIL",
            "reason": "PROJECT_OPERATIONAL_QUEUE_INVALID",
        }

    queue_rq = active.get("id")
    queue_worksheet = active.get("worksheet")
    queue_status = active.get("status")

    if authority.get("project_current_research_checkpoint") != operational.get("latest_checkpoint"):
        return {
            "status": "FAIL",
            "reason": "PROJECT_RESEARCH_CHECKPOINT_POINTER_MISMATCH",
            "authority": authority.get("project_current_research_checkpoint"),
            "operational": operational.get("latest_checkpoint"),
        }

    pointer_fields = {
        "active_id": (operational.get("active_id"), queue_rq),
        "active_worksheet": (operational.get("active_worksheet"), queue_worksheet),
        "active_status": (operational.get("active_status"), queue_status),
        "queue_state": (operational.get("queue_state"), queue.get("queue_state")),
    }
    mismatches = {
        field: {"state": values[0], "queue": values[1]}
        for field, values in pointer_fields.items()
        if values[0] != values[1]
    }
    if mismatches:
        return {
            "status": "FAIL",
            "reason": "PROJECT_QUEUE_POINTER_MISMATCH",
            "mismatches": mismatches,
        }

    if queue_rq is None:
        if any(
            value is not None
            for value in (
                operational.get("active_id"),
                operational.get("active_worksheet"),
                operational.get("active_status"),
            )
        ):
            return {
                "status": "FAIL",
                "reason": "NO_ACTIVE_RQ_STATE_DRIFT",
            }
        if "NO_ACTIVE_RQ" not in str(state.get("mode", "")).upper():
            return {
                "status": "FAIL",
                "reason": "PROJECT_MODE_ACTIVE_STATE_MISMATCH",
                "mode": state.get("mode"),
            }
        if operational.get("latest_checkpoint") != operational.get("last_closure_ref"):
            return {
                "status": "FAIL",
                "reason": "PROJECT_LATEST_CHECKPOINT_MISMATCH",
                "latest_checkpoint": operational.get("latest_checkpoint"),
                "last_closure_ref": operational.get("last_closure_ref"),
            }

    items = queue.get("items") or []
    if not isinstance(items, list):
        return {
            "status": "FAIL",
            "reason": "QUEUE_ITEMS_INVALID",
        }
    items_by_id = {
        item.get("id"): item
        for item in items
        if isinstance(item, dict) and item.get("id")
    }

    last_closed_id = operational.get("last_closed_id")
    if last_closed_id:
        last_item = items_by_id.get(last_closed_id)
        if not isinstance(last_item, dict):
            return {
                "status": "FAIL",
                "reason": "LAST_CLOSED_RQ_MISSING_FROM_QUEUE",
                "last_closed_id": last_closed_id,
            }
        if not str(last_item.get("status", "")).upper().startswith("CLOSED"):
            return {
                "status": "FAIL",
                "reason": "LAST_CLOSED_RQ_NOT_CLOSED",
                "last_closed_id": last_closed_id,
                "queue_status": last_item.get("status"),
            }
        if last_item.get("closure_ref") != operational.get("last_closure_ref"):
            return {
                "status": "FAIL",
                "reason": "LAST_CLOSURE_REF_MISMATCH",
                "last_closed_id": last_closed_id,
                "state_closure_ref": operational.get("last_closure_ref"),
                "queue_closure_ref": last_item.get("closure_ref"),
            }

    if workstream.get("scope") != "WORKSTREAM_CURRENT_0700_ONLY":
        return {
            "status": "FAIL",
            "reason": "WORKSTREAM_SCOPE_UNDECLARED",
            "scope": workstream.get("scope"),
        }
    workstream_project = {
        "project_active_rq": (workstream.get("project_active_rq"), queue_rq),
        "project_queue_state": (
            workstream.get("project_queue_state"),
            queue.get("queue_state"),
        ),
        "project_current_checkpoint": (
            workstream.get("project_current_checkpoint"),
            operational.get("latest_checkpoint"),
        ),
    }
    workstream_mismatches = {
        field: {"workstream": values[0], "project": values[1]}
        for field, values in workstream_project.items()
        if values[0] != values[1]
    }
    if workstream_mismatches:
        return {
            "status": "FAIL",
            "reason": "WORKSTREAM_PROJECT_POINTER_MISMATCH",
            "mismatches": workstream_mismatches,
        }

    active_0700 = state.get("active_0700_workstream") or {}
    if isinstance(active_0700, dict) and str(active_0700.get("status", "")).upper() == "ACTIVE":
        state_0700_rq = active_0700.get("active_rq")
        workstream_question = workstream.get("active_question") or {}
        workstream_0700_rq = (
            workstream_question.get("rq_id")
            if isinstance(workstream_question, dict)
            and str(workstream_question.get("status", "")).upper().startswith("ACTIVE")
            else None
        )
        if state_0700_rq != workstream_0700_rq:
            return {
                "status": "FAIL",
                "reason": "ACTIVE_0700_WORKSTREAM_RQ_MISMATCH",
                "state_active_rq": state_0700_rq,
                "workstream_active_rq": workstream_0700_rq,
            }

    rq012_state = state.get("rq012_v0_holdout_ledger_activation") or {}
    rq012_legacy = state.get("rq012_holdout_state") or {}
    if isinstance(rq012_legacy, dict):
        legacy_note = str(rq012_legacy.get("note", "")).lower()
        if "implement tooling next" in legacy_note:
            return {
                "status": "FAIL",
                "reason": "RQ012_STALE_IMPLEMENTATION_INSTRUCTION",
                "note": rq012_legacy.get("note"),
            }
    rq012_item = items_by_id.get("RQ-012")
    if rq012_state:
        if not isinstance(rq012_item, dict):
            return {
                "status": "FAIL",
                "reason": "RQ012_QUEUE_ITEM_MISSING",
            }
        for field in ("status", "worksheet"):
            if rq012_state.get(field) != rq012_item.get(field):
                return {
                    "status": "FAIL",
                    "reason": "RQ012_STATE_QUEUE_MISMATCH",
                    "field": field,
                    "state": rq012_state.get(field),
                    "queue": rq012_item.get(field),
                }
        if activation_lock is None:
            return {
                "status": "FAIL",
                "reason": "HOLDOUT_ACTIVATION_LOCK_MISSING",
            }
        lock_pairs = {
            "engine_freeze_commit": (
                rq012_state.get("engine_freeze_commit"),
                activation_lock.get("engine_freeze_commit"),
            ),
            "protocol_freeze_commit": (
                rq012_state.get("protocol_freeze_commit"),
                activation_lock.get("protocol_freeze_commit"),
            ),
            "prospective_boundary": (
                rq012_state.get("prospective_boundary"),
                activation_lock.get("prospective_boundary"),
            ),
        }
        lock_mismatches = {
            field: {"state": values[0], "activation_lock": values[1]}
            for field, values in lock_pairs.items()
            if values[0] != values[1]
        }
        if lock_mismatches:
            return {
                "status": "FAIL",
                "reason": "HOLDOUT_ACTIVATION_IDENTITY_MISMATCH",
                "mismatches": lock_mismatches,
            }
        if rq012_state.get("holdout_open") is not False:
            return {
                "status": "FAIL",
                "reason": "HOLDOUT_OPEN_STATE_DRIFT",
            }
        if rq012_state.get("outcome_scoring_authorized") is not False:
            return {
                "status": "FAIL",
                "reason": "HOLDOUT_SCORING_AUTHORIZATION_DRIFT",
            }
        if activation_lock.get("outcome_scoring_enabled") is not False:
            return {
                "status": "FAIL",
                "reason": "HOLDOUT_SCORING_ENABLED",
            }

    state_time = parse_iso_datetime(state.get("updated_at"))
    if state_time is None:
        return {
            "status": "FAIL",
            "reason": "CURRENT_STATE_TIMESTAMP_INVALID",
            "value": state.get("updated_at"),
        }

    newer: list[dict[str, str]] = []
    for label, payload in (
        ("queue", queue),
        ("canonical", canonical),
        ("coverage", ledger),
        ("0700_workstream", workstream),
    ):
        other_time = parse_iso_datetime(payload.get("updated_at"))
        if other_time is not None and other_time > state_time:
            newer.append(
                {
                    "source": label,
                    "updated_at": str(payload.get("updated_at")),
                }
            )

    if newer:
        return {
            "status": "FAIL",
            "reason": "CENTRAL_STATE_STALE",
            "current_state_updated_at": state.get("updated_at"),
            "newer_sources": newer,
        }

    return {
        "status": "PASS",
        "active_rq": queue_rq,
        "queue_state": queue.get("queue_state"),
        "last_closed_id": last_closed_id,
    }

def validate_skill_freeze(skill_manifest: dict[str, Any]) -> dict[str, Any]:
    status = str(skill_manifest.get("status", "")).upper()
    if status != "FROZEN":
        return {
            "status": "FAIL",
            "reason": "SKILL_MANIFEST_NOT_FROZEN",
            "skill_manifest_status": skill_manifest.get("status"),
        }

    skills = skill_manifest.get("skills") or []
    if not isinstance(skills, list) or not skills:
        return {
            "status": "FAIL",
            "reason": "SKILL_MANIFEST_EMPTY",
        }

    verified: list[dict[str, str]] = []
    for item in skills:
        if not isinstance(item, dict):
            return {
                "status": "FAIL",
                "reason": "SKILL_MANIFEST_ENTRY_INVALID",
            }
        rel = item.get("path")
        expected = str(item.get("sha256", "")).lower()
        if not isinstance(rel, str) or not rel or len(expected) != 64:
            return {
                "status": "FAIL",
                "reason": "SKILL_MANIFEST_ENTRY_INCOMPLETE",
                "entry": item,
            }
        path = ROOT / rel
        if not path.exists():
            return {
                "status": "FAIL",
                "reason": "FROZEN_SKILL_MISSING",
                "path": rel,
            }
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            return {
                "status": "FAIL",
                "reason": "FROZEN_SKILL_HASH_MISMATCH",
                "path": rel,
                "expected_sha256": expected,
                "actual_sha256": actual,
            }
        verified.append(
            {
                "id": str(item.get("id", rel)),
                "path": rel,
                "sha256": actual,
                "status": str(item.get("status", "")),
            }
        )

    return {
        "status": "PASS",
        "manifest_status": status,
        "verified": verified,
    }


def sha256_prefix(path: Path, length: int = 12) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest[:length]


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def resolve_repo_path(value: str | None) -> Path | None:
    if not value:
        return None
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            result.append(path)
    return result


def build_manifest() -> dict[str, Any]:
    missing_core = [repo_rel(ROOT / p) for p in CORE_PATHS if not (ROOT / p).exists()]
    if missing_core:
        return {
            "status": "FAIL",
            "reason": "MISSING_CORE_FILES",
            "missing": missing_core,
        }

    state_path = ROOT / "docs/CURRENT_RESEARCH_STATE.json"
    queue_path = ROOT / "research_queue/QUEUE.json"
    canonical_path = ROOT / "docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json"
    ledger_path = ROOT / "docs/SOURCE_COVERAGE_LEDGER.json"
    workstream_path = ROOT / "docs/0700_WORKSTREAM_STATE.json"
    skill_manifest_path = ROOT / "skills/SKILLS_MANIFEST.json"

    state = load_json(state_path)
    queue = load_json(queue_path)
    canonical = load_json(canonical_path)
    ledger = load_json(ledger_path)
    workstream = load_json(workstream_path)
    skill_manifest = load_json(skill_manifest_path)

    rq012_state = state.get("rq012_v0_holdout_ledger_activation") or {}
    activation_lock: dict[str, Any] | None = None
    if isinstance(rq012_state, dict) and rq012_state.get("activation_lock"):
        activation_lock_path = resolve_repo_path(rq012_state.get("activation_lock"))
        if activation_lock_path is not None and activation_lock_path.exists():
            activation_lock = load_json(activation_lock_path)

    skill_freeze = validate_skill_freeze(skill_manifest)
    if skill_freeze.get("status") != "PASS":
        return skill_freeze

    consistency = validate_state_consistency(
        state=state,
        queue=queue,
        canonical=canonical,
        ledger=ledger,
        workstream=workstream,
        activation_lock=activation_lock,
    )
    if consistency.get("status") != "PASS":
        return consistency

    active = queue.get("active") or {}
    if not isinstance(active, dict):
        raise TypeError("research_queue/QUEUE.json -> active must be an object")

    active_worksheet = resolve_repo_path(active.get("worksheet"))
    latest_checkpoint = resolve_repo_path(
        active.get("latest_checkpoint")
        or active.get("checkpoint_ref")
        or state.get("operational_research_queue", {}).get("latest_checkpoint")
        or state.get("rq009_source_gap_closure", {}).get("checkpoint_ref")
    )

    dynamic_required: list[Path] = [ROOT / p for p in CORE_PATHS]
    authority = state.get("state_authority") or {}
    if isinstance(authority, dict):
        tooling_checkpoint = resolve_repo_path(authority.get("latest_operational_tooling_checkpoint"))
        if tooling_checkpoint is not None:
            dynamic_required.append(tooling_checkpoint)
    if active_worksheet is not None:
        dynamic_required.append(active_worksheet)
    if latest_checkpoint is not None:
        dynamic_required.append(latest_checkpoint)

    research_loop = state.get("research_loop") or {}
    if isinstance(research_loop, dict):
        load_order = research_loop.get("load_order") or []
        if isinstance(load_order, list):
            for item in load_order:
                if not isinstance(item, str):
                    continue
                if item.lower().startswith("latest new source evidence"):
                    continue
                resolved = resolve_repo_path(item)
                if resolved is not None:
                    dynamic_required.append(resolved)

    dynamic_required = dedupe_paths(dynamic_required)
    missing_dynamic = [repo_rel(path) for path in dynamic_required if not path.exists()]

    claims = canonical.get("claims") or []
    if not isinstance(claims, list):
        raise TypeError("canonical claim register -> claims must be an array")

    active_claims = [
        claim
        for claim in claims
        if isinstance(claim, dict)
        and str(claim.get("status", "")).startswith("ACTIVE")
    ]

    coverage_entries = ledger.get("entries") or []
    if not isinstance(coverage_entries, list):
        raise TypeError("source coverage ledger -> entries must be an array")
    coverage_status_counts = Counter(
        str(entry.get("status", "UNKNOWN"))
        for entry in coverage_entries
        if isinstance(entry, dict)
    )

    blocked = state.get("blocked_from_claiming") or []
    if not isinstance(blocked, list):
        blocked = []

    next_steps = state.get("next_steps") or []
    if not isinstance(next_steps, list):
        next_steps = []

    manifest_files = []
    for path in dynamic_required:
        if path.exists() and path.is_file():
            manifest_files.append(
                {
                    "path": repo_rel(path),
                    "sha256": sha256_prefix(path),
                }
            )

    status = "PASS" if not missing_dynamic else "FAIL"

    return {
        "status": status,
        "reason": None if status == "PASS" else "MISSING_DYNAMIC_FILES",
        "project": state.get("project"),
        "state_updated_at": state.get("updated_at"),
        "completed_checkpoint": state.get("completed_checkpoint"),
        "state_scope": (state.get("state_authority") or {}).get("scope"),
        "state_reconciliation": (state.get("state_authority") or {}).get("latest_state_reconciliation"),
        "queue_state": queue.get("queue_state"),
        "last_closed_id": (state.get("operational_research_queue") or {}).get("last_closed_id"),
        "active_workstream": {
            "id": workstream.get("workstream"),
            "status": workstream.get("status"),
            "updated_at": workstream.get("updated_at"),
            "active_rq": (workstream.get("active_question") or {}).get("rq_id")
            if isinstance(workstream.get("active_question"), dict)
            else None,
        },
        "active_rq": {
            "id": active.get("id"),
            "title": active.get("title"),
            "status": active.get("status"),
            "worksheet": repo_rel(active_worksheet) if active_worksheet else None,
            "latest_checkpoint": repo_rel(latest_checkpoint) if latest_checkpoint else None,
        },
        "canonical": {
            "updated_at": canonical.get("updated_at"),
            "total_claims": len(claims),
            "active_claims": len(active_claims),
        },
        "coverage": {
            "updated_at": ledger.get("updated_at"),
            "entries": len(coverage_entries),
            "status_counts": dict(sorted(coverage_status_counts.items())),
        },
        "skill_freeze": skill_freeze,
        "blocked_from_claiming": blocked,
        "next_steps": next_steps[:5],
        "required_files": manifest_files,
        "missing": missing_dynamic,
        "comprehension_gate": [
            "State the 07:00 project objective and unknown-state/PASS doctrine.",
            "State the active 07:00 workstream and active RQ/worksheet.",
            "State the latest checkpoint.",
            "State relevant canonical facts and residual unknowns.",
            "Check source coverage before reopening a source/window.",
            "State whether full-system Win/Loss is currently claimable.",
        ],
    }


def print_text(manifest: dict[str, Any]) -> None:
    status = manifest.get("status")
    print(f"NEXUS_RESEARCH_PREFLIGHT={status}")

    if status != "PASS":
        print(f"reason={manifest.get('reason')}")
        for item in manifest.get("missing", []):
            print(f"missing={item}")
        return

    active = manifest["active_rq"]
    workstream = manifest.get("active_workstream") or {}
    canonical = manifest["canonical"]
    coverage = manifest["coverage"]
    skill_freeze = manifest.get("skill_freeze") or {}

    print(f"project={manifest.get('project')}")
    print(f"state_updated_at={manifest.get('state_updated_at')}")
    print(f"completed_checkpoint={manifest.get('completed_checkpoint')}")
    print(f"state_scope={manifest.get('state_scope')}")
    print(f"state_reconciliation={manifest.get('state_reconciliation')}")
    print(f"queue_state={manifest.get('queue_state')}")
    print(f"last_closed_id={manifest.get('last_closed_id')}")
    print(
        "active_workstream="
        f"{workstream.get('id')} | {workstream.get('status')} | {workstream.get('updated_at')}"
    )
    print(f"active_rq={active.get('id')} | {active.get('status')}")
    print(f"active_worksheet={active.get('worksheet')}")
    print(f"latest_checkpoint={active.get('latest_checkpoint')}")
    print(
        "canonical_claims="
        f"{canonical.get('active_claims')} active / {canonical.get('total_claims')} total"
    )
    print(
        "source_coverage="
        f"{coverage.get('entries')} entries | {coverage.get('status_counts')}"
    )
    verified_skills = skill_freeze.get("verified") or []
    print(
        "skill_freeze="
        f"{skill_freeze.get('manifest_status')} | {len(verified_skills)} skill(s) verified"
    )

    blocked = manifest.get("blocked_from_claiming") or []
    if blocked:
        print("blocked_from_claiming=" + "; ".join(str(x) for x in blocked))

    print("--- REQUIRED READ MANIFEST ---")
    for item in manifest.get("required_files", []):
        print(f"{item['sha256']}  {item['path']}")

    print("--- NEXT STEPS ---")
    for index, step in enumerate(manifest.get("next_steps", []), start=1):
        print(f"{index}. {step}")

    print("--- COMPREHENSION GATE ---")
    for gate in manifest.get("comprehension_gate", []):
        print(f"- {gate}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and summarize the restart-safe NEXUS XAU research context."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the preflight manifest as JSON instead of text.",
    )
    args = parser.parse_args()

    try:
        manifest = build_manifest()
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        manifest = {
            "status": "FAIL",
            "reason": "PREFLIGHT_EXCEPTION",
            "error": str(exc),
            "missing": [],
        }

    if args.json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print_text(manifest)

    return 0 if manifest.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
