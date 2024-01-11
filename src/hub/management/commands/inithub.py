from typing import Any

import requests
from constance import config
from django.core.management.base import BaseCommand

from projects.models import TelegramBot


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        token = config.MASTER_BOT_TOKEN
        if not token:
            print("MASTER_BOT_TOKEN is empty!")
            return

        bot = self.get_masterbot(token)
        self.register_masterbot_webhooks_url(bot)

    def register_masterbot_webhooks_url(self, bot):
        base_hook_url = config.BASE_HOOK_URL
        if not base_hook_url:
            print("BASE_HOOK_URL is empty!")

        api_url = config.TELEGRAM_API_URL
        if not api_url:
            print("TELEGRAM_API_URL is empty!")
            return

        request_url = f"{api_url}{bot.telegram_key}"
        webhook_url = f"{base_hook_url}/hub/master/"
        request = f"{request_url}/setWebhook?url={webhook_url}"
        response = requests.post(request, timeout=5).json()

        if response["ok"] and response["result"]:
            bot.is_webhook_set = True
            bot.save()
            print("Webhook is registered")
        else:
            print("Unable to register bot webhook url")

    def get_masterbot(self, token):
        bot, _ = TelegramBot.objects.get_or_create(bot_type="fab", telegram_key=token)
        return bot
