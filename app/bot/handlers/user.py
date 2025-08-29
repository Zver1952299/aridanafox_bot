import logging

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, KICKED, ChatMemberUpdatedFilter
from aiogram.types import Message, FSInputFile, BotCommandScopeChat, CallbackQuery, ChatMemberUpdated
from aiogram.enums import BotCommandScopeType
from app.bot.config import Config
from locales.ru.txt import RU
from app.bot.keyboards.main_menu import get_main_menu_commands
from app.bot.keyboards.keyboards import get_start_kb
from app.bot.utils import send_text_page
from app.bot.enums.command import TextKey
from app.infrastructure.database.db import (
    add_user,
    get_user,
    change_user_alive_status
)
from app.bot.enums.roles import UserRole
from psycopg import AsyncConnection


logger = logging.getLogger(__name__)

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(
        message: Message,
        conn: AsyncConnection,
        bot: Bot,
        config: Config,
        admin_ids: list[int]):
    user_row = await get_user(conn, user_id=message.from_user.id)

    if user_row is None:
        if message.from_user.id in admin_ids:
            role = UserRole.ADMIN
        else:
            role = UserRole.USER
        await add_user(
            conn=conn,
            user_id=message.from_user.id,
            username=message.from_user.username,
            language='ru',
            role=role,
            is_alive=True,
            banned=False
        )
    else:
        role = UserRole(user_row[4])

    if user_row and not user_row[5]:
        await change_user_alive_status(conn, user_id=message.from_user.id, is_alive=True)

    logger.info(f"User {message.from_user.id} started bot.")

    await bot.set_my_commands(
        commands=get_main_menu_commands(role),
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


# @user_router.message(Command('pay'))
# async def process_pay_command(message: Message, bot: Bot, config: Config):
#     data = await bot.send_invoice(chat_id=message.chat.id, title='Тест покупка', description='Описание теста', payload='invoice', provider_token='381764678:TEST:129625', currency='RUB', prices=[LabeledPrice(label='Тест покупка', amount=10000)])
#     print(data)


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


@user_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated, conn: AsyncConnection):
    logger.info(f"User {event.from_user.id} has blocked the bot")
    await change_user_alive_status(conn, user_id=event.from_user.id, is_alive=False)
