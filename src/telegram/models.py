from django.db import models


class User(models.Model):
    telegram_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    created_at = models.DateTimeField(
        "Создан",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Изменён",
        auto_now=True,
    )
