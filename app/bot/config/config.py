import os
import logging

from dataclasses import dataclass
from environs import Env

logger = logging.getLogger(__name__)


@dataclass
class BotSettings:
    token: str
    admin_ids: list[int]


@dataclass
class DatabaseSettings:
    name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class LogSettings:
    level: str
    format: str


@dataclass
class StaticSettings:
    main_photo_path: str


@dataclass
class Config:
    bot: BotSettings
    db: DatabaseSettings
    log: LogSettings
    static: StaticSettings


def load_config(path: str | None = None):
    env = Env()

    if path:
        if not os.path.exists(path):
            logger.warning(f".env file not found at {path}, skipping...")
        else:
            logger.info(f'Loading .env file from {path}')

    env.read_env(path)

    db = DatabaseSettings(
        name=env('POSTGRES_DB'),
        host=env('POSTGRES_HOST'),
        port=env('POSTGRES_PORT'),
        user=env('POSTGRES_USER'),
        password=env('POSTGRES_PASSWORD')

    )

    log = LogSettings(
        level=env('LOG_LEVEL', 'INFO'),
        format=env(
            'LOG_FORMAT', "[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s")
    )

    token = env('BOT_TOKEN')
    raw_ids = env.list('ADMIN_IDS', default=[])

    try:
        admin_ids = [int(x) for x in raw_ids]
    except ValueError as e:
        raise ValueError(f"ADMIN_IDS must be integers, got: {raw_ids}") from e

    if not token:
        raise ValueError("BOT_TOKEN is required in .env")

    logger.info("Configuration loaded successfully")

    return Config(
        bot=BotSettings(token=token, admin_ids=admin_ids),
        db=db,
        log=log,
        static=StaticSettings(main_photo_path=env('MAIN_PHOTO_PATH'))
    )
