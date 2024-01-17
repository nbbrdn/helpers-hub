from django.db import models


class Supervisor(models.Model):
    name = models.CharField("Name", max_length=250, null=True, blank=True)
    telegram_id = models.BigIntegerField("Telegram ID", null=False, unique=True)
    telegram_nickname = models.CharField("Telegram Username", max_length=50)
    email = models.EmailField("Email", null=True, blank=True)
    phone = models.CharField("Phone", max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(
        "Created",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Modified",
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Supervisor"
        verbose_name_plural = "Supervisors"

    def __str__(self) -> str:
        return f"Telegram ID: {self.telegram_id}"


class Router(models.Model):
    name = models.CharField("Name", max_length=250)
    handler = models.CharField("handler", max_length=50, unique=True)

    created_at = models.DateTimeField(
        "Создан",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Изменён",
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Router"
        verbose_name_plural = "Routers"

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    owner = models.ForeignKey(
        Supervisor, on_delete=models.CASCADE, related_name="projects"
    )
    dev_telegram_key = models.CharField(
        "Telegram Key (Dev)", max_length=250, null=False, blank=False
    )
    prod_telegram_key = models.CharField(
        "Telegram Key (Prod)", max_length=250, null=False, blank=False
    )
    router = models.ForeignKey(
        Router, on_delete=models.PROTECT, related_name="projects", null=True, blank=True
    )
    created_at = models.DateTimeField(
        "Создан",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Изменён",
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self) -> str:
        return f"Project (id: {self.pk})"


BOT_TYPE_CHOICES = (
    ("dev", "Development"),
    ("prod", "Production"),
    ("fab", "Fabric"),
)


class TelegramBot(models.Model):
    name = models.CharField("Name", max_length=250, null=True, blank=True)
    username = models.CharField("Username", max_length=250, null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="bots", null=True, blank=True
    )
    bot_type = models.CharField(
        max_length=20, choices=BOT_TYPE_CHOICES, default="dev", verbose_name="Bot Type"
    )
    telegram_key = models.CharField(
        "Telegram Key", max_length=250, null=False, blank=False
    )
    is_webhook_set = models.BooleanField("Webhook is set", null=False, default=False)
    created_at = models.DateTimeField(
        "Created",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Modified",
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Telegram Bot"
        verbose_name_plural = "Telegram Bots"

    def __str__(self) -> str:
        return f"Bot (id: {self.pk}, name: {self.name if self.name else ''}, "


class TelegramBotConfig(models.Model):
    bot = models.ForeignKey(
        TelegramBot, on_delete=models.CASCADE, related_name="configs"
    )
    name = models.CharField("Name", max_length=50)
    value = models.CharField("Value", max_length=50)

    class Meta:
        ordering = ["name"]
        verbose_name = "Config"
        verbose_name_plural = "Congigs"
