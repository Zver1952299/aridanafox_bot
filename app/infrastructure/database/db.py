import logging
from datetime import datetime, timezone
from typing import Any

from app.bot.enums.roles import UserRole
from psycopg import AsyncConnection

logger = logging.getLogger(__name__)


async def add_user(
        conn: AsyncConnection,
        *,
        user_id: int,
        username: str | None = None,
        language: str = 'ru',
        role: UserRole = UserRole.USER,
        is_alive: bool = True,
        banned: bool = False
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                INSERT INTO users(user_id, username, language, role, is_alive, banned)
                VALUES(
                    %(user_id)s,
                    %(username)s,
                    %(language)s,
                    %(role)s,
                    %(is_alive)s,
                    %(banned)s
                ) ON CONFLICT DO NOTHING;
            """,
            params={
                'user_id': user_id,
                'username': username,
                'language': language,
                'role': role,
                'is_alive': is_alive,
                'banned': banned
            },
        )
    logger.info(
        f"User added. Table='users', user_id={user_id}, created_at={datetime.now(timezone.utc)}"
        f"language={language}, role={role}, is_alive={is_alive}, banned={banned}")


async def get_user(
    conn: AsyncConnection,
    *,
    user_id: int
) -> tuple[Any, ...] | None:
    async with conn.cursor() as cursor:
        data = await cursor.execute(
            query="""
                SELECT
                    id,
                    user_id,
                    username,
                    language,
                    role,
                    is_alive,
                    banned,
                    created_at
                    FROM users WHERE user_id = %s;
            """, params=(user_id,),
        )
        row = await data.fetchone()
    logger.info(f"Row is {row}")
    return row if row else None


async def change_user_alive_status(
    conn: AsyncConnection,
    *,
    user_id: int,
    is_alive: bool
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                UPDATE users
                SET is_alive = %s
                WHERE user_id = %s;
            """,
            params=(is_alive, user_id)
        )
    logger.info(f"Updated `is_alive` status to {is_alive} for user {user_id}")
