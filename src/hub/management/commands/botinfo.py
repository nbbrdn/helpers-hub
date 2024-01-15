from typing import Any

import requests
from constance import config
from django.core.management.base import BaseCommand

from projects.models import TelegramBot


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        api_url = config.TELEGRAM_API_URL
        if not api_url:
            print("TELEGRAM_API_URL is empty!")
            return

        bots = TelegramBot.objects.all()
        for bot in bots:
            request_url = f"{api_url}{bot.telegram_key}/getMe"
            response = requests.get(request_url, timeout=5).json()
            if response["ok"]:
                data = response["result"]
                bot.username = data["username"]
                bot.name = data["first_name"]
                bot.save()
                print(f"Bot (id: {bot.pk}) updated")
