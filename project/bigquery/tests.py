import io
import csv
from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch


class TestUploadAdsData(TestCase):
    def setUp(self):
        # create a CSV file with test data
        self.csv_file = io.StringIO()
        csv_writer = csv.writer(self.csv_file)
        csv_writer.writerow(['Campaign', 'Clicks', 'Cost', 'Impressions'])
        csv_writer.writerow(['Test Campaign', '100', '50.0', '1000'])
        self.csv_file.seek(0)

    @patch('google.cloud.bigquery.Client')
    def test_upload_ads_data(self, mock_client):
        # call the management command with mock client
        mock_client.from_service_account_json.return_value = mock_client
        mock_table = mock_client.dataset.return_value.table.return_value
        mock_errors = []
        mock_client.insert_rows.return_value = mock_errors
        call_command('upload_ads_data', credentials_path='/path/to/your/credentials.json',
                     dataset_id='your_dataset_id', table_id='GoogleAds', ads_data=self.csv_file)

        # assert that the BigQuery table was created and data was inserted successfully
        mock_client.dataset.assert_called_once_with('your_dataset_id')
        mock_client.dataset.return_value.table.assert_called_once_with('GoogleAds')
        mock_client.create_table.assert_called_once_with(mock_table, exists_ok=True)
        mock_client.insert_rows.assert_called_once_with(mock_table, [('Test Campaign', 100, 50.0, 1000)])
