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

        base_hook_url = config.BASE_HOOK_URL
        if not base_hook_url:
            print("BASE_HOOK_URL is empty!")

        bots = TelegramBot.objects.exclude(bot_type="fab")
        for bot in bots:
            project_id = bot.project.pk
            bot_id = bot.pk
            request_url = f"{api_url}{bot.telegram_key}"
            webhook_url = f"{base_hook_url}/hub/projects/{project_id}/{bot_id}/"
            request = f"{request_url}/setWebhook?url={webhook_url}"
            response = requests.post(request, timeout=5).json()
            if response["ok"] and response["result"]:
                bot.is_webhook_set = True
                bot.save()
                print(f"{bot} webhook is registered.")
            else:
                print(
                    f"Error while registering bot {bot} webhook. Error: {response['description']}"
                )
