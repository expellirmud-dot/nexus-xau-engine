import json
from pathlib import Path
p=Path(r"D:\nexus-xau-engine-repo\research_queue\QUEUE.json")
d=json.loads(p.read_text(encoding="utf-8"))
for item in d["items"]:
    if item.get("id")=="RQ-012":
        print(json.dumps(item,ensure_ascii=False,indent=2))
