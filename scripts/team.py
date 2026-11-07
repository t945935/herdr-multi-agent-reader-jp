#!/usr/bin/env python3
"""起動済みのidle Agentへ一度配分し、タスク固有の収書を検証する。"""

import argparse
import json
import os
import subprocess
import uuid
from pathlib import Path


def call(*args, timeout=310):
    done = subprocess.run(["herdr", *args], text=True, capture_output=True, timeout=timeout)
    if done.returncode:
        raise RuntimeError(done.stderr or done.stdout)
    return json.loads(done.stdout)["result"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("prompt", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if os.environ.get("HERDR_ENV") != "1":
        raise SystemExit("Herdrが管理するPane内で実行してください")
    agent = call("agent", "get", args.target)["agent"]
    if agent["agent_status"] not in {"idle", "done"}:
        raise SystemExit("タスク開始前にAgentをidle／doneにしてください")
    path = args.output.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise SystemExit("過去のタスクと同じ収書パスは使わず、新しいパスを指定してください")
    task_id = uuid.uuid4().hex
    prompt = args.prompt.read_text(encoding="utf-8") + (
        f"\n\n今回のtask_id={task_id}\ncompletion_path={path}\n"
        '実作業の後にJSONを保存してください：{"task_id":"上記のID","status":"completed",'
        '"summary":"具体的な成果と検証","artifacts":["実際の成果ファイルパス"]}。'
        "完了できない場合はstatusをblockedにし、summaryに理由を書いてください。別のAgentを起動しないでください。"
    )
    settled = call("agent", "prompt", args.target, prompt, "--wait", "--timeout", "300000")
    state = settled["agent"]["agent_status"]
    if state not in {"idle", "done"} or not path.is_file():
        raise SystemExit("受理可能な収書なしでAgentが停止しました。agent get/readで状態を確認してください")
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("task_id") != task_id or receipt.get("status") != "completed" or not receipt.get("summary"):
        raise SystemExit("収書が今回のタスクを完了として示していません")
    for artifact in receipt.get("artifacts", []):
        candidate = Path(artifact)
        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate
        if not candidate.is_file():
            raise SystemExit(f"成果ファイルがありません: {artifact}")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
