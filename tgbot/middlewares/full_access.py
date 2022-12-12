import logging

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data_temp.config import banned_users


class FullAccess(BaseMiddleware):
    # 1
    async def on_pre_process_update(self, update: types.Update, data: dict):
        # logging.info("-------------New Update!-------------")
        # logging.info("1. Pre-process update")
        # logging.info("Next: Process update")
        # data['mw_data'] = "Go to the on_post_process_update"

        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return

        if user in banned_users:
            raise CancelHandler()

    # 2
    # async def on_process_update(self, update: types.Update, data: dict):
    #     logging.info(f"2. Process update, {data=}")
    #     logging.info("Mext: Pre-process message")
    #
    # # 3
    # async def on_pre_process_message(self, message: types.Message, data: dict):
    #     logging.info(f"3. Pre-process message, {data=}")
    #     logging.info("Next: Filters, Process Message")
    #     data["mw_data"] = "Go to the on_process_message"

    # 4 Filters

    # 5
    async def on_process_message(self, message: types.Message, data: dict):
        # logging.info(f'5. Process message')
        # logging.info("Next: Handler")
        # data["mw_data"] = "Go to the Handler"
        logging.info(f'{message.from_user.full_name}: {message.text}')

    # 6 Handlers

    # 7
    # async def on_post_process_message(self, message: types.Message, from_handler: list, data: dict):
    #     logging.info(f"7. Post-process message, {from_handler=}, {data=}")
    #     logging.info("Next: Post-process update")
    #
    # # 8
    # async def on_post_process_update(self, update: types.Update, from_handler: list, data: dict):
    #     logging.info(f"8. Post-process update, {from_handler=}, {data=}")
    #     logging.info("-------------End of Update!-------------")

    async def on_pre_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        await cq.answer()
