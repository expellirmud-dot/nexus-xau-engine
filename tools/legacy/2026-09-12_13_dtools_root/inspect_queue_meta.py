import json
from pathlib import Path
p=Path(r"D:\nexus-xau-engine-repo\research_queue\QUEUE.json")
d=json.loads(p.read_text(encoding="utf-8"))
print(json.dumps({k:v for k,v in d.items() if k not in ("items",)},ensure_ascii=False,indent=2))
