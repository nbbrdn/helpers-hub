import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from telegram.bots.basic.handler import handle_update as basic_update
from telegram.bots.master.handler import handle_update as master_update


@csrf_exempt
def bot(request, project_id, bot_id):
    if request.method == "POST":
        update = json.loads(request.body.decode("utf-8"))
        basic_update(update, bot_id)
        return HttpResponse("ok")
    return HttpResponseBadRequest("Bad Request")


@csrf_exempt
def maser_bot(request):
    if request.method == "POST":
        update = json.loads(request.body.decode("utf-8"))
        master_update(update)
        return HttpResponse("ok")
    return HttpResponseBadRequest("Bad Request")
