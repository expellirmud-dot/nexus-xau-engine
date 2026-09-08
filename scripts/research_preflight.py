from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CORE_PATHS = [
    Path("AGENTS.md"),
    Path("PROJECT_BOOTSTRAP.md"),
    Path("skills/nexus-xau-research/SKILL.md"),
    Path("docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md"),
    Path("TOOLS.md"),
    Path("docs/CURRENT_RESEARCH_STATE.json"),
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

    state = load_json(state_path)
    queue = load_json(queue_path)
    canonical = load_json(canonical_path)
    ledger = load_json(ledger_path)

    active = queue.get("active") or {}
    if not isinstance(active, dict):
        raise TypeError("research_queue/QUEUE.json -> active must be an object")

    active_worksheet = resolve_repo_path(active.get("worksheet"))
    latest_checkpoint = resolve_repo_path(
        active.get("latest_checkpoint")
        or active.get("checkpoint_ref")
        or state.get("rq009_source_gap_closure", {}).get("checkpoint_ref")
    )

    dynamic_required: list[Path] = [ROOT / p for p in CORE_PATHS]
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
        "blocked_from_claiming": blocked,
        "next_steps": next_steps[:5],
        "required_files": manifest_files,
        "missing": missing_dynamic,
        "comprehension_gate": [
            "State the active RQ and worksheet.",
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
    canonical = manifest["canonical"]
    coverage = manifest["coverage"]

    print(f"project={manifest.get('project')}")
    print(f"state_updated_at={manifest.get('state_updated_at')}")
    print(f"completed_checkpoint={manifest.get('completed_checkpoint')}")
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
