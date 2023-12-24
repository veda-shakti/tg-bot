from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from enum import Enum


class MarkupKeys(Enum):
    MAIN_MARKUP             = 1
    CALC_DATE_CHOICE_MARKUP = 2
    CALC_FULL_MARKUP        = 3
    CALC_PART_MARKUP        = 4


class ButtonsKeys(Enum):
    CALC            = '🔢 Рассчитать восходящий знак'
    RACHUKE         = '🌌 Прогноз по оси Раху-Кету'
    CHECK_2023      = '📆 Сверьте каким для вас был 2023'
    DATE_KNOWN      = '✅ Знаю точную дату своего рождения'
    DATE_UNKNOWN    = '❌ Не знаю точную дату своего рождения'
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
    
    def __createInlineMarkup__(self, button_keys: list[ButtonsKeys]) -> ReplyKeyboardMarkup:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=str(button.value), callback_data=str(button.name))] 
                for button in button_keys
            ]
        )
        return markup

    def __init__(self):
        self._markups = {
            MarkupKeys.MAIN_MARKUP: self.__createMarkup__([
                ButtonsKeys.CALC
            ]),

            MarkupKeys.CALC_DATE_CHOICE_MARKUP: self.__createMarkup__([
                ButtonsKeys.DATE_KNOWN,
                ButtonsKeys.DATE_UNKNOWN,
                ButtonsKeys.RETURN
            ]),

            MarkupKeys.CALC_FULL_MARKUP: self.__createMarkup__([
                ButtonsKeys.DATE_KNOWN,
                ButtonsKeys.DATE_UNKNOWN
            ]),

            MarkupKeys.CALC_PART_MARKUP: self.__createMarkup__([
                ButtonsKeys.DATE_KNOWN,
                ButtonsKeys.DATE_UNKNOWN
            ])
        }

    async def __getitem__(self, key: MarkupKeys):
        return self._markups.get(key)


markups = Markups()
