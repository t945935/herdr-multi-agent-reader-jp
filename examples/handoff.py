"""明示的な引き継ぎ記録を検証する。Agentの文章だけを信用しない。"""

import argparse
import hashlib
import json
from pathlib import Path


def validate(record, root):
    required = {"task_id", "from", "to", "completed", "next", "artifacts"}
    if not isinstance(record, dict) or not required <= record.keys():
        raise ValueError("引き継ぎに必要な項目が不足しています")
    if any(not isinstance(record[key], str) or not record[key].strip()
           for key in ["task_id", "from", "to", "completed", "next"]):
        raise ValueError("引き継ぎの文字列項目は空にできません")
    if not isinstance(record["artifacts"], list) or not record["artifacts"]:
        raise ValueError("引き継ぎには成果物が必要です")
    root = Path(root).resolve()
    for artifact in record["artifacts"]:
        if not isinstance(artifact, dict) or set(artifact) != {"path", "sha256"}:
            raise ValueError("成果物にはpathとsha256が必要です")
        path = (root / artifact["path"]).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError("成果物はプロジェクト内のファイルでなければなりません")
        if hashlib.sha256(path.read_bytes()).hexdigest() != artifact["sha256"]:
            raise ValueError("成果物のハッシュが一致しません")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    validate(json.loads(args.record.read_text(encoding="utf-8")), args.root)
    print("引き継ぎを検証しました")
