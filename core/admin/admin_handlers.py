from aiogram import Bot, Dispatcher
from config_local import ADMIN_ID

async def start_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, text='Bot started!')


async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, text='Bot stoped!')


async def setup_admin(dp: Dispatcher):
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
