import logging

from aiogram.types import CallbackQuery
from locales.ru.txt import RU
from app.bot.keyboards.keyboards import get_back_to_start_kb

logger = logging.getLogger(__name__)


async def send_text_page(callback: CallbackQuery, key: str) -> None:
    text = RU.get(key, None)

    if text is None:
        logger.warning(
            f"The text for the key {key} was not found in the locales")
        text = 'Возникла проблема с загрузкой текста. Попробуйте позже.'

    try:
        await callback.message.delete()
    except Exception as e:
        logger.warning(f"Couldn't delete message: {e}")

    logger.info(f"User {callback.from_user.id} opened {key}")

    await callback.message.answer(
        text=text,
        reply_markup=get_back_to_start_kb()
    )
