from django.conf import settings

from telegram.api.methods import get_bot_context, send_message
from telegram.api.types import Message

global_context = settings.FSM_CONTEXT


def handle_update(update, bot_id):
    context = get_bot_context(bot_id)
    message = Message.from_json(update)
    route(message, context)


def route(message: Message, context):
    send_message(message.chat.id, text=message.text, context=context)
