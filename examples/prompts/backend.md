# Backend

変更できるのは `examples/task_manager/main.py` だけです。FastAPI lifespanでテーブルを初期化し、未知のフィールドと型変換を拒否します。POST成功は201、PATCH成功は200、DELETE成功は204、データなしは404、不正入力は422です。PATCHで省略された項目は元の値を維持し、明示的なnullは拒否します。descriptionは空にできます。Database担当が所有するファイルは変更しません。
