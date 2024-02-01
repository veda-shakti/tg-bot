from aiogram.fsm.context import FSMContext
from datetime import datetime, time


async def get_datetime(state: FSMContext) -> datetime:
    user_data = await state.get_data()
    selected_hour = user_data.get("selected_hour")
    selected_minute = user_data.get("selected_minute")
    return datetime.combine(
        user_data.get("selected_date"), 
        time(
            selected_hour if selected_hour != None else 0, 
            selected_minute if selected_minute != None else 0
        )
    )

async def get_skip_state(state: FSMContext) -> bool | None:
    return (await state.get_data()).get("skip_time")
