import json

import requests
from constance import config
from django.conf import settings

from projects.models import TelegramBot
from telegram.api.types import Message

global_context = settings.FSM_CONTEXT


def handle_update(update, bot_id):
    context = get_context(bot_id)
    if "api_url" not in context:
        telegram_api_url = config.TELEGRAM_API_URL
        bot = TelegramBot.objects.get(pk=bot_id)
        token = bot.telegram_key
        api_url = f"{telegram_api_url}{token}"
        context["api_url"] = api_url
    message = Message.from_json(update)
    route(message, context)


def get_context(bot_id: int):
    if bot_id in global_context:
        return global_context[bot_id]
    context = {}
    global_context[bot_id] = context
    return context


def route(message: Message, context):
    send_message(message.chat.id, text=message.text, context=context)


def send_message(chat_id, text, context, reply_markup=None):
    url = context["api_url"]
    params = {"chat_id": chat_id, "text": text}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)
    response = requests.post(f"{url}/sendMessage", params=params, timeout=5)
    return response.json()
