from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField('Роль',
                            choices=ROLES,
                            default='user',
                            max_length=9
                            )
