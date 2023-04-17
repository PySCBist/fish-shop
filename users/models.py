from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


def set_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = (f'{instance.first_name}_'
                             f'{str(timezone.now().timestamp())}')


models.signals.pre_save.connect(set_username, sender=CustomUser)
