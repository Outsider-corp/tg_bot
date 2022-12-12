from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram import Dispatcher
from .states import Test
from tgbot.config import Config


async def enter_testing(message: Message):
    await message.answer('Тестирование начато... \n'
                         'Вопрос №1. \n\n'
                         'Кто создатель этого бота? \n')
    await Test.first()


async def answer_Q1(message: Message, state: FSMContext):
    ans = message.text

    # await state.update_data(ans1 = ans)
    # await  state.update_data(
    #     {
    #         "ans1": ans
    #     }
    # )
    async with state.proxy() as data:
        data["ans1"] = ans

    await message.answer('Вопрос №2. \n\n'
                         'Как прошёл твой день? '
                         '(можно коротко или развёрнуто)')
    await Test.next()


async def answer_Q2(message: Message, state: FSMContext):
    data = await state.get_data()
    ans1 = data.get('ans1')
    ans2 = message.text
    sum_ans = f'Ответ 1:\n{ans1} \n\nОтвет 2:\n{ans2}'
    await message.answer("Спасибо за участие!")
    await message.answer(sum_ans)

    await state.finish()
    # await state.reset_state(with_data=False)
    await send_res_to_admin(message, sum_ans)

async def send_res_to_admin(message: Message, sum_ans):
    for user_id in message.bot['config'].tg_bot.admin_ids:

        await message.bot.send_message(user_id, f'<b>ОТВЕТ ОТ {message.from_user.full_name}</b>\n\n{sum_ans}', parse_mode='html')


def reg_states(dp: Dispatcher):
    dp.register_message_handler(enter_testing, Command('test'))
    dp.register_message_handler(answer_Q1, state=Test.Q1)
    dp.register_message_handler(answer_Q2, state=Test.Q2)
