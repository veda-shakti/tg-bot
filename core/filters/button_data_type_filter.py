from aiogram.filters import Filter
from aiogram.types import CallbackQuery
from core.keyboards.enums.buttons_data import ButtonsData as bd
from core.keyboards.enums.buttons_keys import ButtonsKeys as bk


class ButtonDataTypeFilter(Filter):
    def __init__(self, data_type: bd | bk):
        self.data_type = str(data_type) if isinstance(data_type, bd) else data_type.name
    
    async def __call__(self, callback_query: CallbackQuery) -> bool:
        return callback_query.data.startswith(self.data_type)
