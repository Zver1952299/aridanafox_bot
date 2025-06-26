from aiogram.types import BotCommand
from locales.ru.txt import RU


def get_main_menu_commands() -> list[BotCommand]:
    return [
        BotCommand(
            command='/start',
            description=RU['/start_description']
        ),
        BotCommand(
            command='/help',
            description=RU['/help_description']
        )
    ]
