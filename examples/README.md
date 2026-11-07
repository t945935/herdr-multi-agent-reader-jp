# 例の一覧

すべてのコマンドは読者用パッケージのルートから実行します。Pythonのimportでは `examples.*` を使います。

| テーマ | 実装 | 検収 |
|---|---|---|
| 計算機 | `calculator.py` | 四則演算、ゼロ除算、型境界 |
| 成績システム | `grades.py` | 点数境界、科目不足、同点の競技順位 |
| 引き継ぎ | `handoff.py`、`../scripts/make_handoff.py` | ファイルの存在、プロジェクト範囲、SHA-256 |
| タスク管理サイト | `task_manager/` | CRUD、入力検証、画面、再起動後の永続性 |
| 技術調査 | `research.py` | 主張、出典、引用、不確定状態 |
| 開発パイプライン | `pipeline.py` | 終了コード、タイムアウト、成果物検収、失敗時停止 |
| 復旧可能なキュー | `queue.py` | 重複投入、lease、再起動復旧、dead letter、並行処理 |

セットアップとテストは、パッケージのルートにあるREADMEとrequirements.txtを参照してください。Webサイトを起動するには次を使います。

```bash
.venv/bin/python -m uvicorn examples.task_manager.main:app --host 0.0.0.0 --port 8000
```

Windowsブラウザーでは `http://localhost:8000/` を開きます。真のAgentタスク配分にはHerdrと、インストールおよびログイン済みのAgent CLIが必要です。テストと有限キュー例は有料モデルを呼び出しません。
