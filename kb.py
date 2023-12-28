from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from enum import Enum


class MarkupKeys(Enum):
    MAIN_MARKUP         = 1
    CALC_UNKNOWN_TIME   = 2
    HOURS               = 3
    MINUTES             = 4


class ButtonsKeys(Enum):
    CALC            = '🔢 Рассчитать восходящий знак'
    RACHUKE         = '🌌 Прогноз по оси Раху-Кету'
    CHECK_2023      = '📆 Сверьте каким для вас был 2023'
    DATE_KNOWN      = '✅ Знаю точную дату своего рождения'
    TIME_UNKNOWN    = '❌ Пропустить'
    RETURN          = '↩️ Вернуться'


class Markups:
    def __createMarkup__(self, button_keys: list[ButtonsKeys]) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=str(button.value))] 
                for button in button_keys
            ],
            resize_keyboard=True
        )
        return markup
    
    def __createInlineMarkup__(self, button_keys: list[ButtonsKeys], row_width: int = 1) -> InlineKeyboardMarkup:
        buttons = []
        for button in button_keys:
            if isinstance(button, ButtonsKeys):
                # Для объектов ButtonsKeys используем их свойства value и name
                text = str(button.value)
                callback_data = str(button.name)
            else:
                # Для остальных (чисел) используем сами значения
                text = str(button)
                callback_data = f"time:{button}"  # Пример формата для callback_data

            buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))

        # Разбиваем кнопки на строки согласно row_width
        keyboard = [buttons[i:i + row_width] for i in range(0, len(buttons), row_width)]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def __init__(self):
        self._markups = {
            MarkupKeys.MAIN_MARKUP: self.__createInlineMarkup__([
                ButtonsKeys.CALC
            ]),

            MarkupKeys.CALC_UNKNOWN_TIME: self.__createMarkup__([
                ButtonsKeys.TIME_UNKNOWN
            ]),

            MarkupKeys.HOURS: self.__createInlineMarkup__([
                ' ', 'Час', ' ',
                *[HOUR for HOUR in range(24)]
            ], row_width=3),

            MarkupKeys.MINUTES: self.__createInlineMarkup__([
                ' ', ' ', 'Мин', ' ', ' ',
                *[HOUR for HOUR in range(0, 60, 5)]
            ], row_width=5)
        }

    async def __getitem__(self, key: MarkupKeys):
        return self._markups.get(key)


markups = Markups()
