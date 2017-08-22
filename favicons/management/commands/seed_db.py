"""Command to seed database.

Seeds database with first 200,000 (default) URLs from Alexa Top Million list.

To save 20 rows, run:
python manage.py seed_db 20
"""
import csv
import requests
from StringIO import StringIO
import zipfile

from django.core.management import BaseCommand

from favicons.forms import FavFinderForm


class Command(BaseCommand):
    """Class for command to seed database."""

    help = "Seed database with 200,000 records from the Alexa Top Million list"

    def add_arguments(self, parser):
        """Let us specify how many rows to save to the DB."""
        parser.add_argument('rows', type=int, nargs='?', default=3)

    def handle(self, *args, **options):
        """Let us seed the database!."""
        self.stdout.write('Seeding the database!')

        rows = options.get('rows')

        url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

        request = requests.get(url, headers={'User-Agent': 'Chrome/2.18.4'})

        with zipfile.ZipFile(StringIO(request.content)) as zipAlexa:
            with zipAlexa.open('top-1m.csv', 'r') as csvAlexa:
                reader = csv.reader(csvAlexa)
                count = 0

                for row in reader:
                    row = [i.strip() for i in row]

                    form = FavFinderForm({'url': row[1]})

                    if form.is_valid():
                        form.save()
                        count += 1
                        self.stdout.write('.', ending='')

                    if count >= rows:
                        break

        self.stdout.write('Success!')
