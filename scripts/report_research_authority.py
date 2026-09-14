from __future__ import annotations

import argparse
import json
from pathlib import Path

from nexus_xau.governance.research_governance import (
    authority_report_bytes,
    build_authority_report,
    validate_generated_authority_report,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "docs" / "CANONICAL_CLAIM_REGISTER_2026-09-03.json"
DEFAULT_OUTPUT = ROOT / "results" / "governance" / "research_authority.json"


def _load_object(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"Expected JSON object: {path}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify the derived WO-055 research authority report."
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify an existing report against the canonical source without rewriting it.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write deterministic report JSON to stdout instead of a file.",
    )
    args = parser.parse_args()

    canonical = _load_object(args.source)

    if args.check:
        if not args.output.exists():
            print(
                json.dumps(
                    {
                        "status": "FAIL",
                        "reason": "GENERATED_AUTHORITY_VIEW_MISSING",
                        "output": str(args.output),
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
            return 1
        generated = _load_object(args.output)
        result = validate_generated_authority_report(canonical, generated)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("status") == "PASS" else 1

    report = build_authority_report(canonical)
    if report.get("status") != "PASS":
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 1

    raw = authority_report_bytes(canonical)
    if args.stdout:
        print(raw.decode("utf-8"), end="")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    print(
        json.dumps(
            {
                "status": "PASS",
                "output": str(args.output),
                "claim_count": report.get("claim_count"),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
