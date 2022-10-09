# functions-tamplate

このリポジトリは Cloud functions を用いてデータを取得し BigQuery に挿入するコードのテンプレートです。

## 使い方

このリポジトリはテンプレートリポジトリとなっています。

[テンプレートからリポジトリを作成する](https://docs.github.com/ja/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template)
を参考にリポジトリを利用してください。

このリポジトリに直接書き込むことは NG です。

# 環境構築

# GCP の環境設定

## BigQuery データセットとテーブルの作成

挿入するデータの BigQuery データセットとテーブルを定義します。

1. テーブルのデータスキーマを json 形式で定義する

名前をつけて [./schema](./schema/)に保存しておくことを推奨します。

例)

```json
[
  {
    "name": "timestamp",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
```

参考資料：
[Google 標準 SQL データ型](https://cloud.google.com/bigquery/docs/schemas?hl=ja)

2. BigQuery のページに行き、プロジェクトの右端にある３点リーダーをクリックしてデータセットを作成する

3. 作成したデータセットの３点リーダーをクリックし「テーブルを作成」をクリック。

テーブルにはテーブル名を入力。その他はデフォルトで OK。
スキーマの部分で「テキストとして編集」をアクティブにします。
入力ボックスには 1 で作成した json 形式のテキストをペーストします。

テーブルが作成されれば OK。
問題があった場合は json の形式が間違っていないか確認してください。

# 実装手順

## 推奨環境

|        |     |
| ------ | --- |
| Python | 3.9 |

## 依存関係の管理について

シンプルに利用するため `requrement.txt` に直で記録しています。
使いやすさに応じて[poetry](https://cocoatomo.github.io/poetry-ja/)などでの管理も良いです。

# 前提：

Logan のプロジェクトはつくられている状態。
ローガンの中で新規につくる。

プロジェクト ID がどこから取ってくるのか？
テーブル名だとどこからとってくるのか？
サービスアカウントってなにか？

新規プロジェクトの立ち上げ方。
初心者がやるイメージ。
クローンしているかどうか？

1. BigQuery のテーブルの作り方から

`timestamp`

2. 修正箇所の記載
3.

- pubsub はいれない。
- GitHub Acrions もいれない
