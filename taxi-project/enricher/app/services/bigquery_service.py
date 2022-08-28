import datetime
import json
import os

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account


class BiqQueryClient:
    SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

    def __init__(self, credentials_file_path: str, default_table_id: str = None):
        credentials = service_account.Credentials.from_service_account_file(credentials_file_path, scopes=self.SCOPES)
        self.client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        self.default_table_id = default_table_id

    def _get_table_id(self, table_id=None):
        if table_id:
            return table_id
        else:
            if self.default_table_id:
                return self.default_table_id
            else:
                raise Exception("No table defined")

    def _convert_date_on_dict(self, old_dict):
        new_dict = {}
        for k, v in old_dict.items():
            if isinstance(v, datetime.datetime):
                new_dict[k] = v.isoformat()
            else:
                new_dict[k] = v

        return new_dict

    def create_table(self, schema, table_id: str = None):
        table_id = self._get_table_id(table_id)
        try:
            table = self.client.get_table(table_id)
            print("Table {} already exists.".format(table_id))
        except NotFound:
            table = bigquery.Table(table_id, schema=schema)
        return self.client.create_table(table)

    def insert_row(self, row: dict):
        data = self._convert_date_on_dict(row)
        self.client.insert_rows_json(self._get_table_id(), [data])


bq = BiqQueryClient(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), os.getenv('BIGQUERY_TABLE_ID'))

#
# def insert_receipt(json_rows):
#     # table = client.get_table(config.properties['AUDIT_LOGS_TABLE'])
#     errors = client.insert_rows_json(table, [json_rows])
#
#     if errors:
#         # logging.exception('Error during saving rows to the BigQuery...', errors)
#         return {"detail": {"status": "error", "message": "Oops, something went wrong. Try again in a moment."}}
#
#     return {"detail": {"status": "error", "message": "log successfully saved"}}
