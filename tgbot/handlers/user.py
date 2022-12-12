import re

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from tgbot.filters.private_chat import IsPrivate
from tgbot.misc.throttling import rate_limit


@rate_limit(5, key="start")
async def user_start(message: Message):
    await message.reply(f"Hello, {message.chat.full_name}")


@rate_limit(5, key="start")
async def user_start_ref(message: Message):
    deep_link = message.get_args()
    await message.answer(f"Привет, {message.from_user.full_name} \n\n"
                         "<b>Спасибо, что решил(-а) поучаствовать в бета-тесте Outside-бота</b> \n\n"
                         "Данное сообщение говорит о том, что тебя кто-то позвал (наверное, админ) \n"
                         f"Благодаря этому ты имеешь чуть больше привелегий, чем простые смертные 😈", parse_mode="html")


def reg_user(dp: Dispatcher):
    dp.register_message_handler(user_start_ref, CommandStart(deep_link=re.compile(r'^[0-9]{3,9}$')),IsPrivate())
    dp.register_message_handler(user_start, IsPrivate(), commands=["start"], state="*")
