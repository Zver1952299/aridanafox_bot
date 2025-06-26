from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, BotCommandScopeChat, CallbackQuery
from aiogram.enums import BotCommandScopeType
from locales.ru.txt import RU
from app.bot.keyboards.main_menu import get_main_menu_commands
from app.bot.keyboards.keyboards import get_start_kb, get_back_to_start_kb

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
        caption=RU.get('/start', 'Добро пожаловать!'),
        reply_markup=get_start_kb()
    )


@user_router.callback_query(F.data == "services")
async def process_services_press(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer(
        text=RU.get(
            '/services', 'Возникла проблема с загрузкой текста. Попробуйте позже.'
        ),
        reply_markup=get_back_to_start_kb()
    )
    print(RU.get(
        '/services', 'Возникла проблема с загрузкой текста. Попробуйте позже.'))


@user_router.callback_query(F.data == 'about_me')
async def process_about_me_press(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer(
        text=RU.get(
            '/about_me', 'Возникла проблема с загрузкой текста. Попробуйте позже.'),
        reply_markup=get_back_to_start_kb()
    )


@user_router.callback_query(F.data == 'courses')
async def process_courses_press(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer(
        text=RU.get(
            '/courses', 'Возникла проблема с загрузкой текста. Попробуйте позже.'),
        reply_markup=get_back_to_start_kb()
    )


@user_router.callback_query(F.data == 'back_to_start')
async def process_back_to_start_press(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo=FSInputFile("static/images/main_photo.jpg"),
        caption=RU.get('/start', 'Добро пожаловать!'),
        reply_markup=get_start_kb()
    )
