from aiogram.types import Message
from aiogram.filters import Command

from assets.texts.text_handler import read_text_from_file as rf
from kb import markups, MarkupKeys as mk


def setup_handler(router):
    @router.message(Command("start"))
    async def start_handler(msg: Message):
        await msg.answer(await rf('start'))
        await msg.answer(await rf('start2'), reply_markup=await markups[mk.MAIN_MARKUP])
