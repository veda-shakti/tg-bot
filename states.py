from aiogram.fsm.state import StatesGroup, State


class Calc(StatesGroup):
    date_prompt = State()
    hour_prompt = State()
    minute_prompt = State()
    
