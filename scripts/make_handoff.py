#!/usr/bin/env python3
"""読者用成績実装に対応する引き継ぎ収書の例を作成する。"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "examples/grades.py"
record = {
    "task_id": "grade-api-v1", "from": "developer", "to": "qa",
    "completed": "成績の契約と参考実装を用意しました", "next": "順位と入力検証の回帰テストを実行してください",
    "artifacts": [{"path": "examples/grades.py", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}],
}
out = ROOT / "reports/handoff.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out)
