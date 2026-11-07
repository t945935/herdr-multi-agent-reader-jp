# Developer：成績システムの契約

`examples/grades.py` と `tests/test_contracts.py` の成績関連ケースを先に読んでください。変更してよいのは `examples/grades.py` だけです。既存テストとWebサイトのコードは変更せず、別のAgentも起動しないでください。

契約：科目は国語、英語、数学のちょうど三つです。点数は有限のint／floatとし、bool、文字列、科目不足、余分な科目、0～100の範囲外を拒否します。教材上の契約では平均60点以上を合格とします。生徒が空のリストなら空リストを返します。合計点が丸め前の値で同じ場合は競技順位を使い、入力順を維持します。入力データは変更しません。

`calculate_total`、`calculate_average`、`get_grade`、`rank_students` のインターフェースは維持してください。まず契約と現状を照合し、必要な場合だけ修正します。すでに条件を満たしているなら実装を変更せず、確認結果を説明してください。

`.venv/bin/python -m pytest -q tests/test_contracts.py -k 'ranking or scores'` を実行して検証し、実際のコマンド、終了コード、変更ファイル、未対応事項を `reports/grade-developer.md` に記録してください。Managerが追加するtask_idとcompletion_pathに従って完了収書を作成してください。
