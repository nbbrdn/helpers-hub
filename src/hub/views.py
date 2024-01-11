import json
import requests
from constance import config
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

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
    else:
        return HttpResponseBadRequest("Bad Request")


def handle_update(update):
    message = Message.from_json(update)
    send_message(
        "sendMessage", {"chat_id": message.chat.id, "text": f"you said {message.text}"}
    )


def send_message(method, data):
    req = url + method
    print(req, data)
    return requests.post(req, data)
