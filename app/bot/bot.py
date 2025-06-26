import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from app.bot.config import Config
from app.bot.handlers.user import user_router

logger = logging.getLogger(__name__)


async def main(config: Config) -> None:
    logger.info("Starting bot...")

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    dp['config'] = config

    dp.include_routers(user_router)
    logger.info("Routers included")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)
    finally:
        await bot.session.close()
