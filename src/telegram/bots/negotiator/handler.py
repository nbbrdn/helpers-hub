import collections

from django.conf import settings

from telegram.api.methods import (get_bot_context, get_state,
                                  init_chat_context, send_message)
from telegram.api.types import Message

global_context = settings.FSM_CONTEXT


def handle_update(update, bot_id):
    context = get_bot_context(bot_id)
    message = Message.from_json(update)
    if message.chat.id not in context:
        init_chat_context(message.chat.id, context)
    route(message, context)


def route(message: Message, context):
    current_state = get_state(message.chat.id, context)
    if (
        current_state == "default"
        and message.text
        and message.text.startswith("/start")
    ):
        process_start_command(message, context)
    else:
        states[current_state](message, context)


def process_start_command(message, context):
    placeholder = "Укажите способ выбора кейса"
    options = [
        "Давай разберем случайный кейс",
        "Предложи список из 10 случайных кейсов",
    ]
    text = "Вы хотите выбрать кейс из предложенного списка, или выбрать случайный?"
    keyboard = {
        "keyboard": [
            [{"text": options[0]}],
            [{"text": options[1]}],
        ],
        "resize_keyboard": True,
        "input_field_placeholder": placeholder,
    }
    context[message.chat.id]["state"] = "waiting_case_choice"
    response = send_message(message.chat.id, text, context, reply_markup=keyboard)
    print(response)


def process_unknown_state(message: Message, context):
    response = send_message(message.chat.id, "Моя твоя не понимай 🤔", context)
    print(response)


def process_waiting_case_choice(message: Message, context):
    print("process_waiting_case_choice")


states = collections.defaultdict(lambda: process_unknown_state)
states["waiting_case_choice"] = process_waiting_case_choice
