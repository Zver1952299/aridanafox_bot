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


async def add_user_activity(
        conn: AsyncConnection,
        *,
        user_id: int
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                INSERT INTO activity (user_id)
                VALUES (%s)
                ON CONFLICT (user_id, activity_date)
                DO UPDATE
                SET actions = activity.actions + 1;
            """,
            params=(user_id,)
        )
    logger.info(f"User activity updated. table=`activity`, user_id={user_id}")


async def get_user_role(
        conn: AsyncConnection,
        *,
        user_id: int
) -> UserRole | None:
    async with conn.cursor() as cursor:
        data = await cursor.execute(
            query="""
                SELECT role FROM users WHERE user_id = %s;
            """,
            params=(user_id,)
        )
        row = await data.fetchone()
    if row:
        logger.info(
            f"The user with `user_id`= {user_id} has the role is {row[0]}")
    else:
        logger.warning(
            f"No user with `user_id`= {user_id} found in the database")
    return UserRole(row[0]) if row else None


async def get_statistics(conn: AsyncConnection) -> list[Any] | None:
    async with conn.cursor() as cursor:
        data = await cursor.execute(
            query="""
                SELECT user_id, SUM(actions) AS total_actions
                FROM activity
                GROUP BY user_id
                ORDER BY total_actions DESC
                LIMIT 5;
            """
        )
        rows = await data.fetchall()
    logger.info("Users activity got from table=`activity`")
    return [*rows] if rows else None
