import csv
from django.core.management.base import BaseCommand
from bigquery.models import TableA

class Command(BaseCommand):
    help = 'Imports data from CSV file to Postgres database'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        with open(options['csvfile']) as f:
            reader = csv.DictReader(f)
            for row in reader:
                tablea = TableA(
                    name=row['Name'],
                    age=row['Age'],
                    gender=row['Gender']
                )
                tablea.save()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
