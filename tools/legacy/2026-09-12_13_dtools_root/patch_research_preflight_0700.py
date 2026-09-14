from pathlib import Path

p = Path(r"D:\nexus-xau-engine-repo\scripts\research_preflight.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "import json\nfrom collections import Counter\n",
    "import json\nfrom collections import Counter\nfrom datetime import datetime\n"
)

s = s.replace(
    "    Path(\"docs/CURRENT_RESEARCH_STATE.json\"),\n",
    "    Path(\"docs/CURRENT_RESEARCH_STATE.json\"),\n    Path(\"docs/0700_WORKSTREAM_STATE.json\"),\n"
)

marker = "def sha256_prefix(path: Path, length: int = 12) -> str:\n"
helper = '''def parse_iso_datetime(value: object) -> datetime | None:
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
) -> dict[str, Any]:
    active = queue.get("active") or {}
    active_0700 = state.get("active_0700_workstream") or {}
    workstream_question = workstream.get("active_question") or {}

    queue_rq = active.get("id") if isinstance(active, dict) else None
    state_rq = (
        active_0700.get("active_rq")
        if isinstance(active_0700, dict)
        and str(active_0700.get("status", "")).upper() == "ACTIVE"
        else None
    )
    workstream_rq = (
        workstream_question.get("rq_id")
        if isinstance(workstream_question, dict)
        else None
    )

    rq_values = [value for value in (queue_rq, state_rq, workstream_rq) if value]
    if rq_values and len(set(rq_values)) != 1:
        return {
            "status": "FAIL",
            "reason": "ACTIVE_WORKSTREAM_RQ_MISMATCH",
            "queue_active_rq": queue_rq,
            "state_active_rq": state_rq,
            "workstream_active_rq": workstream_rq,
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
    }


'''
if helper not in s:
    s = s.replace(marker, helper + marker)

s = s.replace(
    '    ledger_path = ROOT / "docs/SOURCE_COVERAGE_LEDGER.json"\n',
    '    ledger_path = ROOT / "docs/SOURCE_COVERAGE_LEDGER.json"\n    workstream_path = ROOT / "docs/0700_WORKSTREAM_STATE.json"\n'
)

s = s.replace(
    "    ledger = load_json(ledger_path)\n\n    active = queue.get(\"active\") or {}\n",
    "    ledger = load_json(ledger_path)\n    workstream = load_json(workstream_path)\n\n"
    "    consistency = validate_state_consistency(\n"
    "        state=state,\n"
    "        queue=queue,\n"
    "        canonical=canonical,\n"
    "        ledger=ledger,\n"
    "        workstream=workstream,\n"
    "    )\n"
    "    if consistency.get(\"status\") != \"PASS\":\n"
    "        return consistency\n\n"
    "    active = queue.get(\"active\") or {}\n"
)

s = s.replace(
    '        "active_rq": {\n',
    '        "active_workstream": {\n'
    '            "id": workstream.get("workstream"),\n'
    '            "status": workstream.get("status"),\n'
    '            "updated_at": workstream.get("updated_at"),\n'
    '            "active_rq": (workstream.get("active_question") or {}).get("rq_id")\n'
    '            if isinstance(workstream.get("active_question"), dict)\n'
    '            else None,\n'
    '        },\n'
    '        "active_rq": {\n'
)

s = s.replace(
    '            "State the active RQ and worksheet.",\n',
    '            "State the active 07:00 workstream and active RQ/worksheet.",\n'
)

s = s.replace(
    '    active = manifest["active_rq"]\n',
    '    active = manifest["active_rq"]\n    workstream = manifest.get("active_workstream") or {}\n'
)

s = s.replace(
    '    print(f"active_rq={active.get(\'id\')} | {active.get(\'status\')}")\n',
    '    print(\n'
    '        "active_workstream="\n'
    '        f"{workstream.get(\'id\')} | {workstream.get(\'status\')} | {workstream.get(\'updated_at\')}"\n'
    '    )\n'
    '    print(f"active_rq={active.get(\'id\')} | {active.get(\'status\')}")\n'
)

p.write_text(s, encoding="utf-8")
print("patched", p)
