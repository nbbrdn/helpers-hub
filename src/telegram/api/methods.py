import json

import requests
from constance import config
from django.conf import settings

from projects.models import TelegramBot

global_context = settings.FSM_CONTEXT


def send_message(chat_id, text, context, reply_markup=None):
    url = context["api_url"]
    params = {"chat_id": chat_id, "text": text}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)
    response = requests.post(f"{url}/sendMessage", params=params, timeout=5)
    return response.json()


def get_bot_context(bot_id: int):
    if bot_id in global_context:
        bot_context = global_context[bot_id]
    else:
        bot_context = {}
        global_context[bot_id] = bot_context

    if "api_url" not in bot_context:
        telegram_api_url = config.TELEGRAM_API_URL
        bot = TelegramBot.objects.get(pk=bot_id)
        token = bot.telegram_key
        api_url = f"{telegram_api_url}{token}"
        bot_context["api_url"] = api_url

    return bot_context


def init_chat_context(chat_id, bot_context):
    chat_context = {}
    chat_context["state"] = "default"
    chat_context["data"] = {}
    bot_context[chat_id] = chat_context


def get_state(chat_id, context):
    return context[chat_id]["state"]


def get_api_url(context):
    return context["api_url"]
