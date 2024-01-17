from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

context = settings.FSM_CONTEXT


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        global context
        context = {}
        print("Storage reset complete")
