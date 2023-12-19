from aiogram.fsm.state import StatesGroup, State


class Calc(StatesGroup):
    date_prompt = State()
    img_prompt = State()
