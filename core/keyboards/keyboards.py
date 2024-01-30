from typing import Any, List, Union
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton as KB, InlineKeyboardButton as IKB, InlineKeyboardMarkup
from .enums.buttons_keys import ButtonsKeys
from .enums.markup_keys import MarkupKeys
from .enums.buttons_data import ButtonsData


class Markups:
    def __create_markup__(
        self, 
        button_keys: List[Union[ButtonsKeys, KB, Any]]
    ) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KB(text=str(button.value))] 
                for button in button_keys
            ],
            resize_keyboard=True
        )
        return markup


    def __create_inline_markup__(
        self, 
        button_keys: List[Union[ButtonsKeys, IKB, Any]], 
        row_width: int = 1
    ) -> InlineKeyboardMarkup:
        """
        Создает инлайновую клавиатуру для Telegram бота.

        Args:
            button_keys: Список кнопок или ключей для создания кнопок.
            row_width: Количество кнопок в одной строке клавиатуры.

        Returns:
            InlineKeyboardMarkup: Объект инлайновой клавиатуры для Telegram бота.
        """
        buttons = [
            IKB(
                text=str(btn.value) if isinstance(btn, ButtonsKeys) else btn.text, 
                callback_data=str(btn.name) if isinstance(btn, ButtonsKeys) else btn.callback_data
            )
            for btn in button_keys
        ]

        keyboard = [buttons[i:i + row_width] for i in range(0, len(buttons), row_width)]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)


    def __init__(self):
        self._markups = {
            MarkupKeys.CALC_MARKUP: self.__create_inline_markup__([
                ButtonsKeys.CALC
            ]),

            MarkupKeys.HOURS: self.__create_inline_markup__([
                *self.create_IKB_placeholders([' ', 'Час', ' ']),
                *self.create_IKB_btn_list(range(24), ButtonsData.HOUR),
                self.__IKB__('Пропустить', str(ButtonsData.SKIP_TIME))
            ], row_width=3),

            MarkupKeys.MINUTES: self.__create_inline_markup__([
                *self.create_IKB_placeholders([' ', ' ', 'Мин', ' ', ' ']),
                *self.create_IKB_btn_list(range(0, 60, 5), ButtonsData.MINUTE)
            ], row_width=5),

            MarkupKeys.YES_NO: self.__create_inline_markup__([
                self.__IKB__('✅ Да', str(ButtonsData.YES)),
                self.__IKB__('❌ Нет', str(ButtonsData.NO))
            ]),

            MarkupKeys.MAIN_MARKUP: self.__create_markup__([
                ButtonsKeys.LUCK_2023,
                ButtonsKeys.TASKS_OPP_2024,
                ButtonsKeys.DETAIL_2024
            ]),
        }


    def __IKB__(self, text: str, callback_data) -> IKB:
        return IKB(text=text, callback_data=callback_data)


    def create_IKB_placeholders(self, lst: list):
        return map(lambda text: self.__IKB__(text, str(ButtonsData.PLACEHOLDER)), lst)
    

    def create_IKB_btn_list(self, lst: list, callback_data_prefix: str) -> List[IKB]:
        return map(lambda text: self.__IKB__(str(text), f"{callback_data_prefix}:{text}"), lst)


    async def __getitem__(self, key: MarkupKeys):
        return self._markups.get(key)


markups = Markups()
