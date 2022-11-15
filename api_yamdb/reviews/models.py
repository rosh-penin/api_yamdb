from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )


class GenreTitle(models.Model):
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

    class Meta:
        unique_together = ('genre', 'title')


class BaseModel(models.Model):
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date', '-pk')
        abstract = True


class Review(BaseModel):
    text = models.TextField('Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rating',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        'Оценка',
        max_length=2,
        help_text='Оценка произведения от 1 до 10'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='rating',
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
            models.CheckConstraint(
                check=models.Q(score__gte=1),
                name='score_gte_1'
            ),
            models.CheckConstraint(
                check=models.Q(score__lte=10),
                name='score_lte_10'
            ),
        ]


class Comment(BaseModel):
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
