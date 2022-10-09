
from xmlrpc.client import Boolean
from google.cloud import bigquery
from google.api_core import exceptions
import json


class Bigquery():
    """
    BigQuery の操作に関するクラス
    """

    def __init__(self, project_id, dataset, table_id):
        self.client = bigquery.Client()
        self.table_path = self.client.get_table(
            f'{project_id}.{dataset}.{table_id}')

    def insert(self, data) -> None:
        try:
            self.client.insert_rows(self.table_path, data)
        except exceptions.BadRequest as e:
            self.log(
                "ERROR", f'failed to publish bq: {e}, request: {data}')

        self.log("INFO",
                 f'success insertion {len(data)} rows to ${self.table_path} ')

    def log(severity, message):
        print(json.dumps(dict(severity=severity, message=message)))
