import logging

import asyncio

from aiogram import Bot

from tgbot.config import Config


async def start_stop_notify(bot: Bot, conf: Config, message: str):
    try:
        for user_id in conf.tg_bot.admin_ids:
            await bot.send_message(user_id, message)
    except Exception as Ex:
        logging.exception(Ex)
    finally:
        await asyncio.sleep(0.05)
