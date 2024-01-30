from aiogram.fsm.state import StatesGroup, State


class Calc(StatesGroup):

    can_calculate = State()

    class Date(StatesGroup):
        date_prompt = State()

    class Time(StatesGroup):
        hour_prompt = State()
        minute_prompt = State()

    class Location(StatesGroup):
        location_prompt = State()
        location_confirm = State()
    
