from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


def NotOverCurrentYearValidator(value):
    current_year = datetime.now().year
    return MaxValueValidator(current_year)(value)


class Category(models.Model):
    """Model for categories."""
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Model for genres."""
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Model for titles."""
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField(
        'Год выпуска',
        validators=[
            NotOverCurrentYearValidator
        ]
    )
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        blank=True
    )

    class Meta():
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'year', 'category'),
                name='triple title constraint'
            ),
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """
    Intermediate model for connecting Title and
    Genre ManyToMany relation.
    """
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genretitle'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genretitle'
    )

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='double genre constraint'
            ),
        ]

    def __str__(self):
        return f'genre "{self.genre}" for title "{self.title}"'


class BaseModel(models.Model):
    """Model for inheriting with pre-set fields and Meta."""
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date', '-pk')
        abstract = True


class Review(BaseModel):
    """Model for reviews."""
    text = models.TextField('Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        help_text='Оценка произведения от 1 до 10'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    def __str__(self):
        return self.text[:20]

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='double_review_constraint'
            ),
        ]


class Comment(BaseModel):
    """Model for comments."""
    text = models.TextField('Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый отзыв'
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
