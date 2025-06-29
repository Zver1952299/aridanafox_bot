import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from psycopg_pool import AsyncConnectionPool
from app.bot.config import Config
from app.bot.handlers.user import user_router
from app.bot.middlewares.database import DataBaseMiddleware
from app.bot.middlewares.statistics import ActivityCounterMiddleware
from app.infrastructure.database.connection import get_pg_pool

logger = logging.getLogger(__name__)


async def main(config: Config) -> None:
    logger.info("Starting bot...")

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    dp['config'] = config

    db_pool: AsyncConnectionPool = await get_pg_pool(
        db_name=config.db.name,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password
    )

    dp.include_routers(user_router)
    logger.info("Routers included")

    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(ActivityCounterMiddleware())
    logger.info("Middlewares included")

    try:
        await dp.start_polling(
            bot, db_pool=db_pool,
            admin_ids=config.bot.admin_ids)
    except Exception as e:
        logger.exception(e)
    finally:
        await bot.session.close()
