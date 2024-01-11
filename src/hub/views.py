import json

import requests
from constance import config
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from projects.models import Supervisor
from telegram.types import Message

telegram_api_url = config.TELEGRAM_API_URL
master_bot_telegram_token = config.MASTER_BOT_TOKEN
url = f"{telegram_api_url}{master_bot_telegram_token}/"


@csrf_exempt
def maser_bot(request):
    if request.method == "POST":
        update = json.loads(request.body.decode("utf-8"))
        handle_update(update)
        return HttpResponse("ok")
    return HttpResponseBadRequest("Bad Request")


def handle_update(update):
    message = Message.from_json(update)
    # send_message(
    #     "sendMessage", {"chat_id": message.chat.id, "text": f"you said {message.text}"}
    # )
    route(message)


def answer(message: Message, text: str):
    send_message("sendMessage", {"chat_id": message.chat.id, "text": text})


def send_message(method, data):
    req = url + method
    requests.post(req, data, timeout=5)


def find_supervisor(user_id: int) -> Supervisor | None:
    return Supervisor.objects.filter(telegram_id=user_id).first()


def process_start_command(message: Message):
    supervisor = find_supervisor(message.from_user.id)
    if supervisor:
        # TODO: Do something if supervisor is already registered
        text = f"Привет, {supervisor.name}! Я тебя знаю!"
        answer(message=message, text=text)
    else:
        # TODO: Do something is supervisor is not registered
        text = "Привет! Кажется, я тебя не знаю 🤔\n\nДавай, я помогу тебе зарегистрироваться!"
        answer(message=message, text=text)


def route(message: Message):
    if message.text.startswith("/start"):
        process_start_command(message)
    else:
        answer(message=message, text="Моя твоя не понимай...")
