from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    """Custom user model with required email field, new bio and role fields."""
    email = models.EmailField('email адрес', unique=True, max_length=254)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField('Роль',
                            choices=ROLES,
                            default='user',
                            max_length=9)

    @property
    def is_admin(self):
        if self.role == 'admin' or self.is_superuser:
            return True
        return False

    @property
    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False
