import logging

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message


class TestMW(BoundFilter):
    async def check(self, message: Message):
        data = ctx_data.get()
        logging.info(f"4. Filter, {data=}")
        logging.info("Next: Process message")
        return {"from_filter": "Filter data"}