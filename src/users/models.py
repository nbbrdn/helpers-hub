from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import HubUserManager


class HubUser(AbstractUser):
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    objects = HubUserManager()

    def __str__(self):
        return self.email
