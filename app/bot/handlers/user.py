from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, BotCommandScopeChat
from aiogram.enums import BotCommandScopeType
from locales.ru.txt import RU
from app.bot.keyboards.main_menu import get_main_menu_commands
from app.bot.keyboards.keyboards import get_start_kb

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    await bot.set_my_commands(
        commands=get_main_menu_commands(),
        scope=BotCommandScopeChat(
            type=BotCommandScopeType.CHAT,
            chat_id=message.from_user.id
        )
    )

    await message.answer_photo(
        photo=FSInputFile("static/images/main_photo.jpg"),
        caption=RU['/start'],
        reply_markup=get_start_kb()
    )
