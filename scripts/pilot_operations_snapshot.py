from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from research_preflight import build_manifest

from nexus_xau.reporting.pilot_operations import (
    archive_health_check,
    build_pilot_operations_snapshot,
    collector_health_check,
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise TypeError(f"expected JSON object: {path}")
    return payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_text(repo_root: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _git_identity(repo_root: Path) -> dict[str, Any]:
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "head": _git_text(repo_root, "rev-parse", "HEAD"),
        "branch": _git_text(repo_root, "rev-parse", "--abbrev-ref", "HEAD"),
        "origin_main": _git_text(repo_root, "rev-parse", "origin/main"),
        "working_tree_clean": status.returncode == 0 and not status.stdout.strip(),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a non-executing Phase 1 pilot operations snapshot."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--mode", choices=("governance", "live", "archive"), default="governance"
    )
    parser.add_argument(
        "--collector-status",
        type=Path,
        default=Path("results/mt5_collector/status.json"),
    )
    parser.add_argument("--archive-window-status")
    parser.add_argument("--archive-error-code")
    parser.add_argument("--rollback-commit")
    parser.add_argument("--rollback-checkpoint")
    parser.add_argument("--rollback-note")
    parser.add_argument("--out", type=Path, required=True)
    return parser

def main() -> int:
    args = _parser().parse_args()
    repo_root = args.repo_root.resolve()

    state_path = repo_root / "docs/CURRENT_RESEARCH_STATE.json"
    readiness_path = repo_root / "docs/PHASE1_READINESS_MATRIX.json"
    registry_path = repo_root / "docs/PHASE1_UNKNOWN_CLASSIFICATION_REGISTRY_V0.1.json"
    workstream_path = repo_root / "docs/0700_WORKSTREAM_STATE.json"

    state = _load_json(state_path)
    readiness = _load_json(readiness_path)
    registry = _load_json(registry_path)
    workstream = _load_json(workstream_path)
    minimal_v2 = workstream.get("minimal_v2")
    project_version = (
        str(minimal_v2.get("version", ""))
        if isinstance(minimal_v2, dict)
        else ""
    )

    if args.mode == "live":
        collector_path = (
            args.collector_status
            if args.collector_status.is_absolute()
            else repo_root / args.collector_status
        )
        collector_payload = (
            _load_json(collector_path) if collector_path.exists() else None
        )
        health_checks = [
            collector_health_check(collector_payload, required_live=True)
        ]
    elif args.mode == "archive":
        health_checks = [
            archive_health_check(
                window_status=args.archive_window_status,
                error_code=args.archive_error_code,
                required=True,
            )
        ]
    else:
        health_checks = [collector_health_check(None, required_live=False)]

    rollback_reference = None
    if args.rollback_commit or args.rollback_checkpoint or args.rollback_note:
        rollback_reference = {
            "git_commit": args.rollback_commit,
            "checkpoint": args.rollback_checkpoint,
            "note": args.rollback_note,
        }

    snapshot = build_pilot_operations_snapshot(
        state=state,
        readiness=readiness,
        registry=registry,
        preflight=build_manifest(),
        health_checks=health_checks,
        git_identity=_git_identity(repo_root),
        project_version=project_version,
        state_sha256=_sha256(state_path),
        registry_sha256=_sha256(registry_path),
        observed_at_utc=datetime.now(UTC).isoformat(timespec="seconds"),
        rollback_reference=rollback_reference,
    )

    out = args.out if args.out.is_absolute() else repo_root / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(snapshot, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())