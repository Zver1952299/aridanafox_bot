from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from locales.ru.txt import RU


def get_start_kb() -> InlineKeyboardMarkup:
    buttons = []
    buttons.append([
        InlineKeyboardButton(
            text=RU['about_me'],
            callback_data='button_1'
        ),
        InlineKeyboardButton(
            text=RU['tg_chennal'],
            url='https://t.me/@andromedalifestar'
        )]
    )
    buttons.append(
        [InlineKeyboardButton(
            text=RU['services'],
            callback_data='button_1'
        ),
            InlineKeyboardButton(
            text=RU['courses'],
            callback_data='button_1'
        )]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
