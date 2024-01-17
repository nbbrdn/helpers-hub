from django.contrib import admin

from .models import Project, Router, Supervisor, TelegramBot, TelegramBotConfig


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


class TelegramBotConfigInline(admin.StackedInline):
    model = TelegramBotConfig
    extra = 0


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "project", "is_webhook_set")
    readonly_fields = ("is_webhook_set",)
    inlines = (TelegramBotConfigInline,)


@admin.register(Router)
class RouterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "handler",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
