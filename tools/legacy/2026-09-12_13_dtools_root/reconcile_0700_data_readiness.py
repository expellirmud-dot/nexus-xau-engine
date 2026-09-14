import json
from pathlib import Path

root = Path(r"D:\nexus-xau-engine-repo")
primary = "docs/0700_DATA_SUFFICIENCY_AND_TEST_STRATEGY_2026-09-13.md"
duplicate = "docs/0700_HISTORICAL_DATA_READINESS_AND_TEST_STRATEGY_2026-09-13.md"

p = root / primary
s = p.read_text(encoding="utf-8")
if "## 9. Consolidated MT5 2026 audit" not in s:
    s += """

## 9. Consolidated MT5 2026 audit

The broader broker-side file was audited directly:

data/raw/XAUUSDm_M1_MT5_2026-05-26_2026-09-01.csv

Observed:

- M1 rows: 97,341
- first timestamp: 2026-05-26 00:00 UTC
- last timestamp: 2026-09-01 23:59 UTC
- unique dates containing data: 85
- exact 00:00 UTC bars, corresponding to the project 07:00 Thailand boundary: 71

Existing native-MT5 resample validation for the same consolidated range:

- M5 local/native mismatch: 0
- H1 local/native mismatch: 0
- H4 local/native mismatch: 0
- D1 local/native mismatch: 0

Existing native counts:

- M5: 19,500
- H1: 1,625
- H4: 438
- D1: 85

This strengthens the classification:

BROKER-SPECIFIC ENGINEERING / CROSS-FEED / REAL-STATE STRESS TEST

It remains non-pristine and bar-based rather than final tick/Bid+Ask execution evidence.

## 10. Required day-level replay output

Every V2 07:00 day should end in an explicit state, including non-trades.

At minimum record:

- 07:00 known_at;
- feed/dataset identity and hash;
- eligible H4 origins;
- origin ambiguity state;
- consumed ratio;
- remaining points;
- point-check status;
- Daily Frame/location status;
- PAT2 FULL-RANGE confirmation status;
- ENTER_CANDIDATE, PASS, UNKNOWN, or DATA_EXCLUDED;
- reason code;
- unseen-state fingerprint/category when applicable;
- outcome fields only after the scoring phase.

The project must learn from WHY WE DID NOT TRADE as well as from post-entry outcomes.
"""
    p.write_text(s, encoding="utf-8")

p = root / "docs" / "0700_WORKSTREAM_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["latest_checkpoint"] = primary
dr = d.get("data_readiness") or {}
dr["checkpoint"] = primary
d["data_readiness"] = dr
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

p = root / "docs" / "CURRENT_RESEARCH_STATE.json"
d = json.loads(p.read_text(encoding="utf-8"))
aw = d.get("active_0700_workstream") or {}
aw["latest_checkpoint"] = primary
d["active_0700_workstream"] = aw
loop = d.get("research_loop") or {}
lo = [x for x in (loop.get("load_order") or []) if x != duplicate]
if primary not in lo:
    lo.insert(8 if len(lo) >= 8 else len(lo), primary)
loop["load_order"] = lo
d["research_loop"] = loop
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

p = root / "research_queue" / "active" / "RQ-013_0700_EXISTING_KNOWLEDGE_REANCHOR.md"
s = p.read_text(encoding="utf-8").replace(duplicate, primary)
p.write_text(s, encoding="utf-8")

p = root / "scripts" / "research_preflight.py"
s = p.read_text(encoding="utf-8")
needle = '    Path("docs/0700_OPERATING_PHILOSOPHY_AND_SUCCESS_CRITERIA_2026-09-13.md"),\n'
first = s.find(needle)
second = s.find(needle, first + len(needle)) if first != -1 else -1
if second != -1:
    s = s[:second] + s[second + len(needle):]
p.write_text(s, encoding="utf-8")

print("reconciled single data-readiness authority")
