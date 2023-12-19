from aiogram import Router

from . import (
    handler_start,
    handler_calc
)

modules = [
    handler_start,
    handler_calc
]

router = Router()


def setup_handlers():
    for module in modules:
        module.setup_handler(router)
