"""主張と出典の根拠を検査し、追跡可能なレポートを生成する。"""

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


def validate(data):
    if not isinstance(data, dict) or not data.get("question"):
        raise ValueError("調査の問いが必要です")
    sources = data.get("sources", [])
    if not isinstance(sources, list) or not sources:
        raise ValueError("出典が必要です")
    by_id = {}
    for source in sources:
        if not {"id", "url", "title", "accessed", "kind"} <= source.keys():
            raise ValueError("出典情報が不足しています")
        parsed = urlparse(source["url"])
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("出典URLはHTTP(S)で指定してください")
        if source["id"] in by_id:
            raise ValueError("出典IDが重複しています")
        by_id[source["id"]] = source
    claims = data.get("claims", [])
    if not claims:
        raise ValueError("主張が必要です")
    for claim in claims:
        if not claim.get("text") or claim.get("status") not in {"supported", "uncertain", "conflict"}:
            raise ValueError("主張の形式が正しくありません")
        evidence = claim.get("evidence", [])
        if claim["status"] == "supported" and not evidence:
            raise ValueError("supportedの主張には根拠が必要です")
        for item in evidence:
            if item.get("source") not in by_id or not item.get("quote"):
                raise ValueError("根拠には既知の出典と引用が必要です")
    return by_id


def render(data):
    sources = validate(data)
    lines = ["# " + data["question"], "", "## 結論と根拠", ""]
    for claim in data["claims"]:
        lines.extend([f"### {claim['text']}", "", "状態：" + claim["status"], ""])
        for evidence in claim.get("evidence", []):
            source = sources[evidence["source"]]
            lines.extend([f"> {evidence['quote']}", "", f"出典：[{source['title']}]({source['url']})", ""])
    lines.extend(["## 出典一覧", ""])
    for source in sources.values():
        lines.append(f"- {source['id']}：[{source['title']}]({source['url']})；{source['kind']}；閲覧日 {source['accessed']}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = render(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(args.output)
