import os
import logging

from dataclasses import dataclass
from environs import Env

logger = logging.getLogger(__name__)


@dataclass
class BotSettings:
    token: str


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

    log = LogSettings(
        level=env('LOG_LEVEL'),
        format=env('LOG_FORMAT')
    )

    logger.info("Configuration loaded successfully")

    return Config(
        bot=BotSettings(token=env('BOT_TOKEN')),
        log=log,
        static=StaticSettings(main_photo_path=env('MAIN_PHOTO_PATH'))
    )
