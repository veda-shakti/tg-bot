from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery

from assets.texts.text_handler import read_text_from_file as rf
from kb import markups, MarkupKeys as mk, ButtonsKeys as bk
from states import Calc

from aiogram3_calendar import dialog_cal_callback, DialogCalendar


def setup_handler(router: Router):

    # Pre-step: return
    @router.message(Calc.date_prompt)
    @router.message(F.text == bk.RETURN.value)
    async def return_calc_handler(msg: Message, state: FSMContext):
        await state.set_state()
        await msg.answer(
            await rf('start'),
            reply_markup=await markups[mk.MAIN_MARKUP]
        )

    # Step 1: Date choise
    @router.message(F.text == bk.CALC.value)
    async def start_calc_handler(msg: Message, state: FSMContext):
        await state.set_state(Calc.date_prompt)
        await msg.answer(
            await rf('calculator_intro'),
            reply_markup=await markups[mk.CALC_DATE_CHOICE_MARKUP]
        )

    # Step 2.1: Date is known
    @router.message(Calc.date_prompt)
    @router.message(F.data == bk.DATE_KNOWN.value)
    async def date_handler_1(msg: Message, state: FSMContext):
        await msg.answer(
            "Выберите дату: ",
            reply_markup=await DialogCalendar().start_calendar()
        )

    # dialog calendar usage
    @router.message(Calc.date_prompt)
    @router.callback_query(dialog_cal_callback.filter())
    async def date_handler_2(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
        print(callback_data)
        selected, date = await DialogCalendar().process_selection(
                            callback_query,
                            callback_data
                        )
        if selected:
            await callback_query.message.answer(
                f'You selected {date.strftime("%d/%m/%Y")}',
                reply_markup=await markups[mk.CALC_DATE_CHOICE_MARKUP]
            )
