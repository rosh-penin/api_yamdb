from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    email = models.EmailField('email address')
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField('Роль',
                            choices=ROLES,
                            default='user',
                            max_length=9
                            )

    is_active = models.BooleanField(
        'active',
        default=False,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    confirmation_code = models.TextField('Код подтверждения',
                                         blank=True,
                                         null=True
                                         )
