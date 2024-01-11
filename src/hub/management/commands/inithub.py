import requests
from constance import config
from typing import Any
from django.core.management.base import BaseCommand

from projects.models import TelegramBot


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        if not self.is_masterbot_set():
            self.create_masterbot()
        else:
            print("masterbot already exists")

    def create_masterbot(self):
        master_bot_telegram_token = config.MASTER_BOT_TOKEN
        if not master_bot_telegram_token:
            print("MASTER_BOT_TOKEN is empty!")
            return

        telegram_api_url = config.TELEGRAM_API_URL
        if not telegram_api_url:
            print("TELEGRAM_API_URL is empty!")
            return

        base_hook_url = config.BASE_HOOK_URL
        if not base_hook_url:
            print("BASE_HOOK_URL is empty!")

        url = f"{telegram_api_url}{master_bot_telegram_token}"
        webhook_url = f"{base_hook_url}/hub/master/"
        request = f"{url}/setWebhook?url={webhook_url}"
        response = requests.post(request).json()

        if response["ok"] == True and response["result"] == True:
            master_bot = TelegramBot()
            master_bot.bot_type = "fab"
            master_bot.telegram_key = master_bot_telegram_token
            master_bot.is_webhook_set = True
            master_bot.save()

        print("Master bot is initialized.")

    def is_masterbot_set(self):
        result = TelegramBot.objects.filter(bot_type="fab")
        return len(result) > 0
