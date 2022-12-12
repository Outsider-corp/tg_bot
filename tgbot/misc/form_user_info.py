import logging
import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from tgbot.misc.states import FormUserInfo


async def fui_enter(message: types.Message, state: FSMContext):
    await message.answer(f'Здравствуйте. Введите свои данные\n\n'
                         f'1. Введите имя пользователя:')
    await FormUserInfo.first()


async def fui_name(message: types.Message, state: FSMContext):
    ans = message.text
    async with state.proxy() as data:
        data['name'] = ans

    await message.answer(f'2. Введите Email:')
    await FormUserInfo.next()


async def fui_email(message: types.Message, state: FSMContext):
    ans = message.text
    if re.search(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$', ans):
        async with state.proxy() as data:
            data['email'] = ans
        await message.answer(f'3. Введите номер телефона:')
        await FormUserInfo.next()
    else:
        await message.answer(f'Введите Email в правильном формате.')


async def fui_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    logging.info(data)
    ans = message.text
    if re.search(r'^((\d|\+\d)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', ans):
        async with state.proxy() as data_new:
            data_new['phone'] = ans
        await message.answer(f'Ваши данные данные:\n\n'
                             f'Имя - {data.get("name")}\n\n'
                             f'Email - {data.get("email")}\n\n'
                             f'Телефон: - {ans}')
        await state.finish()
    else:
        await message.answer(f'Введите номер телефона в правильном формате')


def reg_state_form(dp: Dispatcher):
    dp.register_message_handler(fui_enter, Command('form'), state="*")
    dp.register_message_handler(fui_name, state=FormUserInfo.Name)
    dp.register_message_handler(fui_email, state=FormUserInfo.Email)
    dp.register_message_handler(fui_phone, state=FormUserInfo.Phone)
