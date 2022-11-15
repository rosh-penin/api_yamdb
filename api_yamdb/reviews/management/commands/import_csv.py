import csv
import os

from django.core.management.base import BaseCommand, CommandError

from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Genre, Title, GenreTitle


DATA_FILES_DIR = os.path.join(BASE_DIR, 'static/data/')
ALLOWED_FILENAMES = {
    'category': Category,
    # 'comments': Comments,
    'genre': Genre,
    # 'review': Review,
    'titles': Title,
    # 'users': User,
    'genre_title': GenreTitle,
}


class Command(BaseCommand):
    help = '''Take all .csv files inside "static/data" folder of
        root django project and populate tables. Filenames should be:
        category.csv
        comments.csv
        genre.csv
        review.csv
        titles.csv
        users.csv
        genre_title.csv'''

    def _correct_files(self):
        """Only .csv files allowed to proceed."""
        files = os.listdir(DATA_FILES_DIR)
        genretitle = None
        for file in os.listdir(DATA_FILES_DIR):
            if not file.endswith('.csv'):
                files.remove(file)
            if file == 'genre_title.csv':
                genretitle = files.pop(files.index(file))

        return files, genretitle

    def _populate_table(self, file, model):
        path = os.path.join(DATA_FILES_DIR, file)
        with open(path, 'r', encoding='utf8') as csv_file:
            for row in csv.DictReader(csv_file):
                if 'category' in row:
                    row['category_id'] = row.pop('category')
                model.objects.get_or_create(**row)

    def handle(self, *args, **options):
        files, genretitle = self._correct_files()
        for file in files:
            name = file.split('.')[0]
            if name in ALLOWED_FILENAMES:
                self._populate_table(file, ALLOWED_FILENAMES[name])

        if genretitle is not None and all(
            x in files for x in ('titles.csv', 'genre.csv')
        ):
            file = 'genre_title.csv'
            self._populate_table(file, ALLOWED_FILENAMES[file.split('.')[0]])
