from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from aiogram3_calendar import dialog_cal_callback, DialogCalendar

from assets.texts import read_text_from_file as rf
from core.keyboards import markups, MarkupKeys as mk, ButtonsKeys as bk, ButtonsData as bd
from core.filters import ButtonDataTypeFilter as BtnDataTypeF, IsNotCommandFilter
from core.services import find_city_info, get_location, get_datetime, astro_calc, set_typing, get_skip_state
from core.states import Calc


LOCATION_PROMPT='Введите вашу страну и город в которым вы родились:'

def setup_handler(router: Router):

    @router.callback_query(Calc.Time.minute_prompt, BtnDataTypeF(bd.PLACEHOLDER))
    @router.callback_query(Calc.Time.hour_prompt, BtnDataTypeF(bd.PLACEHOLDER))
    async def ignore_placeholder(callback_query: CallbackQuery, state: FSMContext):
        await callback_query.answer()

    # Step 0: Date choise
    @router.callback_query(Calc.can_calculate, BtnDataTypeF(bk.CALC))
    async def start_calc_handler(callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(Calc.Date.date_prompt)
        await callback_query.message.answer(
            "Выберите дату: ",
            reply_markup=await DialogCalendar().start_calendar(year=2000)
        )

    # Step 1: Calendar
    @router.callback_query(Calc.Date.date_prompt, dialog_cal_callback.filter())
    async def date_handler(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
        selected, date = await DialogCalendar().process_selection(
                            callback_query,
                            callback_data
                        )
        if selected:
            await state.update_data(selected_date=date)
            await callback_query.message.answer(
                f'Дата Вашего рождения: {date.strftime("%d.%m.%Y")}\n\n' +
                'Введите время рождения или нажмите кнопку «Пропустить», если не знаете точное время своего рождения'
            )
            await state.set_state(Calc.Time.hour_prompt)
            await callback_query.message.answer(
                "Теперь выберите час:",
                reply_markup=await markups[mk.HOURS]
            )

    # Step 2: Choose an hour
    @router.callback_query(Calc.Time.hour_prompt, BtnDataTypeF(bd.HOUR))
    async def hour_handler(callback_query: CallbackQuery, state: FSMContext):
        hour = int(callback_query.data.split(":")[1])
        await state.update_data(selected_hour=hour)
        await state.set_state(Calc.Time.minute_prompt)
        await callback_query.message.delete()
        await callback_query.message.answer(
            f"Вы выбрали час: {hour}\nВыберите минуты:", 
            reply_markup=await markups[mk.MINUTES]
        ) 

    # Step 3: Choose a minutes
    @router.callback_query(Calc.Time.minute_prompt, BtnDataTypeF(bd.MINUTE))
    async def minute_handler(callback_query: CallbackQuery, state: FSMContext):
        await set_typing(callback_query)
        selected_minute = int(callback_query.data.split(":")[1])
        await state.update_data(selected_minute=selected_minute)

        full_datetime = await get_datetime(state)

        await callback_query.message.delete()
        await callback_query.message.answer(
            f"Вы выбрали дату и время: {full_datetime.strftime('%d/%m/%Y %H:%M')}"
        )
        await state.set_state(Calc.Location.location_prompt)  
        await callback_query.message.answer(LOCATION_PROMPT)
         

    # Step 4.1: Switch to choose a location
    # from SKIP_TIME (Step 1)
    @router.callback_query(Calc.Time.hour_prompt, BtnDataTypeF(bd.SKIP_TIME))       
    async def location_input1_handler(callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(skip_time=True)

        await callback_query.message.delete()
        await state.set_state(Calc.Location.location_prompt)
        await callback_query.message.answer(LOCATION_PROMPT)


    # Step 4.2: Switch to choose a location
    # from REJECT (Step 5)  
    @router.callback_query(Calc.Location.location_confirm, BtnDataTypeF(bd.NO))
    async def location_input2_handler(callback_query: CallbackQuery, state: FSMContext):
        await callback_query.message.delete()
        await state.set_state(Calc.Location.location_prompt)
        await callback_query.message.answer(LOCATION_PROMPT)


    # Step 4.3: Switch to choose a location   
    # from full date (Step 3)
    @router.message(Calc.Location.location_prompt, IsNotCommandFilter())
    async def location_input3_handler(message: Message, state: FSMContext):
        await state.set_state(Calc.Location.location_prompt)
        
        result = await find_city_info(message.text)

        if not isinstance(result, str):
            address, lat, lon = result
            await state.update_data(location={'lat': float(lat), 'lon': float(lon)})
            await state.set_state(Calc.Location.location_confirm)
            await message.answer(
                f"Это ваш город?\n{address}\nКоординаты: {lat}, {lon}",
                reply_markup=await markups[mk.YES_NO]
            )
        else:
            await message.answer(' '.join([result,"Пожалуйста, попробуйте еще раз."]))

    # Step 5.1: approve to choose a location
    @router.callback_query(Calc.Location.location_confirm, BtnDataTypeF(bd.YES))
    async def location_confirm_handler(callback_query: CallbackQuery, state: FSMContext):
        await set_typing(callback_query)

        results = await astro_calc(await get_location(state), await get_datetime(state))

        await callback_query.message.answer(
            await rf(
                'calculator_result_part' if await get_skip_state(state) else 'calculator_result', 
                **results
            ),
            reply_markup=await markups[mk.MAIN_MARKUP]
        )
        await state.clear()



            




