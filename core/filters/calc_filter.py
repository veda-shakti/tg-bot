from aiogram.filters import Filter
from aiogram.types import Message


class NumberFilter(Filter):
    def is_number(self, text: str) -> bool:
        try:
            int(text)
            return True
        except ValueError:
            return False

    async def check(self, message: Message):
        return self.is_number(message.text)
