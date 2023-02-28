# bigQueryProject

To run this project I have used docker, but you can set up your venv and postgresql server and change the password in the settings.py

The TableA records from the BigQuery can be seen in the django admin. (You can create a superuser with `./manage.py createsuperuser` command to make one.

To update the data of TableA from Google BigQuery to our Django Admin, we can use a management command that I have added to update the data by using the csv file exported from the google developer console. (`./manage.py populate_db_with_google_dataset <csv-file-path>`)

We can use a single django management command to upload dummy data to the GoogleAds Dataset in the BigQuery. (`./manage.py upload_add_metrics <credentials-file-path> <csv-file-path>`) Here the csv-file is the ads_data that we can upload. I have added a file named ads_data.csv. It should be in the same format. We can add any amount of data in that file and use this command to update the data over the GoogleADs Dataset.

Have created another management command to perform actions on Google Ads Accounts i.e pause, unpause, update. To use this command simply (`python manage.py ads_actions pause 1234 5678 --customer-id 1234567890`).

Have written a test case to test upload_ads_data command.
