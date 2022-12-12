import time
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot = Bot(token="")

disp = Dispatcher(bot)


@disp.message_handler()
async def get_mess(mes: types.Message):
    chat_id = mes.chat.id
    # text = "No War"
    # send_mess = await bot.send_message(chat_id=chat_id, text=text)
    # print(send_mess.to_python())
    # send_mess = await bot.send_photo(chat_id=chat_id,
    #                                  photo="https://d1csarkz8obe9u.cloudfront.net/posterpreviews/instagram-no-war-template-design-2fe02b7c2aba4cc998e368e2898d6ae7_screen.jpg?ts=1645822212")
    # print(send_mess.photo[-1].file_unique_id)
    send_time = await bot.send_message(chat_id=chat_id,
                                       text=datetime.fromtimestamp(round(time.time())))
    print(send_time.chat)

executor.start_polling(disp)
