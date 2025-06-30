import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from psycopg import AsyncConnection

from app.bot.filters import UserRoleFilter
from app.bot.enums.roles import UserRole
from app.infrastructure.database.db import get_statistics
from locales.ru.txt import RU

logger = logging.getLogger(__name__)

admin_router = Router()

admin_router.message.filter(UserRoleFilter(UserRole.ADMIN))


@admin_router.message(Command('statistics'))
async def process_statistics_command(message: Message, conn: AsyncConnection):
    statistics = await get_statistics(conn)
    await message.answer(
        text=RU['statistics'].format(
            '\n'.join(
                f"{i}. <b>{stat[0]}</b>: {stat[1]}"
                for i, stat in enumerate(statistics, 1)
            )
        )
    )
