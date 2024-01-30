import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

import config

from core.handlers import setup_handlers
from core.admin import setup_admin


async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
    router = Router()

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    setup_handlers(router)
    # setup_filters(dp)

    await setup_admin(dp)
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
