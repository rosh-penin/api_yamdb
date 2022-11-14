from django.db import models


class Category(models.Model):
    pass


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=100)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    pass
