from aiogram.types import CallbackQuery


async def set_typing(callback_query: CallbackQuery):
    await callback_query.bot.send_chat_action(callback_query.from_user.id, "typing")
