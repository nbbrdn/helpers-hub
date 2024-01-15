from .bots.basic.handler import handle_update as basic
from .bots.negotiator.handler import handle_update as negotiator


def dispatch(handler: str):
    if handler == "negotiator":
        return negotiator
    if handler == "echo":
        return basic
    return basic
