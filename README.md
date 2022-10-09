# functions-tamplate

このリポジトリは Cloud functions を用いてデータを取得し BigQuery に挿入するコードのテンプレートです。

## 使い方

このリポジトリはテンプレートリポジトリとなっています。

[テンプレートからリポジトリを作成する](https://docs.github.com/ja/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template)
を参考にリポジトリを利用してください。

このリポジトリに直接書き込むことは原則 NG です。

# 環境構築

# GCP の環境設定

## BigQuery データセットとテーブルの作成

挿入するデータの BigQuery データセットとテーブルを定義します。

### 1. テーブルのデータスキーマを json 形式で定義する

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

名前をつけて [./schema](./schema/)に保存しておくことを推奨します。

参考資料：
[Google 標準 SQL データ型](https://cloud.google.com/bigquery/docs/schemas?hl=ja)

### 2.データセットの作成

BigQuery のページに行き、プロジェクトの右端にある３点リーダーをクリックしてデータセットを作成する

### 3.テーブルの作成

作成したデータセットの３点リーダーをクリックし「テーブルを作成」をクリック。

テーブルにはテーブル名を入力。その他はデフォルトで OK。
スキーマの部分で「テキストとして編集」をアクティブにします。
入力ボックスには 1 で作成した json 形式のテキストをペーストします。

テーブルが作成されれば OK。
問題があった場合は json の形式が間違っていないか確認してください。

## スケジューラの作成

### 1.スケジューラのページを開く

以下のリンクを開きます。このとき対象のプロジェクトになっているか確認してください。
https://console.cloud.google.com/cloudscheduler

### 2.ジョブを作成

バー上部の「ジョブを作成」をクリックします

### 2-1.スケジューラの定義

頻度には unix-cron 形式で呼び出される頻度を設定します。
このとき、タイムゾーンは日本にすることを忘れないでください。

### 2-2.実行内容を構成

ターゲットタイプは`Pub/Sub` を指定。

#### 2-2-1.トピックの作成

Cloud Pub/Sub トピックはウィンドウ左下の「トピックを作成」から新たに作成します。
これが functions をトリガーするためのトピックとなります。

メッセージについては今回は利用しないため適当に埋めて問題ないです。

以上の設定が完了したら「作成」をクリックしてスケジューラを作成します。

# 実装

## 推奨環境

|        |     |
| ------ | --- |
| Python | 3.9 |

## 依存関係の管理について

シンプルに利用するため `requrement.txt` に直で記録しています。
使いやすさに応じて[poetry](https://cocoatomo.github.io/poetry-ja/)などでの管理も良いです。

## 実装手順

[./sample/main.py](/sample/main.py) のコメントを参考に必要なデータを取得、整形するコードを書いてください。

### 管渠変数の設定

データセットやテーブルなどプロジェクト固有の環境設定が必要になるため、環境変数を利用します。
`env.example` をコピーして `.env` を作成します。

```bash
cp sample/.env.example sample/.env
```

| キー       | 値                                                                                                           |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| PROJECT_ID | [GCP のダッシュボード](https://console.cloud.google.com/home/dashboard)のプロジェクト情報に記載されている ID |
| DATASET    | [前の手順で作成したデータセット名](2.データセットの作成)                                                     |
| TABLE      | [前の手順で作成したテーブルの ID](#3.テーブルの作成)                                                         |
| TOPIC_ID   | [前の手順で作成したトピックの ID ](#2-2-1.トピックの作成)                                                    |

## ローカルでの実行方法

## デプロイ

# テンプレートリポジトリに含まれていないもの

- Pub/Sub を利用した Bigquery Subscription
- CD flow: GitHub Action
