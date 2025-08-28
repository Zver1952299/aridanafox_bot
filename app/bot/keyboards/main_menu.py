from aiogram.types import BotCommand
from locales.ru.txt import RU
from app.bot.enums.roles import UserRole


def get_main_menu_commands(role: UserRole) -> list[BotCommand]:
    if role == UserRole.USER:
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
    elif role == UserRole.ADMIN:
        return [
            BotCommand(
                command='/start',
                description=RU['/start_description']
            ),
            BotCommand(
                command='/help',
                description=RU['/help_description']
            ),
            BotCommand(
                command='/statistics',
                description=RU['/statistics_description']
            )
        ]
