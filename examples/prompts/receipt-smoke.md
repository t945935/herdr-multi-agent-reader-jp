# ローカル実装の検収：読み取り専用確認

`examples/calculator.py` を読み、外部公開されている四つの関数名とゼロ除算時の例外を確認してください。プログラム、テスト、章原稿を変更せず、別のAgentも呼び出さないでください。

Managerが指定するcompletion_pathに完了JSONを書き込みます。summaryには実際に確認した関数名と例外を記載し、artifactsには `examples/calculator.py` の絶対パスを記載してください。書き込める完了記録はこの一つだけです。ファイルを読めない場合はblockedと報告し、内容を捏造しないでください。
