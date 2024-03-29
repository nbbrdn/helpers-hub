import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from projects.models import Project
from telegram.bots.master.handler import handle_update as master_update
from telegram.dispatcher import dispatch


@csrf_exempt
def bot(request, project_id, bot_id):
    if request.method == "POST":
        project = Project.objects.get(pk=project_id)
        if project:
            handler = project.router.handler
            update = json.loads(request.body.decode("utf-8"))
            dispatch(handler)(update, bot_id)
        return HttpResponse("ok")
    return HttpResponseBadRequest("Bad Request")


@csrf_exempt
def maser_bot(request):
    if request.method == "POST":
        update = json.loads(request.body.decode("utf-8"))
        master_update(update)
        return HttpResponse("ok")
    return HttpResponseBadRequest("Bad Request")
