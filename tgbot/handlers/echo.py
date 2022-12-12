from aiogram import Dispatcher, types


async def bot_ans(message: types.Message):
    text = "Героям Слава"

    await message.reply(text)


async def get_id(message: types.Message):
    await message.answer(f"Твой ID: `{message.from_user.id}`", parse_mode="MARKDOWN")


# async def bot_idk(message: types.PhotoSize):
#     return message.reply("I don't know what is it...")


async def bot_echo(message: types.Message):
    text = [
        "This is echo message...",
        "",
        "Your message is:",
        message.text
    ]

    await message.answer("\n".join(text))


def reg_echo(dp: Dispatcher):
    dp.register_message_handler(bot_ans, text="Слава Украине")
    dp.register_message_handler(get_id, text="Мой id")
    # dp.register_message_handler(bot_idk, content_types=types.PhotoSize)
    dp.register_message_handler(bot_echo)
