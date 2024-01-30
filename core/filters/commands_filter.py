from aiogram.types import Message
from aiogram.filters import Filter

class IsCommandFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.text.startswith('/')

class IsNotCommandFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return not message.text.startswith('/')