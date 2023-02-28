from django.core.management.base import BaseCommand
from google.cloud import bigquery
from google.cloud import storage
import csv

class Command(BaseCommand):
    help = 'Uploads ads data to GoogleAds table in BigQuery and calculates metrics'

    def add_arguments(self, parser):
        parser.add_argument('credentials', type=str, help='Path to Credentials file')
        parser.add_argument('ads_data', type=str, help="Path to Ads Data File")

    def handle(self, *args, **options):
        # specify the path to your Google Cloud service account credentials file
        credentials_path = options['credentials']
        ads_data_path = options['ads_data']

        # create a BigQuery client instance
        client = bigquery.Client.from_service_account_json(credentials_path)

        # specify the ID of the BigQuery dataset and table to insert data into
        dataset_id = 'BQ1'
        table_id = 'GoogleAds'

        # create a Cloud Storage client instance
        storage_client = storage.Client.from_service_account_json(credentials_path)

        # create a Cloud Storage bucket and upload the ads data file to it
        bucket_name = 'ads_data_bucket'
        bucket = storage_client.create_bucket(bucket_name)
        blob = bucket.blob('ads_data.csv')
        with open(ads_data_path, 'rb') as f:
            blob.upload_from_file(f)

        # create a BigQuery table schema that matches the ads data
        schema = [
            bigquery.SchemaField('Campaign', 'STRING', mode='NULLABLE'),
            bigquery.SchemaField('Clicks', 'INTEGER', mode='NULLABLE'),
            bigquery.SchemaField('Cost', 'FLOAT', mode='NULLABLE'),
            bigquery.SchemaField('Impressions', 'INTEGER', mode='NULLABLE'),
        ]

        # create the BigQuery table if it doesn't exist
        table_ref = client.dataset(dataset_id).table(table_id)
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table, exists_ok=True)

        # load the ads data into the BigQuery table from the Cloud Storage bucket
        uri = 'gs://{}/ads_data.csv'.format(bucket_name)
        load_job = client.load_table_from_uri(uri, table_ref)
        load_job.result() # wait for the job to complete

        # calculate the metrics and update the table
        sql = """
        UPDATE `{dataset}.{table}`
        SET
            CPA = Cost / Clicks,
            CPC = Cost / Impressions,
            ROAS = Revenue / Cost
        """.format(dataset=dataset_id, table=table_id)
        query_job = client.query(sql)
        query_job.result()

        self.stdout.write(self.style.SUCCESS('Successfully uploaded ads data to BigQuery and calculated metrics'))
