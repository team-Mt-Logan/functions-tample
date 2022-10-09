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

ローカルで実行する場合は BigQuery に挿入する部分で GCP の認証情報が必要になります。
すでにサービスアカウントが存在している場合は 3 までスキップしてください。

### 1.サービスアカウント作成

https://console.cloud.google.com/projectselector/iam-admin/serviceaccounts/create?supportedpurview=project&hl=ja&_ga=2.143226551.363152718.1665190539-1430318064.1642063974&_gac=1.47845077.1665217994.CjwKCAjwv4SaBhBPEiwA9YzZvIghgnpH4pSJUELtYn340-XgDWZ7GJDELJlQqKmfCpeOjiHrsZ1BUBoCctgQAvD_BwE

1. プロジェクトを選択します。
2. [サービス アカウント名] フィールドに名前を入力します。Google Cloud コンソールでは、この名前に基づいて [サービス アカウント ID] フィールドに値が設定されます。

3. [サービス アカウントの説明] フィールドに説明を入力します。例: Service account for bigquery writer
4. [作成して続行] をクリックします。
5. [ロールを選択] リストでロールを選択し、[BigQuery データ編集者]を選択します
6. [続行] をクリックします。
7. [完了] をクリックして、サービス アカウントの作成を完了します。

### 2.サービスアカウントキーを作成

サービス アカウント キーを作成します。

1. Google Cloud コンソールで、作成したサービス アカウントのメールアドレスをクリックします。
2. [キー] をクリックします。
3. [鍵を追加]、[新しい鍵を作成] の順にクリックします。
4. [作成] をクリックします。JSON キーファイルがパソコンにダウンロードされます。
5. [閉じる] をクリックします。
6. 作成したキーファイルを作成する`main.py` があるディレクトリに`credential.json` として保存します。

## 環境変数のエクスポート

環境変数 `GOOGLE_APPLICATION_CREDENTIALS` を、サービス アカウント キーが含まれる JSON ファイルのパスに設定します。 この変数は現在のシェル セッションにのみ適用されるため、新しいセッションを開く場合は、変数を再度設定します。

```bash
export GOOGLE_APPLICATION_CREDENTIALS="credential.json"
```

## デプロイ

以下のコマンドを実行してデプロイします。

# テンプレートリポジトリに含まれていないもの

- Pub/Sub を利用した Bigquery Subscription
- CD flow: GitHub Action
