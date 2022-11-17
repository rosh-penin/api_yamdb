import csv
import os

from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import (Category, Genre, Title, GenreTitle,
                            Comment, Review, User)


DATA_FILES_DIR = os.path.join(BASE_DIR, 'static/data/')
ALLOWED_FILENAMES = {
    'category': Category,
    'comments': Comment,
    'genre': Genre,
    'review': Review,
    'titles': Title,
    'users': User,
    'genre_title': GenreTitle,
}


def sort_list(some_list: list):
    if 'users.csv' in some_list:
        some_list.insert(0, some_list.pop(some_list.index('users.csv')))
    if 'comments.csv' in some_list:
        some_list.insert(6, some_list.pop(some_list.index('comments.csv')))
    if 'titles.csv' in some_list:
        some_list.insert(3, some_list.pop(some_list.index('titles.csv')))

    return some_list


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
        for file in os.listdir(DATA_FILES_DIR):
            if not file.endswith('.csv'):
                files.remove(file)

        return sort_list(files)

    def _populate_table(self, file, model):
        path = os.path.join(DATA_FILES_DIR, file)
        with open(path, 'r', encoding='utf8') as csv_file:
            for row in csv.DictReader(csv_file):
                if 'category' in row:
                    row['category_id'] = row.pop('category')
                if 'author' in row:
                    row['author_id'] = row.pop('author')
                model.objects.get_or_create(**row)

    def handle(self, *args, **options):
        for file in self._correct_files():
            name = file.split('.')[0]
            if name in ALLOWED_FILENAMES:
                self._populate_table(file, ALLOWED_FILENAMES[name])
