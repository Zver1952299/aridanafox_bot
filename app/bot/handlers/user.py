import logging

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, BotCommandScopeChat, CallbackQuery
from aiogram.enums import BotCommandScopeType
from app.bot.config import Config
from locales.ru.txt import RU
from app.bot.keyboards.main_menu import get_main_menu_commands
from app.bot.keyboards.keyboards import get_start_kb
from app.bot.utils import send_text_page
from app.bot.enums import TextKey


logger = logging.getLogger(__name__)

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot, config: Config):
    logger.info(f"User {message.from_user.id} started bot.")

    await bot.set_my_commands(
        commands=get_main_menu_commands(),
        scope=BotCommandScopeChat(
            type=BotCommandScopeType.CHAT,
            chat_id=message.from_user.id
        )
    )

    await message.answer_photo(
        photo=FSInputFile(config.static.main_photo_path),
        caption=RU.get(TextKey.START, 'Добро пожаловать!'),
        reply_markup=get_start_kb()
    )


@user_router.callback_query(F.data == "services")
async def process_services_press(callback: CallbackQuery):
    await send_text_page(callback, TextKey.SERVICES)


@user_router.callback_query(F.data == 'about_me')
async def process_about_me_press(callback: CallbackQuery):
    await send_text_page(callback, TextKey.ABOUT_ME)


@user_router.callback_query(F.data == 'courses')
async def process_courses_press(callback: CallbackQuery):
    await send_text_page(callback, TextKey.COURSES)


@user_router.callback_query(F.data == 'back_to_start')
async def process_back_to_start_press(callback: CallbackQuery, config: Config):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo=FSInputFile(config.static.main_photo_path),
        caption=RU.get(TextKey.START, 'Добро пожаловать!'),
        reply_markup=get_start_kb()
    )
