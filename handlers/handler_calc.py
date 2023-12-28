from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery

from aiogram3_calendar import dialog_cal_callback, DialogCalendar
from datetime import datetime, time

from assets.texts.text_handler import read_text_from_file as rf
from kb import markups, MarkupKeys as mk, ButtonsKeys as bk
from states import Calc


def setup_handler(router: Router):

    # Step 1: dialog calendar usage !!!!! place of this func is important
    @router.message(Calc.date_prompt)
    @router.callback_query(dialog_cal_callback.filter())
    async def date_handler(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
        selected, date = await DialogCalendar().process_selection(
                            callback_query,
                            callback_data
                        )
        if selected:
            await state.update_data(selected_date=date)
            await callback_query.message.answer(f'Дата Вашего рождения: {date.strftime("%d.%m.%Y")}\n\nВведите время рождения или нажмите кнопку «Пропустить», если не знаете время своего рождения')
            await state.set_state(Calc.hour_prompt)
            await callback_query.message.answer(
                "Теперь выберите час:",
                reply_markup=await markups[mk.HOURS]
            )

    # Step 2: Обработчик выбора часа
    @router.message(Calc.hour_prompt)
    @router.callback_query(F.data.count('time'))
    async def hour_handler(callback_query: CallbackQuery, state: FSMContext):
        hour = int(callback_query.data.split(":")[1])  # Исправлено на callback_query.data
        await state.update_data(selected_hour=hour)
        await state.set_state(Calc.minute_prompt)  # Переход к состоянию выбора минут
        await callback_query.message.answer(
            "Выберите минуты:", 
            reply_markup=await markups[mk.MINUTES]  # Предполагаем, что mk.MINUTES - это клавиатура для минут
        )

    # Step 3: Обработчик выбора минут
    @router.message(Calc.minute_prompt)
    @router.callback_query(F.data.count('time'))
    async def minute_handler(callback_query: CallbackQuery, state: FSMContext):
        selected_minute = int(callback_query.data.split(":")[1])  # Исправлено на callback_query.data
        user_data = await state.get_data()
        selected_hour = user_data.get("selected_hour")
        selected_date = user_data.get("selected_date")
        full_datetime = datetime.combine(selected_date, time(selected_hour, selected_minute))
        # await your_processing_function(full_datetime)  # Ваша функция обработки
        await callback_query.message.answer(
            f"Вы выбрали дату и время: {full_datetime.strftime('%d/%m/%Y %H:%M')}",
            reply_markup=await markups[mk.MAIN_MARKUP]
        )
        await state.clear()

    # Step 1: Date choise !!!! this takes all queries
    @router.callback_query(F.data == bk.CALC.name)
    async def start_calc_handler(callback_query: CallbackQuery, state: FSMContext):
        # if callback_query.data == bk.CALC.name:
            await state.set_state(Calc.date_prompt)
            await callback_query.message.answer(
                "Выберите дату: ",
                reply_markup=await DialogCalendar().start_calendar(year=2000)
            )
