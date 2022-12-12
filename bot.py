import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.filters.private_chat import IsPrivate
from tgbot.filters.test_mw import TestMW
from tgbot.handlers.acl_test import reg_acl_test
from tgbot.handlers.admin import reg_admin
from tgbot.handlers.echo import reg_echo
from tgbot.handlers.user import reg_user
from tgbot.middlewares.acl import ACLMiddleware
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.full_access import FullAccess
from tgbot.middlewares.sentinel import Sentinel
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.handlers.testing import reg_states
from tgbot.misc.form_user_info import reg_state_form

logger = logging.getLogger(__name__)


def reg_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(ACLMiddleware())
    dp.setup_middleware(Sentinel())
    dp.setup_middleware(FullAccess())


def reg_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(TestMW)


def reg_all_handlers(dp):
    reg_admin(dp)
    reg_user(dp)
    reg_acl_test(dp)
    reg_states(dp)
    reg_state_form(dp)
    reg_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    reg_all_middlewares(dp, config)
    reg_all_filters(dp)
    reg_all_handlers(dp)

    # start
    try:
        # await start_stop_notify(bot, config, "Бот запускается...")
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
