import collections
import json

import requests
from constance import config
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from projects.models import Project, Supervisor, TelegramBot
from telegram.api.types import Message

context = settings.FSM_CONTEXT

telegram_api_url = config.TELEGRAM_API_URL
master_bot_telegram_token = config.MASTER_BOT_TOKEN
url = f"{telegram_api_url}{master_bot_telegram_token}"


@csrf_exempt
def maser_bot(request):
    if request.method == "POST":
        update = json.loads(request.body.decode("utf-8"))
        handle_update(update)
        return HttpResponse("ok")
    return HttpResponseBadRequest("Bad Request")


def handle_update(update):
    message = Message.from_json(update)
    route(message)


def send_message(chat_id, text, reply_markup=None):
    params = {"chat_id": chat_id, "text": text}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)
    response = requests.post(f"{url}/sendMessage", params=params, timeout=5)
    return response.json()


def find_supervisor(user_id: int) -> Supervisor | None:
    return Supervisor.objects.filter(telegram_id=user_id).first()


def process_start_command(message: Message, context):
    supervisor = find_supervisor(message.from_user.id)
    if supervisor:
        # TODO: Do something if supervisor is already registered
        text = f"Привет, {supervisor.name}! Я тебя знаю!"
        send_message(message.chat.id, text)
    else:
        text = (
            "Привет! Кажется, я тебя не знаю 🤔\n\n"
            "Давай, я помогу тебе зарегистрироваться!\n\n"
            "Для начала представься, как я могу к тебе обращаться:"
        )
        send_message(message.chat.id, text)
        context["state"] = "waiting_name"


def process_waiting_phone_number_state(message: Message, context):
    if message.from_user.phone_number:
        context["data"]["phone_number"] = message.from_user.phone_number
        context["state"] = "waiting_testbot_token"
    elif len(message.text) >= 11 and len(message.text) < 20:
        context["data"]["phone_number"] = message.text
        context["state"] = "waiting_testbot_token"
    else:
        send_message(
            message.chat.id,
            "Хмм... что-то пошло не так. Попробуйте ввести номер телефона с клавиатуры.",
        )


def process_unknown_state(message, context):
    send_message(message.chat.id, "unknown state")


def process_waiting_name_state(message: Message, context):
    context["data"]["name"] = message.text

    if message.from_user.phone_number:
        context["data"]["phone_number"] = message.from_user.phone_number
        context["state"] = "waiting_testbot_token"
        send_message(
            message.chat.id, "Спасибо!\n\nНапишите API ключ бота для тестирования:"
        )
    else:
        send_message(
            message.chat.id,
            "Спасибо!\n А теперь мне понадобится твоя одежда, ключи и мотоцикл",
        )
        send_message(message.chat.id, "Ой... всего лишь номер телефона.\n\n")

        text = "Нажми на кнопку, чтобы поделиться своим номером телефона."
        reply_markup = {
            "keyboard": [
                [{"text": "Поделиться номером телефона", "request_contact": True}]
            ],
            "one_time_keyboard": True,
            "resize_keyboard": True,
        }
        send_message(message.chat.id, text, reply_markup)
        context["state"] = "waiting_phone_number"


def check_token(token):
    request_url = f"{telegram_api_url}{token}/getMe"
    return requests.get(request_url, timeout=5).json()


def process_waiting_testbot_token(message: Message, context):
    token = message.text.strip()
    result = check_token(token)
    print(result)
    if result["ok"]:
        context["data"]["testbot_token"] = token
        context["state"] = "waiting_prodbot_token"
        text = (
            "Великолепно! Вы ввели столько символов и не ошиблись! Вы точно человек?\n"
            "Шучу :)\n\nДвайте теперь также без ошибок введем API ключ для боевого бота:"
        )
    else:
        error = result["description"]
        text = (
            f"Ваш токен не прошел проверку. Ответ сервера: {error}\n\n"
            "Еще раз напишите API ключ бота для тестирования:"
        )
    send_message(message.chat.id, text)


def process_waiting_prodbot_token(message: Message, context):
    token = message.text.strip()
    result = check_token(token)
    if result["ok"]:
        context["data"]["prodbot_token"] = token
        context["state"] = "initialize_project"
    else:
        error = result["description"]
        text = (
            f"Ваш токен не прошел проверку. Ответ сервера: {error}\n\n"
            "Еще раз напишите API ключ боевого бота:"
        )
        send_message(message.chat.id, text)

    create_supervisor(message, context)


def create_supervisor(message: Message, context):
    supervisor = Supervisor()
    user = message.from_user

    if user.first_name and user.last_name:
        supervisor.name = f"{user.first_name} {user.last_name}"

    if user.username:
        supervisor.telegram_nickname = user.username
    else:
        supervisor.telegram_nickname = "<unknown>"

    supervisor.telegram_id = user.telegram_id
    supervisor.phone = user.phone_number

    supervisor.save()
    context["data"]["supervisor"] = supervisor
    send_message(message.chat.id, "Так... Все, я тебя запмнил...")

    create_project(message, context)


def create_project(message, context):
    data = context["data"]
    supervisor = data["supervisor"]
    testbot_token = data["testbot_token"]
    prodbot_token = data["prodbot_token"]

    project = Project()
    project.owner = supervisor
    project.dev_telegram_key = testbot_token
    project.prod_telegram_key = prodbot_token
    project.save()
    data["project"] = project

    send_message(
        message.chat.id, "Уфф... Сформировал для тебя проект...\n\nЕщё чуть-чуть!"
    )

    testbot = create_bot(testbot_token, context, "dev")
    if testbot:
        send_message(message.chat.id, "Тестовый бот создан!")

    prodbot = create_bot(prodbot_token, context, "prod")
    if prodbot:
        send_message(message.chat.id, "Боевой бот создан!")


def create_bot(token, context, bot_type):
    bot = TelegramBot()
    bot.bot_type = bot_type
    bot.telegram_key = token
    bot.project = context["data"]["project"]
    bot.save()
    return bot


states = collections.defaultdict(lambda: process_unknown_state)
states["waiting_phone_number"] = process_waiting_phone_number_state
states["waiting_name"] = process_waiting_name_state
states["waiting_testbot_token"] = process_waiting_testbot_token
states["waiting_prodbot_token"] = process_waiting_prodbot_token


def route(message: Message):
    context = get_context(message)
    cuurent_state = context["state"]

    if message.text and message.text.startswith("/context"):
        send_message(message.chat.id, text=context)
    elif (
        cuurent_state == "default"
        and message.text
        and message.text.startswith("/start")
    ):
        process_start_command(message, context)
    elif message.text and message.text.startswith("/cancel"):
        context["state"] = "default"
        context["data"] = {}
        send_message(
            message.chat.id,
            text="Понять друг друга и простить...\nДавай начнем все с чистого листа!",
        )
    else:
        states[cuurent_state](message, context)


def get_bot_cobtext(token):
    if token in context:
        return context[token]

    bot_context = {}
    context[token] = bot_context
    return bot_context


def get_context(message):
    bot_context = get_bot_cobtext(master_bot_telegram_token)
    chat_id = message.chat.id
    if chat_id in bot_context:
        return bot_context[chat_id]

    chat_context = {}
    chat_context["state"] = "default"
    chat_context["data"] = {}
    bot_context[chat_id] = chat_context
    return chat_context
