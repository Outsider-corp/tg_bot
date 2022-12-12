import logging
import sys

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.utils.deep_linking import get_start_link

from tgbot.filters.private_chat import IsPrivate
from tgbot.filters.test_mw import TestMW
from tgbot.misc.notify_bot_work import start_stop_notify
from tgbot.models.models import User


async def admin_start(message: Message, user: User, mw_data=None, from_filter=None):
    await message.reply("Hello, admin!")
    deep_link = await get_start_link(payload=message.from_user.id)
    await message.answer(f"Твоя реферальная ссылка: {deep_link}")
    if mw_data:
        await message.answer(f'Данные из Middleware: {mw_data} \n'
                             f'Данные из Filter: {from_filter}')
    logging.info("6. Handler")
    logging.info("Next: Post-process message")
    return {"from_handler": "Data from Handler"}


# async def admin_get_ref(message: Message):
#     await pass


async def admin_secret(message: Message):
    try:
        for user_id in message.bot['config'].tg_bot.admin_ids:
            await message.bot.send_message(user_id, f"<b>THIS IS EXTREMELY IMPORTANT MESSAGE"
                                                    f" FROM {message.from_user.full_name}!!!</b>"
                                                    f" \n\n{message.text.replace('@#%', '').strip()}",
                                           parse_mode="html")
    except Exception as Ex:
        logging.exception(Ex)


async def bot_close(message: Message):
    await start_stop_notify(message.bot, message.bot['config'], "Бот выключается...")
    sys.exit()


def reg_admin(dp: Dispatcher):
    # dp.register_message_handler(admin_get_ref,)
    dp.register_message_handler(admin_start, IsPrivate(), TestMW(), commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(admin_secret, IsPrivate(), Text(contains="@#%"), is_admin=True)
    dp.register_message_handler(bot_close, text="Выключить", is_admin=True)
