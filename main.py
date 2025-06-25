import asyncio
import logging
import os
import sys

from app.bot.config import Config, load_config
from app.bot import main

config: Config = load_config()

logging.basicConfig(
    level=getattr(logging, config.log.level, logging.INFO),
    format=config.log.format
)

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    if sys.platform.startswith("win") or os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main(config))
    except Exception as e:
        logger.exception(f"Error when launching the bot - {e}")
        sys.exit(1)
