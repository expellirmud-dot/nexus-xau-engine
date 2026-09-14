from pathlib import Path

p = Path(r"D:\nexus-xau-engine-repo\scripts\research_preflight.py")
s = p.read_text(encoding="utf-8")

# Normalize CORE_PATHS and add skills freeze files.
old = '''CORE_PATHS = [
    Path("AGENTS.md"),
    Path("PROJECT_BOOTSTRAP.md"),
    Path("docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md"),
    Path("skills/nexus-xau-research/SKILL.md"),
    Path("docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md"),
    Path("TOOLS.md"),
    Path("docs/CURRENT_RESEARCH_STATE.json"),
    Path("docs/0700_WORKSTREAM_STATE.json"),
    Path("docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md"),
    Path("docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json"),
    Path("docs/SOURCE_COVERAGE_LEDGER.json"),
    Path("research_queue/QUEUE.json"),
]
'''
new = '''CORE_PATHS = [
    Path("AGENTS.md"),
    Path("PROJECT_BOOTSTRAP.md"),
    Path("docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md"),
    Path("skills/README.md"),
    Path("skills/SKILLS_MANIFEST.json"),
    Path("skills/nexus-xau-research/SKILL.md"),
    Path("docs/NEXUS_PROJECT_MAINTENANCE_POLICY.md"),
    Path("TOOLS.md"),
    Path("docs/CURRENT_RESEARCH_STATE.json"),
    Path("docs/0700_WORKSTREAM_STATE.json"),
    Path("docs/CANONICAL_CLAIM_REGISTER_2026-09-03.json"),
    Path("docs/SOURCE_COVERAGE_LEDGER.json"),
    Path("research_queue/QUEUE.json"),
]
'''
if old not in s:
    raise SystemExit("CORE_PATHS block not found")
s = s.replace(old, new)

marker = '''def sha256_prefix(path: Path, length: int = 12) -> str:
'''
helper = '''def validate_skill_freeze(skill_manifest: dict[str, Any]) -> dict[str, Any]:
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


'''
if helper not in s:
    s = s.replace(marker, helper + marker)

# Load skill manifest and validate before state consistency.
old = '''    workstream_path = ROOT / "docs/0700_WORKSTREAM_STATE.json"

    state = load_json(state_path)
    queue = load_json(queue_path)
    canonical = load_json(canonical_path)
    ledger = load_json(ledger_path)
    workstream = load_json(workstream_path)

    consistency = validate_state_consistency(
'''
new = '''    workstream_path = ROOT / "docs/0700_WORKSTREAM_STATE.json"
    skill_manifest_path = ROOT / "skills/SKILLS_MANIFEST.json"

    state = load_json(state_path)
    queue = load_json(queue_path)
    canonical = load_json(canonical_path)
    ledger = load_json(ledger_path)
    workstream = load_json(workstream_path)
    skill_manifest = load_json(skill_manifest_path)

    skill_freeze = validate_skill_freeze(skill_manifest)
    if skill_freeze.get("status") != "PASS":
        return skill_freeze

    consistency = validate_state_consistency(
'''
if old not in s:
    raise SystemExit("load block not found")
s = s.replace(old, new)

# Add skill freeze to returned manifest.
old = '''        "coverage": {
            "updated_at": ledger.get("updated_at"),
            "entries": len(coverage_entries),
            "status_counts": dict(sorted(coverage_status_counts.items())),
        },
        "blocked_from_claiming": blocked,
'''
new = '''        "coverage": {
            "updated_at": ledger.get("updated_at"),
            "entries": len(coverage_entries),
            "status_counts": dict(sorted(coverage_status_counts.items())),
        },
        "skill_freeze": skill_freeze,
        "blocked_from_claiming": blocked,
'''
if old not in s:
    raise SystemExit("return block not found")
s = s.replace(old, new)

# Print skill freeze summary.
old = '''    coverage = manifest["coverage"]

    print(f"project={manifest.get('project')}")
'''
new = '''    coverage = manifest["coverage"]
    skill_freeze = manifest.get("skill_freeze") or {}

    print(f"project={manifest.get('project')}")
'''
if old not in s:
    raise SystemExit("print vars block not found")
s = s.replace(old, new)

old = '''    print(
        "source_coverage="
        f"{coverage.get('entries')} entries | {coverage.get('status_counts')}"
    )

    blocked = manifest.get("blocked_from_claiming") or []
'''
new = '''    print(
        "source_coverage="
        f"{coverage.get('entries')} entries | {coverage.get('status_counts')}"
    )
    verified_skills = skill_freeze.get("verified") or []
    print(
        "skill_freeze="
        f"{skill_freeze.get('manifest_status')} | {len(verified_skills)} skill(s) verified"
    )

    blocked = manifest.get("blocked_from_claiming") or []
'''
if old not in s:
    raise SystemExit("print coverage block not found")
s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
print("patched", p)
