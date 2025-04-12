# フォルダ名翻訳ツール

DeepL APIを使用して、フォルダ名とファイル名を日本語に翻訳するGUIアプリケーションです。

## 機能

- フォルダとファイルの名前を日本語に翻訳
- GUIによる簡単な操作
- 翻訳のプレビュー機能
- 進行状況のプログレスバー表示

## 必要条件

- Python 3.x
- DeepL API キー

## インストール

1. リポジトリをクローン
```bash
git clone https://github.com/yourusername/folder-translator.git
cd folder-translator
```

2. 必要なパッケージをインストール
```bash
pip install -r requirements.txt
```

## 使用方法

1. アプリケーションを起動
```bash
python folder_translator.py
```

2. GUIで以下の操作を行います：
   - フォルダ選択ボタンで対象フォルダを選択
   - DeepL API Keyを入力
   - プレビューボタンで翻訳結果を確認
   - 実行ボタンで名前の変更を実施

## 注意事項

- フォルダ名やファイル名の変更前に、必ずプレビューで内容を確認してください
- 変更できない文字が含まれる場合は、エラーメッセージが表示されます
- ネットワーク接続が必要です

## ライセンス

MIT License