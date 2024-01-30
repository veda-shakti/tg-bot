from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from assets.texts import read_text_from_file as rf

from core.keyboards.keyboards import markups, MarkupKeys as mk

from core.states import Calc


def setup_handler(router):
    @router.message(Command("start"))
    async def start_handler(msg: Message, state: FSMContext):
        await state.clear()
        await state.set_state(Calc.can_calculate)
        await msg.answer(await rf('start'), reply_markup=ReplyKeyboardRemove())
        await msg.answer(await rf('start2'), reply_markup=await markups[mk.CALC_MARKUP])
        