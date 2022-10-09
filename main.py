
import datetime
import os
from os.path import join, dirname
import requests

from typing import Union

from dotenv import load_dotenv

from libs.bigquery import Bigquery

# dotenv を用いて .env のファイルを読み込みます
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(verbose=True)
load_dotenv(dotenv_path)


# 環境変数の読み込み。ローカルでは .env に書かれた値が入る
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET = os.environ.get("DATASET")
TABLE = os.environ.get("TABLE")


def get_source():
    """
    APIやwebページを叩いて必要なデータを取得して返す関数。
    命名はシチュエーションに応じて変更してください。
    requests でなくてその他のライブラリを用いても問題ありません。
    """
    # 例: GitHub REST API で、Requests のリポジトリをJSON形式で取得する
    r = requests.get("http://api.github.com/repos/psf/requests")
    return r.json()


def parse(data: Union[dict, list[dict]]):
    """
    取得したデータを必要なデータ形式に整形するリポジトリです。
    要件に応じて必要なデータを取得したり、調整して返してください。
    返り値はBigQuery の挿入形式にあわせた dicts の list もしくは tuplesである必要があります。
    詳細は公式ドキュメントを参考にしてください。
    https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_insert_rows
    """
    parsed_data:  dict[str, Union[str, dict[str, Union[dict, list]]]] = {}

    # ここの変換処理を書く
    parsed_data["name"] = data["name"]
    parsed_data["timestamp"] = datetime.datetime.now()

    return [parsed_data]


def main(event=None, context=None):
    """
    Cloud functions で呼びだされる関数です。
    また引数の(event=None, context=None)はイベント駆動のCloud functions では必須の引数になります。
    利用しない場合でも消さないでください。
    """

    # get data
    data = get_source()

    # parse
    parsed_data = parse(data)

    # publish data to bigquery
    bq = Bigquery(project_id=PROJECT_ID, dataset=DATASET, table_id=TABLE)
    bq.insert(parsed_data)


if __name__ == "__main__":
    main()
