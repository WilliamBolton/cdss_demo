import csv
from django.core.management.base import BaseCommand
from table.models import Vitals_table

class Command(BaseCommand):
    help = 'Load Vitals data from a CSV file'

    def handle(self, *args, **options):
        # Replace 'path/to/your/file.csv' with the actual path to your CSV file
        csv_file_path = '/home/wb1115/VSCode_projects/cdss/cdss_1/csv/test.csv'

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Vitals_table.objects.create(
                    metric=row['metric'],
                    zero=row['0'],
                    one=row['1'],
                    two=row['2'],
                    three=row['3'],
                    four=row['4'],
                    five=row['5'],
                    six=row['6'],
                    seven=row['7']
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded Vitals data from CSV'))