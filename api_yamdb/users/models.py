from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    email = models.EmailField('email адрес', unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField('Роль',
                            choices=ROLES,
                            default='user',
                            max_length=9
                            )
    confirmation_code = models.CharField('Код подтверждения',
                                         max_length=50,
                                         blank=True,
                                         null=True
                                         )
