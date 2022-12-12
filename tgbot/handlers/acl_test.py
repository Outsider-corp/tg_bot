from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.misc.sentinel import allow_access
from tgbot.models.models import User

@allow_access(True)
async def block_me(message: types.Message, user: User):
    await message.answer(f'Вы имеете статус: {user.allowed}.\n'
                         f'Теперь доступ запрещён.\n\n'
                         f'Чтобы разблокироваться введите команду /unblock_me')
    user.block()

@allow_access(True)
async def unblock_me(message: types.Message, user: User):
    await message.answer(f'Вы имеете статус: {user.allowed}.\n'
                         f'Теперь доступ разрешён.\n\n'
                         f'Чтобы заблокироваться введите команду /block_me')
    user.allow()


def reg_acl_test(dp: Dispatcher):
    dp.register_message_handler(block_me, Command('block_me'))
    dp.register_message_handler(unblock_me, Command('unblock_me'))
