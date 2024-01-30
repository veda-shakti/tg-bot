from aiogram.types import InlineKeyboardButton
from enum import Enum


class ButtonsData(Enum):
    MINUTE      = 'minute'
    HOUR        = 'hour'
    PLACEHOLDER = 'placeholder'
    SKIP_TIME   = 'skip time'
    YES         = 'yes'
    NO          = 'no'
