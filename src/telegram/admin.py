from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "phone_number",
        "username",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "telegram_id",
        "phone_number",
        "username",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
    )
